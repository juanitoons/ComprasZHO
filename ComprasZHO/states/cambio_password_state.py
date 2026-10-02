import reflex as rx
from ..services import supabase

class CambioPassword(rx.State):
    mostrar_password: bool = False

    @rx.event
    def toggle_show(self, _=None):
        self.mostrar_password = not self.mostrar_password

    @rx.event
    def actualizar(self, form: dict):
        password = form.get("password", "")
        confirmacion = form.get("confirmacion", "")

        if not password or not confirmacion:
            return rx.toast.error("Complete todos los campos")

        if len(password) < 8:
            return rx.toast.error("La contraseña debe tener al menos 8 caracteres")

        if password != confirmacion:
            return rx.toast.error("Las contraseñas no coinciden")

        try:
            supabase.actualizar_password(password)
            return [
                rx.toast.success("Contraseña actualizada con éxito"),
                rx.redirect("/panel")
            ]
        except Exception as e:
            return rx.toast.error(f"Error al actualizar contraseña: {str(e)}")
        