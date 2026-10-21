"""Flujo: tablero de trabajo del departamento (marco TorsaFlow).

Router FastAPI de referencia para integrar en TorsaCore. Es la capa de ejecución
que falta entre el Project Charter / Plan de Trabajo (planificación) y la
Biblioteca técnica en Craft (entregables):

    Charter aprobado → Plan de Trabajo → tarjetas (fases y tareas) → documento en la Biblioteca

Guarda proyectos, tarjetas y el historial de eventos en SQLite; las métricas se
calculan a partir del historial, nunca se introducen a mano.

Integración en main.py:

    from app.flujo import router as flujo_router
    app.include_router(flujo_router)

Puntos a adaptar a TorsaCore (marcados con ADAPTAR):
- `usuario_actual`: sustituir por la dependencia de autenticación de TorsaCore.
- `conexion`: si TorsaCore usa otra base de datos u ORM, sustituir el acceso.
- `FLUJO_DB`: ruta del fichero SQLite (variable de entorno).
"""

from __future__ import annotations

import math
import os
import random
import sqlite3
from datetime import date, datetime, timedelta, timezone
from typing import Iterator, Literal, Optional

from fastapi import APIRouter, Depends, Header, HTTPException, Query
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/flujo", tags=["flujo"])

# --- Políticas del marco (01-comportamiento.md) ----------------------------

ACTIVOS = ("en_curso", "en_validacion")

LIMITE_WIP = {"en_curso": 3, "en_validacion": 2}  # por persona
LIMITE_WIP_TOTAL = sum(LIMITE_WIP.values())
LIMITE_URGENTES = 1  # en todo el departamento
P85_PROVISIONAL = 10  # días hábiles, hasta tener histórico
DIAS_SIN_MOVIMIENTO = 10  # días hábiles para revisión obligatoria
SEMANAS_EN_LISTO = 3  # tras este tiempo sin empezar, vuelve al backlog

TRANSICIONES = {
    "backlog": {"listo", "descartado"},
    "listo": {"en_curso", "backlog", "descartado"},
    "en_curso": {"en_validacion", "hecho", "listo", "backlog", "descartado"},
    "en_validacion": {"hecho", "en_curso", "descartado"},
    "hecho": {"en_curso"},  # reapertura
    "descartado": {"backlog"},
}

Estado = Literal["backlog", "listo", "en_curso", "en_validacion", "hecho", "descartado"]
Clase = Literal["urgente", "fecha_fija", "estandar", "mejora"]

# --- Infraestructura -------------------------------------------------------

ESQUEMA = """
CREATE TABLE IF NOT EXISTS flujo_proyectos (
    id              INTEGER PRIMARY KEY,
    codigo          TEXT NOT NULL UNIQUE,   -- código del Project Charter, p. ej. ES-SAF-DOC-PC-...
    nombre          TEXT NOT NULL,
    cliente         TEXT,
    portafolio      TEXT,                   -- CMS, SAF, AO, NEPTUNE, INFRA, GLB...
    responsable     TEXT,
    estado_charter  TEXT,                   -- Borrador, Revisión, Aprobado
    fecha_inicio    TEXT,
    fecha_fin       TEXT,
    activo          INTEGER NOT NULL DEFAULT 1
);
CREATE TABLE IF NOT EXISTS flujo_tarjetas (
    id                  INTEGER PRIMARY KEY,
    titulo              TEXT NOT NULL,
    responsable         TEXT,
    solicitante         TEXT,
    proyecto_id         INTEGER REFERENCES flujo_proyectos(id),
    clase               TEXT NOT NULL DEFAULT 'estandar',
    estado              TEXT NOT NULL DEFAULT 'backlog',
    fecha_compromiso    TEXT,
    enlace_entregable   TEXT,
    aceptada_por        TEXT,
    bloqueada           INTEGER NOT NULL DEFAULT 0,
    bloqueo_motivo      TEXT,
    bloqueo_depende_de  TEXT,
    bloqueo_desde       TEXT,
    bloqueo_respuesta   TEXT,
    fase                TEXT,   -- fase del Plan de Trabajo de la que sale
    documento_codigo    TEXT,   -- código del entregable en la Biblioteca técnica
    creada_en           TEXT NOT NULL,
    lista_en            TEXT,
    iniciada_en         TEXT,
    terminada_en        TEXT,
    actualizada_en      TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS flujo_eventos (
    id          INTEGER PRIMARY KEY,
    tarjeta_id  INTEGER NOT NULL REFERENCES flujo_tarjetas(id),
    momento     TEXT NOT NULL,
    usuario     TEXT,
    tipo        TEXT NOT NULL,
    desde       TEXT,
    hacia       TEXT,
    detalle     TEXT
);
CREATE INDEX IF NOT EXISTS ix_flujo_tarjetas_estado ON flujo_tarjetas(estado);
CREATE INDEX IF NOT EXISTS ix_flujo_eventos_tarjeta ON flujo_eventos(tarjeta_id);
"""


def conexion() -> Iterator[sqlite3.Connection]:
    """ADAPTAR: acceso a datos. Una conexión por petición."""
    con = sqlite3.connect(os.environ.get("FLUJO_DB", "flujo.db"))
    con.row_factory = sqlite3.Row
    con.executescript(ESQUEMA)
    try:
        yield con
        con.commit()
    finally:
        con.close()


def usuario_actual(x_usuario: Optional[str] = Header(default=None)) -> str:
    """ADAPTAR: sustituir por la autenticación de TorsaCore."""
    return x_usuario or "anonimo"


def ahora() -> datetime:
    return datetime.now(timezone.utc)


def dias_habiles(desde: datetime | date, hasta: datetime | date) -> int:
    """Días laborables (lunes a viernes) entre dos fechas, sin contar la inicial."""
    a = desde.date() if isinstance(desde, datetime) else desde
    b = hasta.date() if isinstance(hasta, datetime) else hasta
    if b <= a:
        return 0
    semanas, resto = divmod((b - a).days, 7)
    total = semanas * 5
    for i in range(1, resto + 1):
        if (a + timedelta(days=i)).weekday() < 5:
            total += 1
    return total


def _iso(dt: datetime) -> str:
    return dt.isoformat(timespec="seconds")


def _dt(valor: Optional[str]) -> Optional[datetime]:
    return datetime.fromisoformat(valor) if valor else None


# --- Modelos ---------------------------------------------------------------


class ProyectoEntrada(BaseModel):
    codigo: str = Field(min_length=2)
    nombre: str = Field(min_length=1)
    cliente: Optional[str] = None
    portafolio: Optional[str] = None
    responsable: Optional[str] = None
    estado_charter: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    activo: bool = True


class FasePlan(BaseModel):
    fase: str = Field(min_length=2)
    actividad: Optional[str] = None
    inicio: Optional[str] = None  # admite «A definir»
    fin: Optional[str] = None
    responsable: Optional[str] = None  # admite «A asignar»


class PlanDeTrabajo(BaseModel):
    fases: list[FasePlan]


class TarjetaEntrada(BaseModel):
    titulo: str = Field(min_length=3)
    responsable: Optional[str] = None
    solicitante: Optional[str] = None
    proyecto_id: Optional[int] = None
    clase: Clase = "estandar"
    estado: Literal["backlog", "listo"] = "backlog"
    fecha_compromiso: Optional[date] = None
    fase: Optional[str] = None


class TarjetaCambios(BaseModel):
    titulo: Optional[str] = Field(default=None, min_length=3)
    responsable: Optional[str] = None
    solicitante: Optional[str] = None
    proyecto_id: Optional[int] = None
    clase: Optional[Clase] = None
    fecha_compromiso: Optional[date] = None
    enlace_entregable: Optional[str] = None
    documento_codigo: Optional[str] = None


class Movimiento(BaseModel):
    estado: Estado
    motivo: Optional[str] = None
    # Saltarse un límite de WIP es posible, pero queda registrado con su porqué.
    justificacion_wip: Optional[str] = None


class Bloqueo(BaseModel):
    motivo: str = Field(min_length=3)
    depende_de: str = Field(min_length=2)
    respuesta_esperada: Optional[date] = None


class Aceptacion(BaseModel):
    por: str = Field(min_length=2)


# --- Reglas ----------------------------------------------------------------


def faltas_listo(t: dict, para_empezar: bool = False) -> list[str]:
    """Definición de Listo. Una tarjeta Lista puede no tener dueño: la toma quien pueda."""
    faltas = []
    if para_empezar and not t.get("responsable"):
        faltas.append("Falta el dueño: tómala tú o asígnala a alguien.")
    elif t.get("responsable") and ("/" in t["responsable"] or "," in t["responsable"]):
        faltas.append("El dueño debe ser una sola persona.")
    if not t.get("proyecto_id"):
        faltas.append("Falta el proyecto (usa «Interno» si no tiene Charter).")
    if t.get("clase") == "fecha_fija" and not t.get("fecha_compromiso"):
        faltas.append("Una tarjeta de fecha fija necesita fecha de compromiso.")
    return faltas


def faltas_hecho(t: dict) -> list[str]:
    """Definición de Hecho: la evidencia, no un validador. El dueño declara Hecho."""
    faltas = []
    if not t.get("enlace_entregable") and not t.get("documento_codigo"):
        faltas.append("Enlaza la evidencia: código en la Biblioteca técnica o enlace de Craft.")
    return faltas


def _wip(con: sqlite3.Connection, responsable: str, estado: str, excluir: int) -> int:
    fila = con.execute(
        "SELECT COUNT(*) FROM flujo_tarjetas WHERE responsable=? AND estado=? AND id<>?",
        (responsable, estado, excluir),
    ).fetchone()
    return fila[0]


def _urgentes_activas(con: sqlite3.Connection, excluir: int) -> int:
    fila = con.execute(
        "SELECT COUNT(*) FROM flujo_tarjetas WHERE clase='urgente' AND id<>? "
        "AND estado IN ('en_curso','en_validacion')",
        (excluir,),
    ).fetchone()
    return fila[0]


# --- Acceso ----------------------------------------------------------------


def _tarjeta(con: sqlite3.Connection, tarjeta_id: int) -> dict:
    fila = con.execute("SELECT * FROM flujo_tarjetas WHERE id=?", (tarjeta_id,)).fetchone()
    if fila is None:
        raise HTTPException(404, "Tarjeta no encontrada")
    return dict(fila)


def _evento(con, tarjeta_id, momento, usuario, tipo, desde=None, hacia=None, detalle=None):
    con.execute(
        "INSERT INTO flujo_eventos (tarjeta_id, momento, usuario, tipo, desde, hacia, detalle) "
        "VALUES (?,?,?,?,?,?,?)",
        (tarjeta_id, _iso(momento), usuario, tipo, desde, hacia, detalle),
    )


def _con_semaforo(t: dict, momento: datetime, p85: int) -> dict:
    """Añade edad y semáforo a una tarjeta activa (02-metricas.md)."""
    t = dict(t)
    t["edad"] = None
    t["semaforo"] = None
    if t["estado"] in ACTIVOS and t.get("iniciada_en"):
        edad = dias_habiles(_dt(t["iniciada_en"]), momento)
        t["edad"] = edad
        t["semaforo"] = "verde" if edad <= p85 / 2 else "ambar" if edad <= p85 else "rojo"
    t["dias_bloqueada"] = dias_habiles(_dt(t["bloqueo_desde"]), momento) if t.get("bloqueo_desde") else None
    ultimo = _dt(t["actualizada_en"])
    t["sin_movimiento"] = (
        t["estado"] not in ("hecho", "descartado")
        and dias_habiles(ultimo, momento) >= DIAS_SIN_MOVIMIENTO
    )
    return t


# --- Proyectos -------------------------------------------------------------


@router.get("/proyectos")
def listar_proyectos(con: sqlite3.Connection = Depends(conexion)):
    return [dict(f) for f in con.execute("SELECT * FROM flujo_proyectos ORDER BY nombre")]


@router.put("/proyectos")
def guardar_proyecto(p: ProyectoEntrada, con: sqlite3.Connection = Depends(conexion)):
    """Alta o actualización por código de Charter. TorsaCore lo llama al guardar un Charter."""
    datos = p.model_dump()
    for campo in ("fecha_inicio", "fecha_fin"):
        datos[campo] = datos[campo].isoformat() if datos[campo] else None
    datos["activo"] = int(p.activo)
    columnas = ", ".join(datos)
    huecos = ", ".join("?" for _ in datos)
    cambios = ", ".join(f"{k}=excluded.{k}" for k in datos if k != "codigo")
    con.execute(
        f"INSERT INTO flujo_proyectos ({columnas}) VALUES ({huecos}) "
        f"ON CONFLICT(codigo) DO UPDATE SET {cambios}",
        tuple(datos.values()),
    )
    fila = con.execute("SELECT * FROM flujo_proyectos WHERE codigo=?", (p.codigo,)).fetchone()
    return dict(fila)


def _sin_definir(valor: Optional[str]) -> bool:
    return not valor or valor.strip().lower() in {"—", "-", "a definir", "a asignar", "pendiente de confirmar"}


@router.post("/proyectos/{proyecto_id}/plan")
def generar_desde_plan(
    proyecto_id: int,
    plan: PlanDeTrabajo,
    con: sqlite3.Connection = Depends(conexion),
    usuario: str = Depends(usuario_actual),
    momento: datetime = Depends(ahora),
):
    """Convierte las fases del Plan de Trabajo aprobado en tarjetas.

    Una tarjeta por fase. Si la fase tiene fecha de fin entra en Listo como
    «fecha fija», con o sin dueño; sin fecha («A definir») entra en Backlog.
    Es idempotente: no duplica fases.
    """
    if con.execute("SELECT 1 FROM flujo_proyectos WHERE id=?", (proyecto_id,)).fetchone() is None:
        raise HTTPException(404, "Proyecto no encontrado")
    existentes = {
        f[0] for f in con.execute(
            "SELECT fase FROM flujo_tarjetas WHERE proyecto_id=? AND fase IS NOT NULL", (proyecto_id,))
    }
    creadas, incompletas = [], []
    for f in plan.fases:
        if f.fase in existentes:
            continue
        responsable = None if _sin_definir(f.responsable) else f.responsable.strip()
        fin = None
        if not _sin_definir(f.fin):
            try:
                fin = date.fromisoformat(f.fin.strip()).isoformat()
            except ValueError:
                fin = None
        completa = bool(fin)  # sin dueño también es Lista: la toma quien pueda
        estado = "listo" if completa else "backlog"
        titulo = f"{f.fase}: {f.actividad}" if f.actividad else f.fase
        cur = con.execute(
            "INSERT INTO flujo_tarjetas (titulo, responsable, solicitante, proyecto_id, clase, estado, "
            "fecha_compromiso, fase, creada_en, lista_en, actualizada_en) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (titulo[:300], responsable, usuario, proyecto_id, "fecha_fija" if fin else "estandar",
             estado, fin, f.fase, _iso(momento), _iso(momento) if completa else None, _iso(momento)),
        )
        _evento(con, cur.lastrowid, momento, usuario, "creada", hacia=estado, detalle="plan de trabajo")
        creadas.append(cur.lastrowid)
        if not completa:
            incompletas.append(f.fase)
    return {"creadas": len(creadas), "ids": creadas, "fases_sin_fecha": incompletas}


# --- Tarjetas --------------------------------------------------------------


@router.get("/tarjetas")
def listar_tarjetas(
    responsable: Optional[str] = None,
    proyecto_id: Optional[int] = None,
    estado: Optional[Estado] = None,
    incluir_cerradas: bool = False,
    con: sqlite3.Connection = Depends(conexion),
    momento: datetime = Depends(ahora),
):
    sql = "SELECT * FROM flujo_tarjetas WHERE 1=1"
    params: list = []
    if responsable:
        sql += " AND responsable=?"
        params.append(responsable)
    if proyecto_id:
        sql += " AND proyecto_id=?"
        params.append(proyecto_id)
    if estado:
        sql += " AND estado=?"
        params.append(estado)
    elif not incluir_cerradas:
        sql += " AND estado NOT IN ('hecho','descartado')"
    sql += " ORDER BY actualizada_en DESC"
    p85 = _p85(con, momento)
    return [_con_semaforo(dict(f), momento, p85) for f in con.execute(sql, params)]


@router.post("/tarjetas", status_code=201)
def crear_tarjeta(
    t: TarjetaEntrada,
    con: sqlite3.Connection = Depends(conexion),
    usuario: str = Depends(usuario_actual),
    momento: datetime = Depends(ahora),
):
    datos = t.model_dump()
    if t.estado == "listo" and (faltas := faltas_listo(datos)):
        raise HTTPException(409, {"reglas": faltas})
    cur = con.execute(
        "INSERT INTO flujo_tarjetas (titulo, responsable, solicitante, proyecto_id, clase, "
        "estado, fecha_compromiso, fase, creada_en, lista_en, actualizada_en) "
        "VALUES (?,?,?,?,?,?,?,?,?,?,?)",
        (
            t.titulo.strip(),
            t.responsable,
            t.solicitante or usuario,
            t.proyecto_id,
            t.clase,
            t.estado,
            t.fecha_compromiso.isoformat() if t.fecha_compromiso else None,
            t.fase,
            _iso(momento),
            _iso(momento) if t.estado == "listo" else None,
            _iso(momento),
        ),
    )
    _evento(con, cur.lastrowid, momento, usuario, "creada", hacia=t.estado)
    return _tarjeta(con, cur.lastrowid)


@router.patch("/tarjetas/{tarjeta_id}")
def editar_tarjeta(
    tarjeta_id: int,
    cambios: TarjetaCambios,
    con: sqlite3.Connection = Depends(conexion),
    usuario: str = Depends(usuario_actual),
    momento: datetime = Depends(ahora),
):
    t = _tarjeta(con, tarjeta_id)
    valores = cambios.model_dump(exclude_unset=True)
    if not valores:
        return t
    if "fecha_compromiso" in valores and valores["fecha_compromiso"]:
        valores["fecha_compromiso"] = valores["fecha_compromiso"].isoformat()
    columnas = ", ".join(f"{k}=?" for k in valores)
    con.execute(
        f"UPDATE flujo_tarjetas SET {columnas}, actualizada_en=? WHERE id=?",
        (*valores.values(), _iso(momento), tarjeta_id),
    )
    if "fecha_compromiso" in valores and valores["fecha_compromiso"] != t["fecha_compromiso"]:
        # Las replanificaciones quedan a la vista: afectan a la fiabilidad.
        _evento(con, tarjeta_id, momento, usuario, "replanificada",
                desde=t["fecha_compromiso"], hacia=valores["fecha_compromiso"])
    else:
        _evento(con, tarjeta_id, momento, usuario, "editada", detalle=", ".join(valores))
    return _tarjeta(con, tarjeta_id)


@router.post("/tarjetas/{tarjeta_id}/mover")
def mover_tarjeta(
    tarjeta_id: int,
    m: Movimiento,
    con: sqlite3.Connection = Depends(conexion),
    usuario: str = Depends(usuario_actual),
    momento: datetime = Depends(ahora),
):
    t = _tarjeta(con, tarjeta_id)
    origen, destino = t["estado"], m.estado
    if destino == origen:
        return t
    if destino not in TRANSICIONES[origen]:
        raise HTTPException(409, {"reglas": [f"No se puede pasar de {origen} a {destino}."]})

    faltas: list[str] = []
    if destino == "descartado" and not m.motivo:
        faltas.append("Indica en una línea por qué se descarta.")
    if destino in ("listo", "en_curso"):
        faltas += faltas_listo(t, para_empezar=destino == "en_curso")
    if destino == "hecho":
        faltas += faltas_hecho(t)
    if faltas:
        raise HTTPException(409, {"reglas": faltas})

    avisos: list[str] = []
    if destino in LIMITE_WIP and t["responsable"]:
        en_destino = _wip(con, t["responsable"], destino, tarjeta_id)
        if en_destino >= LIMITE_WIP[destino]:
            avisos.append(
                f"{t['responsable']} ya tiene {en_destino} tarjetas en {destino} "
                f"(límite {LIMITE_WIP[destino]}). Termina o bloquea una antes de empezar otra."
            )
    if destino in ACTIVOS and t["clase"] == "urgente" and _urgentes_activas(con, tarjeta_id) >= LIMITE_URGENTES:
        avisos.append("Ya hay una tarjeta urgente en curso en el departamento.")
    if avisos and not m.justificacion_wip:
        raise HTTPException(409, {"reglas": avisos, "se_puede_forzar": True})

    sets = {"estado": destino, "actualizada_en": _iso(momento)}
    if destino == "listo" and not t["lista_en"]:
        sets["lista_en"] = _iso(momento)
    if destino == "en_curso" and not t["iniciada_en"]:
        sets["iniciada_en"] = _iso(momento)
    if destino == "hecho":
        sets["terminada_en"] = _iso(momento)
        if not t["iniciada_en"]:
            sets["iniciada_en"] = _iso(momento)
    if origen == "hecho":  # reapertura
        sets["terminada_en"] = None
    if destino in ("hecho", "descartado") and t["bloqueada"]:
        sets.update(bloqueada=0, bloqueo_motivo=None, bloqueo_depende_de=None,
                    bloqueo_desde=None, bloqueo_respuesta=None)
    columnas = ", ".join(f"{k}=?" for k in sets)
    con.execute(f"UPDATE flujo_tarjetas SET {columnas} WHERE id=?", (*sets.values(), tarjeta_id))
    _evento(con, tarjeta_id, momento, usuario, "movida", origen, destino, m.motivo)
    if avisos:
        _evento(con, tarjeta_id, momento, usuario, "wip_forzado", detalle=m.justificacion_wip)
    return _tarjeta(con, tarjeta_id)


class Toma(BaseModel):
    justificacion_wip: Optional[str] = None


@router.post("/tarjetas/{tarjeta_id}/tomar")
def tomar_tarjeta(
    tarjeta_id: int,
    toma: Toma = Toma(),
    con: sqlite3.Connection = Depends(conexion),
    usuario: str = Depends(usuario_actual),
    momento: datetime = Depends(ahora),
):
    """Autoasignación: quien tiene capacidad toma una tarjeta Lista y la empieza."""
    t = _tarjeta(con, tarjeta_id)
    if t["responsable"] and t["responsable"] != usuario:
        raise HTTPException(409, {"reglas": [f"La tarjeta ya es de {t['responsable']}."]})
    if t["estado"] != "listo":
        raise HTTPException(409, {"reglas": ["Solo se toman tarjetas en Listo."]})
    if not t["responsable"]:
        con.execute("UPDATE flujo_tarjetas SET responsable=? WHERE id=?", (usuario, tarjeta_id))
        _evento(con, tarjeta_id, momento, usuario, "tomada")
    return mover_tarjeta(tarjeta_id, Movimiento(estado="en_curso", justificacion_wip=toma.justificacion_wip),
                         con, usuario, momento)


@router.post("/tarjetas/{tarjeta_id}/bloquear")
def bloquear_tarjeta(
    tarjeta_id: int,
    b: Bloqueo,
    con: sqlite3.Connection = Depends(conexion),
    usuario: str = Depends(usuario_actual),
    momento: datetime = Depends(ahora),
):
    t = _tarjeta(con, tarjeta_id)
    if t["estado"] in ("hecho", "descartado"):
        raise HTTPException(409, {"reglas": ["Una tarjeta cerrada no se puede bloquear."]})
    con.execute(
        "UPDATE flujo_tarjetas SET bloqueada=1, bloqueo_motivo=?, bloqueo_depende_de=?, "
        "bloqueo_desde=COALESCE(bloqueo_desde, ?), bloqueo_respuesta=?, actualizada_en=? WHERE id=?",
        (b.motivo, b.depende_de, _iso(momento),
         b.respuesta_esperada.isoformat() if b.respuesta_esperada else None,
         _iso(momento), tarjeta_id),
    )
    _evento(con, tarjeta_id, momento, usuario, "bloqueada", detalle=f"{b.depende_de}: {b.motivo}")
    return _tarjeta(con, tarjeta_id)


@router.post("/tarjetas/{tarjeta_id}/desbloquear")
def desbloquear_tarjeta(
    tarjeta_id: int,
    con: sqlite3.Connection = Depends(conexion),
    usuario: str = Depends(usuario_actual),
    momento: datetime = Depends(ahora),
):
    t = _tarjeta(con, tarjeta_id)
    if not t["bloqueada"]:
        return t
    dias = dias_habiles(_dt(t["bloqueo_desde"]), momento)
    con.execute(
        "UPDATE flujo_tarjetas SET bloqueada=0, bloqueo_motivo=NULL, bloqueo_depende_de=NULL, "
        "bloqueo_desde=NULL, bloqueo_respuesta=NULL, actualizada_en=? WHERE id=?",
        (_iso(momento), tarjeta_id),
    )
    _evento(con, tarjeta_id, momento, usuario, "desbloqueada", detalle=str(dias))
    return _tarjeta(con, tarjeta_id)


@router.post("/tarjetas/{tarjeta_id}/aceptar")
def aceptar_tarjeta(
    tarjeta_id: int,
    a: Aceptacion,
    con: sqlite3.Connection = Depends(conexion),
    usuario: str = Depends(usuario_actual),
    momento: datetime = Depends(ahora),
):
    _tarjeta(con, tarjeta_id)
    con.execute(
        "UPDATE flujo_tarjetas SET aceptada_por=?, actualizada_en=? WHERE id=?",
        (a.por, _iso(momento), tarjeta_id),
    )
    _evento(con, tarjeta_id, momento, usuario, "aceptada", detalle=a.por)
    return _tarjeta(con, tarjeta_id)


@router.get("/tarjetas/{tarjeta_id}/historial")
def historial_tarjeta(tarjeta_id: int, con: sqlite3.Connection = Depends(conexion)):
    _tarjeta(con, tarjeta_id)
    return [dict(f) for f in con.execute(
        "SELECT * FROM flujo_eventos WHERE tarjeta_id=? ORDER BY momento, id", (tarjeta_id,)
    )]


# --- Métricas (02-metricas.md) ---------------------------------------------


def _percentil(valores: list[float], p: float) -> Optional[float]:
    if not valores:
        return None
    orden = sorted(valores)
    k = max(0, min(len(orden) - 1, math.ceil(p / 100 * len(orden)) - 1))  # nearest-rank
    return orden[k]


def _cycle_times(con: sqlite3.Connection, desde: datetime) -> list[int]:
    filas = con.execute(
        "SELECT iniciada_en, terminada_en FROM flujo_tarjetas "
        "WHERE estado='hecho' AND terminada_en>=?",
        (_iso(desde),),
    )
    return [dias_habiles(_dt(f["iniciada_en"]), _dt(f["terminada_en"])) for f in filas]


def _p85(con: sqlite3.Connection, momento: datetime) -> int:
    tiempos = _cycle_times(con, momento - timedelta(weeks=12))
    if len(tiempos) < 10:  # sin histórico suficiente
        return P85_PROVISIONAL
    return max(1, int(_percentil(tiempos, 85)))


def _throughput_semanal(con: sqlite3.Connection, momento: datetime, semanas: int) -> list[int]:
    lunes = (momento - timedelta(days=momento.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
    inicio = lunes - timedelta(weeks=semanas - 1)
    cuentas = [0] * semanas
    for f in con.execute(
        "SELECT terminada_en FROM flujo_tarjetas WHERE estado='hecho' AND terminada_en>=?",
        (_iso(inicio),),
    ):
        i = (_dt(f["terminada_en"]) - inicio).days // 7
        if 0 <= i < semanas:
            cuentas[i] += 1
    return cuentas


def _higiene_proyectos(con: sqlite3.Connection) -> dict:
    """Charters activos listos para ejecutarse: aprobados, con responsable y fechas."""
    activos = [dict(f) for f in con.execute(
        "SELECT * FROM flujo_proyectos WHERE activo=1 AND codigo<>'INTERNO'")]
    completos = [
        p for p in activos
        if (p["estado_charter"] or "").lower() == "aprobado"
        and not _sin_definir(p["responsable"]) and p["fecha_inicio"] and p["fecha_fin"]
    ]
    return {
        "activos": len(activos),
        "completos": len(completos),
        "pct": round(100 * len(completos) / len(activos), 1) if activos else None,
        "incompletos": [p["codigo"] for p in activos if p not in completos],
    }


@router.get("/metricas")
def metricas(
    semanas: int = Query(12, ge=1, le=52),
    con: sqlite3.Connection = Depends(conexion),
    momento: datetime = Depends(ahora),
):
    desde = momento - timedelta(weeks=semanas)
    tiempos = _cycle_times(con, desde)
    p85 = _p85(con, momento)

    activas = [dict(f) for f in con.execute(
        "SELECT * FROM flujo_tarjetas WHERE estado IN ('en_curso','en_validacion')"
    )]
    abiertas = [dict(f) for f in con.execute(
        "SELECT * FROM flujo_tarjetas WHERE estado NOT IN ('hecho','descartado','backlog')"
    )]

    wip: dict[str, int] = {}
    for t in activas:
        clave = t["responsable"] or "(sin responsable)"
        wip[clave] = wip.get(clave, 0) + 1

    edades = [_con_semaforo(t, momento, p85) for t in activas]

    # Fiabilidad: tarjetas con fecha que vencía en el periodo
    vencidas_periodo = [dict(f) for f in con.execute(
        "SELECT * FROM flujo_tarjetas WHERE fecha_compromiso IS NOT NULL "
        "AND fecha_compromiso>=? AND fecha_compromiso<=? AND estado<>'descartado'",
        (desde.date().isoformat(), momento.date().isoformat()),
    )]
    a_tiempo = sum(
        1 for t in vencidas_periodo
        if t["terminada_en"] and _dt(t["terminada_en"]).date().isoformat() <= t["fecha_compromiso"]
    )

    hechas = [dict(f) for f in con.execute(
        "SELECT t.clase, p.nombre AS proyecto, p.portafolio FROM flujo_tarjetas t "
        "LEFT JOIN flujo_proyectos p ON p.id=t.proyecto_id "
        "WHERE t.estado='hecho' AND t.terminada_en>=?",
        (_iso(desde),),
    )]
    por_clase: dict[str, int] = {}
    por_proyecto: dict[str, int] = {}
    por_portafolio: dict[str, int] = {}
    for h in hechas:
        por_clase[h["clase"]] = por_clase.get(h["clase"], 0) + 1
        nombre = h["proyecto"] or "(sin proyecto)"
        por_proyecto[nombre] = por_proyecto.get(nombre, 0) + 1
        cartera = h["portafolio"] or "(sin portafolio)"
        por_portafolio[cartera] = por_portafolio.get(cartera, 0) + 1

    def limpia(t: dict) -> bool:
        if not t["proyecto_id"] or (t["responsable"] and "/" in t["responsable"]):
            return False
        if t["estado"] in ACTIVOS and not t["responsable"]:
            return False
        return not (t["clase"] == "fecha_fija" and not t["fecha_compromiso"])

    return {
        "periodo_semanas": semanas,
        "throughput_semanal": _throughput_semanal(con, momento, semanas),
        "cycle_time": {
            "n": len(tiempos),
            "p50": _percentil(tiempos, 50),
            "p85": _percentil(tiempos, 85),
            "p85_usado_para_semaforo": p85,
        },
        "wip_por_persona": dict(sorted(wip.items(), key=lambda kv: -kv[1])),
        "wip_limite": LIMITE_WIP_TOTAL,
        "edad": {
            "verde": sum(1 for t in edades if t["semaforo"] == "verde"),
            "ambar": sum(1 for t in edades if t["semaforo"] == "ambar"),
            "rojo": sum(1 for t in edades if t["semaforo"] == "rojo"),
        },
        "pct_bloqueado": round(100 * sum(t["bloqueada"] for t in activas) / len(activas), 1) if activas else 0.0,
        "fiabilidad": {
            "comprometidas": len(vencidas_periodo),
            "a_tiempo": a_tiempo,
            "pct": round(100 * a_tiempo / len(vencidas_periodo), 1) if vencidas_periodo else None,
        },
        "distribucion": {"por_clase": por_clase, "por_proyecto": por_proyecto, "por_portafolio": por_portafolio},
        "higiene_pct": round(100 * sum(limpia(t) for t in abiertas) / len(abiertas), 1) if abiertas else 100.0,
        "higiene_proyectos": _higiene_proyectos(con),
    }


@router.get("/prevision")
def prevision(
    n: int = Query(..., ge=1, le=500, description="Número de tarjetas a terminar"),
    semanas_historia: int = Query(12, ge=4, le=52),
    simulaciones: int = Query(5000, ge=100, le=20000),
    con: sqlite3.Connection = Depends(conexion),
    momento: datetime = Depends(ahora),
):
    """Monte Carlo sobre el throughput semanal: ¿en cuántas semanas terminamos N tarjetas?"""
    historia = _throughput_semanal(con, momento, semanas_historia)
    if sum(historia) == 0:
        raise HTTPException(409, {"reglas": ["Aún no hay histórico de tarjetas terminadas."]})
    rnd = random.Random(42)
    resultados = []
    for _ in range(simulaciones):
        hechas, semanas = 0, 0
        while hechas < n and semanas < 520:
            hechas += rnd.choice(historia)
            semanas += 1
        resultados.append(semanas)
    return {
        "n": n,
        "semanas_p50": _percentil(resultados, 50),
        "semanas_p85": _percentil(resultados, 85),
        "semanas_p95": _percentil(resultados, 95),
        "historia_usada": historia,
    }


@router.get("/resumen-semanal")
def resumen_semanal(
    con: sqlite3.Connection = Depends(conexion),
    momento: datetime = Depends(ahora),
):
    """Resumen asíncrono de la semana: sustituye a la reunión, no la necesita."""
    lunes = (momento - timedelta(days=momento.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
    hace_una_semana = lunes - timedelta(weeks=1)
    en_dos_semanas = (momento + timedelta(weeks=2)).date().isoformat()
    p85 = _p85(con, momento)

    def lista(sql: str, params=()):
        return [_con_semaforo(dict(f), momento, p85) for f in con.execute(sql, params)]

    abiertas = lista("SELECT * FROM flujo_tarjetas WHERE estado NOT IN ('hecho','descartado')")
    limite_listo = momento - timedelta(weeks=SEMANAS_EN_LISTO)
    return {
        "semana_iso": f"{momento.isocalendar().year}-W{momento.isocalendar().week:02d}",
        "terminadas_semana_pasada": lista(
            "SELECT * FROM flujo_tarjetas WHERE estado='hecho' AND terminada_en>=? AND terminada_en<?",
            (_iso(hace_una_semana), _iso(lunes)),
        ),
        "vencen_en_2_semanas": [
            t for t in abiertas if t["fecha_compromiso"] and t["fecha_compromiso"] <= en_dos_semanas
        ],
        "libres": [t for t in abiertas if t["estado"] == "listo" and not t["responsable"]],
        "para_desbloquear": [t for t in abiertas if t["bloqueada"] and (t["dias_bloqueada"] or 0) >= 2],
        "bloqueadas": sorted(
            (t for t in abiertas if t["bloqueada"]), key=lambda t: t["bloqueo_desde"] or ""
        ),
        "envejecidas": [t for t in abiertas if t["semaforo"] == "rojo"],
        "sin_movimiento": [t for t in abiertas if t["sin_movimiento"]],
        "listas_sin_empezar_3_semanas": [
            t for t in abiertas
            if t["estado"] == "listo" and t["lista_en"] and _dt(t["lista_en"]) <= limite_listo
        ],
        "sobre_limite_wip": {
            persona: n for persona, n in metricas(12, con, momento)["wip_por_persona"].items()
            if n > LIMITE_WIP_TOTAL
        },
    }
