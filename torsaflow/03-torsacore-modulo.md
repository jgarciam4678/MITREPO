# 03 — Módulo «Flujo» en TorsaCore

Especificación del módulo que lleva el marco a TorsaCore. El código de
referencia está en [`torsacore/`](torsacore/) y sigue la estructura habitual de
TorsaCore (`backend/app/*.py` + `frontend/src/components/*.jsx`).

## Qué hay hoy y qué falta

| Capa | Hoy | Pieza |
|---|---|---|
| **Planificación** | TorsaCore genera el **Project Charter**, lo pasa por aprobación y, una vez aprobado, genera el **Plan de Trabajo** (fases, responsabilidades, riesgos, matriz de pruebas, KPIs, entregables) | Existe |
| **Entregables** | La **Biblioteca técnica** (Craft) guarda documentos con control documental: código, versión, estado, clasificación, portafolio, nivel, autor/responsable/aprobador | Existe |
| **Ejecución** | No hay sitio donde se vea quién hace qué esta semana, qué fase está bloqueada y qué se ha entregado. Las listas de comprobación de Craft son de procedimientos, no de seguimiento | **Flujo (nuevo)** |

Flujo une las dos capas que ya existen: las fases del Plan de Trabajo se
convierten en tarjetas, y una tarjeta solo llega a Hecho cuando su entregable
está en la Biblioteca técnica.

## Decisiones de diseño

| Decisión | Por qué |
|---|---|
| **TorsaCore es el sistema de registro del trabajo del departamento** | Una sola fuente de verdad, en la herramienta que el equipo ya usa a diario. |
| **El catálogo de proyectos son los Project Charters de TorsaCore** | El proyecto de una tarjeta nunca es texto libre: es un código de Charter (o «Interno»). Hereda cliente, portafolio, responsable y fechas. |
| **Las tarjetas de proyecto nacen del Plan de Trabajo** | Al aprobarse un Plan, cada fase se convierte en una tarjeta con su fecha y su responsable. Lo que está «A definir» / «A asignar» entra en Backlog y se ve como hueco. |
| **Hecho = entregable en la Biblioteca técnica** | La tarjeta guarda el código del documento (`documento_codigo`). La evidencia vive en Craft, no en adjuntos. |
| **Las métricas salen del historial de eventos** | Cada movimiento queda registrado. Nadie rellena «% avance» ni informes. |
| **Las reglas avisan, no prohíben** | Saltarse el límite de WIP es posible indicando el porqué; queda registrado y se revisa en la retrospectiva. |

## Modelo de datos

```
flujo_proyectos  (id, codigo, nombre, cliente, portafolio, responsable,
                  estado_charter, fecha_inicio, fecha_fin, activo)
flujo_tarjetas   (id, titulo, responsable, solicitante, proyecto_id, clase, estado,
                  fecha_compromiso, fase, documento_codigo, enlace_entregable, aceptada_por,
                  bloqueada, bloqueo_motivo, bloqueo_depende_de, bloqueo_desde, bloqueo_respuesta,
                  creada_en, lista_en, iniciada_en, terminada_en, actualizada_en)
flujo_eventos    (id, tarjeta_id, momento, usuario, tipo, desde, hacia, detalle)
                  tipo ∈ creada | editada | replanificada | movida | bloqueada |
                         desbloqueada | aceptada | wip_forzado
```

- `flujo_proyectos.codigo` = código del Charter (p. ej. `ES-SAF-DOC-PC-…`); `INTERNO` para trabajo sin Charter.
- `portafolio` usa los mismos valores que el control documental (CMS, SAF, AO, NEPTUNE, INFRA, GLB…).
- **Estados:** `backlog → listo → en_curso → en_validacion → hecho`, más `descartado`.
- **Clases:** `urgente`, `fecha_fija`, `estandar`, `mejora`.
- **Bloqueo** es una marca, no un estado: la tarjeta conserva su columna.
- Las **replanificaciones** de fecha generan un evento propio y cuentan para la fiabilidad.

## Reglas que aplica el backend

| Momento | Regla | Tipo |
|---|---|---|
| Pasar a Listo | Proyecto y, si es *fecha fija*, fecha. El dueño es opcional: una tarjeta Lista puede estar libre | Obligatoria |
| Pasar a En curso | Un dueño único (sin «/» ni «,»). `POST /tomar` lo pone automáticamente | Obligatoria |
| Pasar a En curso | Máx. 3 por persona | Aviso; se puede forzar con justificación |
| Pasar a En validación | Máx. 2 por persona | Aviso; se puede forzar con justificación |
| Pasar a En curso una urgente | Máx. 1 urgente activa en el departamento | Aviso; se puede forzar |
| Pasar a Hecho | Evidencia: código en la Biblioteca o enlace de Craft. Sin validador | Obligatoria |
| Descartar | Motivo en una línea | Obligatoria |
| Bloquear | Motivo + de quién depende | Obligatoria |
| Generar desde el Plan | «A definir», «A asignar», «—» y «Pendiente de confirmar» cuentan como vacíos | Fase a Backlog |

Las reglas rotas devuelven `409` con `{"reglas": [...]}` en lenguaje claro, y
`"se_puede_forzar": true` cuando basta con justificarlo.

## API (`/api/flujo`)

| Método | Ruta | Uso |
|---|---|---|
| `GET` | `/proyectos` | Catálogo de proyectos (Charters) |
| `PUT` | `/proyectos` | Alta/actualización por código de Charter. TorsaCore lo llama al guardar o aprobar un Charter |
| `POST` | `/proyectos/{id}/plan` | `{fases: [{fase, actividad, inicio, fin, responsable}]}`: crea una tarjeta por fase. Idempotente. Devuelve las fases sin fecha o responsable |
| `GET` | `/tarjetas?responsable=&proyecto_id=&estado=` | Tarjetas abiertas con `edad`, `semaforo` y `sin_movimiento` |
| `POST` | `/tarjetas` | Crear (en Backlog o Listo) |
| `PATCH` | `/tarjetas/{id}` | Editar campos, incluido `documento_codigo` |
| `POST` | `/tarjetas/{id}/mover` | `{estado, motivo?, justificacion_wip?}` |
| `POST` | `/tarjetas/{id}/bloquear` · `/desbloquear` | Marca ⚑ |
| `POST` | `/tarjetas/{id}/tomar` | Autoasignación: quien llama se convierte en dueño y la tarjeta pasa a En curso (respeta el límite de WIP) |
| `POST` | `/tarjetas/{id}/aceptar` | Opcional: registrar la conformidad de un tercero (cliente, sitio) cuando el contrato lo pide |
| `GET` | `/tarjetas/{id}/historial` | Eventos de la tarjeta |
| `GET` | `/metricas?semanas=12` | Índices de flujo + `higiene_proyectos` (Charters completos) |
| `GET` | `/prevision?n=20` | Monte Carlo: semanas p50/p85/p95 para terminar N tarjetas |
| `GET` | `/resumen-semanal` | Resumen asíncrono: para desbloquear (2+ días), libres, vencen en 2 semanas, terminadas, envejecidas, sin movimiento, sobre WIP |

## Pantalla

`Flujo.jsx` usa los tokens de `App.css` y las clases de `CMSStudio.css`
(`.cmss-bar`, `.cmss-sec`, `.cmss-sec-h`, `.cmss-pill`, `.btn-primary`,
`.btn-secondary`), de modo que hereda el tema claro/oscuro y se ve como FAS
Setup o CMS Studio.

```
┌ Flujo [Equipo ▾] [Portafolio ▾] [Proyecto ▾] [Nueva tarjeta: verbo + entregable] [Añadir]   Tablero | Resumen ⟳ ┐
├ Terminadas │ Cycle time p85 │ En rojo │ % bloqueado │ Fiabilidad │ Higiene tablero │ Charters completos ┤
├ Backlog │ Listo (libres con botón «Tomar») │ En curso (3/persona) │ En validación (terceros) │ Hecho (7 días) ┤
│  tarjeta: clase · portafolio · edad · título · responsable · proyecto · fase · 📅 · 📄 código · ⚑ motivo │
```

- Borde izquierdo de cada tarjeta = semáforo de edad (verde/ámbar/rojo).
- Fondo tenue rojo = bloqueada. Fecha en rojo = compromiso vencido.
- «sin responsable» / «sin proyecto» en ámbar: higiene pendiente.
- Al mover a Hecho pide el código del documento en la Biblioteca y quién lo acepta.
- Vista **Resumen semanal** = la agenda de la reunión del lunes.

## Integración con TorsaCore — pasos

1. Copiar `torsacore/backend/app/flujo.py` a `backend/app/` y registrar el router en `main.py`:
   ```python
   from app.flujo import router as flujo_router
   app.include_router(flujo_router)
   ```
2. Sustituir `usuario_actual` por la dependencia de autenticación de TorsaCore y,
   si procede, `conexion` por el acceso a datos que use el backend (marcados `ADAPTAR`).
3. Copiar `Flujo.jsx` y `Flujo.css` a `frontend/src/components/`, añadir la
   entrada al menú lateral y las cadenas a `es.json` / `en.json` si se quiere i18n.
4. **Enganche con el Project Charter:** al guardar o cambiar de estado un
   Charter, llamar a `PUT /api/flujo/proyectos` con su código, nombre, cliente,
   portafolio, responsable, estado y fechas. Crear una vez el proyecto `INTERNO`
   (portafolio `GLB`).
5. **Enganche con el Plan de Trabajo:** cuando se aprueba un Plan, enviar su
   tabla *Plan de ejecución* (fase, actividad, inicio, fin) y el responsable de
   cada fase a `POST /api/flujo/proyectos/{id}/plan`. Si la respuesta trae
   `fases_sin_fecha_o_responsable`, mostrarlas en el propio Plan como aviso.
6. **Enganche con la Biblioteca técnica:** al publicar un documento con
   `Proyecto: …` en su control documental, TorsaCore puede proponer cerrar la
   tarjeta abierta de ese proyecto rellenando `documento_codigo`.
7. Opcional: enviar `/resumen-semanal` al canal del departamento los lunes a primera hora.

## Pruebas

```bash
cd torsaflow/torsacore/backend
pip install -r requirements.txt
python -m pytest -q
```

Cubren: Definición de Listo y de Hecho, límite de WIP forzable con registro,
transiciones inválidas, bloqueos, métricas, semáforo de edad, previsión Monte
Carlo, generación de tarjetas desde el Plan de Trabajo e higiene de Charters.

## Clasificación

El tablero contiene nombres de clientes y personas: tratarlo como información
interna (nivel L3 de TorsaCore) y no exponerlo fuera de la red corporativa.
