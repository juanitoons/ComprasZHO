import reflex as rx
from ..utils import iconos
from ..states.inicio_sesion_registro_state import InicioSesionRegistroState
from ..states.inicio_sesion_admin_state import InicioSesionAdminState

def formulario_registro() -> rx.Component:
    return rx.flex(
        rx.color_mode.button(position="top-right"),
        rx.box(
            rx.form(
                rx.vstack(
                    rx.hstack(
                        rx.heading("Registro", size="9", weight="bold"),
                        width="100%",
                        align="center",
                        justify="center",
                    ),
                    rx.vstack(
                        rx.heading("Bienvenido", size="8", weight="bold"),
                        rx.text("Inicia sesión con tu cuenta"),
                        width="100%",
                        align="center",
                        spacing="2"
                    ),
                    rx.vstack(
                        rx.text("Correo Electrónico"),
                        rx.input(
                            rx.input.slot(rx.icon(iconos.MAIL)),
                            placeholder="Correo Electrónico",
                            name="correo",
                            #auto_complete=False,
                            type="email",
                            width="100%", 
                            size="3"
                        ),
                        width="100%",
                        spacing="1"
                    ),
                    rx.vstack(
                        rx.text("Contraseña"),
                        rx.input(
                            rx.input.slot(rx.icon(iconos.PASSWORD)),
                            placeholder="Contraseña",
                            #auto_complete=False,
                            name="password",
                            type=rx.cond(InicioSesionRegistroState.mostrar_password, "text", "password"),
                            width="100%", 
                            size="3"
                            ),
                        width="100%",
                        spacing="1"
                    ),
                    rx.hstack(
                        rx.switch(on_change=InicioSesionRegistroState.toggle_show),
                        rx.text("Mostrar contraseña", weight="medium"),
                        spacing="2",
                        align="center"
                    ),
                    rx.button("Ingresar", type="submit", width="100%", height="40px"),
                    spacing="6",
                ),
                on_submit=InicioSesionRegistroState.ingresar,
                reset_on_submit=True,
            ),
            background=rx.color("gray", 1),
            border_radius="10px",
            min_width="30vw",
            padding="40px",
            box_shadow="0px 10px 20px 0px rgba(0,0,0,0.75)"
        ),
        width="100%",
        min_height="100vh",
        justify="center",
        align="center",
    )

def formulario_admin() -> rx.Component:
    return rx.flex(
        rx.color_mode.button(position="top-right"),
        rx.box(
            rx.form(
                rx.vstack(
                    rx.hstack(
                        rx.heading("Portal Zibarita", size="9", weight="bold"),
                        width="100%",
                        align="center",
                        justify="center",
                    ),
                    rx.vstack(
                        rx.heading("Bienvenido", size="8", weight="bold"),
                        rx.text("Inicia sesión con tu cuenta"),
                        width="100%",
                        align="center",
                        spacing="2"
                    ),
                    rx.vstack(
                        rx.text("Correo Electrónico"),
                        rx.input(
                            rx.input.slot(rx.icon(iconos.MAIL)),
                            placeholder="Correo Electrónico",
                            name="correo",
                            #auto_complete=False,
                            type="email",
                            width="100%", 
                            size="3"
                        ),
                        width="100%",
                        spacing="1"
                    ),
                    rx.vstack(
                        rx.text("Contraseña"),
                        rx.input(
                            rx.input.slot(rx.icon(iconos.PASSWORD)),
                            placeholder="Contraseña",
                            #auto_complete=False,
                            name="password",
                            type=rx.cond(InicioSesionAdminState.mostrar_password, "text", "password"),
                            width="100%", 
                            size="3"
                            ),
                        width="100%",
                        spacing="1"
                    ),
                    rx.hstack(
                        rx.switch(on_change=InicioSesionAdminState.toggle_show),
                        rx.text("Mostrar contraseña", weight="medium"),
                        spacing="2",
                        align="center"
                    ),
                    rx.button("Ingresar", type="submit", width="100%", height="40px"),
                    spacing="6",
                ),
                on_submit=InicioSesionAdminState.ingresar,
                reset_on_submit=True,
            ),
            background=rx.color("gray", 1),
            border_radius="10px",
            min_width="30vw",
            padding="40px",
            box_shadow="0px 10px 20px 0px rgba(0,0,0,0.75)"
        ),
        width="100%",
        min_height="100vh",
        justify="center",
        align="center",
    )