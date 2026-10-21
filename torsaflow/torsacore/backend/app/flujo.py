"""Flujo: tablero de trabajo del departamento (marco TorsaFlow).

Router FastAPI de referencia para integrar en TorsaCore. Guarda tarjetas,
proyectos y el historial de eventos en SQLite; las métricas se calculan a partir
del historial, nunca se introducen a mano.

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
    id          INTEGER PRIMARY KEY,
    nombre      TEXT NOT NULL UNIQUE,
    cliente     TEXT,
    odoo_id     INTEGER UNIQUE,
    activo      INTEGER NOT NULL DEFAULT 1
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
    odoo_ref            TEXT,
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
    nombre: str = Field(min_length=1)
    cliente: Optional[str] = None
    odoo_id: Optional[int] = None
    activo: bool = True


class TarjetaEntrada(BaseModel):
    titulo: str = Field(min_length=3)
    responsable: Optional[str] = None
    solicitante: Optional[str] = None
    proyecto_id: Optional[int] = None
    clase: Clase = "estandar"
    estado: Literal["backlog", "listo"] = "backlog"
    fecha_compromiso: Optional[date] = None
    odoo_ref: Optional[str] = None


class TarjetaCambios(BaseModel):
    titulo: Optional[str] = Field(default=None, min_length=3)
    responsable: Optional[str] = None
    solicitante: Optional[str] = None
    proyecto_id: Optional[int] = None
    clase: Optional[Clase] = None
    fecha_compromiso: Optional[date] = None
    enlace_entregable: Optional[str] = None
    odoo_ref: Optional[str] = None


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


def faltas_listo(t: dict) -> list[str]:
    """Definición de Listo."""
    faltas = []
    if not t.get("responsable"):
        faltas.append("Falta un responsable único.")
    elif "/" in t["responsable"] or "," in t["responsable"]:
        faltas.append("El responsable debe ser una sola persona.")
    if not t.get("proyecto_id"):
        faltas.append("Falta el proyecto (usa «Interno» si no es de cliente).")
    if t.get("clase") == "fecha_fija" and not t.get("fecha_compromiso"):
        faltas.append("Una tarjeta de fecha fija necesita fecha de compromiso.")
    return faltas


def faltas_hecho(t: dict) -> list[str]:
    """Definición de Hecho."""
    faltas = []
    if not t.get("enlace_entregable"):
        faltas.append("Enlaza el entregable (Biblioteca técnica, SharePoint, Odoo o Craft).")
    if not t.get("aceptada_por"):
        faltas.append("Registra la aceptación de quien lo pidió.")
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
    """Alta o actualización por nombre. El sincronizador de Odoo usa este mismo camino."""
    con.execute(
        "INSERT INTO flujo_proyectos (nombre, cliente, odoo_id, activo) VALUES (?,?,?,?) "
        "ON CONFLICT(nombre) DO UPDATE SET cliente=excluded.cliente, "
        "odoo_id=excluded.odoo_id, activo=excluded.activo",
        (p.nombre, p.cliente, p.odoo_id, int(p.activo)),
    )
    fila = con.execute("SELECT * FROM flujo_proyectos WHERE nombre=?", (p.nombre,)).fetchone()
    return dict(fila)


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
        "estado, fecha_compromiso, odoo_ref, creada_en, lista_en, actualizada_en) "
        "VALUES (?,?,?,?,?,?,?,?,?,?,?)",
        (
            t.titulo.strip(),
            t.responsable,
            t.solicitante or usuario,
            t.proyecto_id,
            t.clase,
            t.estado,
            t.fecha_compromiso.isoformat() if t.fecha_compromiso else None,
            t.odoo_ref,
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
        faltas += faltas_listo(t)
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
        "SELECT t.clase, p.nombre AS proyecto FROM flujo_tarjetas t "
        "LEFT JOIN flujo_proyectos p ON p.id=t.proyecto_id "
        "WHERE t.estado='hecho' AND t.terminada_en>=?",
        (_iso(desde),),
    )]
    por_clase: dict[str, int] = {}
    por_proyecto: dict[str, int] = {}
    for h in hechas:
        por_clase[h["clase"]] = por_clase.get(h["clase"], 0) + 1
        nombre = h["proyecto"] or "(sin proyecto)"
        por_proyecto[nombre] = por_proyecto.get(nombre, 0) + 1

    def limpia(t: dict) -> bool:
        if not t["responsable"] or "/" in t["responsable"] or not t["proyecto_id"]:
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
        "distribucion": {"por_clase": por_clase, "por_proyecto": por_proyecto},
        "higiene_pct": round(100 * sum(limpia(t) for t in abiertas) / len(abiertas), 1) if abiertas else 100.0,
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
    """Sustituye al Excel semanal: lo que se mira en la reposición del lunes."""
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
