# 06 — Niveles de gestión y riesgos

> **Regla:** solo los usuarios de TorsaCore pueden ser dueños de una tarjeta,
> líderes de proyecto o responsables de un riesgo.

Tres niveles de gestión, cada uno con su propio ritmo y sus propias decisiones.
Ninguno valida el trabajo del de abajo: cada nivel decide lo suyo y **escala lo
que no puede resolver**.

| Nivel | Quién | Gestiona | Decide | Escala a |
|---|---|---|---|---|
| **Portafolio** | Jefatura | Qué proyectos van primero, la capacidad del equipo, los riesgos altos | Prioridad entre proyectos, qué se para, compromisos nuevos con clientes, recursos | Dirección |
| **Proyecto y riesgos** | N3 · líder de proyecto | Plan, tarjetas Listas, riesgos y relación con el cliente de sus proyectos | Cómo se ejecuta el proyecto, fechas internas, respuesta a cada riesgo | Jefatura: conflictos de prioridad o de personas, riesgos altos, cambios con el cliente |
| **Ejecución autónoma** | N2 | Sus tarjetas: diagnosticar, implementar, validar | Cómo resolver su tarjeta | Líder N3: bloqueos, dudas de alcance |
| **Ejecución guiada** | N1 | Tarjetas bien definidas: instalar, preparar, enviar, inventariar | Cómo ejecutar dentro de lo definido | N2 en lo técnico; líder N3 en bloqueos |

## Qué cambia en las tarjetas

Cada tarjeta lleva un **nivel mínimo**:

| Nivel | Tipo de tarjeta | Ejemplos |
|---|---|---|
| **N3** | Decisión, cliente, definición de estándares, cierre formal | Acordar alcance con el cliente, decidir una propuesta técnica, redactar el informe final |
| **N2** | Diagnóstico, implementación, validación | Analizar una causa raíz, implementar un cambio, validar en sitio |
| **N1** | Ejecución con evidencia clara | Inventariar, preparar material, enviar, instalar |

Regla: **N1 toma tarjetas N1; N2 toma N1 y N2; N3 prepara y toma N3**. Tomar
una de más nivel es posible avisando al líder del proyecto: el tablero lo pregunta.

## Ritmo por nivel

| Nivel | Cada día | Cada semana | Cada mes |
|---|---|---|---|
| **Jefatura** | 5 min: desbloquear y mirar riesgos altos | Lunes, 20 min con los N3 si algo está en rojo | 45 min con los N3: revisión de portafolio |
| **N3** | Sus tarjetas | 30 min: preparar Listas, revisar sus riesgos, reunión con el cliente | Revisión de portafolio con jefatura |
| **N2 / N1** | 5 min: mover sus tarjetas, tomar libres | — | — |

## Gestión de riesgos ligera

Un riesgo es algo que **todavía no ha pasado** y que, si pasa, mueve un hito o el
acta. Lo que ya ha pasado no es un riesgo: es una tarjeta o un bloqueo.

### Cómo se escribe

**Causa → lo que puede pasar → consecuencia.**

> «Si el envío se retiene en aduana, la visita de cierre se retrasa y el acta también.»

### Cómo se valora

| | 1 | 2 | 3 |
|---|---|---|---|
| **Probabilidad** | Poco probable | Posible | Probable |
| **Impacto** | Días, sin afectar al cliente | Mueve un hito | Mueve el acta o afecta a seguridad o contrato |

**Exposición = probabilidad × impacto.**

| Exposición | Nivel | Qué pasa |
|---|---|---|
| 6–9 | **Alto** | Sube solo a la vista de jefatura y a la Cartera |
| 3–4 | Medio | Lo gestiona el líder N3 |
| 1–2 | Bajo | Se vigila |

### Qué se registra

| Campo | Regla |
|---|---|
| **Riesgo** | Causa → evento → consecuencia |
| **Probabilidad e impacto** | De 1 a 3 |
| **Respuesta** | Evitar, mitigar, transferir o aceptar |
| **Acción** | Concreta. Si hace falta trabajo, se crea una tarjeta y se enlaza |
| **Disparador** | La señal observable de que está pasando, con fecha si se puede |
| **Dueño** | Por defecto, el líder N3 del proyecto |
| **Estado** | Abierto, vigilando, materializado, cerrado |
| **Revisado** | Se actualiza al guardarlo; más de 10 días hábiles sin revisar lo marca |

### Ritmo

- **N3**: 10 minutos a la semana revisando los riesgos de sus proyectos.
- **Jefatura**: ve los altos cada día en su vista y los trata en la revisión mensual.
- **Al arrancar un proyecto** y **al empezar su cierre**, el líder N3 hace una lista
  inicial de 5 a 10 riesgos. No más: un registro largo no se revisa.

### Cuando un riesgo se materializa

Pasa a *materializado* y se convierte en trabajo: una tarjeta (urgente si afecta
al cliente) o un bloqueo sobre la tarjeta afectada. El riesgo se cierra cuando
esa tarjeta se cierra.
