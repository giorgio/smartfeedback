# SmartFeedback · Analizador de Comentarios de Clientes

Herramienta web que recoge las opiniones de los clientes de una PYME y
devuelve **qué hay que arreglar primero**: temas, prioridades ordenadas,
acciones sugeridas e informe descargable. Pensada para personas **sin perfil
técnico**: el cliente escribe, el dueño mira el panel.

## El problema

Las PYMEs reciben opiniones de clientes por muchos canales pero no tienen
tiempo ni herramientas para sacarles partido: leen los comentarios uno a uno
(o no los leen) y deciden por intuición qué arreglar primero.

## El usuario

El/la responsable de una PYME, sin conocimientos de programación ni de
análisis de datos. Con SmartFeedback comparte un enlace o un QR con sus
clientes y obtiene en segundos el análisis que antes le costaba una tarde.

## Cómo funciona: doble puerta

1. **Puerta del cliente** (la URL pública): un chat «¿Necesitas ayuda?» donde
   el cliente cuenta su experiencia. El comentario se guarda al instante y
   recibe una respuesta de agradecimiento personalizada según su tono.
2. **Puerta del dueño** (barra lateral, con contraseña): el panel de análisis.
   - Pestaña *Comentarios recibidos*: los que van llegando del chat, con un
     botón para analizarlos.
   - Pestaña *Análisis manual*: pegar texto, subir CSV/TXT o cargar los datos
     de ejemplo sintéticos.
   - Pestaña *Ajustes*: borrado de comentarios para preparar demos.

## Qué analiza

Para cada comentario detecta el **sentimiento** (−100 a +100, con léxico en
español que entiende negaciones como «no me gustó» e intensificadores como
«muy»), la **urgencia** (0–100, por palabras críticas como «denuncia» o
«cancelar», mayúsculas y exclamaciones) y los **temas** (precio, atención al
cliente, envío, calidad, web/app, devoluciones, tiempos de espera e
instalaciones). La **prioridad** de cada tema combina frecuencia (35 %),
porcentaje de negativos (40 %) y urgencia media (25 %).

## Privacidad y coste

- **Coste cero**: desplegada en Streamlit Community Cloud (gratis) y con
  Supabase (plan gratuito) como base de datos.
- **Sin claves de API en el código**: todas las credenciales (contraseña del
  panel, Supabase y, en la semana 3, Gemini) se leen desde los **secretos** de
  Streamlit Cloud en formato TOML — ver `.streamlit/secrets.toml.example`.
- **Sin datos personales reales**: el chat no pide nombre ni email, y los
  datos de ejemplo son reseñas sintéticas de «TecnoHogar», una PYME ficticia.

## Estructura del repositorio

| Archivo | Qué contiene |
|---|---|
| `app.py` | La interfaz web: chat del cliente y panel del dueño (Streamlit) |
| `analyzer.py` | El motor de análisis (sentimiento, urgencia, temas, prioridades) |
| `lexicon.py` | El léxico en español y la definición de temas |
| `db.py` | Almacenamiento: Supabase si hay secretos, CSV local como respaldo |
| `sample_data.py` | 41 reseñas sintéticas de ejemplo |
| `requirements.txt` | Las librerías que necesita la app |
| `.streamlit/secrets.toml.example` | Plantilla de secretos (contraseña, Supabase, Gemini) |

## Configuración de Supabase (5 minutos)

1. Crear un proyecto gratuito en [supabase.com](https://supabase.com).
2. En el SQL Editor, crear la tabla:

   ```sql
   create table comentarios (
     id bigint generated always as identity primary key,
     texto text not null,
     creado_en timestamptz default now()
   );
   ```

3. Copiar la URL y la clave `anon public` (Settings → API) a los secretos
   (ver la plantilla). Si no se configura, la app guarda en un CSV local y
   sigue funcionando.

## Ejecutar en local

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Despliegue (Streamlit Community Cloud)

1. Subir este repositorio a GitHub (público).
2. En [share.streamlit.io](https://share.streamlit.io), **Create app**,
   eligiendo el repositorio, la rama `main` y el archivo `app.py`.
3. En **Settings → Secrets** de la app, pegar las líneas de la plantilla de
   secretos (contraseña del panel y, si se usa, Supabase).
4. La app queda en `https://<nombre>.streamlit.app` y se redespliega sola
   con cada cambio subido a GitHub.

## Trabajo futuro

- Pieza de IA con **Gemini** (semana 3): clasificación asistida por modelo de
  lenguaje y acciones sugeridas redactadas en lenguaje natural. La clave se
  leerá de `GEMINI_API_KEY` en secretos; sin clave, la app sigue funcionando
  con el motor local.
- Conexión automática con redes sociales (Instagram): requiere registrar una
  app en Meta for Developers y superar su revisión de permisos (semanas), por
  lo que queda fuera del alcance de este reto.

## Registro de prompts

Durante el desarrollo se han usado asistentes de IA para generar y revisar el
código (ver el apartado correspondiente del documento de entrega).
