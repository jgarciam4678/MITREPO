# TorsaFlow — marco de trabajo ágil para el departamento

Marco ligero para gestionar el trabajo del departamento sin burocracia y sin
desorden. Combina lo que hoy se considera la mejor práctica en gestión adaptativa:

| Referencia | Qué tomamos |
|---|---|
| **Kanban Method / Kanban Guide (2020)** | Visualizar el trabajo, limitar el trabajo en curso (WIP), gestionar el flujo |
| **Flight Levels** (K. Leopold) | Tres niveles: persona/equipo, coordinación y portafolio |
| **PMBOK 7ª ed.** (PMI) | Gestión por principios y entrega de valor, no por documentos |
| **Scrum Guide (2020)** | Cadencia fija de inspección y adaptación |
| **Métricas de flujo** (Little, Vacanti, Flow Framework) | Throughput, cycle time, edad del trabajo, % bloqueado, fiabilidad |

**Se apoya en lo que ya existe** en TorsaCore y Craft y añade la pieza que
falta, la ejecución del día a día:

```
Project Charter ──▶ Plan de Trabajo ──▶ [ Flujo: tarjetas ] ──▶ Biblioteca técnica (Craft)
  (TorsaCore)         (TorsaCore)          NUEVO                 (entregables con control documental)
```

**Regla de oro:** el tablero es la única fuente de verdad. Lo que no está en el
tablero no existe; lo que está en el tablero se mantiene al día en el momento,
no el viernes.

## Contenido

| Documento | Para quién | Qué contiene |
|---|---|---|
| [01 — Comportamiento](01-comportamiento.md) | Todo el departamento | Principios, roles, cadencias, acuerdos, DoR/DoD, bloqueos |
| [02 — Métricas](02-metricas.md) | Jefatura y PMs | Los índices, cómo se calculan y objetivos |
| [03 — Módulo Flujo en TorsaCore](03-torsacore-modulo.md) | Desarrollo TorsaCore | Modelo de datos, reglas, API, pantallas, enlace con Charter, Plan y Biblioteca |
| [04 — Plan de despliegue](04-despliegue.md) | Jefatura | 90 días, criterios de éxito, antipatrones |
| [`torsacore/`](torsacore/) | Desarrollo TorsaCore | Código de referencia: router FastAPI y componente React |

## En una página

```
 NIVEL 3 · PORTAFOLIO     mensual 60'   ¿En qué proyectos/clientes invertimos? ¿Qué paramos?
 NIVEL 2 · COORDINACIÓN   semanal 30'   ¿Qué entra esta semana? ¿Qué bloqueos externos escalamos?
 NIVEL 1 · EQUIPO         diario 15'    ¿Qué terminamos hoy? ¿Qué está atascado?

 Backlog → Listo → En curso → En validación → Hecho
                    (WIP ≤ 3 por persona)      (con entregable enlazado)
            ⚑ Bloqueado = marca sobre la tarjeta, con motivo, dueño y fecha
```

- Menos de **1 h 45 min de reuniones por persona y semana** en total.
- Sin informes semanales: el resumen semanal lo genera TorsaCore desde el tablero.
- Sin «% de avance» subjetivo: el avance se mide por tarjetas terminadas y tiempos reales.
