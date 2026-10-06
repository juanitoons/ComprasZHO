import reflex as rx
from ..components.widgets_auth import vista_login_google, contenedor_protegido
from ..states.auth_state import AuthState
from ..components.sidebar import sidebar
from ..states.panel_state import PanelState
from ..pages.solicitudes_page import solicitudes


def login_page() -> rx.Component:
    """Página de inicio de sesión con Google OAuth."""
    return vista_login_google()


def hub_page() -> rx.Component:
    return rx.hstack(
        sidebar(),
        rx.vstack(
            rx.match(
                PanelState.active_tab,
                (
                    "solicitudes",
                    rx.vstack(
                        rx.vstack(
                            rx.heading("Solicitudes", size="8"),
                            rx.heading("Resumen general de mantenimiento", size="5", color_scheme="gray"),
                        ),
                        solicitudes(),
                        width="100%",
                        spacing="6"
                    ),
                ),
                (
                    "autorizaciones",
                    rx.vstack(
                        rx.vstack(
                            rx.heading("Autorizaciones", size="8"),
                            rx.heading("Gestión de maquinas y otros activos", size="5", color_scheme="gray"),
                        ),
#                        activos_page(),
                        width="100%",
                        spacing="6"
                    ),
                ),
                (
                    "copy paste",
                    rx.vstack(
                        rx.vstack(
                            rx.heading("Copy Paste Admin", size="8"),
                            rx.heading("Registros de mantenimiento preventivos", size="5", color_scheme="gray"),
                        ),
 #                       preventivos_page(),
                        width="100%",
                        spacing="6"
                    ),
                ),
                (
                    "administrador",
                    rx.vstack(
                        rx.vstack(
                            rx.heading("Administrador", size="8"),
                            rx.heading("Ususarios, accesos y reglas", size="5", color_scheme="gray"),
                        ),
 #                       preventivos_page(),
                        width="100%",
                        spacing="6"
                    ),
                )
            ),
            padding="40px",
            # CAMBIOS AQUÍ:
            flex="1",               # Hace que tome solo el espacio restante al lado del sidebar
            height="100vh",         # Asegura que respete la altura de la ventana
            overflow_y="auto",      # Permite scroll vertical en el contenido si es muy largo
            overflow_x="auto",      # Permite scroll horizontal interno si la tabla es más ancha que la pantalla
        ),
        width="100vw",              # Asegura el ancho completo de la ventana del navegador
        height="100vh",
        spacing="0",
        #bg=rx.color("gray", 1),     # Fondo base opcional para que contraste con el sidebar
    )
