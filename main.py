import streamlit as st
from rag import chat

st.title("Hospital Enquiry Bot", 
        text_alignment='center')
st.set_page_config(
    page_title="Hospital Enquiry Bot",
    page_icon="🏥",
    layout="centered"
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("Ask a question about the hospital")

if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )
   
    with st.chat_message("user"):
        st.write(question)
    
    response = chat(question)
    answer = response

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    with st.chat_message("assistant"):
        st.markdown(answer)
