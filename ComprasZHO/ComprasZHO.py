import reflex as rx
from .pages.inicio_sesion import inicio_sesion_registro_page, inicio_sesion_admin_page
from rxconfig import config


class State(rx.State):
    """The app state."""


def index() -> rx.Component:
    return inicio_sesion_admin_page()
    


app = rx.App()
app.add_page(index)
