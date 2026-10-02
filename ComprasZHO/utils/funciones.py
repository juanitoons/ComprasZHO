import reflex as rx
from datetime import datetime
from ..utils import iconos

def color_estatus(status):
    return rx.cond(
        status == "Finalizado",
        rx.color("green", 9),
        rx.cond(
            status == "Pendiente",
            rx.color("orange", 9),
            rx.color("red", 9)
        )
    )

# def estatus(valor):
#     return rx.cond(
#         valor,
#         rx.box(
#             border_radius="9999px",
#             background=rx.color("green", 9),
#             width="20px",
#             height="20px"
#         ),
#         rx.box(
#             border_radius="9999px",
#             background=rx.color("red", 9),
#             width="20px",
#             height="20px"
#         )
#     )

def estatus_activo(valor):
    return rx.match(
        valor,
        (
            "OPERATIVO",
            rx.badge(
                rx.hstack(
                    rx.el.span(
                        class_name="w-1.5 h-1.5 rounded-full bg-emerald-500"
                    ),
                    rx.text("OPERATIVO", weight="bold"),
                    align="center"
                ),
                variant="surface",
                color_scheme="green"
            )
        ),
        (
            "EN MANTENIMIENTO",
            rx.badge(
                rx.hstack(
                    rx.el.span(
                        class_name="w-1.5 h-1.5 rounded-full bg-amber-500"
                    ),
                    rx.text("EN MANTENIMIENTO", weight="bold"),
                    align="center"
                ),
                variant="surface",
                color_scheme="amber"
            )
        ),
        (
            "FUERA DE SERVICIO",
            rx.badge(
                rx.hstack(
                    rx.el.span(
                        class_name="w-1.5 h-1.5 rounded-full bg-red-500"
                    ),
                    rx.text("FUERA DE SERVICIO", weight="bold"),
                    align="center"
                ),
                variant="surface",
                color_scheme="red"
            )
        ),
        rx.el.span(
            valor,
            class_name="inline-flex items-center px-2 py-0.5 rounded-md text-xs font-semibold bg-gray-100 text-gray-700 w-fit",
        ),
    )

def tipo_mantenimiento(valor):
    return rx.match(
        valor,
        (
            "PREVENTIVO",
            rx.badge(
                rx.hstack(
                    rx.icon(
                        iconos.PREVENTIVO,
                        size=18
                    ),
                    rx.text("PREVENTIVO", weight="bold"),
                    align="center"
                ),
                variant="surface",
                color_scheme="indigo"
            )
        ),
        (
            "CORRECTIVO",
            rx.badge(
                rx.hstack(
                    rx.icon(
                        iconos.CORRECTIVO,
                        size=18
                    ),
                    rx.text("CORRECTIVO", weight="bold"),
                    align="center"
                ),
                variant="surface",
                color_scheme="tomato"
            )
        ),
        rx.el.span(
            valor,
            class_name="inline-flex items-center px-2 py-0.5 rounded-md text-xs font-semibold bg-gray-100 text-gray-700 w-fit",
        ),
    )

def estatus_mantenimiento(valor):
    return rx.match(
        valor,
        (
            "PROGRAMADO",
            rx.badge(
                rx.hstack(
                    rx.el.span(
                        class_name="w-1.5 h-1.5 rounded-full bg-blue-500"
                    ),
                    rx.text("PROGRAMADO", weight="bold"),
                    align="center"
                ),
                variant="surface",
                color_scheme="blue"
            )
        ),
        (
            "REALIZADO",
            rx.badge(
                rx.hstack(
                    rx.el.span(
                        class_name="w-1.5 h-1.5 rounded-full bg-emerald-500"
                    ),
                    rx.text("REALIZADO", weight="bold"),
                    align="center"
                ),
                variant="surface",
                color_scheme="green"
            )
        ),
        (
            "EN PROCESO",
            rx.badge(
                rx.hstack(
                    rx.el.span(
                        class_name="w-1.5 h-1.5 rounded-full bg-amber-500"
                    ),
                    rx.text("EN PROCESO", weight="bold"),
                    align="center"
                ),
                variant="surface",
                color_scheme="amber"
            )
        ),
        (
            "CANCELADO",
            rx.badge(
                rx.hstack(
                    rx.el.span(
                        class_name="w-1.5 h-1.5 rounded-full bg-red-500"
                    ),
                    rx.text("CANCELADO", weight="bold"),
                    align="center"
                ),
                variant="surface",
                color_scheme="red"
            )
        ),
        rx.el.span(
            valor,
            class_name="inline-flex items-center px-2 py-0.5 rounded-md text-xs font-semibold bg-gray-100 text-gray-700 w-fit",
        ),
    )

def tipo_mantenimiento_historial(valor):
    rx.match(
        valor,
        (
            "PREVENTIVO",
            rx.box(
                rx.icon(iconos.PREVENTIVO, size=40, color=rx.color("indigo", 9)),
                background=rx.color("indigo", 3),
                border_radius="20px",
                padding="10px"
            ),
        ),
        (
            "CORRECTIVO",
            rx.box(
                rx.icon(iconos.CORRECTIVO, size=40, color=rx.color("tomato", 9)),
                background=rx.color("tomato", 3),
                border_radius="20px",
                padding="10px"
            ),
        ),

    ),

def estatus_proveedor(valor):
    return rx.match(
        valor,
        (
            "ACTIVO",
            rx.badge(
                rx.hstack(
                    rx.el.span(
                        class_name="w-1.5 h-1.5 rounded-full bg-emerald-500"
                    ),
                    rx.text("ACTIVO", weight="bold"),
                    align="center"
                ),
                variant="surface",
                color_scheme="green"
            )
        ),
        (
            "INACTIVO",
            rx.badge(
                rx.hstack(
                    rx.el.span(
                        class_name="w-1.5 h-1.5 rounded-full bg-red-500"
                    ),
                    rx.text("INACTIVO", weight="bold"),
                    align="center"
                ),
                variant="surface",
                color_scheme="red"
            )
        ),
        rx.el.span(
            valor,
            class_name="inline-flex items-center px-2 py-0.5 rounded-md text-xs font-semibold bg-gray-100 text-gray-700 w-fit",
        ),
    )

def es_fecha_valida(fecha_str: str) -> bool:
    """Valida si una fecha (str YYYY-MM-DD) es válida y tiene un año realista de 4 dígitos (1900 a 9999)."""
    if not fecha_str or not isinstance(fecha_str, str):
        return False
    fecha_str = fecha_str.strip()
    try:
        partes = fecha_str.split("-")
        if len(partes) != 3:
            return False
        anio_str = partes[0]
        if len(anio_str) != 4:
            return False
        anio = int(anio_str)
        if anio < 1900 or anio > 9999:
            return False
        datetime.strptime(fecha_str, "%Y-%m-%d")
        return True
    except Exception:
        return False