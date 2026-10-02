import reflex as rx
from ..components.widgets_cambio_password import formulario

def cambio_password_page():
    return rx.vstack(
        formulario(),
        width="100%"
    )