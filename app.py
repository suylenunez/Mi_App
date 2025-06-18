import streamlit as st
import requests

# Leer API key desde secrets.toml
API_KEY = st.secrets["GROQ_API_KEY"]
API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Modelos disponibles
modelos = ["llama3-8b-8192", "llama3-70b-8192", "mixtral-8x7b-32768", "gemma-7b-it"]

# Inicializar historial
if "messages" not in st.session_state:
    st.session_state.messages = []

# Configuración lateral
st.sidebar.title("Configuración de la IA")
modelo_seleccionado = st.sidebar.selectbox("Seleccionar modelo", modelos)

# Título
st.title("🧠 Mi chat de IA")

# Mostrar historial del chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Entrada del usuario
entrada = st.chat_input("Escribí tu mensaje aquí...")

if entrada:
    # Mostrar mensaje del usuario
    st.chat_message("user").markdown(entrada)
    st.session_state.messages.append({"role": "user", "content": entrada})

    # Preparar solicitud a la API de Groq
    payload = {
        "model": modelo_seleccionado,
        "messages": st.session_state.messages,
        "temperature": 0.7
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # Llamar a la API
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]

        # Mostrar respuesta del bot
        st.chat_message("assistant").markdown(content)
        st.session_state.messages.append({"role": "assistant", "content": content})

    except Exception as e:
        st.error(f"Error al llamar a la API: {e}")
