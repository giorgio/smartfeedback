# Analizador de Comentarios de Clientes

Herramienta web que analiza los comentarios de los clientes de una PYME
(reseñas, encuestas, mensajes de soporte) y devuelve **qué temas hay que
arreglar primero**, con prioridades ordenadas, acciones sugeridas y un
informe descargable.

Pensada para personas **sin perfil técnico**: pegar → analizar → actuar.

## El problema

Las PYMEs reciben opiniones de clientes por muchos canales (Google, encuestas,
email, WhatsApp) pero no tienen tiempo ni herramientas para sacarles partido:
leen los comentarios uno a uno y deciden por intuición qué arreglar primero.

## El usuario

El/la responsable de una PYME o de atención al cliente, sin conocimientos de
programación ni de análisis de datos. Hoy resuelve el problema leyendo todo a
mano (o no leyéndolo). La app le da en 10 segundos lo que le llevaría una tarde.

## Qué hace la app

1. **Entrada flexible**: pegar comentarios (uno por línea), subir un CSV/TXT
   o cargar datos de ejemplo sintéticos.
2. **Análisis automático**: para cada comentario detecta el sentimiento
   (−100 a +100), la urgencia (0–100) y los temas que toca (precio, atención
   al cliente, envío, calidad, web/app, devoluciones, tiempos de espera,
   instalaciones).
3. **Prioridades de actuación**: ranking que combina frecuencia (35 %),
   porcentaje de negativos (40 %) y urgencia media (25 %), con una acción
   sugerida por tema y los comentarios más urgentes.
4. **Informes descargables**: resumen ejecutivo en Markdown y detalle
   comentario a comentario en CSV.

## Cómo se calcula la prioridad

- **Sentimiento**: léxico en español con negaciones («no me gustó») e
  intensificadores («muy», «súper»), normalizado entre −100 y +100.
- **Urgencia**: palabras críticas («denuncia», «estafa», «cancelar»…),
  mayúsculas sostenidas y signos de exclamación.
- **Temas**: diccionarios de palabras clave por categoría.

## Privacidad y coste

- **100 % local**: el análisis se ejecuta dentro de la propia app; ningún
  comentario se envía a servidores de terceros.
- **Coste cero**: desplegada gratis en Streamlit Community Cloud.
- **Sin claves de API en el código**: la versión 0 no necesita ninguna clave.
  La pieza de IA con Gemini (semana 3) leerá la clave desde los secretos de
  Streamlit Cloud (`GEMINI_API_KEY` en formato TOML), nunca del repositorio.
- **Sin datos personales reales**: los datos de ejemplo son reseñas sintéticas
  de «TecnoHogar», una PYME ficticia.

## Estructura del repositorio

| Archivo | Qué contiene |
|---|---|
| `app.py` | La interfaz web (Streamlit) |
| `analyzer.py` | El motor de análisis (sentimiento, urgencia, temas, prioridades) |
| `lexicon.py` | El léxico en español y la definición de temas |
| `sample_data.py` | 41 reseñas sintéticas de ejemplo |
| `requirements.txt` | Las librerías que necesita la app |
| `.streamlit/secrets.toml.example` | Plantilla para la clave de Gemini (semana 3) |

## Ejecutar en local

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Despliegue (Streamlit Community Cloud)

1. Subir este repositorio a GitHub (público).
2. En [share.streamlit.io](https://share.streamlit.io), **Create app**,
   eligiendo el repositorio, la rama `main` y el archivo `app.py`.
3. La app queda en `https://<nombre>.streamlit.app` y se redespliega sola
   con cada cambio subido a GitHub.

## Registro de prompts

Durante el desarrollo se han usado asistentes de IA para generar y revisar el
código (ver el apartado correspondiente del documento de entrega).
