"""Analizador de Comentarios de Clientes — app Streamlit.

Versión 0: motor de análisis 100 % local (léxico en español), sin llamadas
externas. En la semana 3 se añade la pieza de IA con Gemini leyendo la clave
desde st.secrets (nunca en el código); si no hay clave, la app sigue
funcionando con el motor local.
"""

import pandas as pd
import plotly.express as px
import streamlit as st

from analyzer import (
    NEGATIVO,
    NEUTRO,
    POSITIVO,
    analyze_comments,
    parse_csv,
    split_comments,
    to_csv,
    to_markdown_report,
)
from sample_data import SAMPLE_COMMENTS
from lexicon import TOPICS

SENTIMENT_COLORS = {POSITIVO: "#16a34a", NEUTRO: "#d4a017", NEGATIVO: "#dc2626"}
SENTIMENT_LABEL = {POSITIVO: "Positivo", NEUTRO: "Neutro", NEGATIVO: "Negativo"}
SENTIMENT_BADGE = {POSITIVO: "green", NEUTRO: "orange", NEGATIVO: "red"}
TOPIC_LABEL = {t["id"]: t["label"] for t in TOPICS}

st.set_page_config(
    page_title="Analizador de Comentarios de Clientes",
    page_icon="💬",
    layout="wide",
)

# --------------------------------------------------------------------------- #
# Cabecera
# --------------------------------------------------------------------------- #
st.title("💬 Analizador de Comentarios de Clientes")
st.caption(
    "Descubre qué opinan tus clientes y qué debes arreglar primero · "
    "🔒 100 % local: tus datos no salen de esta app"
)

if "result" not in st.session_state:
    st.session_state.result = None

# --------------------------------------------------------------------------- #
# Cómo funciona (solo antes del primer análisis)
# --------------------------------------------------------------------------- #
if st.session_state.result is None:
    c1, c2, c3 = st.columns(3)
    c1.info("**1 · Pega o sube**\n\nCopia reseñas, encuestas o mensajes de soporte: un comentario por línea. También vale un CSV.")
    c2.info("**2 · Pulsa Analizar**\n\nEl motor detecta sentimiento, temas y urgencia de cada comentario, aquí mismo, sin servidores.")
    c3.info("**3 · Actúa**\n\nObtén las prioridades ordenadas, con acciones sugeridas y un informe listo para compartir.")

# --------------------------------------------------------------------------- #
# Entrada de datos
# --------------------------------------------------------------------------- #
st.subheader("Comentarios a analizar")


# Los callbacks se ejecutan ANTES de crear los widgets, por lo que pueden
# modificar st.session_state.raw_text sin conflictos con el text_area.
def load_example():
    st.session_state.raw_text = "\n".join(SAMPLE_COMMENTS)
    st.session_state.result = analyze_comments(SAMPLE_COMMENTS)


def handle_upload():
    f = st.session_state.get("uploader")
    if f is None:
        return
    content = f.read().decode("utf-8", errors="replace")
    texts = parse_csv(content) if f.name.lower().endswith(".csv") else split_comments(content)
    if texts:
        st.session_state.raw_text = "\n".join(texts)
        st.session_state.result = analyze_comments(texts)


def reset_all():
    st.session_state.result = None
    st.session_state.raw_text = ""


raw_text = st.text_area(
    "Escribe un comentario por línea",
    placeholder="Ejemplo:\nEl pedido llegó tarde y nadie me avisó del retraso.\nLa atención telefónica fue excelente, muy amables.",
    height=160,
    key="raw_text",
)

col_a, col_b, col_c, col_d = st.columns([2, 2, 2, 2])
analyze_clicked = col_a.button(
    f"✨ Analizar {len(split_comments(raw_text)) or ''} comentarios".rstrip(),
    type="primary",
    width="stretch",
)
col_b.button("📄 Cargar datos de ejemplo", width="stretch", on_click=load_example)
col_c.file_uploader(
    "Subir CSV o TXT",
    type=["csv", "txt"],
    label_visibility="collapsed",
    key="uploader",
    on_change=handle_upload,
)
col_d.button("🔄 Empezar de nuevo", width="stretch", on_click=reset_all)

st.caption(
    "Los datos de ejemplo son reseñas sintéticas de «TecnoHogar», una PYME ficticia. "
    "No uses datos personales reales."
)


if analyze_clicked:
    texts = split_comments(raw_text)
    if not texts:
        st.warning("No se encontraron comentarios. Pega texto (uno por línea) o sube un CSV.")
    else:
        st.session_state.result = analyze_comments(texts)

result = st.session_state.result

# --------------------------------------------------------------------------- #
# Resultados
# --------------------------------------------------------------------------- #
if result is not None:
    st.divider()
    total = result.total
    s = result.sentiment_counts
    pct = lambda n: round(n / total * 100) if total else 0

    # KPIs
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Comentarios", total, f"{s[NEGATIVO]} negativos ({pct(s[NEGATIVO])} %)", delta_color="inverse")
    k2.metric("Satisfacción global", f"{result.global_score}/100")
    k3.metric("Urgencia media", f"{result.avg_urgency}/100")
    top = result.priorities[0] if result.priorities else None
    k4.metric("Prioridad nº 1", top.label if top else "—", f"prioridad {top.priority_score}/100" if top else "")

    # Gráficos
    g1, g2 = st.columns(2)

    with g1:
        st.markdown("**Distribución del sentimiento**")
        pie_df = pd.DataFrame(
            {
                "Sentimiento": [SENTIMENT_LABEL[k] for k in (POSITIVO, NEUTRO, NEGATIVO)],
                "Comentarios": [s[POSITIVO], s[NEUTRO], s[NEGATIVO]],
            }
        )
        fig_pie = px.pie(
            pie_df,
            names="Sentimiento",
            values="Comentarios",
            hole=0.55,
            color="Sentimiento",
            color_discrete_map={SENTIMENT_LABEL[k]: v for k, v in SENTIMENT_COLORS.items()},
        )
        fig_pie.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=300)
        st.plotly_chart(fig_pie, width="stretch")

    with g2:
        st.markdown("**Prioridad por tema** (frecuencia + negatividad + urgencia)")
        bar_df = pd.DataFrame(
            {
                "Tema": [p.label for p in result.priorities[:8]],
                "Prioridad": [p.priority_score for p in result.priorities[:8]],
            }
        ).sort_values("Prioridad")
        fig_bar = px.bar(bar_df, x="Prioridad", y="Tema", orientation="h", range_x=[0, 100])
        fig_bar.update_traces(marker_color="#4f46e5")
        fig_bar.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=300)
        st.plotly_chart(fig_bar, width="stretch")

    # Ranking de prioridades
    st.subheader("🎯 Prioridades de actuación")
    d1, d2, _ = st.columns([2, 2, 6])
    d1.download_button(
        "⬇️ Informe (Markdown)",
        data=to_markdown_report(result),
        file_name="informe-comentarios.md",
        mime="text/markdown",
        width="stretch",
    )
    d2.download_button(
        "⬇️ Detalle (CSV)",
        data="﻿" + to_csv(result),
        file_name="analisis-comentarios.csv",
        mime="text/csv",
        width="stretch",
    )

    for i, p in enumerate(result.priorities, start=1):
        with st.container(border=True):
            head_l, head_r = st.columns([6, 2])
            head_l.markdown(f"**#{i} · {p.label}**")
            head_r.markdown(f"Prioridad **{p.priority_score}/100**")
            st.progress(p.priority_score / 100)
            neg_style = " 🔴" if p.negative_pct >= 50 else ""
            st.caption(
                f"{p.mentions} menciones · {p.negative_pct} % negativas{neg_style} · "
                f"Urgencia media {p.avg_urgency}/100"
            )
            st.markdown(f"✅ **Acción sugerida:** {p.action}")
            with st.expander(f"Ver comentarios más urgentes ({len(p.examples)})"):
                for e in p.examples:
                    st.markdown(f'- "{e}"')

    # Palabras clave y detalle
    st.subheader("🔑 Palabras más repetidas")
    chips = " ".join(
        f":{'red' if k['negative'] else 'green'}[**{k['word']}** · {k['count']}]"
        for k in result.top_keywords
    )
    st.markdown(chips)
    st.caption("Rojo = aparece sobre todo en comentarios negativos")

    st.subheader("📋 Detalle por comentario")
    filtro = st.radio(
        "Filtrar por sentimiento",
        ["Todos", "Negativos", "Neutros", "Positivos"],
        horizontal=True,
        label_visibility="collapsed",
    )
    filtro_map = {"Todos": None, "Negativos": NEGATIVO, "Neutros": NEUTRO, "Positivos": POSITIVO}
    comments = [
        c for c in result.comments if filtro_map[filtro] is None or c.sentiment == filtro_map[filtro]
    ]
    for c in comments:
        with st.container(border=True):
            st.markdown(c.text)
            badges = [f":{SENTIMENT_BADGE[c.sentiment]}[**{SENTIMENT_LABEL[c.sentiment]}** {c.sentiment_score:+d}]"]
            if c.urgency >= 40:
                badges.append(f":orange[**Urgencia** {c.urgency}]")
            badges += [f":gray[{TOPIC_LABEL.get(t, t)}]" for t in c.topics]
            st.markdown(" ".join(badges))
    if not comments:
        st.caption("No hay comentarios con este filtro.")

# --------------------------------------------------------------------------- #
# Metodología
# --------------------------------------------------------------------------- #
with st.expander("ℹ️ Cómo se calcula la prioridad"):
    st.markdown(
        """
Cada comentario recibe:

- una **puntuación de sentimiento** (−100 a +100) según un léxico en español
  con negaciones e intensificadores,
- una **urgencia** (0–100) por palabras críticas, mayúsculas y exclamaciones, y
- uno o varios **temas** por palabras clave.

La **prioridad** de cada tema combina su frecuencia (35 %), el porcentaje de
comentarios negativos (40 %) y la urgencia media (25 %).

Todo el procesamiento se ejecuta en esta app: **ningún dato se envía a ningún
servidor de terceros**.
"""
    )

st.divider()
st.caption(
    "Analizador de Comentarios de Clientes · Herramienta local y gratuita · "
    "Sin claves de API en el código · Sin envío de datos"
)
