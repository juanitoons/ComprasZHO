from pydantic import BaseModel
from datetime import datetime

class ActivoModelo(BaseModel):
    id: str
    folio: str
    nombre: str
    descripcion: str
    sucursal: str
    area: str
    categoria: str
    tipo_equipo: str
    marca: str
    modelo: str
    numero_serie: str
    link_ficha_tecnica: str
    estatus: str
    fecha_registro: datetime

class MantenimientoModelo(BaseModel):
    id: str
    folio: str
    activo: str
    sucursal: str
    tipo: str
    estatus: str
    operacion_problema: str
    proveedor: str
    fecha_registro: str
    link_evidencia: str
    costo_cotizado: str
    comentarios: str

class PreventivoModelo(BaseModel):
    id: str
    folio: str
    activo: str
    sucursal: str
    tipo: str
    estatus: str
    operacion: str
    proveedor: str
    fecha_registro: str

class CorrectivoModelo(BaseModel):
    id: str
    folio: str
    activo: str
    sucursal: str
    tipo: str
    estatus: str
    problema: str
    proveedor: str
    fecha_registro: str
    link_evidencia: str
    costo_cotizado: str
    comentarios: str

class MantenimientosRecientesModelo(BaseModel):
    id: str
    folio: str
    activo: str
    sucursal: str
    tipo: str
    estatus: str
    fecha_registro: str

class ProveedorModelo(BaseModel):
    id: str
    nombre: str
    estatus: str
    fecha_registro: str

class EventoCalendario(BaseModel):
    id: str = ""
    folio: str = ""
    activo: str = ""
    sucursal: str = ""
    tipo: str = ""
    estatus: str = ""
    operacion: str = ""
    proveedor: str = ""
    fecha: str = ""

class DiaCalendario(BaseModel):
    dia: int = 0
    fecha_str: str = ""
    es_mes_actual: bool = True
    es_hoy: bool = False
    eventos: list[EventoCalendario] = []
    tiene_eventos: bool = False
    cantidad_eventos: int = 0