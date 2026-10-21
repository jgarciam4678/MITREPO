# 01 — Marco de comportamiento

Las herramientas no ordenan a un equipo; los hábitos sí. Este documento define
los hábitos mínimos. Todo lo que no está aquí queda a criterio de cada persona.

## 1. Seis principios

1. **Todo el trabajo visible.** Si te ocupa más de 2 horas, va al tablero. Las
   peticiones por chat, correo o pasillo se convierten en tarjeta antes de empezar.
2. **Dejar de empezar, empezar a terminar.** Máximo **3 tarjetas En curso por
   persona**. Para empezar algo nuevo, primero terminas, entregas o bloqueas otra cosa.
3. **Un responsable, un entregable, una fecha.** Cada tarjeta tiene un único
   responsable (no «Ana / Luis»), empieza por un verbo y nombra lo que se
   entrega. Si no tiene fecha, no es un compromiso: es una intención.
4. **Un bloqueo se ve en 24 h y se escala en 48 h.** Esperar a otra área, al
   cliente o a un proveedor es normal; esperar en silencio no.
5. **Hecho es entregado y aceptado.** No «casi terminado» ni «al 90 %». Hecho
   significa que quien lo pidió lo tiene y el enlace al entregable está en la tarjeta.
6. **Decidir con datos del flujo.** Las conversaciones sobre prioridades y
   capacidad se apoyan en las métricas de [02](02-metricas.md), no en impresiones.

## 2. Tres niveles de trabajo (Flight Levels)

| Nivel | Qué se ve | Quién | Cadencia |
|---|---|---|---|
| **3 · Portafolio** | Proyectos y clientes activos, su estado y su prioridad relativa | Jefatura + PMs | Mensual |
| **2 · Coordinación** | Dependencias con Comercial, Desarrollo, proveedores y cliente | Jefatura + PMs + facilitador | Semanal |
| **1 · Equipo** | Tarjetas de cada persona, del Backlog a Hecho | Todo el equipo | Diario |

Los problemas suben de nivel cuando el nivel inferior no puede resolverlos; las
prioridades bajan del nivel superior. Nadie prioriza su propio trabajo contra el
de otro proyecto: eso se decide en nivel 3.

## 3. Roles (sin crear cargos nuevos)

| Rol | Lo ejerce | Responsabilidad |
|---|---|---|
| **Responsable de tarjeta** | Cualquier persona | Mueve su tarjeta en el momento, declara bloqueos, enlaza el entregable |
| **Dueño de proyecto** | PM o ingeniero líder del proyecto | Ordena el backlog de su proyecto, negocia fechas con el cliente interno o externo |
| **Facilitador de flujo** | Rotativo cada mes | Conduce el diario y la reunión semanal, vigila tarjetas envejecidas y límites de WIP |
| **Jefatura** | Jefe de departamento | Decide prioridades entre proyectos, desbloquea lo que el equipo no puede, protege el WIP |

## 4. Estados y políticas del tablero

| Estado | Entra cuando… (política explícita) |
|---|---|
| **Backlog** | Alguien lo propone. Sin requisitos. Se poda cada mes. |
| **Listo** | Cumple la *Definición de Listo* (abajo). Es lo que se puede empezar ya. |
| **En curso** | El responsable empieza a trabajar. Límite: 3 por persona. |
| **En validación** | Entregado a quien lo pidió y pendiente de su aceptación. Límite: 2 por persona. |
| **Hecho** | Cumple la *Definición de Hecho*. |
| **Descartado** | Se decide no hacerlo. Con motivo en una línea. Descartar también es gestionar. |

**Bloqueado no es una columna**: es una marca ⚑ sobre la tarjeta, que se queda en
su estado. Obliga a indicar *motivo*, *de quién depende* y *desde cuándo*.

> «En pausa» desaparece. Una tarjeta está bloqueada (con motivo y dueño), vuelve
> al Backlog o se descarta.

### Clases de servicio

| Clase | Ejemplo | Regla |
|---|---|---|
| **Urgente** | Incidencia de cliente parada, fallo en producción | Salta la cola. Máximo 1 en todo el departamento a la vez. |
| **Fecha fija** | Entregable comprometido con cliente, auditoría | Se empieza con margen; se revisa cada semana. |
| **Estándar** | La mayoría del trabajo | Orden del backlog. |
| **Mejora interna** | Guías de taller, herramientas, documentación propia | Cupo reservado del ~20 % de la capacidad para que no se coma ni se olvide. |

### Definición de Listo (DoR) — 4 preguntas

1. ¿El título empieza por un verbo y nombra el entregable? («Elaborar protocolo de pruebas SAF», no «Protocolo»).
2. ¿Tiene un único responsable y un proyecto del catálogo (o «Interno»)?
3. ¿Cabe en **2 semanas** o menos? Si no, se parte en tarjetas más pequeñas.
4. Si es un compromiso con alguien: ¿tiene fecha acordada con esa persona?

### Definición de Hecho (DoD) — 3 comprobaciones

1. El entregable está enlazado en la tarjeta (Biblioteca técnica de TorsaCore,
   SharePoint, Odoo o Craft). No se adjuntan copias.
2. Quien lo pidió lo ha aceptado (basta un «OK» registrado en la tarjeta).
3. Si es documentación técnica, está publicada en la Biblioteca técnica con su
   código y tabla de control.

## 5. Cadencias (≤ 1 h 45 min por persona y semana)

| Reunión | Cuándo | Duración | Quién | Formato |
|---|---|---|---|---|
| **Diario de flujo** | Cada día, misma hora | 15 min | Equipo | De pie frente al tablero. Se recorre **de derecha a izquierda** (lo más cerca de Hecho primero). Solo se habla de bloqueos, tarjetas envejecidas y ayuda necesaria. No es una ronda de «qué hice ayer». |
| **Reposición semanal** | Lunes | 30 min | Jefatura, PMs, facilitador | ¿Qué terminamos? ¿Qué entra a Listo? ¿Qué compromisos de fecha vencen en 2 semanas? Sustituye al Excel semanal. |
| **Bloqueos externos** | Semanal, tras la reposición | 20 min | Jefatura + enlaces de Comercial/Desarrollo | Solo tarjetas con ⚑ que dependen de otra área. Sale una fecha o una decisión por tarjeta. |
| **Revisión de portafolio** | Primer lunes del mes | 60 min | Jefatura + PMs | Métricas del mes, prioridad de proyectos, qué paramos para poder empezar otra cosa. |
| **Retrospectiva** | Último viernes del mes | 45 min | Todo el equipo | Una sola mejora concreta al proceso, con responsable. Se revisa la del mes anterior. |

## 6. Gestión de bloqueos y escalado

| Tiempo bloqueado | Qué pasa |
|---|---|
| **0 h** | El responsable marca ⚑ con motivo, dependencia y fecha esperada de respuesta. |
| **48 h** | Pasa al dueño de proyecto, que contacta con el responsable de la otra parte. |
| **5 días hábiles** | Sube a la reunión de bloqueos externos; jefatura decide: escalar, replanificar o descartar. |
| **15 días hábiles** | Se trata en la revisión de portafolio. Un bloqueo de tres semanas es una decisión pendiente, no una espera. |

Las dependencias externas (Comercial, Desarrollo, proveedor, cliente) siempre
tienen un **dueño interno** que las persigue.

## 7. Acuerdos de trabajo

- Cada persona actualiza sus tarjetas **cuando cambia algo**, no al final de la semana.
- Una tarjeta sin movimiento durante **10 días hábiles** se revisa en el diario: se
  desbloquea, se parte o se devuelve al Backlog.
- Una tarjeta en Listo sin empezar durante **3 semanas** no era prioritaria: vuelve
  al Backlog o se descarta en la reposición semanal.
- No hay «% de avance». Si una tarjeta es grande, se parte o se usa una lista de
  comprobación dentro de la tarjeta.
- Las peticiones que llegan por chat se responden con «créala en el tablero y la
  vemos en la reposición» salvo que sean urgentes.
- La reunión se cancela si no hay nada que tratar. Nadie defiende una reunión vacía.

## 8. Lo que este marco NO pide

- Actas de reunión (las decisiones quedan en la tarjeta).
- Informes de estado semanales (los genera TorsaCore).
- Planes de proyecto detallados para trabajo interno.
- Estimaciones en horas. Se mide el tiempo real (cycle time) y se predice con él.
