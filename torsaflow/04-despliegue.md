# 04 — Plan de despliegue (90 días)

El marco se introduce de forma evolutiva (principio del Kanban Method: *empieza
por lo que haces ahora*). No se reorganiza a nadie ni se cambian cargos.

## Fase 0 — Preparar (semana 1)

| Acción | Responsable | Resultado |
|---|---|---|
| Ejecutar el importador sobre el Excel semanal en modo diagnóstico | Jefatura | Línea base: % sin proyecto, sin fecha, tareas arrastradas, carga por persona |
| **Limpieza inicial** en una sesión de 60 min: todo lo «Por iniciar» con 3+ semanas se descarta o vuelve a Backlog; cada «En pausa» recibe motivo y dueño o se descarta | Jefatura + PMs | Tablero creíble desde el día 1 |
| Desplegar el módulo Flujo en TorsaCore y sincronizar proyectos de Odoo | Desarrollo TorsaCore | Módulo operativo |
| Cargar las tarjetas abiertas con el importador | Jefatura | Tablero con el trabajo real |
| Presentar el marco al equipo: 30 min, solo los 6 principios y las 5 cadencias | Jefatura | Todos saben qué cambia el lunes |

## Fase 1 — Piloto (semanas 2–3)

- Un subequipo (4–6 personas) usa el tablero y el diario de 15 min.
- El resto sigue con el Excel, pero la jefatura ya prepara la reunión del lunes
  con el *Resumen semanal* de TorsaCore.
- Al final: retro de 30 min con el piloto, ajustar límites de WIP si hace falta.

## Fase 2 — Todo el departamento (semanas 4–6)

- Todo el departamento en el tablero. **El Excel semanal se congela** (solo lectura).
- Arrancan la reposición semanal, la reunión de bloqueos externos y el facilitador rotativo.
- Se invita a Comercial y Desarrollo a la reunión de bloqueos externos.

## Fase 3 — Medir y mejorar (semanas 7–12)

- Primera revisión de portafolio con métricas reales (ya hay 6 semanas de histórico).
- Se sustituye el p85 provisional por el real.
- Las fechas a clientes se empiezan a dar con la previsión de TorsaCore (*«con un 85 % de confianza, en 4 semanas»*).
- Retrospectiva mensual: una mejora al proceso por mes.

## Criterios de éxito a 90 días

| Índice | Objetivo |
|---|---|
| Higiene del tablero | ≥ 95 % |
| Tarjetas activas sin proyecto | 0 |
| Personas por encima de 5 tarjetas activas | 0 |
| Tarjetas en Listo con 3+ semanas | 0 |
| Fiabilidad de compromiso | ≥ 80 % |
| Bloqueos con más de 5 días hábiles sin escalar | 0 |
| Excel semanal | Retirado |
| Tiempo de reuniones por persona y semana | ≤ 1 h 45 min |

## Antipatrones a vigilar

| Señal | Qué hacer |
|---|---|
| El tablero se actualiza el viernes «para la reunión» | El diario se hace frente al tablero; si no está al día, se actualiza ahí mismo, delante de todos, una vez. Funciona. |
| Todo es urgente | Solo 1 urgente a la vez. Si hay dos, la jefatura decide cuál cede. |
| Tarjetas gigantes que viven semanas en curso | Si supera el p85, se parte en el diario. |
| Se fuerza el WIP cada semana | Es un problema de prioridades, no del límite: va a la revisión de portafolio. |
| «Bloqueado» como sitio cómodo donde aparcar | Escalado a 48 h y a 5 días; a los 15 días, decisión en portafolio. |
| El diario se convierte en «qué hice ayer» | El facilitador recorre el tablero de derecha a izquierda y solo pregunta por bloqueos y edad. |
| Se piden informes aparte del tablero | Se responde con el enlace al Resumen semanal. Si falta un dato, se añade al módulo, no a un Excel. |
