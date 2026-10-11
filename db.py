"""Capa de almacenamiento de comentarios.

Dos modos, elegidos automáticamente:

- **Supabase** (nube, gratis): si existen SUPABASE_URL y SUPABASE_KEY en
  st.secrets. Las claves NUNCA van en el código; se configuran en Streamlit
  Cloud (App settings → Secrets, formato TOML).
- **Respaldo local** (archivo CSV): si no hay secretos configurados. Sirve
  para desarrollo y para que la app nunca se rompa por falta de configuración.
"""

import csv
import os
from datetime import datetime

import streamlit as st

LOCAL_FILE = "comentarios_locales.csv"
TABLE = "comentarios"


def _secret(name: str) -> str:
    try:
        return st.secrets.get(name, "")
    except Exception:
        return ""


def use_supabase() -> bool:
    """True si hay credenciales de Supabase configuradas como secretos."""
    return bool(_secret("SUPABASE_URL") and _secret("SUPABASE_KEY"))


def _client():
    # Importación perezosa: la app funciona aunque supabase no esté instalado
    from supabase import create_client

    return create_client(_secret("SUPABASE_URL"), _secret("SUPABASE_KEY"))


def save_comment(text: str) -> None:
    """Guarda un comentario nuevo."""
    text = text.strip()
    if not text:
        return
    if use_supabase():
        _client().table(TABLE).insert({"texto": text}).execute()
    else:
        is_new = not os.path.exists(LOCAL_FILE)
        with open(LOCAL_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if is_new:
                writer.writerow(["fecha", "texto"])
            writer.writerow([datetime.now().isoformat(timespec="seconds"), text])


def load_comments() -> list:
    """Devuelve todos los comentarios guardados (solo los textos)."""
    if use_supabase():
        res = _client().table(TABLE).select("texto").order("id").execute()
        return [row["texto"] for row in res.data if row.get("texto")]
    if not os.path.exists(LOCAL_FILE):
        return []
    with open(LOCAL_FILE, encoding="utf-8") as f:
        return [row["texto"] for row in csv.DictReader(f) if row.get("texto")]


def delete_all() -> None:
    """Borra todos los comentarios (para pruebas y para la demo)."""
    if use_supabase():
        _client().table(TABLE).delete().neq("texto", "").execute()
    elif os.path.exists(LOCAL_FILE):
        os.remove(LOCAL_FILE)
