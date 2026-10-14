# Especificación · SmartFeedback

> Analizador inteligente de comentarios y prioridades de clientes para pymes.

## 1. Problema y usuario

* **Quién tiene el problema:** el/la responsable de una pyme (tienda online o negocio local) que recibe comentarios de clientes por la web, reseñas o correo.

* **Cómo lo resuelve hoy:** los lee a mano cuando tiene tiempo, o directamente no los lee; no hay ningún análisis.

* **Qué le molesta de cómo lo hace hoy:** los comentarios se acumulan sin orden; no sabe qué es urgente ni qué temas se repiten, y los clientes no reciben ninguna respuesta inmediata.

* **Qué parte resuelve la IA:** entender el texto libre del cliente, clasificarlo por tema y urgencia y redactar una primera respuesta útil. **Qué queda fuera:** responder públicamente en nombre de la empresa y la conexión en tiempo real con redes sociales (ver apartado 8).

## 2. Qué hace el producto

1. **Chat «¿Necesitas ayuda?»** para el cliente: escribe su comentario y recibe al momento una respuesta útil según el tema (pedidos, devoluciones, producto, atención…).
2. **Panel del dueño con contraseña:** clasifica todos los comentarios por tema, sentimiento y prioridad, con gráficos.
3. **Informe descargable** con el resumen de lo que más se repite y lo más urgente.

## 3. Entradas y salidas

| El usuario da…                         | La app devuelve…                                              | Ejemplo                                                    |
| -------------------------------------- | ------------------------------------------------------------- | ---------------------------------------------------------- |
| Un comentario en texto libre (cliente) | Una respuesta de ayuda inmediata y el registro del comentario | «mi pedido no ha llegado» → pasos para localizar el pedido |
| Comentarios acumulados (dueño)         | Tabla y gráficos por tema, sentimiento y prioridad, e informe | «3 quejas de envío esta semana, prioridad alta»            |

## 4. La pieza de IA

* **Opción elegida:** API de un LLM (Gemini, modelo `gemini-3.8-flash`, SDK `google-genai`).

* **Por qué:** clasifica y redacta sobre texto libre en español sin necesidad de entrenar ni etiquetar datos; la capa gratuita sobra para este uso.

* **Instrucciones para el modelo (system prompt):** «Eres el asistente de atención al cliente de una pyme. Clasifica cada comentario en un tema (pedidos, devoluciones, producto, atención, precio, web, tiempos, instalaciones) y una urgencia (alta, media, baja), y responde al cliente en español, con frases cortas, amables y accionables. Si el mensaje no trata de la tienda, di amablemente que solo puedes ayudar con temas de atención al cliente. No inventes datos de pedidos.»

* **Respaldo:** si la API falla o se agota la cuota, la app usa un motor local de reglas (palabras clave) y muestra un mensaje claro al usuario; nunca un error en rojo.

## 5. Flujo del usuario

**Cliente:**

1. Abre la URL y ve solo el chat «¿Necesitas ayuda?».
2. Escribe su comentario.
3. Recibe una respuesta útil al momento; su comentario queda registrado de forma anónima.

**Dueño:**

1. Abre la barra lateral (flecha ›) → «Acceso del equipo».
2. Escribe la contraseña del panel.
3. Pulsa «Actualizar» y «Analizar comentarios»: ve temas, prioridades y gráficos, y descarga el informe.

## 6. Restricciones

* Coste cero: capa gratuita de la API de Gemini, Streamlit Community Cloud y Supabase, todo gratis.

* Las claves van en secretos (`st.secrets` en Streamlit Cloud), nunca en el código.

* Sin datos personales reales: los ejemplos son inventados y el cliente no da ningún dato.

* Lenguaje sencillo, para alguien sin conocimientos técnicos: el cliente solo ve un chat y el dueño solo necesita una contraseña y dos botones.

* El panel del dueño está protegido con contraseña y escondido de la vista del cliente.

## 7. Criterios de aceptación

La app está bien si:

| Entrada                                        | Resultado esperado                                                                          |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------- |
| «mi pedido no ha llegado»                      | Respuesta con pasos para el pedido; se guarda con tema «envío/pedidos» y prioridad alta     |
| «quiero devolver un producto»                  | Respuesta con los pasos de devolución; tema «devoluciones»                                  |
| Texto vacío o solo espacios                    | No se guarda nada; aviso amable pidiendo que escriba algo                                   |
| «¿quién ganó el partido ayer?» (fuera de tema) | Respuesta amable diciendo que solo puede ayudar con temas de atención al cliente            |
| Cuota de la API agotada o sin conexión         | La app responde con el motor local y muestra un mensaje claro, sin errores en rojo          |
| Fallo al guardar en la base de datos           | El cliente ve «no he podido registrarlo por un problema técnico, inténtalo en unos minutos» |
| Contraseña del panel incorrecta                | Aviso de contraseña incorrecta; se sigue mostrando solo el chat                             |

## 8. Fuera de alcance (por ahora)

* Conexión en tiempo real con Instagram u otras redes (exige revisión de app de Meta, inviable en 4 semanas).

* Respuesta automática pública en nombre de la empresa.

* Multi-idioma y panel con usuarios y roles.

## 9. Despliegue

* **Ruta:** A (Streamlit Community Cloud), desde el repositorio público de GitHub.

* **Base de datos:** Supabase (plan gratuito), tabla `comentarios` con permisos para el rol `anon`.

