import streamlit as st
from rag import ask_customer_assistant

st.set_page_config(
    page_title="Customer Support Assistant",
    page_icon="💬",
    layout="centered"
)

st.title("💬 Customer Support Assistant")

st.caption(
    "Tanyakan apa saja seputar pesanan, pembatalan, refund, "
    "dan hal lain terkait layanan pelanggan."
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input(
    "Tulis pertanyaanmu di sini..."
)

if question:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Mencari informasi..."):
            result = ask_customer_assistant(question)
            answer = result["answer"]

        st.markdown(answer)

        with st.expander("📚 Sumber informasi"):
            for source in result["sources"]:
                st.write(
                    "**" + str(source.metadata.get("title")) + "**"
                )
                st.caption(
                    source.metadata.get("source")
                )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )