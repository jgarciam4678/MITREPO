# 02 — Métricas (los índices)

Ocho índices, todos calculados automáticamente por TorsaCore a partir del
historial de movimientos de las tarjetas. Nadie rellena métricas a mano.

## Índices de flujo

| # | Índice | Definición | Objetivo inicial | Para qué sirve |
|---|---|---|---|---|
| 1 | **Throughput** | Tarjetas que llegan a Hecho por semana | Estable o creciente | Capacidad real del equipo |
| 2 | **Cycle time (p85)** | Días desde *En curso* hasta *Hecho*; percentil 85 | ≤ 10 días hábiles | «El 85 % de las tarjetas se termina en X días»: la base para comprometer fechas |
| 3 | **WIP por persona** | Tarjetas en *En curso* + *En validación* | ≤ 5 (3 en curso + 2 en validación) | Multitarea, que es la causa principal de retrasos |
| 4 | **Edad del trabajo** | Días que lleva una tarjeta activa sin terminar | Ninguna > p85 de cycle time | Detectar lo que se atasca **antes** de que llegue tarde |
| 5 | **% bloqueado** | Tarjetas activas con ⚑ / tarjetas activas | < 15 % | Dependencias externas que nos frenan |
| 6 | **Fiabilidad de compromiso** | Tarjetas con fecha terminadas a tiempo / tarjetas con fecha que vencieron en el periodo | ≥ 80 % | Credibilidad del departamento ante clientes y otras áreas |
| 7 | **Distribución del trabajo** | % de Hecho por clase de servicio y por proyecto | Mejora interna ≈ 20 % | Saber en qué se va realmente la capacidad |
| 8 | **Higiene del tablero** | % de tarjetas activas con responsable único, proyecto y (si aplica) fecha | ≥ 95 % | Que los demás índices sean fiables |

### Por qué estos y no otros

- **Ley de Little:** `cycle time medio = WIP medio / throughput`. Con el mismo
  equipo, la única forma de entregar antes es tener **menos cosas a la vez**. Por
  eso el límite de WIP es la palanca principal del marco.
- **% de avance** no está: es subjetivo, se estanca en el 80–90 % y no predice
  nada. La edad del trabajo sí predice.
- **Horas imputadas** no están: miden esfuerzo, no entrega.

## Previsión sin estimar

Con el histórico de cycle time se responde a «¿para cuándo?» sin estimar:

- Una tarjeta: *«El 85 % de nuestras tarjetas se termina en 9 días hábiles o menos.»*
- Un conjunto de N tarjetas: simulación Monte Carlo con el throughput semanal de
  las últimas 8–12 semanas (TorsaCore lo calcula; ver [03](03-torsacore-modulo.md)).

## Cómo se leen en las reuniones

| Reunión | Índices que se miran |
|---|---|
| Diario | Edad del trabajo (tarjetas en ámbar/rojo) y ⚑ bloqueadas |
| Reposición semanal | WIP por persona, compromisos que vencen en 2 semanas, throughput de la semana |
| Revisión de portafolio | Los ocho, tendencia de 3 meses, distribución por proyecto |
| Retrospectiva | El índice que peor haya evolucionado → una mejora |

## Semáforo de edad

| Color | Edad de la tarjeta activa |
|---|---|
| Verde | ≤ 50 % del p85 de cycle time |
| Ámbar | 50–100 % del p85 |
| Rojo | > p85: se habla en el diario de hoy |

Mientras no haya histórico (primeras 6 semanas) se usa un p85 provisional de 10 días hábiles.
