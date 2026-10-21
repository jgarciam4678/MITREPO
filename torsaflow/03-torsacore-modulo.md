# 03 — Módulo «Flujo» en TorsaCore

Especificación del módulo que lleva el marco a TorsaCore. El código de
referencia está en [`torsacore/`](torsacore/) y sigue la estructura habitual de
TorsaCore (`backend/app/*.py` + `frontend/src/components/*.jsx`).

## Decisiones de diseño

| Decisión | Por qué |
|---|---|
| **TorsaCore es el sistema de registro del trabajo del departamento** (no el Excel, no el chat) | Una sola fuente de verdad. Todo el equipo ya entra en TorsaCore cada día. |
| **Odoo sigue siendo el sistema de proyectos y tickets** | Flujo **no** duplica Odoo: lee de él el catálogo de proyectos y enlaza tickets (`odoo_ref`). Así el campo «proyecto» nunca es texto libre ni «-». |
| **Las métricas salen del historial de eventos** | Cada movimiento queda registrado. Nadie rellena «% avance» ni informes. |
| **Las reglas avisan, no prohíben** | Saltarse el límite de WIP es posible indicando el porqué; queda registrado y se revisa en la retrospectiva. Es un marco ágil, no un sistema de permisos. |
| **Definición de Listo y de Hecho en el propio flujo** | No se puede mover a Hecho sin enlace al entregable y aceptación; no se puede empezar sin responsable único y proyecto. |

## Modelo de datos

```
flujo_proyectos  (id, nombre, cliente, odoo_id, activo)
flujo_tarjetas   (id, titulo, responsable, solicitante, proyecto_id, clase, estado,
                  fecha_compromiso, enlace_entregable, aceptada_por,
                  bloqueada, bloqueo_motivo, bloqueo_depende_de, bloqueo_desde, bloqueo_respuesta,
                  odoo_ref, creada_en, lista_en, iniciada_en, terminada_en, actualizada_en)
flujo_eventos    (id, tarjeta_id, momento, usuario, tipo, desde, hacia, detalle)
                  tipo ∈ creada | editada | replanificada | movida | bloqueada |
                         desbloqueada | aceptada | wip_forzado | importada
```

- **Estados:** `backlog → listo → en_curso → en_validacion → hecho`, más `descartado`.
- **Clases:** `urgente`, `fecha_fija`, `estandar`, `mejora`.
- **Bloqueo** es una marca, no un estado: la tarjeta conserva su columna.
- Las **replanificaciones** de fecha generan un evento propio: son visibles y
  cuentan para la fiabilidad.

## Reglas que aplica el backend

| Momento | Regla | Tipo |
|---|---|---|
| Pasar a Listo o En curso | Responsable único (sin «/» ni «,»), proyecto, fecha si es *fecha fija* | Obligatoria |
| Pasar a En curso | Máx. 3 por persona | Aviso; se puede forzar con justificación |
| Pasar a En validación | Máx. 2 por persona | Aviso; se puede forzar con justificación |
| Pasar a En curso una urgente | Máx. 1 urgente activa en el departamento | Aviso; se puede forzar |
| Pasar a Hecho | Enlace al entregable + aceptación registrada | Obligatoria |
| Descartar | Motivo en una línea | Obligatoria |
| Bloquear | Motivo + de quién depende | Obligatoria |

Las reglas rotas devuelven `409` con `{"reglas": [...]}` en lenguaje claro, y
`"se_puede_forzar": true` cuando basta con justificarlo.

## API (`/api/flujo`)

| Método | Ruta | Uso |
|---|---|---|
| `GET` | `/proyectos` | Catálogo de proyectos |
| `PUT` | `/proyectos` | Alta/actualización (lo usa el sincronizador de Odoo) |
| `GET` | `/tarjetas?responsable=&proyecto_id=&estado=` | Tarjetas abiertas con `edad`, `semaforo` y `sin_movimiento` |
| `POST` | `/tarjetas` | Crear (en Backlog o Listo) |
| `PATCH` | `/tarjetas/{id}` | Editar campos |
| `POST` | `/tarjetas/{id}/mover` | `{estado, motivo?, justificacion_wip?}` |
| `POST` | `/tarjetas/{id}/bloquear` · `/desbloquear` | Marca ⚑ |
| `POST` | `/tarjetas/{id}/aceptar` | `{por}`: aceptación del solicitante |
| `GET` | `/tarjetas/{id}/historial` | Eventos de la tarjeta |
| `GET` | `/metricas?semanas=12` | Los 8 índices de [02](02-metricas.md) |
| `GET` | `/prevision?n=20` | Monte Carlo: semanas p50/p85/p95 para terminar N tarjetas |
| `GET` | `/resumen-semanal` | Lo que se mira el lunes: terminadas, vencen en 2 semanas, bloqueadas, envejecidas, sin movimiento, sobre WIP |

## Pantalla

`Flujo.jsx` usa los tokens de `App.css` y las clases de `CMSStudio.css`
(`.cmss-bar`, `.cmss-sec`, `.cmss-sec-h`, `.cmss-pill`, `.btn-primary`,
`.btn-secondary`), de modo que hereda el tema claro/oscuro y se ve como FAS
Setup o CMS Studio.

```
┌ Flujo [Todo el equipo ▾] [Todos los proyectos ▾] [Nueva tarjeta: verbo + entregable] [Añadir]  Tablero | Resumen ⟳ ┐
├ Terminadas semana │ Cycle time p85 │ En rojo │ % bloqueado │ Fiabilidad │ Higiene ┤
├ Backlog │ Listo │ En curso (3/persona) │ En validación (2/persona) │ Hecho (7 días) ┤
│  tarjeta: clase · edad · título · responsable · proyecto · 📅 · ⚑ motivo · [→ siguiente] [⚑]          │
```

- Borde izquierdo de cada tarjeta = semáforo de edad (verde/ámbar/rojo).
- Fondo tenue rojo = bloqueada. Fecha en rojo = compromiso vencido.
- «sin responsable» / «sin proyecto» en ámbar: higiene pendiente.
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
4. **Sincronizador de proyectos desde Odoo** (tarea programada diaria): leer
   `project.project` activos por XML-RPC, con la misma conexión a Odoo que ya
   usa TorsaCore, y llamar a `PUT /api/flujo/proyectos` con
   `{nombre, cliente, odoo_id}`. Añadir siempre un proyecto «Interno».
5. **Migración del Excel semanal:**
   ```bash
   cd backend
   python -m app.importar_seguimiento_cw seguimiento_cw.xlsx             # diagnóstico
   python -m app.importar_seguimiento_cw seguimiento_cw.xlsx --db flujo.db  # carga
   ```
   Carga solo lo abierto de la hoja CW más reciente. «En pausa» entra como
   bloqueada; «Por iniciar» sin proyecto o responsable único entra en Backlog.
6. Opcional: aviso del resumen semanal al canal de Teams del departamento los
   lunes a primera hora (webhook entrante con el JSON de `/resumen-semanal`).

## Pruebas

```bash
cd torsaflow/torsacore/backend
pip install -r requirements.txt
python -m pytest -q
```

Cubren: Definición de Listo y de Hecho, límite de WIP forzable con registro,
transiciones inválidas, bloqueos, métricas, semáforo de edad, previsión Monte
Carlo e importación del Excel (con un Excel sintético, sin datos reales).

## Clasificación

El tablero contiene nombres de clientes y personas: tratarlo como información
interna (nivel L3 de TorsaCore) y no exponerlo fuera de la red corporativa.
