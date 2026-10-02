import reflex as rx
from ..services import supabase

class CambioPassword(rx.State):
    mostrar_password: bool = False

    @rx.event
    def toggle_show(self):
        self.mostrar_password = not self.mostrar_password

    @rx.event
    def actualizar(self, form:dict):
        if form["password"] != form["confirmacion"]:
            return rx.toast.error("Las contraseñas no coinciden")

        supabase.actualizar_password(form["password"])
        return [
            rx.toast.success("Contraseña actualizada con éxito"),
            rx.redirect("/panel")
        ]
        