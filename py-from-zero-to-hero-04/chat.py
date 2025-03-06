## start using:
## => python -m venv .venv
## => .venv\Scripts\activate
## => pip install -r .\requirements.txt
## => python -m streamlit run chat.py

import streamlit as st
import requests
import uuid

from config import config_class

st.markdown("<h1 style='text-align: center;'>Best Price</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Customer Service</h3>", unsafe_allow_html=True)

left_co, cent_co,last_co = st.columns(3)
with cent_co:
    st.image("best-price-logo.png", caption="Best Price")

# generate a client_id to be used during the chat
if "client_id" not in st.session_state:
    st.session_state.client_id = str(uuid.uuid4())

# load messages
if "messages" not in st.session_state:
    st.session_state.messages = []

def ask_question(question):
    url = config_class.APP_BACKEND_URL + "/info"
    payload = {
        "client_id": st.session_state.client_id,
        "question": question
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json().get("answer", "Error trying to get the server answer.")
    return f"Erro: {response.status_code} - {response.text}"

# load messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# app start
prompt = st.chat_input("Type your question:")
if prompt:
    # Add user messages to the history
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)
    
    # GEt the api answer
    answer = ask_question(prompt)
    
    # Add assistant messages to the history
    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)