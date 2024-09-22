import streamlit as st
from src.pipeline import EduQuery

edu_query = EduQuery()

st.title('Welcome to Edu Query!')

# Chat History
if 'messages' not in st.session_state:
    st.session_state.messages = []
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

prompt = st.chat_input("Ask EduQuery")
if prompt:
    with st.chat_message('user'):
        st.markdown(prompt)

    st.session_state.messages.append({'role': 'user', 'content': prompt})

    response = ''
    try:
        response = edu_query.ask(prompt)
    except Exception as e:
        response = f'Oops! The following issue occurred: {e}'

    with st.chat_message('assistant'):
        st.markdown(response)

    st.session_state.messages.append({'role': 'assistant', 'content': 'response'})
