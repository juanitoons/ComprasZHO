import reflex as rx
from ..components.widgets_auth import vista_login_google, contenedor_protegido
from ..states.auth_state import AuthState


def login_page() -> rx.Component:
    """Página de inicio de sesión con Google OAuth."""
    return vista_login_google()


def hub_page() -> rx.Component:
    """Página principal (Hub Dashboard) protegida por autenticación RBAC."""
    return contenedor_protegido(
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.heading(f"Hola, {AuthState.user_nombre}", size="8"),
                    rx.text("¿Qué necesitas hacer hoy?", color_scheme="gray"),
                    align_items="start"
                ),
                rx.spacer(),
                rx.button("Cerrar Sesión", on_click=AuthState.logout, color_scheme="red", variant="outline"),
                width="100%",
                align="center",
                padding_bottom="24px"
            ),
            rx.divider(),
            rx.grid(
                rx.cond(
                    AuthState.puede_ver_solicitudes,
                    rx.card(
                        rx.vstack(
                            rx.heading("1. Solicitudes", size="5"),
                            rx.text("Crear orden de compra o solicitud de fondos"),
                            rx.badge("Tus solicitudes activos", color_scheme="blue"),
                            rx.button("Ingresar", width="100%"),
                            spacing="3"
                        ),
                        padding="20px"
                    )
                ),
                rx.cond(
                    AuthState.puede_ver_autorizaciones,
                    rx.card(
                        rx.vstack(
                            rx.heading("2. Autorizaciones", size="5"),
                            rx.text("Bandeja de firmas pendientes"),
                            rx.badge("Pendientes por firmar", color_scheme="orange"),
                            rx.button("Ingresar", width="100%"),
                            spacing="3"
                        ),
                        padding="20px"
                    )
                ),
                rx.cond(
                    AuthState.puede_ver_copy_paste,
                    rx.card(
                        rx.vstack(
                            rx.heading("3. Copy Paste Admin", size="5"),
                            rx.text("Exportar 10 columnas (B-K) para Excel"),
                            rx.badge("Listas para pegar", color_scheme="green"),
                            rx.button("Ingresar", width="100%"),
                            spacing="3"
                        ),
                        padding="20px"
                    )
                ),
                rx.cond(
                    AuthState.puede_ver_admin,
                    rx.card(
                        rx.vstack(
                            rx.heading("4. Administrador", size="5"),
                            rx.text("Usuarios, roles, catálogos y topes"),
                            rx.badge("Gestión total", color_scheme="purple"),
                            rx.button("Ingresar", width="100%"),
                            spacing="3"
                        ),
                        padding="20px"
                    )
                ),
                columns="2",
                spacing="4",
                width="100%"
            ),
            width="100%",
            max_width="1000px",
            padding="40px"
        )
    )
