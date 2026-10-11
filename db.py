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


class StorageError(Exception):
    """Error al guardar o leer comentarios (p. ej., permisos de Supabase)."""


def save_comment(text: str) -> None:
    """Guarda un comentario nuevo. Lanza StorageError si falla."""
    text = text.strip()
    if not text:
        return
    try:
        if use_supabase():
            _client().table(TABLE).insert({"texto": text}).execute()
        else:
            is_new = not os.path.exists(LOCAL_FILE)
            with open(LOCAL_FILE, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                if is_new:
                    writer.writerow(["fecha", "texto"])
                writer.writerow([datetime.now().isoformat(timespec="seconds"), text])
    except Exception as e:  # la app nunca debe romperse delante del cliente
        raise StorageError(str(e)) from e


def load_comments() -> list:
    """Devuelve todos los comentarios guardados (solo los textos)."""
    try:
        if use_supabase():
            res = _client().table(TABLE).select("texto").order("id").execute()
            return [row["texto"] for row in res.data if row.get("texto")]
        if not os.path.exists(LOCAL_FILE):
            return []
        with open(LOCAL_FILE, encoding="utf-8") as f:
            return [row["texto"] for row in csv.DictReader(f) if row.get("texto")]
    except Exception as e:
        raise StorageError(str(e)) from e


def delete_all() -> None:
    """Borra todos los comentarios (para pruebas y para la demo)."""
    try:
        if use_supabase():
            _client().table(TABLE).delete().neq("texto", "").execute()
        elif os.path.exists(LOCAL_FILE):
            os.remove(LOCAL_FILE)
    except Exception as e:
        raise StorageError(str(e)) from e
