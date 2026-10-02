import reflex as rx
import base64
import uuid
import io
from ..services import supabase
from ..utils import constantes

class InicioSesionRegistroState(rx.State):
    auth_token: str = rx.LocalStorage("")
    refresh_token: str = rx.LocalStorage("")
    user_id: str = ""
    nombre:str = rx.LocalStorage("")
    empleado_id: str = rx.LocalStorage("")

    mostrar_password: bool = False # MANEJO DE MOSTRAR CONTRASEÑA


    @rx.event
    def ingresar(self, form:dict):
        if not form["correo"] or not form["password"]:
            return rx.toast.error("Complete los campos")
        
        try:
            respuesta = supabase.autenticacion(form["correo"], form["password"])

            # Error controlado
            if "error" in respuesta:
                return rx.toast.error(respuesta["error"])

            session = respuesta["session"]

            # Guardamos los tokens en el estado (se periste en LocalStorage)
            self.auth_token = session.session.access_token
            self.refresh_token = session.session.refresh_token
            self.user_id = respuesta["user_id"]

            empleado = respuesta["empleado"]
            self.nombre = empleado["nombre"]
            self.empleado_id = empleado["id"]
            
            sistemas = respuesta["sistemas"]

            if not constantes.SISTEMA in sistemas:
                return rx.toast.error("Acceso denegado")
            return [
                rx.toast.success("Bienvenido"),
                rx.redirect("/registrar")
                ]
        
        except Exception as e:
            error_msg = str(e)
            print(error_msg)

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
        supabase.cierre_sesion() # Cierre de sesion de supabase
        return rx.redirect("/inicio-sesion-registro", replace=True)

    @rx.event
    def on_load(self):
        if self.auth_token and self.refresh_token:
            try:
                supabase.restaurar_sesion(self.auth_token, self.refresh_token)
            except:
                self.logout()
        else:
            return rx.redirect("/inicio-sesion-registro")

    @rx.var
    def is_logged_in(self) -> bool:
        return self.auth_token != ""
    
    @rx.event
    def toggle_show(self):
        self.mostrar_password = not self.mostrar_password