# SmartFeedback · Analizador de Comentarios de Clientes

**Enlace a la app:** https://smartfeedback-vtgeqwtt82kmzgrbtmytht.streamlit.app/
**Autor/a:** Jorge Recabarren

Herramienta web que recoge las opiniones de los clientes de una PYME y
devuelve **qué hay que arreglar primero**: temas, prioridades ordenadas,
acciones sugeridas e informe descargable. Pensada para personas **sin perfil
técnico**: el cliente escribe, el dueño mira el panel.

## Pitch

Las pymes reciben comentarios de clientes por la web, reseñas y correos, pero nadie los analiza: se acumulan sin saber qué es urgente ni qué se repite. SmartFeedback es un chat «¿Necesitas ayuda?» donde el cliente deja su comentario y recibe una respuesta útil al momento, y un panel donde el dueño ve todos los comentarios clasificados por tema y prioridad. La IA entiende texto libre en español y decide el tema y la urgencia de cada mensaje, algo que a mano costaría horas cada semana. De la primera prueba aprendí que un cliente no debe ver nada del panel, y cambié la entrada para esconderlo tras una contraseña. El siguiente paso es conectar la IA de verdad (Gemini) para que las respuestas se adapten a cada comentario, no solo a su tema.

## El problema

El responsable de una pyme recibe comentarios de clientes por varios canales y los revisa a mano cuando tiene tiempo, o no los revisa. Así no sabe qué quejas son urgentes ni qué problemas se repiten, y los clientes se quedan sin respuesta. Merece la pena resolverlo porque una mala experiencia sin respuesta es un cliente que no vuelve, y estas empresas no tienen presupuesto ni perfil técnico para contratar una herramienta a medida.

## El usuario

El/la responsable de una PYME, sin conocimientos de programación ni de
análisis de datos. Con SmartFeedback comparte un enlace o un QR con sus
clientes y obtiene en segundos el análisis que antes le costaba una tarde.

## Qué hace la app

1. El cliente abre la URL y ve un chat «¿Necesitas ayuda?»: escribe su comentario y recibe al momento una respuesta útil según el tema (pedidos, devoluciones, producto, atención…). El comentario queda guardado de forma anónima.
2. El dueño entra al panel desde la barra lateral con una contraseña, pulsa «Actualizar» y «Analizar», y ve los comentarios clasificados por tema, sentimiento y prioridad, con gráficos y un informe descargable.

### Cómo funciona: doble puerta

1. **Puerta del cliente** (la URL pública): un chat «¿Necesitas ayuda?» donde
   el cliente cuenta su experiencia. El comentario se guarda al instante y
   recibe una respuesta de agradecimiento personalizada según su tono.
2. **Puerta del dueño** (barra lateral, con contraseña): el panel de análisis.
   - Pestaña *Comentarios recibidos*: los que van llegando del chat, con un
     botón para analizarlos.
   - Pestaña *Análisis manual*: pegar texto, subir CSV/TXT o cargar los datos
     de ejemplo sintéticos.
   - Pestaña *Ajustes*: borrado de comentarios para preparar demos.

### Qué analiza

Para cada comentario detecta el **sentimiento** (−100 a +100, con léxico en
español que entiende negaciones como «no me gustó» e intensificadores como
«muy»), la **urgencia** (0–100, por palabras críticas como «denuncia» o
«cancelar», mayúsculas y exclamaciones) y los **temas** (precio, atención al
cliente, envío, calidad, web/app, devoluciones, tiempos de espera e
instalaciones). La **prioridad** de cada tema combina frecuencia (35 %),
porcentaje de negativos (40 %) y urgencia media (25 %).

## La pieza de IA

- **Qué usa:** API de Gemini (modelo `gemini-3.8-flash`, SDK `google-genai`) para clasificar tema y urgencia y redactar las respuestas; un motor local de reglas hace hoy esa función y queda como respaldo.
- **Por qué esa opción:** clasifica texto libre en español sin entrenar ni etiquetar datos, y la capa gratuita sobra para este volumen.
- **Qué pasa si falla:** la app responde con el motor local y muestra un mensaje claro («ahora mismo no puedo responder, prueba en un minuto»); si falla el guardado, el cliente ve un aviso amable de problema técnico. Nunca un error en rojo.

## Cómo la he construido

- **Herramientas:** Kimi (agente de programación) para generar y corregir el código, GitHub desde la web, Streamlit Community Cloud y Supabase.
- **Fichero de contexto del agente:** [AGENTS.md](AGENTS.md)
- **Prompts clave:**
  1. «Quisiera hacer un analizador inteligente de comentarios y prioridades de clientes.»
  2. «El programa debería discernir si el mensaje es sobre la atención al cliente, pedidos, quejas, etc.»
  3. «El mensaje que debería recibir el cliente debería ser "¿necesitas ayuda?" y poder entregarle la ayuda.»
  4. «Eso no debería estar ahí» (sobre el selector cliente/dueño visible; resultado: acceso del dueño escondido en la barra lateral).
  5. «El proyecto no puede usar clave API en el código, es uno de los requerimientos básicos.»
- **Qué delegué al agente y qué revisé a mano:** delegué la generación del código, la conexión con Supabase y el diagnóstico de errores; revisé a mano, probando la app desplegada, que el chat respondiera con sentido, que el guardado funcionara de verdad y que el cliente no viera nada del panel.

## Prueba y mejora

| Quién la probó | Qué probó | Qué pasó | Qué cambié |
|---|---|---|---|
| Yo, como cliente | Enviar «mi pedido no ha llegado» | El chat respondía pero no se guardaba: la clave de Supabase estaba incompleta en Secrets | Corregida la clave y verificado el guardado con una prueba de conexión directa |
| Yo, como cliente | Mirar la página de entrada | Se veía un selector «Soy cliente / Soy el dueño» que un cliente real no debería ver | Escondido el acceso al panel en la barra lateral, con contraseña |
| [compañero/a, semana 3] | | | |

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
| `app.py` | La interfaz web: chat del cliente y panel del dueño (Streamlit), con integración de Gemini y respaldo local |
| `analyzer.py` | El motor de análisis (sentimiento, urgencia, temas, prioridades) |
| `lexicon.py` | El léxico en español y la definición de temas |
| `db.py` | Almacenamiento: Supabase si hay secretos, CSV local como respaldo |
| `sample_data.py` | 41 reseñas sintéticas de ejemplo |
| `requirements.txt` | Las librerías que necesita la app |
| `AGENTS.md` | Fichero de contexto para agentes de programación |
| `especificacion.md` | La especificación del reto (problema, usuario, funcionalidades) |
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
# Poned SUPABASE_URL, SUPABASE_KEY y PANEL_PASSWORD en .streamlit/secrets.toml
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

## Capturas

[La app funcionando, la app ante un caso límite o error, un momento del trabajo con la IA y la prueba. Sin ninguna clave a la vista.]
