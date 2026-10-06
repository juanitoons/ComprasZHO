import reflex as rx
from ..utils import iconos
from ..states.panel_state import PanelState

"""Funcion reutilizable para crear un botón de navegación en el sidebar"""
def nav_item(icono:str, label:str, tab_id:str):
    is_active = PanelState.active_tab == tab_id
    return rx.button(
        rx.hstack(
            rx.icon(icono, size=20),
            rx.text(label, weight="bold"),
            width="100%",
            justify="start",
            align="center"
        ),
        variant=rx.cond(
            is_active,
            "soft",
            "ghost"
        ),
        color_scheme=rx.cond(
            is_active,
            "blue",
            "gray"
        ),
        #variant="surface",
        # variant="ghost",
        width="100%",
        size="3",
        on_click=lambda: PanelState.set_tab(tab_id),
    )

"""Contenido interno del sidebar con los botones para navegar"""
def sidebar_content():
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.icon("monitor_cog", color=rx.color("accent", 8), size=30),
                rx.vstack(
                    rx.text("Sistemas", size="4", weight="bold"),
                    rx.text("Panel de Gestión", size="2", color_scheme="gray"),
                    spacing="0"
                ),
                align="center"
            ),
            rx.vstack(
                nav_item(iconos.DASHBOARD, "Solicitudes", "solicitudes"),
                nav_item(iconos.ASIGNACION, "Autorizaciones", "autorizaciones"),
                nav_item(iconos.PERSONAL, "Copy Paste", "copy paste"),
                nav_item(iconos.ASIGNACION, "Administrador", "administrador"),
                #nav_item(iconos.CONFIGURACION, "Configuración", "config"),
                width="100%",
                spacing="6"
            ),
            spacing="6"
        ),
        width="100%",
        padding="20px"
    )

"""Sidebar que se muestra en el panel de control"""
def sidebar():
    return rx.vstack(
        sidebar_content(),
        perfil_preferencias(),
        width="260px",
        height="100vh",
        flex_shrink="0",
        bg=rx.color("gray", 1),
        justify="between"
    )

def perfil_preferencias():
    return rx.vstack(
        rx.hstack(
            rx.avatar(fallback="ZH", radius="full"),
            rx.vstack(
            #    rx.text(InicioSesionAdminState.nombre, weight="bold"),
                rx.text("Admin", color_scheme="gray", size="1"),
                spacing="0"
            ),
        ),
        rx.hstack(
            rx.color_mode.button(),
            #rx.icon_button(iconos.CIERRE_SESION, variant="ghost", color_scheme="gray", radius="full", on_click=InicioSesionAdminState.logout),
            justify="end",
            align="center",
            width="100%"
        ),
        width="100%",
        padding="20px",
        justify="between"
    )