# SmartFeedback

**Enlace a la app:** https://smartfeedback-vtgeqwtt82kmzgrbtmytht.streamlit.app/
**Autor/a:** Jorge Recabarren

## Pitch

Las pymes reciben comentarios de clientes por la web, reseñas y correos, pero nadie los analiza: se acumulan sin saber qué es urgente ni qué se repite. SmartFeedback es un chat «¿Necesitas ayuda?» donde el cliente deja su comentario y recibe una respuesta útil al momento, y un panel donde el dueño ve todos los comentarios clasificados por tema y prioridad. La IA entiende texto libre en español y decide el tema y la urgencia de cada mensaje, algo que a mano costaría horas cada semana. De la primera prueba aprendí que un cliente no debe ver nada del panel, y cambié la entrada para esconderlo tras una contraseña. El siguiente paso es conectar la IA de verdad (Gemini) para que las respuestas se adapten a cada comentario, no solo a su tema.

## El problema

El responsable de una pyme recibe comentarios de clientes por varios canales y los revisa a mano cuando tiene tiempo, o no los revisa. Así no sabe qué quejas son urgentes ni qué problemas se repiten, y los clientes se quedan sin respuesta. Merece la pena resolverlo porque una mala experiencia sin respuesta es un cliente que no vuelve, y estas empresas no tienen presupuesto ni perfil técnico para contratar una herramienta a medida.

## Qué hace la app

1. El cliente abre la URL y ve un chat «¿Necesitas ayuda?»: escribe su comentario y recibe al momento una respuesta útil según el tema (pedidos, devoluciones, producto, atención…).
2. El comentario queda guardado de forma anónima.
3. El dueño entra al panel desde la barra lateral con una contraseña, pulsa «Actualizar» y «Analizar», y ve los comentarios clasificados por tema, sentimiento y prioridad, con gráficos y un informe descargable.

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

## Ejecutar en local (opcional)

```bash
pip install -r requirements.txt
# Poned SUPABASE_URL, SUPABASE_KEY y PANEL_PASSWORD en .streamlit/secrets.toml
streamlit run app.py
```

## Capturas

[La app funcionando, la app ante un caso límite o error, un momento del trabajo con la IA y la prueba. Sin ninguna clave a la vista.]
