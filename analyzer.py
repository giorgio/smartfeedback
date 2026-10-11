"""Motor de análisis de comentarios de clientes.

Todo el procesamiento es local: ningún dato sale del equipo del usuario.
Puerto directo del motor TypeScript del prototipo (mismos algoritmos y pesos).
"""

import math
import re
import unicodedata
from dataclasses import dataclass, field
from datetime import datetime

from lexicon import (
    POSITIVE_WORDS,
    NEGATIVE_WORDS,
    INTENSIFIERS,
    DIMINISHERS,
    NEGATIONS,
    URGENCY_WORDS,
    TOPICS,
    STOPWORDS,
)

POSITIVO, NEUTRO, NEGATIVO = "positivo", "neutro", "negativo"


@dataclass
class CommentAnalysis:
    id: int
    text: str
    sentiment: str
    sentiment_score: int  # -100 (muy negativo) a +100 (muy positivo)
    urgency: int  # 0 a 100
    topics: list = field(default_factory=list)
    keywords: list = field(default_factory=list)


@dataclass
class TopicPriority:
    topic_id: str
    label: str
    mentions: int
    negative_count: int
    negative_pct: int
    avg_urgency: int
    priority_score: int  # 0 a 100
    action: str
    examples: list = field(default_factory=list)


@dataclass
class AnalysisResult:
    total: int
    analyzed_at: datetime
    comments: list
    sentiment_counts: dict
    avg_score: int
    avg_urgency: int
    priorities: list
    top_keywords: list
    global_score: int  # 0-100, tipo satisfacción


def normalize(text: str) -> str:
    """Minúsculas y sin tildes (para búsquedas de temas y urgencia)."""
    nfkd = unicodedata.normalize("NFD", text.lower())
    return "".join(c for c in nfkd if unicodedata.category(c) != "Mn")


def tokenize(text: str) -> list:
    """Conserva las tildes para que coincidan con las claves del léxico."""
    return [
        t
        for t in re.sub(r"[^a-záéíóúüñ0-9\s]", " ", text.lower()).split()
        if t
    ]


def analyze_sentiment(tokens: list) -> tuple:
    raw = 0.0
    keywords = []

    for i, t in enumerate(tokens):
        pos = POSITIVE_WORDS.get(t, 0)
        neg = NEGATIVE_WORDS.get(t, 0)
        if not pos and not neg:
            continue

        value = float(pos) if pos > 0 else float(-neg)

        # Modificadores en una ventana de 3 palabras hacia atrás
        multiplier = 1.0
        negated = False
        for w in tokens[max(0, i - 3):i]:
            if w in NEGATIONS:
                negated = True
            if w in INTENSIFIERS:
                multiplier = max(multiplier, 1.6)
            if w in DIMINISHERS:
                multiplier = min(multiplier, 0.5)
        if negated:
            value = -value * 0.8
        value *= multiplier

        raw += value
        keywords.append(t)

    # Normalizar a -100..100 con saturación suave
    score = round(100 * math.tanh(raw / 6))
    return score, keywords


def analyze_urgency(text: str, tokens: list, sentiment_score: int) -> int:
    urgency = 0
    norm = normalize(text)

    for phrase, weight in URGENCY_WORDS.items():
        if normalize(phrase) in norm:
            urgency += weight

    # Signos de exclamación y mayúsculas sostenidas
    urgency += min(len(re.findall(r"!", text)) * 6, 18)
    urgency += min(len(re.findall(r"\b[A-ZÁÉÍÓÚÑ]{4,}\b", text)) * 8, 24)

    # Comentarios negativos largos suelen implicar más implicación emocional
    if sentiment_score < -30:
        urgency += 15
    if sentiment_score < -60:
        urgency += 10
    if len(tokens) > 60:
        urgency += 5

    return min(100, round(urgency))


def detect_topics(text: str) -> list:
    norm = normalize(text)
    return [
        topic["id"]
        for topic in TOPICS
        if any(normalize(k) in norm for k in topic["keywords"])
    ]


def analyze_comments(texts: list) -> AnalysisResult:
    clean = [t.strip() for t in texts if t and len(t.strip()) > 2]

    comments = []
    for i, text in enumerate(clean, start=1):
        tokens = tokenize(text)
        score, keywords = analyze_sentiment(tokens)
        urgency = analyze_urgency(text, tokens, score)
        topics = detect_topics(text)
        sentiment = POSITIVO if score >= 15 else (NEGATIVO if score <= -15 else NEUTRO)
        comments.append(
            CommentAnalysis(i, text, sentiment, score, urgency, topics, keywords)
        )

    sentiment_counts = {POSITIVO: 0, NEUTRO: 0, NEGATIVO: 0}
    for c in comments:
        sentiment_counts[c.sentiment] += 1

    # Prioridad por tema: frecuencia x negatividad x urgencia media
    by_topic = {}
    for c in comments:
        for t in (c.topics or ["otros"]):
            by_topic.setdefault(t, []).append(c)

    max_mentions = max([len(v) for v in by_topic.values()], default=1)

    priorities = []
    for topic_id, lst in by_topic.items():
        topic_def = next((t for t in TOPICS if t["id"] == topic_id), None)
        negative = [c for c in lst if c.sentiment == NEGATIVO]
        negative_pct = len(negative) / len(lst) if lst else 0
        avg_urgency = sum(c.urgency for c in lst) / len(lst)
        frequency_score = len(lst) / max_mentions
        priority_score = round(
            100 * (0.35 * frequency_score + 0.40 * negative_pct + 0.25 * (avg_urgency / 100))
        )
        examples = [c.text for c in sorted(lst, key=lambda c: -c.urgency)[:3]]
        priorities.append(
            TopicPriority(
                topic_id=topic_id,
                label=topic_def["label"] if topic_def else "Otros temas",
                mentions=len(lst),
                negative_count=len(negative),
                negative_pct=round(negative_pct * 100),
                avg_urgency=round(avg_urgency),
                priority_score=priority_score,
                action=topic_def["action"]
                if topic_def
                else "Revisar manualmente los comentarios sin categoría para detectar temas emergentes.",
                examples=examples,
            )
        )
    priorities.sort(key=lambda p: -p.priority_score)

    # Palabras clave más repetidas (sin stopwords)
    freq = {}
    for c in comments:
        for t in tokenize(c.text):
            if len(t) < 4 or t in STOPWORDS:
                continue
            entry = freq.setdefault(t, {"count": 0, "neg": 0, "pos": 0})
            entry["count"] += 1
            if c.sentiment == NEGATIVO:
                entry["neg"] += 1
            if c.sentiment == POSITIVO:
                entry["pos"] += 1
    top_keywords = [
        {"word": w, "count": v["count"], "negative": v["neg"] > v["pos"]}
        for w, v in sorted(freq.items(), key=lambda kv: -kv[1]["count"])[:15]
    ]

    avg_score = round(sum(c.sentiment_score for c in comments) / len(comments)) if comments else 0
    avg_urgency = round(sum(c.urgency for c in comments) / len(comments)) if comments else 0
    global_score = round((avg_score + 100) / 2)

    return AnalysisResult(
        total=len(comments),
        analyzed_at=datetime.now(),
        comments=comments,
        sentiment_counts=sentiment_counts,
        avg_score=avg_score,
        avg_urgency=avg_urgency,
        priorities=priorities,
        top_keywords=top_keywords,
        global_score=global_score,
    )


def split_comments(raw: str) -> list:
    """Divide un texto pegado en comentarios: uno por línea no vacía."""
    return [line.strip() for line in raw.splitlines() if line.strip()]


def parse_csv(content: str) -> list:
    """Parser CSV con detección de separador y de columna de comentarios."""
    import csv
    import io as _io

    first_line = content.splitlines()[0] if content.splitlines() else ""
    delimiter = ";" if first_line.count(";") > first_line.count(",") else ","
    rows = [r for r in csv.reader(_io.StringIO(content), delimiter=delimiter) if any(c.strip() for c in r)]
    if not rows:
        return []

    header = [normalize(h.strip()) for h in rows[0]]
    header_names = [
        "comentario", "comentarios", "comment", "comments", "review",
        "resena", "opinion", "opiniones", "texto", "feedback", "mensaje",
    ]
    col_index = next(
        (i for i, h in enumerate(header) if any(n in h for n in header_names)), -1
    )
    has_header = col_index >= 0
    data_rows = rows[1:] if has_header else rows
    col = col_index if has_header else 0
    return [
        r[col].strip() for r in data_rows if len(r) > col and len(r[col].strip()) > 2
    ]


def to_csv(result: AnalysisResult) -> str:
    """Genera el informe CSV de resultados (separador ;)."""
    topic_label = {t["id"]: t["label"] for t in TOPICS}

    def esc(s: str) -> str:
        return '"' + s.replace('"', '""') + '"'

    lines = ["id;comentario;sentimiento;puntuacion_sentimiento;urgencia;temas"]
    for c in result.comments:
        labels = ", ".join(topic_label.get(t, t) for t in c.topics)
        lines.append(
            f"{c.id};{esc(c.text)};{c.sentiment};{c.sentiment_score};{c.urgency};{esc(labels)}"
        )
    return "\r\n".join(lines)


def to_markdown_report(result: AnalysisResult) -> str:
    """Genera el informe ejecutivo en Markdown."""
    s, total = result.sentiment_counts, result.total
    pct = lambda n: round(n / total * 100) if total else 0
    # Formato de fecha manual (strftime('%-d') no funciona en Windows)
    meses = ["enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"]
    d = result.analyzed_at
    fecha = f"{d.day} de {meses[d.month - 1]} de {d.year}"

    lines = [
        "# Informe de análisis de comentarios de clientes",
        "",
        f"Fecha del análisis: {fecha} · Comentarios analizados: {total}",
        "",
        "## Resumen",
        "",
        f"- Índice global de satisfacción: **{result.global_score}/100**",
        f"- Positivos: {s[POSITIVO]} ({pct(s[POSITIVO])} %) · Neutros: {s[NEUTRO]} ({pct(s[NEUTRO])} %) · Negativos: {s[NEGATIVO]} ({pct(s[NEGATIVO])} %)",
        f"- Urgencia media: {result.avg_urgency}/100",
        "",
        "## Prioridades de actuación",
        "",
    ]
    for i, p in enumerate(result.priorities, start=1):
        lines += [
            f"### {i}. {p.label} — prioridad {p.priority_score}/100",
            "",
            f"- Menciones: {p.mentions} · Negativas: {p.negative_pct} % · Urgencia media: {p.avg_urgency}/100",
            f"- Acción sugerida: {p.action}",
        ]
        if p.examples:
            lines.append("- Comentarios destacados:")
            lines += [f'  - "{e}"' for e in p.examples]
        lines.append("")

    lines += [
        "---",
        "Informe generado localmente con el Analizador de Comentarios de Clientes. Ningún dato ha salido del navegador.",
    ]
    return "\n".join(lines)
