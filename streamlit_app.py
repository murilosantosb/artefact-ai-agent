import uuid

import streamlit as st 

from src.agent.graph import agent

st.set_page_config(
    page_title="Empório da Música",
    page_icon="🎸",
)

st.title("🎸 Empório da Música")
st.caption("Assistente virtual de atendimento")


# Initialize session
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []


# Start a new conversation
if st.sidebar.button("Nova conversa"):
    st.session_state.thread_id = str(uuid.uuid4())
    st.session_state.messages = []
    st.rerun()


# Display conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Receive customer message
if prompt := st.chat_input("Como posso ajudar?"):

    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    config = {
        "configurable": {
            "thread_id": st.session_state.thread_id
        }
    }

    with st.chat_message("assistant"):
        with st.spinner("Consultando informações..."):
            try:
                result = agent.invoke(
                    {
                        "messages": [
                            {"role": "user", "content": prompt}
                        ]
                    },
                    config=config,
                )

                response = result["messages"][-1].content

            except Exception:
                response = (
                    "Desculpe, ocorreu um erro ao processar "
                    "sua mensagem. Tente novamente."
                )

        st.markdown(response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
    })