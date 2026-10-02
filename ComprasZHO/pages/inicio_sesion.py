import reflex as rx
from ..components.widgets_inicio_sesion import formulario_registro, formulario_admin

def inicio_sesion_registro_page():
    return rx.vstack(
        formulario_registro(),
        width="100%"
    )

def inicio_sesion_admin_page():
    return rx.vstack(
        formulario_admin(),
        width="100%"
    )