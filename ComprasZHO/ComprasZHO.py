import reflex as rx
from .pages.inicio_sesion import inicio_sesion_registro_page, inicio_sesion_admin_page
from .pages.cambio_password import cambio_password_page
from .pages.login import login_page, hub_page
from .pages.test_page import test_page
from rxconfig import config


class State(rx.State):
    """The app state."""


def index() -> rx.Component:
    return login_page()


app = rx.App()
app.add_page(index, route="/")
app.add_page(login_page, route="/login")
app.add_page(hub_page, route="/hub")
app.add_page(test_page, route="/test")
app.add_page(inicio_sesion_admin_page, route="/inicio-sesion-admin")
app.add_page(inicio_sesion_registro_page, route="/inicio-sesion-registro")
app.add_page(cambio_password_page, route="/cambio-password")


