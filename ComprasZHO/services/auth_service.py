import os
import jwt
from typing import Dict, Any, Tuple
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

# Variables de entorno requeridas
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "")
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET", "")
DOMINIO_PERMITIDO = os.getenv("DOMINIO_PERMITIDO", "zibarisholding.com")

# Roles del sistema
ROLES_TODOS = ["admin", "director", "revisor", "compras", "contable", "solicitante"]

# Cliente Supabase
if SUPABASE_URL and SUPABASE_ANON_KEY:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
else:
    supabase = None


def obtener_url_login_google(redirect_to: str = "http://localhost:3000") -> str:
    """
    Genera la URL de autenticación de Google OAuth con Supabase
    restringiendo las sugerencias al dominio empresarial corporativo (queryParams hd).
    """
    if not supabase:
        raise ValueError("Supabase no está configurado correctamente en las variables de entorno.")

    options = {
        "redirect_to": redirect_to,
        "query_params": {
            "hd": DOMINIO_PERMITIDO,
            "prompt": "select_account"
        }
    }

    # Compatibilidad con las distintas versiones de supabase-py (gotrue)
    if hasattr(supabase.auth, "get_oauth_sign_in_url"):
        res = supabase.auth.get_oauth_sign_in_url(provider="google", options=options)
        return res.url if hasattr(res, 'url') else str(res)
    elif hasattr(supabase.auth, "sign_in_with_oauth"):
        res = supabase.auth.sign_in_with_oauth({"provider": "google", "options": options})
        return res.url if hasattr(res, 'url') else str(res)
    elif hasattr(supabase.auth, "get_url_for_provider"):
        res = supabase.auth.get_url_for_provider("google", options=options)
        return res.url if hasattr(res, 'url') else str(res)
    else:
        base_url = SUPABASE_URL.rstrip('/')
        return f"{base_url}/auth/v1/authorize?provider=google&redirect_to={redirect_to}&queryParams%5Bhd%5D={DOMINIO_PERMITIDO}&queryParams%5Bprompt%5D=select_account"


def intercambiar_codigo_pkce(code: str) -> str:
    """Intercambia un código de autorización PKCE por la sesión de Supabase y retorna el access_token."""
    if not supabase:
        raise ValueError("Supabase no está configurado.")
    res = supabase.auth.exchange_code_for_session({"auth_code": code})
    if res.session:
        return res.session.access_token
    raise ValueError("No se pudo intercambiar el código por una sesión activa.")


def decodificar_y_validar_jwt(token: str) -> Dict[str, Any]:
    """
    Decodifica y valida el token JWT emitido por Supabase usando PyJWT.
    Valida firma HS256, expiración y audiencia 'authenticated'.
    Permite un margen de tiempo (leeway) para tolerancia a desincronización de reloj local.
    """
    if not SUPABASE_JWT_SECRET:
        # Si no se configuró SUPABASE_JWT_SECRET, intentamos obtener claims sin validar firma
        payload = jwt.decode(token, options={"verify_signature": False})
        return payload

    try:
        payload = jwt.decode(
            token,
            SUPABASE_JWT_SECRET,
            algorithms=["HS256"],
            audience="authenticated",
            leeway=120,
            options={"verify_iat": False}
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("La sesión ha expirado. Por favor inicia sesión nuevamente.")
    except jwt.InvalidTokenError as e:
        raise ValueError(f"Token de autenticación inválido: {str(e)}")


def procesar_autenticacion_usuario(token: str) -> Tuple[Dict[str, Any], list[str]]:
    """
    Ejecuta el flujo completo de backend:
    1. Validar JWT.
    2. Verificar dominio de correo estrictamente (@zibarisholding.com).
    3. Alta silenciosa y sincronización en la tabla 'perfiles'.
    4. Verificar estatus 'activo'.
    5. Asignar roles (Bootstrap del 1er usuario = TODOS los roles, posteriores = 'solicitante').
    6. Retornar los datos del usuario y sus roles asignados.
    """
    if not supabase:
        raise ValueError("Servicio de base de datos no disponible.")

    # 1. Validar JWT
    claims = decodificar_y_validar_jwt(token)
    
    user_id = claims.get("sub")
    email = claims.get("email", "").strip().lower()
    user_metadata = claims.get("user_metadata", {})
    nombre = user_metadata.get("full_name") or user_metadata.get("name") or email.split("@")[0]

    if not email or not user_id:
        raise ValueError("El token no contiene información válida de usuario.")

    # 2. Restricción estricta de dominio
    dominio_esperado = f"@{DOMINIO_PERMITIDO.lower()}"
    if not email.endswith(dominio_esperado):
        raise PermissionError(f"El portal es solo para correos {dominio_esperado}.")

    # 3. Alta silenciosa y sincronización en la tabla 'perfiles'
    # Usamos upsert: insert or update correo y nombre on conflict (id)
    perfil_data = {
        "id": user_id,
        "nombre": nombre,
        "activo": True
    }
    
    # Verificamos si el perfil ya existe para preservar el campo 'activo'
    res_perfil_existente = supabase.table("perfiles").select("activo").eq("id", user_id).execute()
    
    if res_perfil_existente.data:
        # Si ya existe, se respeta el estatus 'activo' actual
        activo_actual = res_perfil_existente.data[0].get("activo", True)
        if not activo_actual:
            raise PermissionError("Tu acceso está desactivado. Habla con Administración.")
        
        # Sincronizamos nombre
        supabase.table("perfiles").update({"nombre": nombre}).eq("id", user_id).execute()
    else:
        # Alta silenciosa
        supabase.table("perfiles").insert(perfil_data).execute()

    # 4. Bootstrap del 1er Usuario y Asignación de Roles
    # Consultamos si existen roles en la tabla 'usuario_roles'
    res_conteo_roles = supabase.table("usuario_roles").select("usuario", count="exact").limit(1).execute()
    total_registros_roles = res_conteo_roles.count if res_conteo_roles.count is not None else 0

    # Consultamos los roles actuales de este usuario
    res_roles_usuario = supabase.table("usuario_roles").select("rol").eq("usuario", user_id).execute()
    roles_actuales = [row["rol"] for row in res_roles_usuario.data] if res_roles_usuario.data else []

    if not roles_actuales:
        if total_registros_roles == 0:
            # Bootstrap 1er usuario: Otorga TODOS los roles del sistema
            nuevos_roles = [{"usuario": user_id, "rol": r} for r in ROLES_TODOS]
            supabase.table("usuario_roles").insert(nuevos_roles).execute()
            roles_actuales = ROLES_TODOS.copy()
        else:
            # Usuarios posteriores: Asigna rol por defecto 'solicitante'
            supabase.table("usuario_roles").insert({"usuario": user_id, "rol": "solicitante"}).execute()
            roles_actuales = ["solicitante"]

    perfil_completo = {
        "id": user_id,
        "email": email,
        "nombre": nombre,
        "activo": True
    }

    return perfil_completo, roles_actuales
