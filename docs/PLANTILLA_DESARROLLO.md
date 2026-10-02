# Plantilla y Guía de Desarrollo — Portal de Solicitudes y Órdenes de Compra (Grupo Zibarita)

> **Basado en:** `docs/especificacion.md` (v2 · 13-sep-2026)  
> **Stack:** Supabase (Postgres + Auth + RLS + Storage) + Python (Reflex / FastAPI)  
> **Zona Horaria:** `America/Tijuana` (UTC en DB)

---

## 📋 Resumen del Proyecto y Roles

El portal automatiza y sustituye los machotes de Word y Excel para las solicitudes y órdenes de compra del **Grupo Zibarita** (Punto Zibarita, Saketori, Mantequilla, etc.).

### Matriz de Roles y Permisos

| Rol | Solicitudes | Autorizaciones | Copy Paste | Administrador |
| :--- | :--- | :--- | :--- | :--- |
| **`solicitante`** | Crea y consulta las suyas | — | — | — |
| **`revisor`** *(Maritza / Admin)* | Ve todas | Revisa y rechaza | — | — |
| **`director`** *(Pedro / Dir. Gral)* | Ve todas | Autoriza y rechaza | Ve | Sí |
| **`compras`** | Ve las autorizadas | Marca comprada | — | — |
| **`contable`** | Ve las autorizadas | — | Exporta y marca pegado | — |
| **`admin`** | Gestión total | Gestión total | Gestión total | Alta usuarios, catálogos, topes |

> **Regla de Oro:** Ningún usuario puede firmar dos pasos de la misma solicitud. Si el revisor es el solicitante, salta directo a Dirección (validado en backend/DB).

---

## 🔄 Máquina de Estados de la Solicitud

- `borrador` ➔ `enviada` ➔ `revisada` ➔ `autorizada` ➔ `comprada` ➔ `pegada`
- Estados alternos: `rechazada` (con motivo obligatorio $\ge$ 10 chars) o `cancelada` (solo el solicitante antes de `revisada`).
- Salto automático `revisada` ➔ `autorizada` cuando `total <= tope_autorizacion` ($5,000 MXN).

---

## 🗄️ 1. Esquema de Base de Datos (Supabase / Postgres SQL)

Guarda este script e ejecútalo en el **SQL Editor** de Supabase para estructurar toda la base de datos:

```sql
-- ========================================================
-- 1. TABLAS DE USUARIOS Y ROLES
-- ========================================================

create table public.perfiles (
  id            uuid primary key references auth.users(id) on delete cascade,
  nombre        text not null,
  puesto        text,
  activo        boolean not null default true,
  creado        timestamptz not null default now()
);

create type public.rol_t as enum ('solicitante','revisor','director','compras','contable','admin');

create table public.usuario_roles (
  usuario uuid references public.perfiles(id) on delete cascade,
  rol     public.rol_t not null,
  primary key (usuario, rol)
);

-- ========================================================
-- 2. CATÁLOGOS BASE
-- ========================================================

create table public.proveedores (
  id           serial primary key,
  nombre       text unique not null,
  razon_social text,
  rfc          text,
  dias_credito int not null default 0,
  activo       boolean not null default true
);

create table public.unidades_negocio (
  clave    text primary key, -- Hipodromo, Cacho, Peninsula, Brecha, Xochicalco, Cedis, Corporativo, Comercial
  nombre   text not null,
  sociedad text not null check (sociedad in ('ZHO','PZ2'))
);

create table public.unidades_productivas (
  id             serial primary key,
  unidad_negocio text references public.unidades_negocio(clave),
  nombre         text not null,
  centro_costo_inv text,
  activo         boolean default true
);

create table public.centros_costo (
  clave text primary key
);

create table public.categorias (
  id      serial primary key,
  cubeta  text check (cubeta in ('GG','MO','MP')),
  nombre  text not null
);

-- ========================================================
-- 3. SOLICITUDES Y PARTIDAS
-- ========================================================

create type public.estado_t as enum ('borrador','enviada','revisada','autorizada','comprada','pegada','rechazada','cancelada');
create type public.tipo_t   as enum ('orden_compra','fondos');

create table public.solicitudes (
  id                uuid primary key default gen_random_uuid(),
  folio             text unique not null,          -- Formato: 260911-OC-STARTUPLEGAL-01
  tipo              public.tipo_t not null default 'orden_compra',
  estado            public.estado_t not null default 'borrador',
  solicitante       uuid not null references public.perfiles(id),
  area              text not null,                 -- MKT, Mantenimiento, RND, Proyectos, RH, Compras, etc.
  unidad_negocio    text not null references public.unidades_negocio(clave),
  unidad_productiva text not null,               -- 'Ope Mixto' por defecto
  sociedad          text not null check (sociedad in ('ZHO','PZ2')),
  cubeta            text not null check (cubeta in ('GG','MO','MP')),
  centro_costo      text not null references public.centros_costo(clave),
  categoria         text not null,
  proveedor_id      int references public.proveedores(id),
  proveedor_texto   text,                          -- Para proveedores nuevos temporales
  tipo_compra       text,
  prioridad         text default 'normal',
  moneda            text not null default 'MXN' check (moneda in ('MXN','USD')),
  tipo_cambio       numeric(10,4),
  subtotal          numeric(14,2) not null default 0,
  tasa_iva          numeric(4,2)  not null default 8.00, -- 8.00%, 16.00%, 0.00%
  iva               numeric(14,2) not null default 0,
  total             numeric(14,2) not null default 0,
  total_mxn         numeric(14,2) not null default 0,
  fecha_documento   date not null,
  fecha_pago        date not null,
  dias_credito      int not null default 0,
  fecha_limite      date generated always as (fecha_documento + dias_credito) stored,
  forma_pago        text not null,                 -- 01-Efectivo, 02-Cheque, 03-Transferencia, 04-Interno
  justificacion     text not null,
  uuid_cfdi         text,                          -- Folio fiscal Factura SAT
  creado            timestamptz not null default now()
);

create table public.partidas (
  id              bigserial primary key,
  solicitud       uuid not null references public.solicitudes(id) on delete cascade,
  orden           int not null,
  descripcion     text not null,
  unidad          text not null,
  cantidad        numeric(12,3) not null check (cantidad > 0),
  precio_unitario numeric(14,2) not null check (precio_unitario >= 0),
  importe         numeric(14,2) generated always as (cantidad * precio_unitario) stored
);

-- ========================================================
-- 4. BITÁCORA DE EVENTOS (SUSTITUTO DE FIRMAS)
-- ========================================================

create table public.eventos (
  id              bigserial primary key,
  solicitud       uuid not null references public.solicitudes(id) on delete cascade,
  accion          text not null, -- enviar | revisar | autorizar | comprar | pegar | rechazar | despegar
  estado_anterior public.estado_t,
  estado_nuevo    public.estado_t,
  actor           uuid references public.perfiles(id),
  automatico      boolean not null default false,
  motivo          text,
  ip              inet,
  cuando          timestamptz not null default now()
);

-- ========================================================
-- 5. HISTÓRICO DE EXPORTACIONES (COPY/PASTE ADMIN)
-- ========================================================

create table public.exportaciones (
  id       bigserial primary key,
  libro    text not null,      -- Ej: 'ZHO (GG)'
  filas    int not null,
  actor    uuid references public.perfiles(id),
  cuando   timestamptz not null default now(),
  deshecha boolean not null default false
);

create table public.exportacion_solicitudes (
  exportacion bigint references public.exportaciones(id) on delete cascade,
  solicitud   uuid references public.solicitudes(id),
  primary key (exportacion, solicitud)
);

create table public.config (
  clave text primary key,
  valor jsonb not null
);

-- Configuración inicial por defecto
insert into public.config (clave, valor) values
  ('tope_autorizacion', '5000'::jsonb),
  ('iva_default', '8'::jsonb);

-- ========================================================
-- 6. POLÍTICAS DE SEGURIDAD (RLS)
-- ========================================================

alter table public.solicitudes enable row level security;
alter table public.partidas enable row level security;

create or replace function public.tiene_rol(r public.rol_t) returns boolean language sql stable as $$
  select exists (
    select 1 from public.usuario_roles ur
    where ur.usuario = auth.uid() and ur.rol = r
  )
$$;

create policy leer_solicitudes on public.solicitudes for select using (
  solicitante = auth.uid() 
  or public.tiene_rol('revisor') 
  or public.tiene_rol('director')
  or public.tiene_rol('compras') 
  or public.tiene_rol('contable') 
  or public.tiene_rol('admin')
);

create policy crear_solicitudes on public.solicitudes for insert with check (
  solicitante = auth.uid() and estado in ('borrador','enviada')
);

create policy editar_borrador on public.solicitudes for update using (
  solicitante = auth.uid() and estado = 'borrador'
);
```

---

## 📊 2. Módulo Copy/Paste — Estructura de las 10 Columnas Exactas (B a K)

El módulo contable exporta **únicamente 10 columnas** que se pegan a partir de la celda **B** en los libros `Control GG`, `MO` y `MP`.

| Columna | Nombre en el Control | Origen del Dato | Formato / Ejemplo |
| :---: | :--- | :--- | :--- |
| **B** | Fecha Factura / Remisión | `fecha_documento` | `dd/mm/aaaa` (Ej: `13/09/2026`) |
| **C** | Factura | Folio + 1ra Partida | Ej: `260911-OC-STARTUPLEGAL-01 (Honorarios)` |
| **D** | Proveedor | Nombre en Padrón | Exacto carácter por carácter (para VLOOKUP) |
| **E** | Moneda | `moneda` | `Pesos` o `Dolares` |
| **F** | Importe | `total` con IVA | `NUMERIC(14,2)` sin comas de miles |
| **G** | Tipo de Pago | `forma_pago` | `01-Efectivo`, `02-Cheque`, `03-Transferencia`, `04-Interno` |
| **H** | Fecha de Pago | `fecha_pago` | `dd/mm/aaaa` |
| **I** | Categoría | `categoria` | Del catálogo de la cubeta (GG/MO/MP) |
| **J** | Punto Zibarita | `unidad_negocio` | Ej: `Hipodromo`, `Cacho`, `Peninsula` |
| **K** | Centro de Costo | `centro_costo` | `OPE. Mixto`, `Inversion`, etc. |

---

## ✅ 3. Checklist de Desarrollo por Fases

- [ ] **Fase 1: Base** (Auth Google OAuth, perfiles, roles, RLS, Hub con tarjetas y contadores)
- [ ] **Fase 2: Orden de Compra** (Captura, partidas, folios, IVA 8%/16%, cadena de firmas, bitácora)
- [ ] **Fase 3: Copy Paste** (Export TSV/XLSX B-K, marcar pegado, histórico, deshacer 24h)
- [ ] **Fase 4: Fondos y Adjuntos** (Formatos de fondos, Supabase Storage)
- [ ] **Fase 5: Cierre Fiscal** (UUID CFDI, conciliación)
