import streamlit as st

st.title("SmartFeedback")

comentario = st.text_input("Escribe un comentario de cliente:")

if comentario:
    st.write(f"Comentario recibido: {comentario}")
