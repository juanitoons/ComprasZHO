import reflex as rx

"""Manejo de estado del panel de control, enfocado en el sidebar"""
class PanelState(rx.State):
    # El estado inicial de la pestaña activa
    active_tab: str = "resumen"

    # CORREGIDO: Eliminamos @rx.event. 
    # Al ser un método normal dentro de rx.State, Reflex ya sabe qué hacer.
    def set_tab(self, tab: str):
        self.active_tab = tab
