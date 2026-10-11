"""SmartFeedback — Analizador de Comentarios de Clientes (app Streamlit).

Doble puerta:
- **Puerta del cliente** (vista por defecto): chat "¿Necesitas ayuda?" donde
  el cliente deja su comentario. Es el enlace/QR que comparte la PYME.
- **Puerta del dueño** (barra lateral, con contraseña): panel de análisis con
  sentimiento, temas, prioridades, gráficos e informes descargables.

Los comentarios se guardan en Supabase (gratis) si hay credenciales en
st.secrets, o en un CSV local como respaldo. La pieza de IA con Gemini
(semana 3) leerá su clave también desde st.secrets, nunca del código.
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
from db import delete_all, load_comments, save_comment, use_supabase
from lexicon import TOPICS
from sample_data import SAMPLE_COMMENTS

SENTIMENT_COLORS = {POSITIVO: "#16a34a", NEUTRO: "#d4a017", NEGATIVO: "#dc2626"}
SENTIMENT_LABEL = {POSITIVO: "Positivo", NEUTRO: "Neutro", NEGATIVO: "Negativo"}
SENTIMENT_BADGE = {POSITIVO: "green", NEUTRO: "orange", NEGATIVO: "red"}
TOPIC_LABEL = {t["id"]: t["label"] for t in TOPICS}

st.set_page_config(
    page_title="SmartFeedback · Analizador de Comentarios",
    page_icon="💬",
    layout="wide",
)


def _secret(name: str, default: str = "") -> str:
    try:
        return st.secrets.get(name, default)
    except Exception:
        return default


# --------------------------------------------------------------------------- #
# Vista del cliente: chat "¿Necesitas ayuda?"
# --------------------------------------------------------------------------- #
def render_cliente():
    st.title("💬 ¿Necesitas ayuda?")
    st.caption("Cuéntanos tu experiencia. Tu opinión nos ayuda a mejorar.")

    with st.chat_message("assistant"):
        st.markdown(
            "¡Hola! 👋 Soy el asistente de atención al cliente. "
            "¿Cómo fue tu experiencia con nosotros? "
            "Puedes contarme lo que quieras: el pedido, el envío, la atención recibida..."
        )

    for msg in st.session_state.get("chat", []):
        with st.chat_message(msg["role"]):
            st.markdown(msg["text"])

    comentario = st.chat_input("Escribe aquí tu comentario...")
    if comentario:
        st.session_state.setdefault("chat", []).append({"role": "user", "text": comentario})
        save_comment(comentario)
        # Mini-análisis inmediato para personalizar el agradecimiento
        resultado = analyze_comments([comentario])
        sentimiento = resultado.comments[0].sentiment if resultado.comments else NEUTRO
        if sentimiento == NEGATIVO:
            respuesta = (
                "Lamento que tu experiencia no haya sido buena. 😔 "
                "Tu comentario ya está registrado y el equipo lo revisará con prioridad. "
                "Gracias por ayudarnos a mejorar."
            )
        elif sentimiento == POSITIVO:
            respuesta = (
                "¡Muchas gracias por tus palabras! 😊 "
                "Nos alegra que tu experiencia fuera buena. Tu opinión ya está registrada."
            )
        else:
            respuesta = (
                "Gracias por tu comentario, ya está registrado. "
                "Lo tendremos en cuenta para seguir mejorando. 🙌"
            )
        st.session_state.chat.append({"role": "assistant", "text": respuesta})
        st.rerun()

    with st.expander("ℹ️ Qué pasa con tu comentario"):
        st.markdown(
            "Tu comentario se guarda de forma anónima y el equipo lo analiza "
            "para detectar qué debe mejorar primero. No pedimos ni guardamos "
            "datos personales."
        )


# --------------------------------------------------------------------------- #
# Vista del dueño: panel de análisis
# --------------------------------------------------------------------------- #
def render_results(result):
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

    # Palabras clave
    st.subheader("🔑 Palabras más repetidas")
    chips = " ".join(
        f":{'red' if k['negative'] else 'green'}[**{k['word']}** · {k['count']}]"
        for k in result.top_keywords
    )
    st.markdown(chips or "Sin palabras destacadas todavía.")
    st.caption("Rojo = aparece sobre todo en comentarios negativos")

    # Detalle por comentario
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


def render_panel():
    st.title("📊 Panel del dueño")
    modo = "☁️ Supabase (nube)" if use_supabase() else "💾 Archivo local (respaldo)"
    st.caption(f"Almacenamiento activo: {modo} · 🔒 Ninguna clave aparece en el código")

    tab_recibidos, tab_manual, tab_ajustes = st.tabs(
        ["📥 Comentarios recibidos", "📝 Análisis manual", "⚙️ Ajustes"]
    )

    # ----- Comentarios recibidos desde el chat -----
    with tab_recibidos:
        col_r1, col_r2, _ = st.columns([2, 2, 6])
        if col_r1.button("🔄 Actualizar", width="stretch"):
            st.rerun()
        comentarios = load_comments()
        col_r2.metric("Recibidos", len(comentarios))

        if not comentarios:
            st.info(
                "Todavía no hay comentarios. Comparte el enlace de la app (o un QR) "
                "con tus clientes: al abrirlo verán el chat de «¿Necesitas ayuda?». "
                "Cuando escriban, sus comentarios aparecerán aquí."
            )
        else:
            if st.button("✨ Analizar comentarios recibidos", type="primary"):
                st.session_state.result_recibidos = analyze_comments(comentarios)
            if "result_recibidos" in st.session_state:
                render_results(st.session_state.result_recibidos)

    # ----- Análisis manual (pegar / subir / ejemplo) -----
    with tab_manual:
        st.markdown("Pega comentarios (uno por línea), sube un CSV/TXT o usa los datos de ejemplo.")

        def load_example():
            st.session_state.raw_text = "\n".join(SAMPLE_COMMENTS)
            st.session_state.result_manual = analyze_comments(SAMPLE_COMMENTS)

        def handle_upload():
            f = st.session_state.get("uploader")
            if f is None:
                return
            content = f.read().decode("utf-8", errors="replace")
            texts = parse_csv(content) if f.name.lower().endswith(".csv") else split_comments(content)
            if texts:
                st.session_state.raw_text = "\n".join(texts)
                st.session_state.result_manual = analyze_comments(texts)

        raw_text = st.text_area(
            "Un comentario por línea",
            placeholder="El pedido llegó tarde y nadie me avisó del retraso.\nLa atención telefónica fue excelente, muy amables.",
            height=140,
            key="raw_text",
        )
        col_a, col_b, col_c = st.columns([2, 2, 2])
        if col_a.button(
            f"✨ Analizar {len(split_comments(raw_text)) or ''} comentarios".rstrip(),
            type="primary",
            width="stretch",
        ):
            texts = split_comments(raw_text)
            if not texts:
                st.warning("No se encontraron comentarios. Pega texto o sube un CSV.")
            else:
                st.session_state.result_manual = analyze_comments(texts)
        col_b.button("📄 Datos de ejemplo", width="stretch", on_click=load_example)
        col_c.file_uploader(
            "Subir CSV o TXT",
            type=["csv", "txt"],
            label_visibility="collapsed",
            key="uploader",
            on_change=handle_upload,
        )
        st.caption("Los datos de ejemplo son reseñas sintéticas de «TecnoHogar», una PYME ficticia.")

        if "result_manual" in st.session_state:
            render_results(st.session_state.result_manual)

    # ----- Ajustes -----
    with tab_ajustes:
        st.markdown("**Zona de mantenimiento**")
        st.caption("Borrar los comentarios recibidos (útil antes de una demo).")
        confirmar = st.checkbox("Sí, quiero borrar TODOS los comentarios recibidos")
        if st.button("🗑️ Borrar comentarios", disabled=not confirmar):
            delete_all()
            st.session_state.pop("result_recibidos", None)
            st.success("Comentarios borrados.")
            st.rerun()

    with st.expander("ℹ️ Cómo se calcula la prioridad"):
        st.markdown(
            """
Cada comentario recibe una **puntuación de sentimiento** (−100 a +100, léxico
en español con negaciones e intensificadores), una **urgencia** (0–100, por
palabras críticas, mayúsculas y exclamaciones) y uno o varios **temas** por
palabras clave.

La **prioridad** de cada tema combina su frecuencia (35 %), el porcentaje de
comentarios negativos (40 %) y la urgencia media (25 %).
"""
        )


# --------------------------------------------------------------------------- #
# Enrutado: cliente por defecto, dueño con contraseña en la barra lateral
# --------------------------------------------------------------------------- #
st.sidebar.title("SmartFeedback")
rol = st.sidebar.radio("¿Quién eres?", ["👤 Soy cliente", "🔑 Soy el dueño"])

if rol == "👤 Soy cliente":
    render_cliente()
else:
    password = st.sidebar.text_input("Contraseña del panel", type="password")
    password_correcta = _secret("PANEL_PASSWORD", "demo1234")
    if not password:
        st.sidebar.info("Introduce la contraseña para ver el panel de análisis.")
        render_cliente()
    elif password != password_correcta:
        st.sidebar.error("Contraseña incorrecta.")
        render_cliente()
    else:
        st.sidebar.success("Acceso concedido ✅")
        render_panel()

st.sidebar.divider()
st.sidebar.caption(
    "SmartFeedback · Herramienta gratuita · Sin claves de API en el código · "
    "Los comentarios se guardan de forma anónima"
)
