# Título principal
import streamlit as st
import requests

API_URL = "https://api.groq.com/openai/v1/chat/completions"
modelos = ["llama3-8b-8192", "llama3-70b-8192", "mixtral-8x7b-32768", "gemma-7b-it"]

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Barra lateral para configuración ---
st.sidebar.title("Configuración de la IA")

# Entrada de la clave en la interfaz (no se guarda)
API_KEY = st.sidebar.text_input("🔐 Ingresá tu API Key de Groq", type="password")

# Selección de modelo
modelo_seleccionado = st.sidebar.selectbox("Seleccionar modelo", modelos)

st.title("🧠 Mi chat de IA")

# Mostrar mensajes anteriores
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Entrada de mensaje
entrada = st.chat_input("Escribí tu mensaje aquí...")

if entrada:
    # Verificar que se ingresó la clave
    if not API_KEY:
        st.warning("Por favor, ingresá tu API Key en la barra lateral.")
        st.stop()

    st.chat_message("user").markdown(entrada)
    st.session_state.messages.append({"role": "user", "content": entrada})

    payload = {
        "model": modelo_seleccionado,
        "messages": st.session_state.messages,
        "temperature": 0.7
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]

        st.chat_message("assistant").markdown(content)
        st.session_state.messages.append({"role": "assistant", "content": content})

    except Exception as e:
        st.error(f"Error al llamar a la API: {e}")
