import reflex as rx

def selectores(texto,contenido):
    return rx.vstack(
        rx.text(texto),
        rx.select(contenido)
    )

def solicitudes():
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.button(
                    "Nueva solicitud",
                    border_radius="1em",
                    box_sizing="border-box",
                    color="white",
                    opacity=1,
                ),
                rx.button(
                    "Mis solicitudes",
                    border_radius="1em",
                    box_sizing="border-box",
                    color="white",
                    opacity=1,
                )
            ),
            rx.container(
                rx.vstack(
                    rx.hstack(
                        rx.text("Levantar solicitud", font_weight="bold", color="white"),
                        rx.radio(
                            [""
                            "Orden de compra", "Fondos"], direction="row"
                        )
                    ),
                rx.divider(size="4"),
                rx.hstack(
                    selectores("UNIDAD DE NEGOCIO",["Brecha","hola"]),
                    selectores("AREA QUE SOLICITA",["Operacion de la unidad"])
                )
                )
            )
        ),
        width="100%"
    )
