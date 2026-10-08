import reflex as rx


class SolicitudState(rx.State):
    tab_activa: str = "nueva"  # "nueva" | "mis_solicitudes"
    tipo_solicitud: str = "Orden de compra"  # "Orden de compra" | "Fondos"

    # Form fields
    unidad_negocio: str = "Brecha"
    area_solicita: str = "Operación de la unidad"
    responsable: str = "asistente asistente"
    departamento: str = ""
    unidad_productiva: str = "Ope Mixto"
    proveedor: str = ""
    moneda: str = "MXN"
    forma_pago: str = "03-Transferencia"
    tipo_cambio: str = "17.4000"
    cubeta: str = "GG"
    centro_costos: str = "OPE. Mixto"
    categoria: str = "Artículos de limpieza"
    prioridad: str = "Media (pago en las próximas 2 semanas)"
    tipo_compra: str = "Gasto General"
    iva: str = "8% franja fronteriza"
    fecha_documento: str = "2026-10-07"
    fecha_pago_prevista: str = "2026-10-07"
    justificacion: str = ""

    # Partidas dynamic table
    partidas: list[dict] = [
        {"descripcion": "", "unidad": "Pieza", "cantidad": 0, "pu": 0.0},
        {"descripcion": "", "unidad": "Pieza", "cantidad": 0, "pu": 0.0},
        {"descripcion": "", "unidad": "Pieza", "cantidad": 0, "pu": 0.0},
    ]

    def set_tab(self, tab: str):
        self.tab_activa = tab

    def set_tipo_solicitud(self, tipo: str):
        self.tipo_solicitud = tipo

    def set_cubeta(self, cubeta: str):
        self.cubeta = cubeta

    def set_unidad_negocio(self, val: str):
        self.unidad_negocio = val

    def set_area_solicita(self, val: str):
        self.area_solicita = val

    def set_responsable(self, val: str):
        self.responsable = val

    def set_departamento(self, val: str):
        self.departamento = val

    def set_unidad_productiva(self, val: str):
        self.unidad_productiva = val

    def set_proveedor(self, val: str):
        self.proveedor = val

    def set_moneda(self, val: str):
        self.moneda = val

    def set_forma_pago(self, val: str):
        self.forma_pago = val

    def set_tipo_cambio(self, val: str):
        self.tipo_cambio = val

    def set_centro_costos(self, val: str):
        self.centro_costos = val

    def set_categoria(self, val: str):
        self.categoria = val

    def set_prioridad(self, val: str):
        self.prioridad = val

    def set_tipo_compra(self, val: str):
        self.tipo_compra = val

    def set_iva(self, val: str):
        self.iva = val

    def set_fecha_documento(self, val: str):
        self.fecha_documento = val

    def set_fecha_pago_prevista(self, val: str):
        self.fecha_pago_prevista = val

    def set_justificacion(self, val: str):
        self.justificacion = val

    def agregar_partida(self):
        if len(self.partidas) < 10:
            self.partidas.append({"descripcion": "", "unidad": "Pieza", "cantidad": 0, "pu": 0.0})

    def eliminar_partida(self, index: int):
        if len(self.partidas) > 1:
            self.partidas.pop(index)

    def update_partida_descripcion(self, index: int, val: str):
        if 0 <= index < len(self.partidas):
            self.partidas[index]["descripcion"] = val

    def update_partida_unidad(self, index: int, val: str):
        if 0 <= index < len(self.partidas):
            self.partidas[index]["unidad"] = val

    def update_partida_cantidad(self, index: int, val: str):
        if 0 <= index < len(self.partidas):
            try:
                self.partidas[index]["cantidad"] = float(val) if val != "" else 0
            except ValueError:
                pass

    def update_partida_pu(self, index: int, val: str):
        if 0 <= index < len(self.partidas):
            try:
                self.partidas[index]["pu"] = float(val) if val != "" else 0.0
            except ValueError:
                pass

    def enviar_a_revision(self):
        return rx.window_alert("Solicitud enviada a revisión correctamente.")

    def vista_previa(self):
        return rx.window_alert("Abriendo vista previa de la solicitud...")

