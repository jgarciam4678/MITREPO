"""Pruebas del router Flujo. Ejecutar desde torsaflow/torsacore/backend: pytest -q"""

from datetime import datetime, timedelta, timezone

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app import flujo

LUNES = datetime(2026, 10, 19, 9, 0, tzinfo=timezone.utc)


class Reloj:
    def __init__(self, momento):
        self.momento = momento

    def __call__(self):
        return self.momento

    def avanzar(self, **kw):
        self.momento += timedelta(**kw)


@pytest.fixture
def entorno(tmp_path, monkeypatch):
    monkeypatch.setenv("FLUJO_DB", str(tmp_path / "flujo.db"))
    app = FastAPI()
    app.include_router(flujo.router)
    reloj = Reloj(LUNES)
    app.dependency_overrides[flujo.ahora] = reloj
    cliente = TestClient(app, headers={"X-Usuario": "jefatura"})
    proyecto = cliente.put("/api/flujo/proyectos", json={
        "codigo": "INTERNO", "nombre": "Interno", "portafolio": "GLB"}).json()
    return cliente, reloj, proyecto["id"]


def nueva(cliente, proyecto_id, **extra):
    datos = {"titulo": "Elaborar guía de taller", "responsable": "ana",
             "proyecto_id": proyecto_id, "estado": "listo", **extra}
    r = cliente.post("/api/flujo/tarjetas", json=datos)
    assert r.status_code == 201, r.text
    return r.json()


def mover(cliente, tid, estado, **extra):
    return cliente.post(f"/api/flujo/tarjetas/{tid}/mover", json={"estado": estado, **extra})


def test_dias_habiles():
    viernes = datetime(2026, 10, 23)
    assert flujo.dias_habiles(viernes, viernes + timedelta(days=3)) == 1  # lunes
    assert flujo.dias_habiles(LUNES, LUNES + timedelta(days=14)) == 10


def test_definicion_de_listo(entorno):
    cliente, _, pid = entorno
    r = cliente.post("/api/flujo/tarjetas", json={"titulo": "Revisar cosas", "estado": "listo"})
    assert r.status_code == 409
    reglas = r.json()["detail"]["reglas"]
    assert any("responsable" in x for x in reglas) and any("proyecto" in x for x in reglas)

    r = cliente.post("/api/flujo/tarjetas", json={
        "titulo": "Reparar pantallas", "responsable": "ana / luis", "proyecto_id": pid, "estado": "listo"})
    assert r.status_code == 409


def test_limite_wip_se_puede_forzar_con_justificacion(entorno):
    cliente, _, pid = entorno
    ids = [nueva(cliente, pid, titulo=f"Tarea {i}")["id"] for i in range(4)]
    for tid in ids[:3]:
        assert mover(cliente, tid, "en_curso").status_code == 200
    r = mover(cliente, ids[3], "en_curso")
    assert r.status_code == 409 and r.json()["detail"]["se_puede_forzar"]
    r = mover(cliente, ids[3], "en_curso", justificacion_wip="Incidencia de cliente")
    assert r.status_code == 200
    tipos = [e["tipo"] for e in cliente.get(f"/api/flujo/tarjetas/{ids[3]}/historial").json()]
    assert "wip_forzado" in tipos


def test_definicion_de_hecho(entorno):
    cliente, _, pid = entorno
    tid = nueva(cliente, pid)["id"]
    mover(cliente, tid, "en_curso")
    r = mover(cliente, tid, "hecho")
    assert r.status_code == 409 and len(r.json()["detail"]["reglas"]) == 2
    cliente.patch(f"/api/flujo/tarjetas/{tid}", json={"documento_codigo": "ES-CMS-PROC-EJEMPLO"})
    cliente.post(f"/api/flujo/tarjetas/{tid}/aceptar", json={"por": "pm"})
    assert mover(cliente, tid, "hecho").json()["estado"] == "hecho"


def test_transicion_invalida_y_descarte_con_motivo(entorno):
    cliente, _, pid = entorno
    tid = nueva(cliente, pid)["id"]
    assert mover(cliente, tid, "hecho").status_code == 409  # listo -> hecho no existe
    assert mover(cliente, tid, "descartado").status_code == 409
    assert mover(cliente, tid, "descartado", motivo="Ya no aplica").status_code == 200


def test_bloqueo_y_metricas(entorno):
    cliente, reloj, pid = entorno
    a = nueva(cliente, pid, titulo="Tarea A", fecha_compromiso="2026-10-23")["id"]
    b = nueva(cliente, pid, titulo="Tarea B")["id"]
    mover(cliente, a, "en_curso")
    mover(cliente, b, "en_curso")
    r = cliente.post(f"/api/flujo/tarjetas/{b}/bloquear",
                     json={"motivo": "Esperando propuesta", "depende_de": "Comercial"})
    assert r.json()["bloqueada"] == 1

    reloj.avanzar(days=2)
    cliente.patch(f"/api/flujo/tarjetas/{a}", json={"enlace_entregable": "https://x"})
    cliente.post(f"/api/flujo/tarjetas/{a}/aceptar", json={"por": "pm"})
    mover(cliente, a, "hecho")

    reloj.avanzar(days=5)
    m = cliente.get("/api/flujo/metricas?semanas=4").json()
    assert m["cycle_time"]["n"] == 1 and m["cycle_time"]["p50"] == 2
    assert m["pct_bloqueado"] == 100.0
    assert m["fiabilidad"] == {"comprometidas": 1, "a_tiempo": 1, "pct": 100.0}
    assert m["wip_por_persona"] == {"ana": 1}

    resumen = cliente.get("/api/flujo/resumen-semanal").json()
    assert resumen["semana_iso"] == "2026-W44"
    assert [t["id"] for t in resumen["terminadas_semana_pasada"]] == [a]
    assert [t["id"] for t in resumen["bloqueadas"]] == [b]


def test_semaforo_de_edad(entorno):
    cliente, reloj, pid = entorno
    tid = nueva(cliente, pid)["id"]
    mover(cliente, tid, "en_curso")
    reloj.avanzar(days=21)  # 15 días hábiles > p85 provisional de 10
    tarjeta = cliente.get("/api/flujo/tarjetas").json()[0]
    assert tarjeta["semaforo"] == "rojo" and tarjeta["sin_movimiento"]


def test_prevision_monte_carlo(entorno):
    cliente, reloj, pid = entorno
    assert cliente.get("/api/flujo/prevision?n=5").status_code == 409
    for i in range(6):
        tid = nueva(cliente, pid, titulo=f"Tarea {i}")["id"]
        mover(cliente, tid, "en_curso", justificacion_wip="prueba")
        cliente.patch(f"/api/flujo/tarjetas/{tid}", json={"enlace_entregable": "https://x"})
        cliente.post(f"/api/flujo/tarjetas/{tid}/aceptar", json={"por": "pm"})
        mover(cliente, tid, "hecho")
        reloj.avanzar(days=7)
    p = cliente.get("/api/flujo/prevision?n=10").json()
    assert p["semanas_p50"] <= p["semanas_p85"] <= p["semanas_p95"]


def test_tarjetas_desde_plan_de_trabajo(entorno):
    cliente, _, _ = entorno
    proyecto = cliente.put("/api/flujo/proyectos", json={
        "codigo": "ES-SAF-DOC-PC-DEMO", "nombre": "Demo SAF", "portafolio": "SAF",
        "responsable": "pm", "estado_charter": "Aprobado"}).json()
    plan = {"fases": [
        {"fase": "Visita técnica", "actividad": "Levantamiento de operación",
         "inicio": "2026-11-02", "fin": "2026-11-06", "responsable": "ana"},
        {"fase": "Aprobación SSOMA", "inicio": "A definir", "fin": "A definir", "responsable": "A asignar"},
    ]}
    r = cliente.post(f"/api/flujo/proyectos/{proyecto['id']}/plan", json=plan).json()
    assert r["creadas"] == 2 and r["fases_sin_fecha_o_responsable"] == ["Aprobación SSOMA"]
    tarjetas = {t["fase"]: t for t in cliente.get(f"/api/flujo/tarjetas?proyecto_id={proyecto['id']}").json()}
    assert tarjetas["Visita técnica"]["estado"] == "listo"
    assert tarjetas["Visita técnica"]["clase"] == "fecha_fija"
    assert tarjetas["Aprobación SSOMA"]["estado"] == "backlog"
    # idempotente
    assert cliente.post(f"/api/flujo/proyectos/{proyecto['id']}/plan", json=plan).json()["creadas"] == 0

    # el Charter no tiene fechas: cuenta como incompleto en la higiene de proyectos
    h = cliente.get("/api/flujo/metricas").json()["higiene_proyectos"]
    assert h == {"activos": 1, "completos": 0, "pct": 0.0, "incompletos": ["ES-SAF-DOC-PC-DEMO"]}
