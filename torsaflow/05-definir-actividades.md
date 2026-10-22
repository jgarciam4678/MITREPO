# 05 — Cómo definir una actividad

Una actividad está bien definida cuando **cualquiera del equipo puede tomarla
sin preguntar nada y cualquiera puede comprobar que está hecha sin haber
estado allí**. Ese es el único criterio. Todo lo demás son pasos para llegar a él.

Definir es trabajo del responsable de portafolio: es la parte de «buscar y preparar los
problemas». Resolverlos es trabajo del dueño.

## De un pendiente a una tarjeta: 7 pasos

### 1. Copia el pendiente tal como llegó

La frase de la reunión, del correo o del cliente, sin interpretar. Va en
«Incluye» o en el historial: es el origen y evita discusiones después.

> «Concentradores: se están produciendo bloqueos, fallos de encendido o
> situaciones en las que desconectan el sistema. Existe un ticket abierto con Soporte.»

### 2. Escribe el resultado, no la tarea

¿Qué tiene que ser verdad cuando esto esté resuelto? Es el campo **Para qué**.
Un resultado se observa; una tarea solo se hace.

| Tarea (no) | Resultado (sí) |
|---|---|
| Revisar los concentradores | Ningún concentrador se bloquea ni apaga el sistema |
| Mirar el modo limpieza | Vehículos a distinta cota no generan alertas de mismo nivel |
| Seguimiento de alertas | Las alertas de LDV bajan sin perder detección |

### 3. Parte en pasos que una persona termina en 2 semanas

Cada tarjeta debe caber en **10 días hábiles** y producir algo comprobable. Si
no se sabe cómo resolverlo, la primera tarjeta es para **averiguarlo**, con
plazo cerrado. El patrón más habitual:

```
Diagnosticar / Decidir  ──▶  Corregir / Implementar  ──▶  Verificar en sitio
    (qué pasa)                  (cambiarlo)                (comprobar que funciona)
```

Ejemplo: los concentradores se convierten en *Analizar la causa raíz* (10 d) →
*Aplicar la corrección* (5 d) → se verifica en el *periodo de estabilidad*.

### 4. Título: verbo en infinitivo + qué + dónde

| Verbos que terminan | Verbos que no terminan nunca |
|---|---|
| Diagnosticar, Decidir, Definir, Fabricar, Preparar, Enviar, Instalar, Corregir, Implementar, Desplegar, Verificar, Validar, Redactar, Firmar | Revisar, Gestionar, Hacer seguimiento, Apoyar, Ver, Coordinar, Mirar |

Si solo encaja un verbo de la derecha, aún no sabes qué se entrega: vuelve al paso 2.
*«Revisar la interacción cargador–camión»* pasa a *«Revisar la interacción
cargador frontal–camión **y proponer ajuste**»*: ahora hay algo que entregar.

### 5. Evidencia de hecho: algo que se pueda enlazar

La prueba de que está hecha, sin validador. Test: **¿alguien que no estuvo podría
decir sí o no mirando solo el enlace?**

| Débil | Fuerte |
|---|---|
| Concentradores corregidos | Corrección aplicada en toda la flota afectada (registro de cambios por vehículo) |
| Pantallas cambiadas | Lista de vehículos con foto de la pantalla gris instalada |
| Cliente informado | Correo enviado al cliente con el esquema de criticidad y su respuesta |
| Documento hecho | Informe publicado en la Biblioteca técnica con código ES-CMS-INF-… |

Tipos de evidencia válidos: documento con código en la Biblioteca técnica,
captura o exportación de la plataforma, fotos de instalación, registro de
cambios, correo con el cliente, acta firmada.

### 6. Dependencias y fecha

- **Depende de**: solo las tarjetas cuyo *resultado* necesitas para empezar. No
  personas con las que hablarás.
- **Duración** en días hábiles, por tallas, no en horas:

  | Talla | Días hábiles | Ejemplo |
  |---|---|---|
  | S | 1–2 | Inventariar pantallas, instalar un cable |
  | M | 3–5 | Diagnosticar en remoto, ajustar una configuración |
  | L | 6–10 | Fabricar un lote, implementar y probar un cambio de software |
  | > 10 | — | Se parte en dos tarjetas |

- **Inicio** = cuando termina su última dependencia. **Fin** = inicio + duración.
- **Fecha fija** solo si hay un compromiso con alguien de fuera.

### 7. Perfil, dueño y prioridad

- **Perfil** siempre (Soporte, Producción, Campo…): dice quién puede tomarla.
- **Dueño** solo si la tarjeta necesita a una persona concreta. Si no, queda **libre**.
- **Prioridad**:

  | | Cuándo |
  |---|---|
  | **P1** | Bloquea el cierre, afecta a la seguridad o a un compromiso con el cliente |
  | **P2** | Necesaria para cerrar, sin urgencia |
  | **P3** | Mejora: puede quedar para después del cierre |

## La ficha

| Campo | Pregunta que responde | Regla |
|---|---|---|
| **Título** | ¿Qué se hace? | Verbo en infinitivo + qué + dónde |
| **Para qué** | ¿Qué resultado buscamos? | Algo observable, no una tarea |
| **Incluye** | ¿Qué entra exactamente? | El pendiente original y los límites |
| **Perfil / dueño** | ¿Quién puede tomarla? | Perfil siempre; nombre solo si hace falta |
| **Prioridad** | ¿Cuánto importa? | P1 / P2 / P3 según la tabla |
| **Depende de** | ¿Qué resultado necesito antes? | Solo tarjetas, no personas |
| **Inicio / fin** | ¿Cuándo? | Por tallas; > 10 días se parte |
| **Evidencia de hecho** | ¿Cómo se demuestra? | Enlazable y binaria |
| **Entregable** | ¿Qué queda en la Biblioteca? | Código si es un documento |

## Comprobación final (la hace el editor del tablero)

1. El título empieza por un verbo que termina.
2. Tiene «Para qué».
3. Tiene evidencia de hecho.
4. Dura 10 días hábiles o menos.
5. Tiene perfil o dueño.
6. Si es de fecha fija, tiene fecha de fin.

Si las seis están en verde, la tarjeta puede pasar a **Listo**.
