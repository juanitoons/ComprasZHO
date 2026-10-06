import json
import reflex as rx
from typing import List
from ..services.auth_service import (
    obtener_url_login_google,
    procesar_autenticacion_usuario,
    intercambiar_codigo_pkce
)


class AuthState(rx.State):
    """Estado global de Autenticación y Control de Accesos Basado en Roles (RBAC)."""
    
    auth_token: str = rx.LocalStorage("")
    user_id: str = rx.LocalStorage("")
    user_email: str = rx.LocalStorage("")
    user_nombre: str = rx.LocalStorage("")
    user_roles_json: str = rx.LocalStorage("[]")
    
    is_authenticating: bool = False
    error_message: str = ""
    last_processed_code: str = ""

    @rx.var
    def user_roles(self) -> List[str]:
        """Deserializa y retorna la lista de roles desde LocalStorage JSON."""
        if not self.user_roles_json:
            return []
        try:
            return json.loads(self.user_roles_json)
        except Exception:
            return []

    @rx.var
    def is_logged_in(self) -> bool:
        """Indica si existe una sesión activa almacenada."""
        return self.auth_token != "" and self.user_id != ""

    @rx.var
    def es_admin(self) -> bool:
        """Retorna True si el usuario posee los roles 'admin' o 'director'."""
        return any(rol in ["admin", "director"] for rol in self.user_roles)

    @rx.var
    def es_director(self) -> bool:
        return "director" in self.user_roles

    @rx.var
    def es_revisor(self) -> bool:
        return "revisor" in self.user_roles

    @rx.var
    def es_compras(self) -> bool:
        return "compras" in self.user_roles

    @rx.var
    def es_contable(self) -> bool:
        return "contable" in self.user_roles

    @rx.var
    def es_solicitante(self) -> bool:
        return "solicitante" in self.user_roles

    @rx.var
    def puede_ver_solicitudes(self) -> bool:
        return any(r in self.user_roles for r in ["solicitante", "admin", "director"])

    @rx.var
    def puede_ver_autorizaciones(self) -> bool:
        return any(r in self.user_roles for r in ["revisor", "director", "admin"])

    @rx.var
    def puede_ver_copy_paste(self) -> bool:
        return any(r in self.user_roles for r in ["contable", "admin", "director"])

    @rx.var
    def puede_ver_admin(self) -> bool:
        return any(r in self.user_roles for r in ["admin", "director"])

    def tiene(self, *roles_requeridos: str) -> bool:
        """Verifica si el usuario posee al menos uno de los roles indicados (en backend/eventos)."""
        return any(r in self.user_roles for r in roles_requeridos)

    @rx.event
    def procesar_codigo_oauth(self):
        """Si la URL trae el parámetro ?code=..., intercambia por token y procesa la sesión."""
        params = self.router.page.params
        code = params.get("code")
        if not code or code == self.last_processed_code:
            return

        self.last_processed_code = code
        self.is_authenticating = True
        self.error_message = ""
        
        try:
            token = intercambiar_codigo_pkce(code)
            perfil, roles = procesar_autenticacion_usuario(token)
            
            self.auth_token = token
            self.user_id = perfil["id"]
            self.user_email = perfil["email"]
            self.user_nombre = perfil["nombre"]
            self.user_roles_json = json.dumps(roles)
            self.is_authenticating = False
            
            yield rx.toast.success(f"Bienvenido {self.user_nombre}")
            yield rx.redirect("/test")
        except PermissionError as pe:
            self.is_authenticating = False
            self.error_message = str(pe)
            self.limpiar_sesion()
            yield rx.toast.error(str(pe))
        except Exception as e:
            self.is_authenticating = False
            self.error_message = str(e)
            self.limpiar_sesion()
            yield rx.toast.error(f"Error al procesar callback OAuth: {str(e)}")

    @rx.event
    def iniciar_sesion_google(self):
        """Redirige al usuario al flujo Google OAuth con restricción de dominio."""
        try:
            url_oauth = obtener_url_login_google()
            return rx.redirect(url_oauth)
        except Exception as e:
            self.error_message = str(e)
            return rx.toast.error(f"Error al iniciar OAuth: {str(e)}")

    @rx.event
    def callback_autenticacion(self, token: str):
        """
        Recibe el JWT emitido tras el flujo OAuth y procesa
        la validación, alta silenciosa y carga de roles.
        """
        self.is_authenticating = True
        self.error_message = ""
        
        try:
            perfil, roles = procesar_autenticacion_usuario(token)
            
            self.auth_token = token
            self.user_id = perfil["id"]
            self.user_email = perfil["email"]
            self.user_nombre = perfil["nombre"]
            self.user_roles_json = json.dumps(roles)
            self.is_authenticating = False
            
            yield rx.toast.success(f"Bienvenido {self.user_nombre}")
            yield rx.redirect("/test")
        except PermissionError as pe:
            self.is_authenticating = False
            self.error_message = str(pe)
            self.limpiar_sesion()
            yield rx.toast.error(str(pe))
        except Exception as e:
            self.is_authenticating = False
            self.error_message = str(e)
            self.limpiar_sesion()
            yield rx.toast.error(f"Error de autenticación: {str(e)}")

    @rx.event
    def verificar_sesion_protegida(self, roles_requeridos: List[str] = None):
        """
        Guardia de vista: verifica si hay sesión válida y si el usuario cumple
        con los roles requeridos. Redirige al login si no tiene acceso.
        """
        if not self.is_logged_in:
            yield rx.redirect("/")
            return

        if roles_requeridos:
            tiene_acceso = any(r in self.user_roles for r in roles_requeridos)
            if not tiene_acceso:
                yield rx.toast.error("No tienes permisos suficientes para acceder a este módulo.")
                yield rx.redirect("/hub")

    @rx.event
    def logout(self):
        """Cierra la sesión y limpia el almacenamiento local."""
        self.limpiar_sesion()
        yield rx.toast.info("Sesión cerrada correctamente")
        yield rx.redirect("/")

    def limpiar_sesion(self):
        self.auth_token = ""
        self.user_id = ""
        self.user_email = ""
        self.user_nombre = ""
        self.user_roles_json = "[]"
        self.error_message = ""
