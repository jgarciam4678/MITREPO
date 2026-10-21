# 01 — Marco de comportamiento

Un equipo pequeño de gente que resuelve problemas no necesita validadores ni
reuniones diarias: necesita saber qué hay que resolver, poder tomarlo y que
los bloqueos lleguen rápido a quien puede quitarlos. Este documento define los
hábitos mínimos para eso. Todo lo demás queda a criterio de cada persona.

## 1. Seis principios

1. **Todo el trabajo visible.** Si te ocupa más de 2 horas, va al tablero. Las
   peticiones por chat, correo o pasillo se convierten en tarjeta antes de empezar.
2. **Cada tarjeta tiene un dueño, y el dueño decide.** El dueño resuelve la
   tarjeta de principio a fin, decide cómo y pide ayuda a quien la necesite. No
   hay aprobadores intermedios ni matrices de responsabilidad.
3. **Se toma, no se asigna.** Las tarjetas Listas pueden estar libres; quien
   tiene capacidad toma la siguiente. La jefatura solo asigna cuando la tarjeta
   requiere a una persona concreta.
4. **Dejar de empezar, empezar a terminar.** Máximo **3 tarjetas En curso por
   persona**. Para tomar otra, primero terminas o marcas un bloqueo.
5. **Hecho se demuestra con evidencia, no con una firma.** El dueño declara
   Hecho enlazando la evidencia (documento en la Biblioteca técnica, enlace de
   Craft). Solo el cliente firma, y solo en los hitos de contrato.
6. **Los bloqueos suben solos.** Esperar a otra área, al cliente o a un
   proveedor es normal; esperar en silencio no. El dueño marca ⚑ y TorsaCore
   se lo hace llegar a la jefatura sin necesidad de reunión.

## 2. Roles

Solo dos, sin cargos nuevos:

| Rol | Qué hace | Qué no hace |
|---|---|---|
| **Dueño de la tarjeta** (cualquier persona) | Toma la tarjeta, la resuelve, decide cómo, marca los bloqueos en el momento y la cierra con evidencia | Pedir permiso para resolver dentro de su tarjeta |
| **Jefatura** | Busca y prepara los problemas en el mundo real y los convierte en tarjetas Listas; quita bloqueos que el equipo no puede quitar; decide prioridades entre proyectos; trata con el cliente | Validar cada tarjeta, pedir informes, convocar reuniones de seguimiento |

## 3. Tres niveles de trabajo (Flight Levels)

| Nivel | Qué se ve | Dónde |
|---|---|---|
| **3 · Portafolio** | Portafolios (CMS, SAF, AO, NEPTUNE, INFRA…) y sus Project Charters: qué proyectos van primero, qué se para | TorsaCore · Charter |
| **2 · Proyecto** | Fases del Plan de Trabajo y dependencias con Comercial, Desarrollo, proveedores y cliente | TorsaCore · Plan de Trabajo |
| **1 · Tarjetas** | Lo que cada persona está resolviendo, del Backlog a Hecho | TorsaCore · Flujo |

```
Project Charter ──▶ Plan de Trabajo ──fases──▶ Tarjetas (Flujo) ──▶ Evidencia en la Biblioteca técnica (Craft)
```

## 4. Estados del tablero

| Estado | Significa |
|---|---|
| **Backlog** | Identificado, todavía sin preparar. |
| **Listo** | Preparado para empezar (cumple la Definición de Listo). Puede estar **libre**, sin dueño. |
| **En curso** | Alguien lo ha tomado. Límite: 3 por persona. |
| **En validación** | Solo cuando un tercero tiene que probarlo (cliente, sitio). Lo interno pasa directo a Hecho. |
| **Hecho** | Con evidencia enlazada. |
| **Descartado** | Se decide no hacerlo, con motivo en una línea. Descartar también es gestionar. |

**Bloqueado no es una columna**: es una marca ⚑ sobre la tarjeta, con *motivo* y
*de quién depende*. «En pausa» no existe: una tarjeta está bloqueada, vuelve al
Backlog o se descarta.

### Clases de servicio

| Clase | Ejemplo | Regla |
|---|---|---|
| **Urgente** | Incidencia de cliente cubierta por el SLA, fallo en producción | Salta la cola. Máximo 1 en todo el departamento a la vez. |
| **Fecha fija** | Entregable comprometido con cliente | Se empieza con margen. |
| **Estándar** | La mayoría del trabajo | Se toma en orden. |
| **Mejora interna** | Guías, herramientas, documentación propia | ~20 % de la capacidad para que no se olvide. |

### Definición de Listo — 3 preguntas

1. ¿El título empieza por un verbo y nombra el resultado? («Corregir la ordenación de alertas por distancia», no «Alertas»).
2. ¿Tiene proyecto (o «Interno») y, si hay compromiso, fecha?
3. ¿Cabe en **2 semanas** o menos? Si no, se parte.

Preparar tarjetas Listas es el trabajo principal de la jefatura.

### Definición de Hecho

1. La evidencia está enlazada en la tarjeta: código en la Biblioteca técnica o enlace de Craft.
2. Si es documentación técnica, se publica con su control documental completo.

Nadie más tiene que aprobarla. Si algo resulta no estar bien, la tarjeta se
reabre: es más barato que validar todo por adelantado.

## 5. Ritmo: asíncrono por defecto

No hay reunión diaria. El tablero y los avisos automáticos de TorsaCore hacen
ese trabajo.

| Qué | Cuándo | Cómo |
|---|---|---|
| **Actualizar el tablero** | Cuando algo cambia | Cada dueño mueve su tarjeta en el momento. Dos clics, no un informe. |
| **Avisos automáticos** | Continuo | Bloqueada 2 días hábiles → aviso a jefatura. Tarjeta en rojo por edad → aviso a su dueño. Hay tarjetas libres → visibles para todos. |
| **Revisión del lunes** | Semanal, 20 min como máximo | Jefatura (y quien quiera) sobre el *Resumen semanal*: lo que hay que desbloquear, lo que vence en 2 semanas y qué preparar como Listo. **Si el resumen no marca nada, no hay reunión.** |
| **Mirada mensual** | Una vez al mes, 45 min | Las métricas del mes y una sola mejora al proceso. |

Total: menos de una hora por persona y semana.

## 6. Bloqueos

| Tiempo bloqueado | Qué pasa |
|---|---|
| **0** | El dueño marca ⚑: qué falta y de quién depende. |
| **2 días hábiles** | TorsaCore lo pone en «Para desbloquear». La jefatura lo resuelve fuera del tablero: llamada, visita, decisión. |
| **2 semanas** | Ya no es una espera, es una decisión: escalar, replanificar o descartar. |

## 7. Acuerdos de trabajo

- Una tarjeta sin movimiento en **10 días hábiles** la revisa su dueño: se
  desbloquea, se parte o vuelve al Backlog.
- Una tarjeta Lista que nadie toma en **3 semanas** no era prioritaria: vuelve al
  Backlog o se descarta.
- No hay «% de avance». Si una tarjeta es grande, se parte.
- Si fuerzas el límite de 3, escribe por qué. No pasa nada; sirve para ver
  patrones en la mirada mensual.

## 8. Lo que este marco NO pide

- Validadores por actividad ni matrices RACI.
- Reuniones diarias, puntos de historia ni sprints.
- Actas de reunión (las decisiones quedan en la tarjeta).
- Informes de estado (los genera TorsaCore).
- Estimaciones en horas. Se mide el tiempo real y se predice con él.
