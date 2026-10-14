# AGENTS.md · SmartFeedback

> Este fichero lo leen los agentes de programación antes de tocar el código.

## Qué es este proyecto

Analizador inteligente de comentarios de clientes para pymes: un chat «¿Necesitas ayuda?» donde el cliente deja su comentario y recibe ayuda al momento, y un panel con contraseña donde el dueño ve los comentarios clasificados por tema y prioridad.

## Cómo está hecho

- Python 3.12.
- Interfaz: Streamlit (ruta A, desplegada en Streamlit Community Cloud).
- Almacenamiento: Supabase (tabla `comentarios`), con respaldo en CSV local si no hay credenciales.
- IA (semana 3): API de Gemini con el SDK `google-genai`, clave en `st.secrets["GEMINI_API_KEY"]`, con el motor local de reglas de `analyzer.py` como respaldo.
- Archivos: `app.py` (interfaz y enrutado), `analyzer.py` (clasificación por tema, sentimiento y prioridad), `lexicon.py` (temas y respuestas de ayuda), `db.py` (guardado en Supabase/CSV), `sample_data.py` (ejemplos inventados), `requirements.txt` y `README.md`.
- La especificación completa está en `especificacion.md`.

## Reglas

- Las claves van SIEMPRE en secretos (`st.secrets` en Streamlit Cloud): `SUPABASE_URL`, `SUPABASE_KEY`, `PANEL_PASSWORD` y `GEMINI_API_KEY`. Nunca en el código, en el README ni en el chat.
- Cada llamada a la API o a la base de datos va dentro de `try/except` y muestra un mensaje claro y amable para el usuario; nunca un error en rojo.
- Textos de la interfaz en español, sencillos, pensados para alguien sin conocimientos técnicos.
- El cliente solo ve el chat: ningún control del panel puede ser visible para él.
- Cambios pequeños: uno por petición. Al terminar, explica qué has cambiado y por qué.
- Si añades una librería, añádela también a `requirements.txt` y dilo.
- No uses datos personales reales. Para probar, inventa ejemplos.

## Cómo comprobar que funciona

- En local: `streamlit run app.py` (con `.streamlit/secrets.toml`), o haz push y revisa la app en Streamlit Cloud.
- Casos de prueba (entrada → lo que esperamos):
  1. «mi pedido no ha llegado» → respuesta con pasos para el pedido; se guarda con tema envío y prioridad alta.
  2. «quiero devolver un producto» → respuesta con los pasos de devolución.
  3. «¿quién ganó el partido?» → la app dice amablemente que solo ayuda con temas de atención al cliente.
  4. Panel: contraseña correcta → aparecen los comentarios clasificados; contraseña incorrecta → aviso y solo se ve el chat.

## Qué no hacer

- No borres ni reescribas el README sin preguntar.
- No cambies el modelo ni la arquitectura (chat + panel, Supabase) sin preguntar.
- No hagas push ni despliegues sin que yo lo haya revisado.
