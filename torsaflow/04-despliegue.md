# 04 — Plan de despliegue (90 días)

El marco se introduce de forma evolutiva (principio del Kanban Method: *empieza
por lo que haces ahora*). Se apoya en lo que ya funciona en TorsaCore (Charter y
Plan de Trabajo) y en Craft (Biblioteca técnica). No se reorganiza a nadie ni se
cambian cargos.

## Fase 0 — Preparar (semanas 1–2)

| Acción | Responsable | Resultado |
|---|---|---|
| **Completar Charters activos**: responsable, fecha de inicio y de fin, criterios de éxito; pasarlos a *Aprobado* o archivarlos | Dueños de proyecto | Índice 9 «Charters completos» medible desde el día 1 |
| **Completar Planes de Trabajo**: cada fase con fechas y cada rol asignado (fuera los «A definir» / «A asignar») | Dueños de proyecto | Planes ejecutables |
| **Limpieza de la Biblioteca**: atacar los pendientes de «00 - Índice documental» (duplicados, páginas de prueba, control documental incompleto, «Pendiente de confirmar» en autor/responsable/aprobador) | Portafolio + responsables de portafolio | Línea base de los índices 11 y 12 |
| Desplegar el módulo Flujo en TorsaCore con los enganches de Charter y Plan | Desarrollo TorsaCore | Módulo operativo |
| Generar las tarjetas desde los Planes aprobados y añadir el trabajo interno en curso (proyecto «Interno») | Portafolio + PMs | Tablero con el trabajo real |
| Presentar el marco al equipo: 30 min, solo los 6 principios y las 5 cadencias | Portafolio | Todos saben qué cambia el lunes |

## Fase 1 — Piloto (semanas 3–4)

- Un portafolio o subequipo (4–6 personas) trabaja solo con el tablero y los avisos automáticos.
- El responsable de portafolio prepara la reunión del lunes con el *Resumen semanal* de TorsaCore.
- Al final: retro de 30 min con el piloto, ajustar límites de WIP si hace falta.

## Fase 2 — Todo el departamento (semanas 5–7)

- Todo el departamento en el tablero. Cualquier otra lista de seguimiento deja de mantenerse.
- Arranca la revisión del lunes (20 min, solo si el resumen marca algo).
- Se invita a Comercial y Desarrollo a la reunión de bloqueos externos.
- Ningún proyecto nuevo genera tarjetas sin Charter aprobado y Plan completo.

## Fase 3 — Medir y mejorar (semanas 8–13)

- Primera revisión de portafolio con métricas reales (ya hay 6 semanas de histórico).
- Se sustituye el p85 provisional por el real.
- Las fechas a clientes se empiezan a dar con la previsión de TorsaCore (*«con un 85 % de confianza, en 4 semanas»*).
- Retrospectiva mensual: una mejora al proceso por mes.

## Criterios de éxito a 90 días

| Índice | Objetivo |
|---|---|
| Charters activos completos (aprobados, con responsable y fechas) | 100 % |
| Fases de Plan de Trabajo con fecha y responsable | 100 % |
| Higiene del tablero | ≥ 95 % |
| Personas por encima de 5 tarjetas activas | 0 |
| Tarjetas en Listo con 3+ semanas | 0 |
| Fiabilidad de compromiso | ≥ 80 % |
| Bloqueos con más de 5 días hábiles sin escalar | 0 |
| Documentos de la Biblioteca con autor/responsable/aprobador con nombre | ≥ 95 % |
| Tiempo de reuniones por persona y semana | < 1 h |

## Antipatrones a vigilar

| Señal | Qué hacer |
|---|---|
| Charter aprobado con fechas «—» o Plan con todo «A definir» | No genera tarjetas Listas: se queda en Backlog hasta que el responsable de portafolio lo prepare. |
| El tablero se actualiza el viernes «para la reunión» | Sin tablero al día no llegan los avisos ni se ven las tarjetas libres: el coste lo paga el propio equipo. Se habla una vez, en la mirada mensual. |
| Todo es urgente | Solo 1 urgente a la vez. Si hay dos, el responsable de portafolio decide cuál cede. |
| Tarjetas gigantes que viven semanas en curso | Si supera el p85, su dueño la parte. |
| Se fuerza el WIP cada semana | Es un problema de prioridades, no del límite: va a la revisión de portafolio. |
| «Bloqueado» como sitio cómodo donde aparcar | Escalado a 48 h y a 5 días; a los 15 días, decisión en portafolio. |
| Todo se queda esperando a que alguien lo apruebe | No hay aprobadores internos: el dueño cierra con evidencia; si algo falla, se reabre. |
| Se piden informes aparte del tablero | Se responde con el enlace al Resumen semanal. Si falta un dato, se añade al módulo, no a otra hoja. |
