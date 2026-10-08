import reflex as rx
from ..states.solicitud_state import SolicitudState


def campo_label(texto: str):
    return rx.text(
        texto,
        font_size="0.75rem",
        font_weight="700",
        color="#8f96a3",
        letter_spacing="0.04em",
        margin_bottom="4px",
    )


def subtexto_ayuda(texto: str):
    return rx.text(
        texto,
        font_size="0.75rem",
        color="#6b7280",
        margin_top="4px",
    )


def render_partida_row(item: dict, index: int):
    return rx.hstack(
        rx.input(
            placeholder="Qué se compra",
            value=item["descripcion"],
            on_change=lambda val: SolicitudState.update_partida_descripcion(index, val),
            bg="#181a20",
            border="1px solid #2d3344",
            color="white",
            border_radius="6px",
            size="2",
            flex="3",
        ),
        rx.select(
            ["Pieza", "Kilo", "Litro", "Paquete", "Caja", "Servicio"],
            value=item["unidad"],
            on_change=lambda val: SolicitudState.update_partida_unidad(index, val),
            bg="#181a20",
            border="1px solid #2d3344",
            color="white",
            border_radius="6px",
            size="2",
            flex="1.5",
        ),
        rx.input(
            type="number",
            value=item["cantidad"].to_string(),
            on_change=lambda val: SolicitudState.update_partida_cantidad(index, val),
            bg="#181a20",
            border="1px solid #2d3344",
            color="white",
            border_radius="6px",
            size="2",
            flex="1",
        ),
        rx.input(
            type="number",
            value=item["pu"].to_string(),
            on_change=lambda val: SolicitudState.update_partida_pu(index, val),
            bg="#181a20",
            border="1px solid #2d3344",
            color="white",
            border_radius="6px",
            size="2",
            flex="1",
        ),
        rx.box(
            rx.text(
                "–",
                color="#6b7280",
                font_size="0.875rem",
            ),
            flex="1",
            display="flex",
            align_items="center",
            padding_x="8px",
        ),
        rx.button(
            "×",
            size="1",
            variant="soft",
            color_scheme="gray",
            on_click=lambda: SolicitudState.eliminar_partida(index),
            cursor="pointer",
            padding_x="8px",
        ),
        width="100%",
        spacing="2",
        align="center",
    )


def solicitudes_form():
    return rx.box(
        rx.vstack(
            # Pestanas superiores
            rx.hstack(
                rx.button(
                    "Nueva solicitud",
                    bg=rx.cond(SolicitudState.tab_activa == "nueva", "#1c202b", "transparent"),
                    color=rx.cond(SolicitudState.tab_activa == "nueva", "white", "#9ca3af"),
                    border=rx.cond(SolicitudState.tab_activa == "nueva", "1px solid #3b4254", "1px solid transparent"),
                    border_radius="20px",
                    padding_x="18px",
                    font_weight="bold",
                    size="2",
                    on_click=lambda: SolicitudState.set_tab("nueva"),
                ),
                rx.button(
                    "Mis solicitudes",
                    bg=rx.cond(SolicitudState.tab_activa == "mis_solicitudes", "#1c202b", "transparent"),
                    color=rx.cond(SolicitudState.tab_activa == "mis_solicitudes", "white", "#9ca3af"),
                    border=rx.cond(SolicitudState.tab_activa == "mis_solicitudes", "1px solid #3b4254", "1px solid transparent"),
                    border_radius="20px",
                    padding_x="18px",
                    font_weight="bold",
                    size="2",
                    on_click=lambda: SolicitudState.set_tab("mis_solicitudes"),
                ),
                spacing="2",
                margin_bottom="12px",
            ),

            # Card Principal Formulario
            rx.box(
                rx.vstack(
                    # Header de la card: Titulo y Toggle Tipo de Solicitud
                    rx.hstack(
                        rx.text("Levantar solicitud", font_size="1.25rem", font_weight="bold", color="white"),
                        rx.spacer(),
                        rx.hstack(
                            rx.button(
                                "Orden de compra",
                                bg=rx.cond(SolicitudState.tipo_solicitud == "Orden de compra", "white", "#181a20"),
                                color=rx.cond(SolicitudState.tipo_solicitud == "Orden de compra", "black", "#9ca3af"),
                                font_weight="bold",
                                size="2",
                                padding_x="16px",
                                border_radius="6px 0 0 6px",
                                on_click=lambda: SolicitudState.set_tipo_solicitud("Orden de compra"),
                            ),
                            rx.button(
                                "Fondos",
                                bg=rx.cond(SolicitudState.tipo_solicitud == "Fondos", "white", "#181a20"),
                                color=rx.cond(SolicitudState.tipo_solicitud == "Fondos", "black", "#9ca3af"),
                                font_weight="bold",
                                size="2",
                                padding_x="16px",
                                border_radius="0 6px 6px 0",
                                on_click=lambda: SolicitudState.set_tipo_solicitud("Fondos"),
                            ),
                            spacing="0",
                            border="1px solid #2d3344",
                            border_radius="6px",
                            overflow="hidden",
                        ),
                        width="100%",
                        align="center",
                    ),

                    rx.divider(border_color="#272a36", margin_y="12px"),

                    # Grid de Campos
                    rx.grid(
                        # Fila 1: Unidad de Negocio / Area que solicita
                        rx.vstack(
                            campo_label("UNIDAD DE NEGOCIO *"),
                            rx.select(
                                ["Brecha", "Unidad Norte", "Unidad Sur"],
                                value=SolicitudState.unidad_negocio,
                                on_change=SolicitudState.set_unidad_negocio,
                                bg="#181a20",
                                border="1px solid #2d3344",
                                color="white",
                                border_radius="6px",
                                width="100%",
                                size="2",
                            ),
                            subtexto_ayuda("Se pega en la hoja ZHO."),
                            width="100%",
                            align="start",
                        ),
                        rx.vstack(
                            campo_label("ÁREA QUE SOLICITA *"),
                            rx.select(
                                ["Operación de la unidad", "Administración", "Mantenimiento"],
                                value=SolicitudState.area_solicita,
                                on_change=SolicitudState.set_area_solicita,
                                bg="#181a20",
                                border="1px solid #2d3344",
                                color="white",
                                border_radius="6px",
                                width="100%",
                                size="2",
                            ),
                            width="100%",
                            align="start",
                        ),

                        # Fila 2: Responsable / Departamento
                        rx.vstack(
                            campo_label("RESPONSABLE"),
                            rx.input(
                                placeholder="asistente asistente",
                                value=SolicitudState.responsable,
                                on_change=SolicitudState.set_responsable,
                                bg="#181a20",
                                border="1px solid #2d3344",
                                color="white",
                                border_radius="6px",
                                width="100%",
                                size="2",
                            ),
                            width="100%",
                            align="start",
                        ),
                        rx.vstack(
                            campo_label("DEPARTAMENTO"),
                            rx.input(
                                placeholder="Corporativo, Cocina...",
                                value=SolicitudState.departamento,
                                on_change=SolicitudState.set_departamento,
                                bg="#181a20",
                                border="1px solid #2d3344",
                                color="white",
                                border_radius="6px",
                                width="100%",
                                size="2",
                            ),
                            width="100%",
                            align="start",
                        ),

                        # Fila 3: Unidad Productiva (Ocupa las 2 columnas)
                        rx.box(
                            rx.vstack(
                                campo_label("UNIDAD PRODUCTIVA A LA QUE SE CARGA *"),
                                rx.select(
                                    ["Ope Mixto", "Unidad Productiva A", "Unidad Productiva B"],
                                    value=SolicitudState.unidad_productiva,
                                    on_change=SolicitudState.set_unidad_productiva,
                                    bg="#181a20",
                                    border="1px solid #2d3344",
                                    color="white",
                                    border_radius="6px",
                                    width="100%",
                                    size="2",
                                ),
                                subtexto_ayuda("Gasto de toda la ubicación (renta, luz, vigilancia): se carga a Ope Mixto."),
                                width="100%",
                                align="start",
                            ),
                            grid_column="span 2",
                        ),

                        # Fila 4: Proveedor (Ocupa las 2 columnas)
                        rx.box(
                            rx.vstack(
                                campo_label("PROVEEDOR *"),
                                rx.input(
                                    placeholder="Escribe para buscar en el padrón",
                                    value=SolicitudState.proveedor,
                                    on_change=SolicitudState.set_proveedor,
                                    bg="#181a20",
                                    border="1px solid #2d3344",
                                    color="white",
                                    border_radius="6px",
                                    width="100%",
                                    size="2",
                                ),
                                width="100%",
                                align="start",
                            ),
                            grid_column="span 2",
                        ),

                        # Fila 5: Moneda / Forma de Pago
                        rx.vstack(
                            campo_label("MONEDA *"),
                            rx.select(
                                ["MXN", "USD", "EUR"],
                                value=SolicitudState.moneda,
                                on_change=SolicitudState.set_moneda,
                                bg="#181a20",
                                border="1px solid #2d3344",
                                color="white",
                                border_radius="6px",
                                width="100%",
                                size="2",
                            ),
                            width="100%",
                            align="start",
                        ),
                        rx.vstack(
                            campo_label("FORMA DE PAGO *"),
                            rx.select(
                                ["03-Transferencia", "01-Efectivo", "02-Cheque", "99-Por definir"],
                                value=SolicitudState.forma_pago,
                                on_change=SolicitudState.set_forma_pago,
                                bg="#181a20",
                                border="1px solid #2d3344",
                                color="white",
                                border_radius="6px",
                                width="100%",
                                size="2",
                            ),
                            width="100%",
                            align="start",
                        ),

                        # Fila 6: Tipo de Cambio / Cubeta
                        rx.vstack(
                            campo_label("TIPO DE CAMBIO (DOF)"),
                            rx.input(
                                value=SolicitudState.tipo_cambio,
                                on_change=SolicitudState.set_tipo_cambio,
                                bg="#181a20",
                                border="1px solid #2d3344",
                                color="white",
                                border_radius="6px",
                                width="100%",
                                size="2",
                            ),
                            width="100%",
                            align="start",
                        ),
                        rx.vstack(
                            campo_label("CUBETA *"),
                            rx.hstack(
                                rx.button(
                                    "GG",
                                    bg=rx.cond(SolicitudState.cubeta == "GG", "white", "#181a20"),
                                    color=rx.cond(SolicitudState.cubeta == "GG", "black", "#9ca3af"),
                                    font_weight="bold",
                                    size="2",
                                    flex="1",
                                    border_radius="6px 0 0 6px",
                                    on_click=lambda: SolicitudState.set_cubeta("GG"),
                                ),
                                rx.button(
                                    "MP",
                                    bg=rx.cond(SolicitudState.cubeta == "MP", "white", "#181a20"),
                                    color=rx.cond(SolicitudState.cubeta == "MP", "black", "#9ca3af"),
                                    font_weight="bold",
                                    size="2",
                                    flex="1",
                                    border_radius="0",
                                    on_click=lambda: SolicitudState.set_cubeta("MP"),
                                ),
                                rx.button(
                                    "MO",
                                    bg=rx.cond(SolicitudState.cubeta == "MO", "white", "#181a20"),
                                    color=rx.cond(SolicitudState.cubeta == "MO", "black", "#9ca3af"),
                                    font_weight="bold",
                                    size="2",
                                    flex="1",
                                    border_radius="0 6px 6px 0",
                                    on_click=lambda: SolicitudState.set_cubeta("MO"),
                                ),
                                spacing="0",
                                border="1px solid #2d3344",
                                border_radius="6px",
                                overflow="hidden",
                                width="100%",
                            ),
                            subtexto_ayuda("Define a qué libro se pega"),
                            width="100%",
                            align="start",
                        ),

                        # Fila 7: Centro de Costos / Categoria
                        rx.vstack(
                            campo_label("CENTRO DE COSTOS *"),
                            rx.select(
                                ["OPE. Mixto", "Holding", "Administrativo"],
                                value=SolicitudState.centro_costos,
                                on_change=SolicitudState.set_centro_costos,
                                bg="#181a20",
                                border="1px solid #2d3344",
                                color="white",
                                border_radius="6px",
                                width="100%",
                                size="2",
                            ),
                            subtexto_ayuda("Inversión es cargo al Holding: no entra a GG/MO/MP"),
                            width="100%",
                            align="start",
                        ),
                        rx.vstack(
                            campo_label("CATEGORÍA *"),
                            rx.select(
                                ["Artículos de limpieza", "Papelería", "Mantenimiento", "Alimentos", "Bebidas"],
                                value=SolicitudState.categoria,
                                on_change=SolicitudState.set_categoria,
                                bg="#181a20",
                                border="1px solid #2d3344",
                                color="white",
                                border_radius="6px",
                                width="100%",
                                size="2",
                            ),
                            width="100%",
                            align="start",
                        ),

                        # Fila 8: Prioridad / Tipo de Compra
                        rx.vstack(
                            campo_label("PRIORIDAD *"),
                            rx.select(
                                ["Media (pago en las próximas 2 semanas)", "Alta (Urgente)", "Baja"],
                                value=SolicitudState.prioridad,
                                on_change=SolicitudState.set_prioridad,
                                bg="#181a20",
                                border="1px solid #2d3344",
                                color="white",
                                border_radius="6px",
                                width="100%",
                                size="2",
                            ),
                            width="100%",
                            align="start",
                        ),
                        rx.vstack(
                            campo_label("TIPO DE COMPRA *"),
                            rx.select(
                                ["Gasto General", "Inversión", "Caja Chica"],
                                value=SolicitudState.tipo_compra,
                                on_change=SolicitudState.set_tipo_compra,
                                bg="#181a20",
                                border="1px solid #2d3344",
                                color="white",
                                border_radius="6px",
                                width="100%",
                                size="2",
                            ),
                            width="100%",
                            align="start",
                        ),

                        # Fila 9: IVA / Fecha del documento
                        rx.vstack(
                            campo_label("IVA *"),
                            rx.select(
                                ["8% franja fronteriza", "16% General", "0% Exento", "Retención IVA"],
                                value=SolicitudState.iva,
                                on_change=SolicitudState.set_iva,
                                bg="#181a20",
                                border="1px solid #2d3344",
                                color="white",
                                border_radius="6px",
                                width="100%",
                                size="2",
                            ),
                            width="100%",
                            align="start",
                        ),
                        rx.vstack(
                            campo_label("FECHA DEL DOCUMENTO *"),
                            rx.input(
                                type="date",
                                value=SolicitudState.fecha_documento,
                                on_change=SolicitudState.set_fecha_documento,
                                bg="#181a20",
                                border="1px solid #2d3344",
                                color="white",
                                border_radius="6px",
                                width="100%",
                                size="2",
                            ),
                            width="100%",
                            align="start",
                        ),

                        # Fila 10: Fecha de pago prevista
                        rx.vstack(
                            campo_label("FECHA DE PAGO PREVISTA *"),
                            rx.input(
                                type="date",
                                value=SolicitudState.fecha_pago_prevista,
                                on_change=SolicitudState.set_fecha_pago_prevista,
                                bg="#181a20",
                                border="1px solid #2d3344",
                                color="white",
                                border_radius="6px",
                                width="100%",
                                size="2",
                            ),
                            width="100%",
                            align="start",
                        ),
                        rx.box(width="100%"),  # Espaciador en la columna derecha de la fila 10

                        columns="2",
                        spacing="4",
                        width="100%",
                    ),

                    rx.divider(border_color="#272a36", margin_y="16px"),

                    # Sección PARTIDAS
                    rx.vstack(
                        campo_label("PARTIDAS"),
                        # Encabezados de la tabla de partidas
                        rx.hstack(
                            rx.text("DESCRIPCIÓN", font_size="0.7rem", font_weight="bold", color="#71717a", flex="3"),
                            rx.text("UNIDAD", font_size="0.7rem", font_weight="bold", color="#71717a", flex="1.5"),
                            rx.text("CANTIDAD", font_size="0.7rem", font_weight="bold", color="#71717a", flex="1"),
                            rx.text("P.U.", font_size="0.7rem", font_weight="bold", color="#71717a", flex="1"),
                            rx.text("IMPORTE", font_size="0.7rem", font_weight="bold", color="#71717a", flex="1"),
                            rx.box(width="28px"),  # Espacio para el boton de eliminar
                            width="100%",
                            spacing="2",
                            padding_x="4px",
                        ),
                        # Filas dinámicas de partidas
                        rx.foreach(
                            SolicitudState.partidas,
                            render_partida_row,
                        ),
                        # Boton Agregar Partida
                        rx.hstack(
                            rx.button(
                                "Agregar partida",
                                bg="#1c202b",
                                border="1px solid #3b4254",
                                color="white",
                                font_weight="bold",
                                size="2",
                                border_radius="6px",
                                on_click=SolicitudState.agregar_partida,
                            ),
                            rx.text("Máximo 10", font_size="0.75rem", color="#6b7280"),
                            spacing="3",
                            align="center",
                            margin_top="8px",
                        ),
                        width="100%",
                        spacing="3",
                        align="start",
                    ),

                    rx.divider(border_color="#272a36", margin_y="16px"),

                    # Sección JUSTIFICACIÓN / OBSERVACIONES
                    rx.vstack(
                        campo_label("JUSTIFICACIÓN / OBSERVACIONES *"),
                        rx.text_area(
                            placeholder="Para qué se necesita y qué pasa si no se compra",
                            value=SolicitudState.justificacion,
                            on_change=SolicitudState.set_justificacion,
                            bg="#181a20",
                            border="1px solid #2d3344",
                            color="white",
                            border_radius="6px",
                            width="100%",
                            rows="3",
                        ),
                        width="100%",
                        align="start",
                    ),

                    margin_top="8px",
                    spacing="4",
                    width="100%",
                ),
                bg="#12141a",
                border="1px solid #232733",
                border_radius="10px",
                padding="24px",
                width="100%",
            ),

            # Botones de Acciones Finales (Enviar a revisión / Vista previa)
            rx.hstack(
                rx.button(
                    "Enviar a revisión",
                    bg="white",
                    color="black",
                    font_weight="bold",
                    border_radius="6px",
                    padding_x="20px",
                    size="3",
                    on_click=SolicitudState.enviar_a_revision,
                ),
                rx.button(
                    "Vista previa",
                    bg="#181a20",
                    border="1px solid #2d3344",
                    color="white",
                    font_weight="bold",
                    border_radius="6px",
                    padding_x="20px",
                    size="3",
                    on_click=SolicitudState.vista_previa,
                ),
                spacing="3",
                margin_top="16px",
            ),

            width="100%",
            align="start",
            spacing="3",
        ),
        width="100%",
        padding="16px",
    )

