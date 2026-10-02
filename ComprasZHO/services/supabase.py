import os
import datetime
import calendar
from dotenv import load_dotenv
from supabase import create_client, Client
from ..utils import constantes

# Cargar las variables .env
load_dotenv()

# Conexion centralizada
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_ANON_KEY")

# Solo creamos el cliente si las variables existen. 
if url and key:
    supabase: Client = create_client(supabase_url=url, supabase_key=key)
else:
    supabase = None

def autenticacion(email, password):
    session = supabase.auth.sign_in_with_password({
        "email": email,
        "password": password
    })

    user_id = session.user.id
  
    accesos = supabase.table("acceso_sistemas").select("sistemas(nombre), personal(nombre), rol").eq("personal_id", session.user.user_metadata["personal_id"]).execute()
    
    sistemas = [
        {"rol": a["rol"], "sistema": a["sistemas"]["nombre"], "nombre_personal": a["personal"]["nombre"]}
        for a in accesos.data
    ]

    return {
        "session": session,
        "user_id": user_id,
        "sistemas": sistemas
    }

def cierre_sesion():
    supabase.auth.sign_out()

def restaurar_sesion(auth_token, refresh_token):
    supabase.auth.set_session(auth_token, refresh_token)

def actualizar_password(nueva_password):
    supabase.auth.update_user({
        "password": nueva_password,
        "data": {"needs_password_change": False}
    })

"""SUCURSALES"""
def consultar_sucursales():
    respuesta = supabase.schema(constantes.SCHEMA).table("sucursales").select("*").execute()
    return respuesta.data

"""ACTIVOS"""
def consultar_activos():
    respuesta = supabase.schema(constantes.SCHEMA)\
    .table("maquinas")\
    .select("*, sucursales(nombre)")\
    .execute()
    return respuesta.data

def insertar_activo(datos: dict):
    supabase.schema(constantes.SCHEMA).table("maquinas").insert(datos).execute()

def actualizar_activo(id: str, datos: dict):
    supabase.schema(constantes.SCHEMA).table("maquinas").update(datos).eq("id", id).execute()

def consultar_activos_sucursal(sucursal_id):
    respuesta = supabase.schema(constantes.SCHEMA)\
        .table("maquinas")\
        .select("id, folio, nombre")\
        .eq("sucursal_id", sucursal_id)\
        .execute()
    
    # Combinamos folio y nombre, manteniendo el id separado
    datos_formateados = [
        {
            "id": fila["id"],
            "activo": f"{fila['folio']} - {fila['nombre']}"
        }
        for fila in respuesta.data
    ]
    
    return datos_formateados

def consultar_activo_folio(folio: str):
    respuesta = supabase.schema(constantes.SCHEMA)\
    .table("maquinas")\
    .select("*, sucursales(nombre)")\
    .eq("folio", folio)\
    .execute()
    return respuesta.data

def conteo_activos_totales():
    respuesta = supabase.schema(constantes.SCHEMA)\
        .table("maquinas")\
        .select("*", count="exact")\
        .limit(0)\
        .execute()

    return respuesta.count

def conteo_activos_mantenimiento():
    respuesta = supabase.schema(constantes.SCHEMA)\
        .table("maquinas")\
        .select("*", count="exact")\
        .eq("estatus", "EN MANTENIMIENTO")\
        .limit(0)\
        .execute()

    return respuesta.count

def conteo_activos_fuera_servicio():
    respuesta = supabase.schema(constantes.SCHEMA)\
        .table("maquinas")\
        .select("*", count="exact")\
        .eq("estatus", "FUERA DE SERVICIO")\
        .limit(0)\
        .execute()

    return respuesta.count

"""REGISTROS DE MANTENIMIENTO"""
def consultar_registros(tipo: str = ""):
    # Consultamos directamente la vista que es publica
    query = supabase.schema(constantes.SCHEMA)\
        .table("v_mantenimientos_publicos")\
        .select("*")\
        .order("created_at", desc=True)

    if tipo == "PREVENTIVO":
        query = query.eq("tipo", tipo)
        respuesta = query.execute()
        return respuesta.data

    elif tipo == "CORRECTIVO":
        query = query.eq("tipo", tipo)
        respuesta = query.execute()
        return respuesta.data

    else:
        respuesta = query.execute()
        return respuesta.data


def consultar_registros_id(folio: str):
    # Consultamos directamente la vista que es publica
    respuesta = supabase.schema(constantes.SCHEMA)\
        .table("v_mantenimientos_publicos")\
        .select("*")\
        .eq("maquina_folio", folio)\
        .order("created_at", desc=True)\
        .execute()
    return respuesta.data

def insertar_registro(datos: dict):
    supabase.schema(constantes.SCHEMA).table("mantenimientos").insert(datos).execute()

def actualizar_registro(id: str, datos: dict):
    supabase.schema(constantes.SCHEMA).table("mantenimientos").update(datos).eq("id", id).execute()

def eliminar_registro(id: str):
    supabase.schema(constantes.SCHEMA).table("mantenimientos").delete().eq("id", id).execute()

"""DASHBOARD / RESUMEN GENERAL"""
def consultar_registros_recientes():
    # Consultamos directamente la vista que es publica
    respuesta = supabase.schema(constantes.SCHEMA)\
        .table("v_mantenimientos_publicos")\
        .select("*")\
        .order("created_at", desc=True)\
        .limit(5)\
        .execute()

    return respuesta.data

def conteo_activos_operando():
    respuesta = supabase.schema(constantes.SCHEMA)\
        .table("maquinas")\
        .select("*", count="exact")\
        .eq("estatus", "OPERATIVO")\
        .limit(0)\
        .execute()

    return respuesta.count

def conteo_mantenimientos_programados():
    respuesta = supabase.schema(constantes.SCHEMA)\
        .table("v_mantenimientos_publicos")\
        .select("*", count="exact")\
        .eq("estatus", "PROGRAMADO")\
        .limit(0)\
        .execute()

    return respuesta.count

def conteo_mantenimientos_pendientes():
    respuesta = supabase.schema(constantes.SCHEMA)\
        .table("v_mantenimientos_publicos")\
        .select("*", count="exact")\
        .eq("estatus", "EN PROCESO")\
        .limit(0)\
        .execute()

    return respuesta.count

def datos_barras():
    """
    Retorna la siguiente estructura de datos (ejemplo):
    [{'name': 'CACHO', 'OPERATIVO': 0, 'EN MANTENIMIENTO': 0}, {'name': 'HIPODROMO', 'OPERATIVO': 0, 'EN MANTENIMIENTO': 0}]
    """
    respuesta = supabase.schema(constantes.SCHEMA)\
        .rpc("get_sucursales_status_stats", params={})\
        .execute()

    return respuesta.data

def datos_pastel(fecha_actual: datetime.date):
    try:
        # Calcular el rango del mes para la columna 'fecha' (YYYY-MM-DD)
        primer_dia = fecha_actual.replace(day=1).strftime("%Y-%m-%d")
        ultimo_dia = fecha_actual.replace(day=calendar.monthrange(fecha_actual.year, fecha_actual.month)[1]).strftime("%Y-%m-%d")
        
        # Consultamos en la vista publica v_mantenimientos_publicos
        respuesta = supabase.schema(constantes.SCHEMA)\
            .table("v_mantenimientos_publicos")\
            .select("estatus")\
            .gte("fecha", primer_dia)\
            .lte("fecha", ultimo_dia)\
            .execute()
            
        if respuesta.data:
            return respuesta.data

        # Si no hay registros en el mes actual, se obtienen todos los registros
        respuesta_todos = supabase.schema(constantes.SCHEMA)\
            .table("v_mantenimientos_publicos")\
            .select("estatus")\
            .execute()

        return respuesta_todos.data
    except Exception as e:
        print(f"Error al consultar Supabase: {e}")
        return []


"""PROVEEDORES"""
def consultar_proveedores():
    respuesta = supabase.schema(constantes.SCHEMA)\
        .table("proveedores")\
        .select("*")\
        .execute()
    return respuesta.data

def insertar_proveedor(datos: dict):
    supabase.schema(constantes.SCHEMA).table("proveedores").insert(datos).execute()

def actualizar_proveedor(id: str, datos: dict):
    supabase.schema(constantes.SCHEMA).table("proveedores").update(datos).eq("id", id).execute()

def conteo_preventivos_programados():
    respuesta = supabase.schema(constantes.SCHEMA)\
        .table("v_mantenimientos_publicos")\
        .select("*", count="exact")\
        .eq("tipo", "PREVENTIVO")\
        .eq("estatus", "PROGRAMADO")\
        .limit(0)\
        .execute()

    return respuesta.count

def conteo_preventivos_pendientes():
    respuesta = supabase.schema(constantes.SCHEMA)\
        .table("v_mantenimientos_publicos")\
        .select("*", count="exact")\
        .eq("tipo", "PREVENTIVO")\
        .eq("estatus", "EN PROCESO")\
        .limit(0)\
        .execute()

    return respuesta.count

def conteo_preventivos_realizados():
    respuesta = supabase.schema(constantes.SCHEMA)\
        .table("v_mantenimientos_publicos")\
        .select("*", count="exact")\
        .eq("tipo", "PREVENTIVO")\
        .eq("estatus", "REALIZADO")\
        .limit(0)\
        .execute()

    return respuesta.count

def conteo_preventivos_cancelados():
    respuesta = supabase.schema(constantes.SCHEMA)\
        .table("v_mantenimientos_publicos")\
        .select("*", count="exact")\
        .eq("tipo", "PREVENTIVO")\
        .eq("estatus", "CANCELADO")\
        .limit(0)\
        .execute()

    return respuesta.count

def conteo_correctivos_programados():
    respuesta = supabase.schema(constantes.SCHEMA)\
        .table("v_mantenimientos_publicos")\
        .select("*", count="exact")\
        .eq("tipo", "CORRECTIVO")\
        .eq("estatus", "PROGRAMADO")\
        .limit(0)\
        .execute()

    return respuesta.count

def conteo_correctivos_pendientes():
    respuesta = supabase.schema(constantes.SCHEMA)\
        .table("v_mantenimientos_publicos")\
        .select("*", count="exact")\
        .eq("tipo", "CORRECTIVO")\
        .eq("estatus", "EN PROCESO")\
        .limit(0)\
        .execute()

    return respuesta.count

def conteo_correctivos_realizados():
    respuesta = supabase.schema(constantes.SCHEMA)\
        .table("v_mantenimientos_publicos")\
        .select("*", count="exact")\
        .eq("tipo", "CORRECTIVO")\
        .eq("estatus", "REALIZADO")\
        .limit(0)\
        .execute()

    return respuesta.count

def conteo_correctivos_cancelados():
    respuesta = supabase.schema(constantes.SCHEMA)\
        .table("v_mantenimientos_publicos")\
        .select("*", count="exact")\
        .eq("tipo", "CORRECTIVO")\
        .eq("estatus", "CANCELADO")\
        .limit(0)\
        .execute()

    return respuesta.count