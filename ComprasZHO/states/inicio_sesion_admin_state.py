import reflex as rx
from ..services import supabase
from ..utils import constantes


class InicioSesionAdminState(rx.State):
    auth_token: str = rx.LocalStorage("")
    refresh_token: str = rx.LocalStorage("")
    user_id: str = ""
    nombre: str = rx.LocalStorage("")
    empleado_id: str = rx.LocalStorage("")
    rol: str = rx.LocalStorage("")

    mostrar_password: bool = False # MANEJO DE MOSTRAR CONTRASEÑA

    @rx.event
    def ingresar(self, form: dict):
        correo = form.get("correo", "").strip()
        password = form.get("password", "").strip()

        if not correo or not password:
            return rx.toast.error("Complete todos los campos")
        
        try:
            respuesta = supabase.autenticacion(correo, password)

            # Error controlado
            if "error" in respuesta:
                return rx.toast.error(respuesta["error"])

            session = respuesta["session"]

            # Guardamos los tokens en el estado (se persiste en LocalStorage)
            self.auth_token = session.session.access_token
            self.refresh_token = session.session.refresh_token
            self.user_id = respuesta["user_id"]

            
            sistemas = respuesta.get("sistemas", [])

            for i in sistemas:
                if i["sistema"] == constantes.SISTEMA:
                    self.rol = i["rol"]
                    self.nombre = i["nombre_personal"]
                    break
                else:
                    return rx.toast.error("Acceso denegado: No cuenta con permisos para este sistema")

            """SE OBTIENE LOS METADATOS"""
            user_metadata = session.user.user_metadata

            # VARIABLE QUE DETERMINA SI NECESITA CAMBIAR SU CONTRASEÑA POR PRIMERA VEZ
            needs_change = user_metadata.get("needs_password_change", False)
            if needs_change:
                return rx.redirect("/cambio-password")
            
            return [
                rx.toast.success(f"Bienvenido {self.nombre}"),
                rx.redirect("/panel")
            ]
        
        except Exception as e:
            error_msg = str(e)
            print(f"Error en ingresar: {error_msg}")

            if "Email not confirmed" in error_msg:
                return rx.toast.error("Correo no confirmado")

            if "Invalid login credentials" in error_msg:
                return rx.toast.error("Correo o contraseña incorrectos")
            
            return rx.toast.error("Error del sistema")

    @rx.event
    def logout(self):
        self.auth_token = ""
        self.refresh_token = ""
        self.user_id = ""
        self.nombre = ""
        self.empleado_id = ""
        self.rol = ""
        try:
            supabase.cierre_sesion() # Cierre de sesion de supabase
        except Exception as e:
            print(f"Error en cierre de sesión: {e}")
        return rx.redirect("/inicio-sesion-admin", replace=True)

    @rx.event
    def check_authenticated(self):
        if not self.auth_token:
            return rx.redirect("/inicio-sesion-admin")
        try:
            if self.auth_token and self.refresh_token:
                supabase.restaurar_sesion(self.auth_token, self.refresh_token)
        except Exception as e:
            print(f"Error restaurando sesión: {e}")
            return self.logout()

    @rx.event
    def check_already_logged_in(self):
        if self.auth_token:
            return rx.redirect("/panel")

    @rx.var
    def is_logged_in(self) -> bool:
        return self.auth_token != ""
    
    @rx.event
    def toggle_show(self):
        self.mostrar_password = not self.mostrar_password