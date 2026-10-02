# Portal de Solicitudes y Órdenes de Compra — Grupo Zibarita

**Especificación técnica para el programador · v2 · 13-sep-2026**

Dueño: Pedro Velarde, Dirección General · Stack: Supabase (Postgres + Auth + RLS + Storage) y Python (FastAPI) · Zona horaria America/Tijuana

---

Instrucciones para el programador: qué construir, con qué reglas y en qué orden. Stack: Supabase (Postgres + Auth + RLS + Storage) y Python (FastAPI). Sustituye el machote de Word y el pre-sistema en página que ya opera.

## 01. Veredicto sobre la estructura propuesta

La estructura de portada + cuatro módulos **sí hace sentido** y es la correcta para este tamaño de operación. Cuatro cambios antes de programar:

### Sí: cuatro módulos, uno por trabajo real

Solicitar, autorizar, pasar a Excel y administrar son cuatro trabajos distintos que hacen cuatro personas distintas. Separarlos evita la pantalla-todo donde nadie encuentra su tarea.

### Ajuste 1 — Los cuatro links no son páginas, son permisos

Si el portal muestra las cuatro tarjetas a todos, tres de cada cuatro clics terminan en "no tienes acceso". El hub debe pintar **solo los módulos del rol**, y cada tarjeta trae su contador: “7 por autorizar”, “12 listas para pegar”. Un portal sin números en la portada obliga a entrar a ver si hay algo, y la gente deja de entrar.

### Ajuste 2 — Falta el módulo de consulta

El que pide quiere saber “¿ya me lo autorizaron?” sin hablarle a nadie. Si no existe esa vista, el WhatsApp a Administración sigue igual y el portal no ahorra trabajo. Va dentro de Solicitudes como **Mis solicitudes**, con el estado y quién la tiene detenida.

### Ajuste 3 — “Pegado” es un estado, no un botón

Marcar pegado tiene que guardar quién y cuándo, sacar la fila de la vista activa y dejarla en histórico. Y necesita **deshacer dentro de 24 h**: alguien va a picarle antes de pegar, es cuestión de tiempo. Sin deshacer, esa orden se pierde de la vista y se paga dos veces o no se paga.

### Ajuste 4 — Nada de contraseñas: **Entrar con Google**

**Decidido el 13-sep-2026.** El correo de la empresa es Google Workspace, así que el acceso es Google OAuth restringido al dominio `zibarisholding.com`. Nadie inventa contraseñas, nadie las olvida, nadie las resetea, y quien sale de la empresa pierde el acceso al portal en el momento en que se le desactiva el correo — sin que nadie tenga que acordarse de darlo de baja aquí.

En Supabase: Authentication → Providers → Google, con el *hosted domain* del dominio de la empresa; y una validación en el servidor que rechace cualquier correo fuera de él. Contraseña propia solo como excepción, para un proveedor externo o alguien sin correo de la casa.

## 02. Decisiones ya cerradas

Salieron de operar el prototipo. No se vuelven a discutir: se programan así.

| Tema                     | Decisión                                                                                                                                                        |
|--------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Acceso                   | Entrar con Google, dominio `zibarisholding.com`. Sin contraseñas propias.                                                                                       |
| Folio de orden de compra | `AAMMDD-OC-PROVEEDOR-##` — ejemplo `260911-OC-STARTUPLEGAL-01`. Consecutivo por día y proveedor.                                                                |
| Centro de costo          | Solo tres: **OPE. Mixto**, **Materia Prima** e **Inversión**. Los 21 `INV. <proyecto>` del catálogo viejo se retiran: no se usó ninguno en los últimos 6 meses. |
| Inversión                | Es cargo al Holding y **no entra** a Control GG, MO ni MP: sale en un destino propio, `Holding (Inversión)`.                                                    |
| Unidad productiva        | Campo obligatorio, distinto del centro de costo. Catálogo por ubicación en la sección 07.                                                                       |
| Área solicitante         | Campo aparte de la unidad productiva: MKT, Mantenimiento, RND, Proyectos e Inversión, RH, Compras, Gerencia de Costos, AyF, Dirección, Operación.               |
| Gasto que cruza unidades | No se prorratea. Va a la unidad de negocio **Comercial**. El presupuesto por porcentaje fijo se controla aparte.                                                |
| IVA                      | 8% por defecto (franja fronteriza), cambiable a 16% o exento **por documento**.                                                                                 |
| Pegado al control        | Diez columnas, B a K. Marcar pegado manda a histórico, con deshacer de 24 h.                                                                                    |

**Sigue abierto:** el monto tope sin firma de Dirección, y qué hacer cuando una orden autorizada cambia de monto al llegar la factura.

## 15. Estado: ya existe un prototipo funcionando

Antes de programar, revísalo: ahí están las reglas ya peleadas contra la operación real, y los catálogos cargados de los libros Control GG, MO y MP (356 proveedores con días de crédito, categorías por cubeta, unidades productivas por ubicación).

- Portada con identificación, menú de cuatro módulos y contadores por rol.
- Orden de compra con partidas, IVA, folio automático y la hoja formateada igual que el machote de Word, con las cuatro firmas.
- Cadena Revisó → Autorizó → Compras, con tope de autorización configurable.
- Bloque de 10 columnas con copiar, CSV y marcar pegado con histórico.

Es un pre-sistema y vive dentro de la cuenta de Claude de Dirección: no se comparte con el equipo. El sistema en Supabase lo sustituye, no lo complementa.

## 14. Roles y matriz de permisos

Cinco roles. Un usuario puede tener varios (Roberto es solicitante y compras). El rol vive en base de datos, nunca en el front.

<table>
<colgroup>
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 20%" />
</colgroup>
<thead>
<tr class="header">
<th>Rol</th>
<th>Solicitudes</th>
<th>Autorizaciones</th>
<th>Copy Paste</th>
<th>Administrador</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><strong>solicitante</strong><br />
<span class="mini">gerentes, chefs, jefes de área</span></td>
<td>Crea y consulta las suyas</td>
<td>—</td>
<td>—</td>
<td>—</td>
</tr>
<tr class="even">
<td><strong>revisor</strong><br />
<span class="mini">Administración (Maritza)</span></td>
<td>Ve todas</td>
<td>Revisa y rechaza</td>
<td>—</td>
<td>—</td>
</tr>
<tr class="odd">
<td><strong>director</strong><br />
<span class="mini">Dirección General (Pedro)</span></td>
<td>Ve todas</td>
<td>Autoriza y rechaza</td>
<td>Ve</td>
<td>Sí</td>
</tr>
<tr class="even">
<td><strong>compras</strong></td>
<td>Ve las autorizadas</td>
<td>Marca comprada</td>
<td>—</td>
<td>—</td>
</tr>
<tr class="odd">
<td><strong>contable</strong><br />
<span class="mini">quien pega en el control</span></td>
<td>Ve las autorizadas</td>
<td>—</td>
<td>Exporta y marca pegado</td>
<td>—</td>
</tr>
<tr class="even">
<td><strong>admin</strong></td>
<td colspan="4">Alta y baja de usuarios, roles, catálogos, tope de autorización. No firma por nadie.</td>
</tr>
</tbody>
</table>

**Regla dura:** nadie firma dos pasos de la misma solicitud. Si el revisor es también el solicitante, la solicitud salta directo a Dirección. Eso se valida en el servidor, no en la pantalla.

## 03. Máquina de estados

borrador**→**enviada**→**revisada**→**autorizada**→**comprada**→**pegada

Desde cualquier estado antes de `pegada` se puede ir a `rechazada` (con motivo obligatorio) o `cancelada` (solo el solicitante, solo antes de revisada). El salto `revisada → autorizada` es automático cuando el total es menor o igual al **tope de autorización** configurado; queda registrado como “autorizado por regla de tope”, nunca a nombre de una persona.

Cada transición escribe un renglón en `eventos`: quién, qué, cuándo, desde qué IP. Esa tabla es la que sustituye las cuatro firmas del papel, y es la que se enseña cuando alguien pregunta quién autorizó.

## 04. Pantallas

### Portada — acceso

- Correo y contraseña. Logo de Grupo Zibarita, fondo limpio, nada más. Sin registro público: **al portal solo se entra por invitación** del administrador.
- “Olvidé mi contraseña” manda el correo de recuperación de Supabase. Sesión de 12 horas; al vencer, vuelve a la portada sin perder lo capturado.
- Un solo mensaje de error para correo malo y contraseña mala: *“Correo o contraseña incorrectos.”* No se le dice a nadie qué correos existen.
- Bloqueo temporal a los 5 intentos fallidos (Supabase lo trae).

### Hub — “¿qué necesitas hacer?”

- Saludo con el nombre, y de una a cuatro tarjetas según el rol, cada una con su contador en vivo.
- Debajo, **“Tus pendientes”**: las tres cosas que esa persona tiene detenidas hoy. Un portal que no dice qué falta, no se usa.

### 1 · Solicitudes

Dos formatos en un mismo módulo, porque el 80% del uso es el primero:

- **Orden de compra** — el machote completo: encabezado, partidas, IVA, justificación.
- **Solicitud de fondos** — nómina, reembolso, caja chica, servicios, fondo de capital.
- **Mis solicitudes** — estado, quién la tiene, y botón de recordatorio.

Adjuntos obligatorios por tipo: cotización en orden de compra, ticket en reembolso.

### 2 · Autorizaciones

Bandeja de lo que **a esa persona** le toca firmar, no de todo. Cada renglón abre la hoja completa como el machote. Botones: firmar, rechazar con motivo, o pedir aclaración (regresa al solicitante sin matar la orden). Autorización en lote solo para montos bajo el tope.

### 3 · Copy Paste Admin

Filtro por libro destino: ZHO/PZ2 × GG/MO/MP. Tabla con las 10 columnas exactas (B a K), botón de copiar, descarga XLSX, y **“Marcar como pegadas”** que las manda a histórico. Pestaña de histórico con el deshacer de 24 h y el filtro por fecha de pegado.

### 4 · Administrador

Invitar usuario por correo, asignar roles, desactivar (nunca borrar). Catálogos editables: proveedores con días de crédito y RFC, unidades productivas, centros de costo, categorías. Tope de autorización. Bitácora de quién cambió qué.

## 05. Reglas de la frontera y del país

Esto es lo que distingue un portal hecho para Tijuana de una plantilla genérica. Todas son obligatorias.

- **IVA 8% / 16%.** Tijuana está en la franja fronteriza norte: la tasa por defecto es **8%**, pero se elige por documento porque hay proveedores fuera de la franja al 16%, y hay conceptos exentos. La tasa se guarda en el renglón, no se calcula al vuelo después.
- **Dos monedas.** Compras en dólares son normales aquí. Se guarda `moneda`, `importe`, `tipo_cambio` y `importe_mxn` calculado. Nunca se guarda un dólar convertido a peso sin el tipo de cambio que se usó. El tipo de cambio es el **DOF de la fecha de pago**.
- **Razón social y RFC** del proveedor, separados del nombre comercial. En el padrón viven los tres.
- **Amarre fiscal.** Campo `uuid_cfdi` en la solicitud, se llena cuando llega la factura. Es lo que cierra el círculo entre lo que se autorizó y lo que Hacienda ve. Hoy no existe y es el hueco más caro del proceso.
- **Fechas.** Todo se guarda en UTC (`timestamptz`) y se muestra en `America/Tijuana`. La frontera cambia horario en fechas distintas al resto de México: no se calcula la zona a mano, se usa la base de datos.
- **Días de crédito y fecha límite.** Salen del padrón de proveedores, igual que el `VLOOKUP` del control actual.
- **Dinero en `NUMERIC(14,2)`**, jamás en flotante. Los centavos que se pierden en un `float` descuadran el control a fin de mes.
- **Todo en español**, con las palabras de la casa: Punto Zibarita, unidad productiva, Ope Mixto, cubeta, centro de costo. Nada de “submit”, “request” ni “approve”.

## 06. Modelo de datos

Postgres en Supabase. Solo lo esencial; los catálogos completos salen de los libros Control GG, MO y MP.

    -- perfil ligado a la autenticación de Supabase
    create table perfiles (
      id            uuid primary key references auth.users(id) on delete cascade,
      nombre        text not null,
      puesto        text,
      activo        boolean not null default true,
      creado        timestamptz not null default now()
    );

    create type rol_t as enum ('solicitante','revisor','director','compras','contable','admin');
    create table usuario_roles (
      usuario uuid references perfiles(id) on delete cascade,
      rol     rol_t not null,
      primary key (usuario, rol)
    );

    -- catálogos (los edita el administrador, no el programador)
    create table proveedores (
      id serial primary key, nombre text unique not null, razon_social text, rfc text,
      dias_credito int not null default 0, activo boolean not null default true);
    create table unidades_negocio (
      clave text primary key,          -- Hipodromo, Cacho, Peninsula, Brecha, Xochicalco, Cedis, Corporativo, Comercial
      nombre text not null, sociedad text not null check (sociedad in ('ZHO','PZ2')));
    create table unidades_productivas (
      id serial primary key, unidad_negocio text references unidades_negocio(clave),
      nombre text not null, centro_costo_inv text, activo boolean default true);
    create table centros_costo (clave text primary key);
    create table categorias (id serial primary key, cubeta text check (cubeta in ('GG','MO','MP')), nombre text);

    create type estado_t as enum
      ('borrador','enviada','revisada','autorizada','comprada','pegada','rechazada','cancelada');
    create type tipo_t   as enum ('orden_compra','fondos');

    create table solicitudes (
      id              uuid primary key default gen_random_uuid(),
      folio           text unique not null,          -- 260911-OC-STARTUPLEGAL-01
      tipo            tipo_t not null,
      estado          estado_t not null default 'borrador',
      solicitante     uuid not null references perfiles(id),
      area            text not null,                 -- quién pide: MKT, Mantenimiento, RND, Proyectos...
      unidad_negocio  text not null references unidades_negocio(clave),
      unidad_productiva text not null,               -- a qué se carga; 'Ope Mixto' si es de toda la ubicación
      sociedad        text not null check (sociedad in ('ZHO','PZ2')),
      cubeta          text not null check (cubeta in ('GG','MO','MP')),
      centro_costo    text not null references centros_costo(clave),
      categoria       text not null,
      proveedor_id    int references proveedores(id),
      proveedor_texto text,                          -- proveedor nuevo aún no dado de alta
      tipo_compra     text, prioridad text,
      moneda          text not null default 'MXN' check (moneda in ('MXN','USD')),
      tipo_cambio     numeric(10,4),
      subtotal        numeric(14,2) not null default 0,
      tasa_iva        numeric(4,2)  not null default 8.00,
      iva             numeric(14,2) not null default 0,
      total           numeric(14,2) not null default 0,
      total_mxn       numeric(14,2) not null default 0,
      fecha_documento date not null,
      fecha_pago      date not null,
      dias_credito    int not null default 0,
      fecha_limite    date generated always as (fecha_documento + dias_credito) stored,
      forma_pago      text not null,
      justificacion   text not null,
      uuid_cfdi       text,
      creado          timestamptz not null default now()
    );

    create table partidas (
      id bigserial primary key,
      solicitud uuid not null references solicitudes(id) on delete cascade,
      orden int not null, descripcion text not null, unidad text not null,
      cantidad numeric(12,3) not null check (cantidad > 0),
      precio_unitario numeric(14,2) not null check (precio_unitario >= 0),
      importe numeric(14,2) generated always as (cantidad * precio_unitario) stored
    );

    -- la bitácora que sustituye las firmas: solo se inserta, nunca se edita ni se borra
    create table eventos (
      id bigserial primary key,
      solicitud uuid not null references solicitudes(id) on delete cascade,
      accion text not null,        -- enviar | revisar | autorizar | comprar | pegar | rechazar | despegar
      estado_anterior estado_t, estado_nuevo estado_t,
      actor uuid references perfiles(id),
      automatico boolean not null default false,   -- true cuando la autorizó la regla de tope
      motivo text, ip inet,
      cuando timestamptz not null default now()
    );

    create table exportaciones (
      id bigserial primary key, libro text not null,      -- 'ZHO (GG)' ...
      filas int not null, actor uuid references perfiles(id),
      cuando timestamptz not null default now(), deshecha boolean not null default false
    );
    create table exportacion_solicitudes (
      exportacion bigint references exportaciones(id) on delete cascade,
      solicitud uuid references solicitudes(id), primary key (exportacion, solicitud)
    );

    create table config (clave text primary key, valor jsonb not null);
    -- {'tope_autorizacion': 5000, 'iva_default': 8}

## 09b. Catálogo de unidades productivas

Tal como lo fijó Dirección el 13-sep-2026. `Ope Mixto` es siempre la opción por defecto: el gasto de toda la ubicación.

| Unidad de negocio             | Sociedad | Unidades productivas                                                            |
|-------------------------------|----------|---------------------------------------------------------------------------------|
| Hipódromo                     | PZ2      | Hipodromo · Casa Zibarita · Bar Jamon · Saketori H · Mantequilla H · Ope Mixto  |
| Cacho                         | ZHO      | Mantequilla C · Saketori/Ziba · Saketori C · Nikkei Norteño · Willy · Ope Mixto |
| Brecha                        | ZHO      | Saketori B · Mantequilla B · Ope Mixto                                          |
| Península                     | ZHO      | Mantequilla AM · Mantequilla PM · Ope Mixto                                     |
| Xochicalco                    | ZHO      | Mantequilla Cafe · Kala · Ope Mixto                                             |
| Gerencia de Costos (CEDIS)    | ZHO      | Mano de Obra · Gastos Generales · Ope Mixto                                     |
| Corporativo                   | ZHO      | Mano de Obra · Gastos Generales · Ope Mixto                                     |
| Comercial (cruza ubicaciones) | ZHO      | Ope Mixto · Campaña de marca · Campaña de una unidad                            |

## 10. Seguridad: RLS, no confianza en el front

Row Level Security activo en **todas** las tablas. El front esconde botones; la base de datos es la que impide. Si un día alguien abre la consola del navegador, la política es lo único que lo detiene.

    alter table solicitudes enable row level security;

    create or replace function tiene_rol(r rol_t) returns boolean language sql stable as $$
      select exists (select 1 from usuario_roles ur
                     where ur.usuario = auth.uid() and ur.rol = r) $$;

    -- el solicitante ve las suyas; revisor, director, compras y contable ven todas
    create policy leer on solicitudes for select using (
      solicitante = auth.uid() or tiene_rol('revisor') or tiene_rol('director')
      or tiene_rol('compras') or tiene_rol('contable') or tiene_rol('admin'));

    -- solo crea el dueño, y solo en borrador o enviada
    create policy crear on solicitudes for insert with check (
      solicitante = auth.uid() and estado in ('borrador','enviada'));

    -- el solicitante edita únicamente mientras está en borrador
    create policy editar_borrador on solicitudes for update using (
      solicitante = auth.uid() and estado = 'borrador');

Los cambios de estado **no** se hacen con `UPDATE` desde el cliente: pasan por funciones de Postgres `security definer` (o por la API de Python con la *service key*) que validan la transición, que el actor tenga el rol y que no esté firmando dos pasos. Un `UPDATE` directo a `estado` queda prohibido para todos.

## 08. API en Python (FastAPI)

Python se queda con lo que no debe vivir en el navegador. El resto de las lecturas puede ir directo a Supabase con RLS.

| Endpoint                          | Qué hace                      | Cuidado                                                                                                                                                                               |
|-----------------------------------|-------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `POST /solicitudes`               | Crea y asigna folio           | El folio se genera en Postgres con `advisory lock` por (fecha, proveedor). Contar filas para el consecutivo produce folios repetidos en cuanto dos personas capturan al mismo tiempo. |
| `POST /solicitudes/{id}/enviar`   | borrador → enviada            | Recalcula subtotal, IVA y total **en el servidor**. Lo que mande el navegador se ignora.                                                                                              |
| `POST /solicitudes/{id}/firmar`   | revisar · autorizar · comprar | Valida rol, transición y no-doble-firma. Aplica la regla de tope. Escribe en `eventos`.                                                                                               |
| `POST /solicitudes/{id}/rechazar` | → rechazada                   | Motivo obligatorio, mínimo 10 caracteres.                                                                                                                                             |
| `GET /exportar?libro=ZHO(GG)`     | Devuelve las 10 columnas      | Formatos `tsv` y `xlsx`. Fechas `dd/mm/aaaa`, importes con dos decimales y sin separador de miles.                                                                                    |
| `POST /exportar/marcar`           | → pegada                      | Una sola transacción: crea la exportación, liga las solicitudes y cambia estados. Si algo falla, no se marca nada.                                                                    |
| `POST /exportar/{id}/deshacer`    | Regresa a autorizada          | Solo dentro de 24 h y solo por quien exportó o un admin.                                                                                                                              |
| `POST /usuarios/invitar`          | Alta por correo               | Usa `auth.admin.inviteUserByEmail`. La *service key* vive solo en el servidor, nunca en el front.                                                                                     |

Librerías: `fastapi`, `supabase-py`, `pydantic` para validar, `openpyxl` para el XLSX. El token de Supabase se valida en cada petición y de ahí sale el `auth.uid()`; nunca se recibe el id de usuario como parámetro.

## 09. El bloque que se pega — exacto

Diez columnas, en este orden, que corresponden a **B hasta K** de la hoja del control. Ni una más: de la `M` a la `U` son fórmulas de la tabla de Excel y se calculan solas. Pegar de más las destruye.

| Col | Encabezado en el control | De dónde sale                                           |
|-----|--------------------------|---------------------------------------------------------|
| B   | Fecha Factura / Remisión | `fecha_documento`, formato dd/mm/aaaa                   |
| C   | Factura                  | Folio + primera partida                                 |
| D   | Proveedor                | Nombre del padrón, idéntico                             |
| E   | Moneda                   | Pesos / Dolares                                         |
| F   | Importe                  | `total` con IVA                                         |
| G   | Tipo de Pago             | 01-Efectivo · 02-Cheque · 03-Transferencia · 04-Interno |
| H   | Fecha de Pago            | `fecha_pago`                                            |
| I   | Categoria                | Del catálogo de la cubeta                               |
| J   | Punto Zibarita           | Unidad de negocio                                       |
| K   | Centro de Costo          | OPE. Mixto o INV. …                                     |

El nombre del proveedor debe coincidir carácter por carácter con el padrón del libro: de ahí sale el `VLOOKUP` de días de crédito. Un acento de más rompe la fórmula en silencio.

## 10. Reglas de interfaz

- **Celular primero.** El gerente captura parado en la sucursal. Todo debe funcionar a 360 px, con campos grandes y teclado numérico en los montos (`inputmode="decimal"`).
- **Nada de callejones sin salida.** Toda pantalla vacía dice qué hacer y trae el botón para hacerlo.
- **Guardado automático del borrador** cada pocos segundos. En la sucursal se cae el wifi y se pierde media orden capturada; eso basta para que la gente vuelva al papel.
- **Confirmar solo lo irreversible**: rechazar y marcar pegado. Todo lo demás, directo.
- **Errores en español y con la salida**: “Falta la cotización del proveedor” y el botón para adjuntarla, no “Error 422”.
- **Los totales se ven mientras se captura**, no al final.
- **Avisos por correo** en tres momentos: te toca firmar, te rechazaron algo tuyo, ya se pagó. Nada más — un portal que manda correo por todo se convierte en correo que nadie abre.

## 11. Fases

| Fase                      | Alcance                                              | Listo cuando                                                          |
|---------------------------|------------------------------------------------------|-----------------------------------------------------------------------|
| **1 · Base**              | Auth, perfiles, roles, catálogos, RLS, hub           | Un invitado entra y ve solo sus módulos                               |
| **2 · Orden de compra**   | Captura, partidas, folio, cadena de firmas, bitácora | Una OC real corre de captura a autorizada sin tocar Word              |
| **3 · Copy Paste**        | Export TSV/XLSX, marcar pegado, histórico, deshacer  | Se pega en el Control sin corregir a mano y las fórmulas siguen vivas |
| **4 · Fondos y adjuntos** | El otro formato, Storage para cotizaciones y tickets | Un reembolso con ticket llega completo a Administración               |
| **5 · Cierre fiscal**     | UUID del CFDI, conciliación contra lo pagado         | Cada peso autorizado tiene su factura amarrada                        |

## 12. Lo que NO debe hacer

- **No borrar nada.** Todo es desactivar o cancelar. El histórico es el valor del sistema.
- **No calcular montos en el navegador** como fuente de verdad. Se muestran ahí, se recalculan en el servidor.
- **No inventar catálogos.** Proveedores, categorías y centros de costo salen de los libros que ya existen; si falta uno, se da de alta en Administrador, no en el código.
- **No poner la *service key* de Supabase en el front.** Ni en variables de entorno del navegador.
- **No prorratear entre unidades todavía.** Hoy el gasto comercial se controla aparte con un porcentaje fijo por ubicación; meter prorrateo cambia el número de renglones que se pegan al Excel.
- **No pedir dos veces el mismo dato.** Si el proveedor está en el padrón, sus días de crédito, RFC y razón social se llenan solos.

## 13. Definiciones que faltan

Sin estas tres, el programador se va a inventar una respuesta:

1.  **Tope de autorización** por debajo del cual no se requiere firma de Dirección. Un solo número, en pesos.
2.  **Quién ocupa cada rol** el día del arranque: nombre y correo de revisor, director, compras y contable.
3.  **Qué hacer con una orden autorizada que cambia de monto** al llegar la factura: ¿se corrige y se vuelve a autorizar, o entra una nota de ajuste? Pasa seguido con materia prima.

## 16. Entrega

- **Dónde vive:** Supabase para base de datos, autenticación y archivos; la API de Python y el front en un servicio de despliegue sencillo. Dominio propio bajo `zibarisholding.com` para que el equipo lo reconozca.
- **Cuentas a nombre de la empresa**, no del programador: Supabase, el hosting y el proyecto de Google Cloud del OAuth. Es la diferencia entre contratar un servicio y quedar amarrado a una persona.
- **Qué se entrega:** el repositorio, el respaldo de la base, las credenciales en un gestor, y un documento de una página de cómo dar de alta a alguien nuevo.
- **Datos de arranque:** los tres libros Control GG, MO y MP son la fuente de los catálogos. El padrón de proveedores se carga completo con días de crédito, RFC y razón social.
- **Criterio de aceptación global:** una orden de compra real corre de captura a pegada en el control sin abrir Word ni retecleo, y el Excel conserva sus fórmulas.

