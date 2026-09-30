import streamlit as st
from openai import OpenAI
import os

st.set_page_config(
    page_title="Churras AI",
    page_icon="🔥"
)

st.title("🔥 Churras AI")
st.subheader("Seu assistente inteligente para churrasco")

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("Chave da OpenAI não configurada.")
    st.stop()

client = OpenAI(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": """
Você é o Churras AI, um assistente especializado
em churrasco profissional e doméstico.

Ajude com:

- cortes de carne
- técnicas de churrasqueira
- fogo e brasa
- defumação
- temperos
- receitas
- quantidade de carne
- custos
- precificação
- cardápios
- ideias para churrasqueiros profissionais

Responda de maneira prática, clara e amigável.
"""
        }
    ]

for message in st.session_state.messages:

    if message["role"] != "system":

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

prompt = st.chat_input(
    "Ex: Vou fazer churrasco para 30 pessoas. Quanto de carne preciso?"
)

if prompt:

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    response = client.chat.completions.create(
        model="gpt-5.6",
        messages=st.session_state.messages
    )

    answer = response.choices[0].message.content

    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
