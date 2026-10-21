// Flujo: tablero del departamento (marco TorsaFlow).
// Usa los tokens de App.css y las clases de CMSStudio.css (.cmss-bar, .cmss-sec, .cmss-pill)
// para verse como un módulo más de TorsaCore.
// ADAPTAR: si TorsaCore tiene un cliente HTTP propio (token, base URL), sustituir `api`.

import { useCallback, useEffect, useMemo, useState } from "react";
import "./Flujo.css";

const BASE = "/api/flujo";

async function api(ruta, opciones = {}) {
  const r = await fetch(`${BASE}${ruta}`, {
    credentials: "include",
    headers: { "Content-Type": "application/json" },
    ...opciones,
    body: opciones.body ? JSON.stringify(opciones.body) : undefined,
  });
  const datos = await r.json().catch(() => ({}));
  if (!r.ok) {
    const error = new Error("flujo");
    error.detalle = datos.detail || {};
    throw error;
  }
  return datos;
}

const COLUMNAS = [
  { id: "backlog", titulo: "Backlog" },
  { id: "listo", titulo: "Listo" },
  { id: "en_curso", titulo: "En curso", limite: 3 },
  { id: "en_validacion", titulo: "En validación", limite: 2 },
  { id: "hecho", titulo: "Hecho (7 días)" },
];

const SIGUIENTE = {
  backlog: ["listo"],
  listo: ["en_curso", "backlog"],
  en_curso: ["en_validacion", "hecho", "listo"],
  en_validacion: ["hecho", "en_curso"],
  hecho: [],
};

const NOMBRE_ESTADO = Object.fromEntries(COLUMNAS.map((c) => [c.id, c.titulo.replace(" (7 días)", "")]));

const CLASES = {
  urgente: "Urgente",
  fecha_fija: "Fecha fija",
  estandar: "Estándar",
  mejora: "Mejora interna",
};

function hace7dias() {
  return new Date(Date.now() - 7 * 864e5).toISOString();
}

function Tarjeta({ t, proyectos, onMover, onBloqueo, onEditar }) {
  const proyecto = proyectos.find((p) => p.id === t.proyecto_id);
  const vencida = t.fecha_compromiso && t.estado !== "hecho" && t.fecha_compromiso < new Date().toISOString().slice(0, 10);
  return (
    <article className={`flujo-card ${t.bloqueada ? "is-bloqueada" : ""} ${t.semaforo ? `edad-${t.semaforo}` : ""}`}>
      <header className="flujo-card-h">
        <span className={`cmss-pill flujo-clase-${t.clase}`}>{CLASES[t.clase]}</span>
        {proyecto?.portafolio && <span className="cmss-pill">{proyecto.portafolio}</span>}
        {t.edad != null && <span className="flujo-edad" title="Días hábiles en curso">{t.edad} d</span>}
      </header>
      <button type="button" className="flujo-titulo" onClick={() => onEditar(t)}>{t.titulo}</button>
      <div className="flujo-meta">
        <span>{t.responsable || <em className="flujo-falta">sin responsable</em>}</span>
        <span>{proyecto ? proyecto.nombre : <em className="flujo-falta">sin proyecto</em>}</span>
        {t.fase && <span>Fase: {t.fase}</span>}
        {t.fecha_compromiso && <span className={vencida ? "flujo-vencida" : ""}>📅 {t.fecha_compromiso}</span>}
        {t.documento_codigo && <span>📄 {t.documento_codigo}</span>}
      </div>
      {t.bloqueada ? (
        <p className="flujo-bloqueo">⚑ {t.bloqueo_depende_de}: {t.bloqueo_motivo}</p>
      ) : null}
      <footer className="flujo-acciones">
        {SIGUIENTE[t.estado].map((e) => (
          <button key={e} type="button" className="btn-secondary cmss-sm" onClick={() => onMover(t, e)}>
            → {NOMBRE_ESTADO[e]}
          </button>
        ))}
        {t.estado !== "hecho" && (
          <button type="button" className="btn-secondary cmss-sm" onClick={() => onBloqueo(t)}>
            {t.bloqueada ? "Desbloquear" : "⚑ Bloquear"}
          </button>
        )}
      </footer>
    </article>
  );
}

function Metricas({ m }) {
  if (!m) return null;
  const ultima = m.throughput_semanal.at(-1) ?? 0;
  const datos = [
    ["Terminadas esta semana", ultima],
    ["Cycle time p85", m.cycle_time.p85 != null ? `${m.cycle_time.p85} d` : "—"],
    ["En rojo por edad", m.edad.rojo],
    ["% bloqueado", `${m.pct_bloqueado} %`],
    ["Fiabilidad", m.fiabilidad.pct != null ? `${m.fiabilidad.pct} %` : "—"],
    ["Higiene tablero", `${m.higiene_pct} %`],
    ["Charters completos", m.higiene_proyectos.pct != null ? `${m.higiene_proyectos.pct} %` : "—"],
  ];
  return (
    <section className="flujo-kpis">
      {datos.map(([etiqueta, valor]) => (
        <div key={etiqueta} className="cmss-sec flujo-kpi">
          <span className="cmss-sec-h">{etiqueta}</span>
          <strong>{valor}</strong>
        </div>
      ))}
    </section>
  );
}

function Resumen({ r }) {
  if (!r) return <p className="module-empty">Cargando resumen…</p>;
  const bloques = [
    ["Terminadas la semana pasada", r.terminadas_semana_pasada],
    ["Vencen en 2 semanas", r.vencen_en_2_semanas],
    ["Bloqueadas", r.bloqueadas],
    ["En rojo por edad", r.envejecidas],
    ["Sin movimiento 10 días", r.sin_movimiento],
    ["En Listo hace 3 semanas (¿Backlog o descartar?)", r.listas_sin_empezar_3_semanas],
  ];
  return (
    <div className="flujo-resumen">
      {Object.keys(r.sobre_limite_wip).length > 0 && (
        <p className="flujo-aviso">
          Sobre el límite de WIP: {Object.entries(r.sobre_limite_wip).map(([p, n]) => `${p} (${n})`).join(", ")}
        </p>
      )}
      {bloques.map(([titulo, lista]) => (
        <section key={titulo} className="cmss-sec">
          <h3 className="cmss-sec-h">{titulo} · {lista.length}</h3>
          <ul>
            {lista.map((t) => (
              <li key={t.id}>
                <strong>{t.titulo}</strong> — {t.responsable || "sin responsable"}
                {t.bloqueada ? ` · ⚑ ${t.bloqueo_depende_de}` : ""}
                {t.fecha_compromiso ? ` · 📅 ${t.fecha_compromiso}` : ""}
              </li>
            ))}
          </ul>
        </section>
      ))}
    </div>
  );
}

export default function Flujo() {
  const [vista, setVista] = useState("tablero");
  const [tarjetas, setTarjetas] = useState([]);
  const [hechas, setHechas] = useState([]);
  const [proyectos, setProyectos] = useState([]);
  const [metricas, setMetricas] = useState(null);
  const [resumen, setResumen] = useState(null);
  const [filtro, setFiltro] = useState({ responsable: "", proyecto: "", portafolio: "" });
  const [error, setError] = useState(null);
  const [nueva, setNueva] = useState("");

  const cargar = useCallback(async () => {
    try {
      const [abiertas, cerradas, ps, m] = await Promise.all([
        api("/tarjetas"),
        api("/tarjetas?estado=hecho"),
        api("/proyectos"),
        api("/metricas"),
      ]);
      setTarjetas(abiertas);
      setHechas(cerradas.filter((t) => t.terminada_en >= hace7dias()));
      setProyectos(ps);
      setMetricas(m);
      setError(null);
    } catch {
      setError("No se pudo cargar el tablero.");
    }
  }, []);

  useEffect(() => { cargar(); }, [cargar]);
  useEffect(() => {
    if (vista === "resumen") api("/resumen-semanal").then(setResumen).catch(() => setResumen(null));
  }, [vista, tarjetas]);

  const responsables = useMemo(
    () => [...new Set([...tarjetas, ...hechas].map((t) => t.responsable).filter(Boolean))].sort(),
    [tarjetas, hechas],
  );

  const portafolios = useMemo(
    () => [...new Set(proyectos.map((p) => p.portafolio).filter(Boolean))].sort(),
    [proyectos],
  );
  const portafolioDe = (t) => proyectos.find((p) => p.id === t.proyecto_id)?.portafolio;

  const visibles = [...tarjetas, ...hechas].filter(
    (t) =>
      (!filtro.responsable || t.responsable === filtro.responsable) &&
      (!filtro.proyecto || String(t.proyecto_id) === filtro.proyecto) &&
      (!filtro.portafolio || portafolioDe(t) === filtro.portafolio),
  );

  const conReglas = async (accion) => {
    try {
      await accion();
      await cargar();
    } catch (e) {
      const reglas = e.detalle?.reglas || ["No se pudo guardar."];
      if (e.detalle?.se_puede_forzar) return reglas;
      setError(reglas.join(" "));
    }
    return null;
  };

  const mover = async (t, estado) => {
    const tieneEntregable = t.documento_codigo || t.enlace_entregable;
    if (estado === "hecho" && (!tieneEntregable || !t.aceptada_por)) {
      const entregable = tieneEntregable || window.prompt("Código del entregable en la Biblioteca técnica (o enlace de Craft):");
      if (!entregable) return;
      const por = t.aceptada_por || window.prompt("¿Quién lo ha aceptado?");
      if (!por) return;
      const campo = /^https?:\/\//.test(entregable) ? "enlace_entregable" : "documento_codigo";
      await conReglas(async () => {
        if (!tieneEntregable) await api(`/tarjetas/${t.id}`, { method: "PATCH", body: { [campo]: entregable } });
        await api(`/tarjetas/${t.id}/aceptar`, { method: "POST", body: { por } });
      });
    }
    const avisos = await conReglas(() => api(`/tarjetas/${t.id}/mover`, { method: "POST", body: { estado } }));
    if (avisos) {
      const porque = window.prompt(`${avisos.join("\n")}\n\nSi aun así hay que empezarla, indica por qué:`);
      if (porque) {
        await conReglas(() =>
          api(`/tarjetas/${t.id}/mover`, { method: "POST", body: { estado, justificacion_wip: porque } }),
        );
      }
    }
  };

  const bloqueo = async (t) => {
    if (t.bloqueada) return conReglas(() => api(`/tarjetas/${t.id}/desbloquear`, { method: "POST" }));
    const depende_de = window.prompt("¿De quién depende? (Comercial, Desarrollo, cliente, proveedor…)");
    if (!depende_de) return;
    const motivo = window.prompt("¿Qué falta exactamente?");
    if (!motivo) return;
    return conReglas(() => api(`/tarjetas/${t.id}/bloquear`, { method: "POST", body: { depende_de, motivo } }));
  };

  const editar = async (t) => {
    const titulo = window.prompt("Título (verbo + entregable):", t.titulo);
    if (titulo == null) return;
    const responsable = window.prompt("Responsable único:", t.responsable || "");
    const fecha = window.prompt("Fecha de compromiso (AAAA-MM-DD, vacío si no hay):", t.fecha_compromiso || "");
    await conReglas(() =>
      api(`/tarjetas/${t.id}`, {
        method: "PATCH",
        body: { titulo, responsable: responsable || null, ...(fecha ? { fecha_compromiso: fecha } : {}) },
      }),
    );
  };

  const crear = async (ev) => {
    ev.preventDefault();
    if (nueva.trim().length < 3) return;
    await conReglas(() =>
      api("/tarjetas", {
        method: "POST",
        body: {
          titulo: nueva.trim(),
          responsable: filtro.responsable || null,
          proyecto_id: filtro.proyecto ? Number(filtro.proyecto) : null,
        },
      }),
    );
    setNueva("");
  };

  return (
    <div className="flujo">
      <header className="cmss-bar">
        <h2 className="cmss-title">Flujo</h2>
        <select value={filtro.responsable} onChange={(e) => setFiltro({ ...filtro, responsable: e.target.value })}>
          <option value="">Todo el equipo</option>
          {responsables.map((r) => <option key={r} value={r}>{r}</option>)}
        </select>
        <select value={filtro.portafolio} onChange={(e) => setFiltro({ ...filtro, portafolio: e.target.value })}>
          <option value="">Todos los portafolios</option>
          {portafolios.map((p) => <option key={p} value={p}>{p}</option>)}
        </select>
        <select value={filtro.proyecto} onChange={(e) => setFiltro({ ...filtro, proyecto: e.target.value })}>
          <option value="">Todos los proyectos</option>
          {proyectos.filter((p) => p.activo).map((p) => <option key={p.id} value={p.id}>{p.nombre}</option>)}
        </select>
        <form className="flujo-nueva" onSubmit={crear}>
          <input value={nueva} onChange={(e) => setNueva(e.target.value)} placeholder="Nueva tarjeta: verbo + entregable" />
          <button type="submit" className="btn-primary cmss-sm">Añadir</button>
        </form>
        <div className="flujo-vistas">
          <button type="button" className={`btn-secondary cmss-sm ${vista === "tablero" ? "is-on" : ""}`} onClick={() => setVista("tablero")}>Tablero</button>
          <button type="button" className={`btn-secondary cmss-sm ${vista === "resumen" ? "is-on" : ""}`} onClick={() => setVista("resumen")}>Resumen semanal</button>
          <button type="button" className="btn-secondary cmss-sm" onClick={cargar}>⟳</button>
        </div>
      </header>

      {error && <p className="form-error" role="alert" onClick={() => setError(null)}>{error}</p>}
      <Metricas m={metricas} />

      {vista === "resumen" ? (
        <Resumen r={resumen} />
      ) : (
        <div className="flujo-tablero">
          {COLUMNAS.map((c) => {
            const lista = visibles.filter((t) => t.estado === c.id);
            const porPersona = filtro.responsable && c.limite && lista.length > c.limite;
            return (
              <section key={c.id} className={`cmss-sec flujo-col ${porPersona ? "is-sobre-limite" : ""}`}>
                <h3 className="cmss-sec-h">
                  {c.titulo} · {lista.length}
                  {c.limite ? <span className="flujo-limite"> (límite {c.limite}/persona)</span> : null}
                </h3>
                {lista.length === 0 && <p className="module-empty">—</p>}
                {lista.map((t) => (
                  <Tarjeta key={t.id} t={t} proyectos={proyectos} onMover={mover} onBloqueo={bloqueo} onEditar={editar} />
                ))}
              </section>
            );
          })}
        </div>
      )}
    </div>
  );
}
