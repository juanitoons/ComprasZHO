import reflex as rx
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
