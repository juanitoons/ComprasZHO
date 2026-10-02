import reflex as rx
from ..states.cambio_password_state import CambioPassword

def formulario() -> rx.Component:
    return rx.flex(
        rx.color_mode.button(position="top-right"),
        rx.box(
            rx.form(
                rx.vstack(
                    rx.vstack(
                        rx.heading("Bienvenido", size="8", weight="bold"),
                        rx.text("Cambia tu contraseña", size="6", color_scheme="gray"),
                        width="100%",
                        align="center",
                        spacing="2"
                    ),
                    rx.vstack(
                        rx.text("Contraseña"),
                        rx.input(
                            placeholder="Contraseña",
                            name="password",
                            type=rx.cond(CambioPassword.mostrar_password, "text", "password"),
                            width="100%", 
                            size="3"
                        ),
                        rx.text("Mínimo 8 caracteres", size="1", color_scheme="gray"),
                        width="100%",
                        spacing="1"
                    ),
                    rx.vstack(
                        rx.text("Confirmar Contraseña"),
                        rx.input(
                            placeholder="Confirmar Contraseña",
                            name="confirmacion",
                            type=rx.cond(CambioPassword.mostrar_password, "text", "password"),
                            width="100%", 
                            size="3"
                        ),
                        rx.text("Mínimo 8 caracteres", size="1", color_scheme="gray"),
                        width="100%",
                        spacing="1"
                    ),
                    rx.hstack(
                        rx.switch(on_change=CambioPassword.toggle_show),
                        rx.text("Mostrar contraseña", weight="medium"),
                        spacing="2",
                        align="center"
                    ),
                    rx.button("Cambiar contraseña", type="submit", width="100%", height="40px"),
                    spacing="6",
                ),
                on_submit=CambioPassword.actualizar,
                reset_on_submit=False,
            ),
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