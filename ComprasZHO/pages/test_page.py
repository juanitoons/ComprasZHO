import reflex as rx
from ..components.widgets_auth import contenedor_protegido
from ..states.auth_state import AuthState


def test_page() -> rx.Component:
    """Página de prueba para verificar que el login y los roles se hayan cargado correctamente."""
    return contenedor_protegido(
        rx.vstack(
            rx.card(
                rx.vstack(
                    rx.hstack(
                        rx.icon(tag="circle_check", size=32, color="var(--green-9)"),
                        rx.vstack(
                            rx.heading(" Autenticación Exitosa (Modo Prueba)", size="6"),
                            rx.text("La sesión de Google OAuth y Supabase se inició correctamente."),
                            align_items="start",
                            spacing="1"
                        ),
                        width="100%",
                        align="center",
                        spacing="3"
                    ),
                    rx.divider(margin_y="16px"),
                    
                    # Información del Perfil
                    rx.vstack(
                        rx.heading(" Datos del Perfil Sincronizado", size="4"),
                        rx.hstack(
                            rx.text("ID de Usuario:", weight="bold"),
                            rx.code(AuthState.user_id),
                            spacing="2"
                        ),
                        rx.hstack(
                            rx.text("Nombre Completo:", weight="bold"),
                            rx.text(AuthState.user_nombre),
                            spacing="2"
                        ),
                        rx.hstack(
                            rx.text("Correo Electrónico:", weight="bold"),
                            rx.text(AuthState.user_email),
                            spacing="2"
                        ),
                        align_items="start",
                        spacing="2",
                        width="100%"
                    ),
                    
                    rx.divider(margin_y="16px"),
                    
                    # Roles asignados
                    rx.vstack(
                        rx.heading(" Roles Asignados en Base de Datos (RBAC)", size="4"),
                        rx.hstack(
                            rx.foreach(
                                AuthState.user_roles,
                                lambda r: rx.badge(r, color_scheme="blue", variant="solid", size="2")
                            ),
                            spacing="2",
                            wrap="wrap"
                        ),
                        rx.cond(
                            AuthState.es_admin,
                            rx.callout(
                                "👑 Eres el PRIMER USUARIO o ADMINISTRADOR. Tienes acceso completo a todos los módulos.",
                                icon="crown",
                                color_scheme="purple",
                                width="100%",
                                margin_top="8px"
                            )
                        ),
                        align_items="start",
                        spacing="2",
                        width="100%"
                    ),

                    rx.divider(margin_y="16px"),

                    # Módulos permitidos
                    rx.vstack(
                        rx.heading(" Permisos de Módulos Habilitados", size="4"),
                        rx.hstack(
                            rx.badge("1. Solicitudes", color_scheme=rx.cond(AuthState.puede_ver_solicitudes, "green", "gray")),
                            rx.badge("2. Autorizaciones", color_scheme=rx.cond(AuthState.puede_ver_autorizaciones, "green", "gray")),
                            rx.badge("3. Copy Paste Admin", color_scheme=rx.cond(AuthState.puede_ver_copy_paste, "green", "gray")),
                            rx.badge("4. Administrador", color_scheme=rx.cond(AuthState.puede_ver_admin, "green", "gray")),
                            spacing="2",
                            wrap="wrap"
                        ),
                        align_items="start",
                        spacing="2",
                        width="100%"
                    ),

                    rx.divider(margin_y="16px"),

                    # Acciones de Prueba
                    rx.hstack(
                        rx.button(
                            "Ir al Hub Principal",
                            on_click=rx.redirect("/hub"),
                            color_scheme="blue",
                            variant="solid"
                        ),
                        rx.button(
                            "Cerrar Sesión",
                            on_click=AuthState.logout,
                            color_scheme="red",
                            variant="outline"
                        ),
                        spacing="3",
                        width="100%",
                        justify="end"
                    ),
                    padding="24px",
                    width="100%"
                ),
                width="100%",
                max_width="700px"
            ),
            width="100%",
            min_height="100vh",
            justify="center",
            align="center",
            padding="24px"
        )
    )
