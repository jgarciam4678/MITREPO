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
| [05 — Cómo definir una actividad](05-definir-actividades.md) | Jefatura y quien prepare trabajo | De un pendiente a una tarjeta en 7 pasos, la ficha y la comprobación final |
| [06 — Niveles de gestión y riesgos](06-niveles-y-riesgos.md) | Jefatura y líderes N3 | Portafolio (jefatura), proyecto y riesgos (N3), ejecución (N2, N1); registro de riesgos ligero |
| [`torsacore/`](torsacore/) | Desarrollo TorsaCore | Código de referencia: router FastAPI y componente React |

## En una página

```
 Jefatura (portafolio): prioridades entre proyectos, capacidad, riesgos altos, desbloqueos
 N3 (proyecto):         prepara tarjetas Listas, lleva riesgos y cliente
 N2 / N1 (ejecución):   toman tarjetas de su nivel ──▶ las resuelven ──▶ Hecho con evidencia
 TorsaCore:             bloqueos de 2+ días y riesgos altos ──▶ suben solos a jefatura

 Backlog → Listo (libre) → En curso → Hecho
                           (≤ 3 por persona)   (evidencia enlazada, sin validador)
            ⚑ Bloqueado = marca sobre la tarjeta, con motivo y de quién depende
```

- Sin reunión diaria, sin RACI, sin validadores por actividad.
- Una revisión de 20 minutos el lunes, solo si el resumen automático marca algo.
- Sin informes semanales: el resumen semanal lo genera TorsaCore desde el tablero.
- Sin «% de avance» subjetivo: el avance se mide por tarjetas terminadas y tiempos reales.
