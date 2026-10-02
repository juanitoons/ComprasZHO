import reflex as rx
from typing import List, Callable
from ..states.auth_state import AuthState


def boton_google_login() -> rx.Component:
    """Componente de UI para iniciar sesión mediante Google OAuth con el dominio corporativo."""
    return rx.vstack(
        rx.button(
            rx.hstack(
                rx.icon(tag="chrome", size=20),
                rx.text("Entrar con Google", weight="bold", size="3"),
                align="center",
                spacing="3"
            ),
            on_click=AuthState.iniciar_sesion_google,
            width="100%",
            height="48px",
            variant="solid",
            color_scheme="blue",
            cursor="pointer",
            border_radius="8px"
        ),
        rx.text(
            "Acceso restringido a cuentas @zibarisholding.com",
            size="1",
            color_scheme="gray",
            align="center"
        ),
        spacing="2",
        width="100%"
    )


def vista_login_google() -> rx.Component:
    """Pantalla completa de Inicio de Sesión limpia y corporativa para Grupo Zibarita."""
    return rx.flex(
        rx.color_mode.button(position="top-right"),
        rx.box(
            rx.vstack(
                rx.vstack(
                    rx.heading("Grupo Zibarita", size="8", weight="bold"),
                    rx.text("Portal de Solicitudes y Órdenes de Compra", size="3", color_scheme="gray"),
                    align="center",
                    spacing="2",
                    width="100%"
                ),
                rx.divider(margin_y="4px"),
                boton_google_login(),
                rx.cond(
                    AuthState.error_message != "",
                    rx.callout(
                        AuthState.error_message,
                        icon="triangle_alert",
                        color_scheme="red",
                        width="100%"
                    )
                ),
                spacing="6",
                width="100%"
            ),
            background=rx.color("gray", 1),
            border_radius="12px",
            min_width="340px",
            max_width="420px",
            padding="32px",
            box_shadow="0px 10px 25px rgba(0,0,0,0.15)"
        ),
        width="100%",
        min_height="100vh",
        justify="center",
        align="center",
        background="var(--gray-2)",
        on_mount=AuthState.procesar_codigo_oauth
    )


def contenedor_protegido(
    contenido: rx.Component,
    roles_requeridos: List[str] = None
) -> rx.Component:
    """
    Wrapper de UI para envolver vistas que requieran autenticación y roles específicos.
    Muestra advertencia o redirige en caso de no contar con acceso.
    """
    return rx.cond(
        AuthState.is_logged_in,
        contenido,
        rx.flex(
            rx.spinner(size="3"),
            on_mount=AuthState.verificar_sesion_protegida(roles_requeridos),
            width="100%",
            min_height="100vh",
            justify="center",
            align="center"
        )
    )
