import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.colored_header import colored_header
from streamlit_chat import message
import pandas as pd
import numpy as np
import sys
from typing import Optional
from dotenv import load_dotenv
import time
import pyperclip

def main() -> None:

    load_dotenv()

    sys.path.append("../")
    from llm.chat import ChatInstance, Message

    st.set_page_config(
        page_title="AIWriter - AI Content to your heart's desire!"
    )

    conn = st.experimental_connection("enigma_matrix", type="sql")

    with st.sidebar:
        st.title("WriteFinity")
        st.markdown("""
        ## About
        A fully automated content flow tailored to your brand!
        Powered by:
        - [StreamLit](<https://streamlit.io/>)
                    
        💡 Note: API key required!
        """)
        add_vertical_space(16)
        st.write('Made with ❤️ by [Arthur Riechert](<cybrco.ai>)')

    if "chat" not in st.session_state:
        st.session_state["chat"] = ChatInstance([
                Message(role="user", content="Hello, Alfred!"),
                Message(role="assistant", content="Hello, Artie!")
            ],
            api_key=st.secrets["api_keys"]["openai"]
        )

    if "clean_memory" not in st.session_state:
        st.session_state.clean_memory = False

    def get_prompt() -> Optional[str]:
        return st.chat_input(
            placeholder="Your legendary prompt goes here!"
        )

    input_container = st.container()
    colored_header(label='Welcome to WriteFinity!', description='', color_name='blue-30')
    response_container = st.container()

    with input_container:
        prompt = get_prompt()

    with response_container:

        for index, chat in enumerate(st.session_state['chat'].history):
            if chat["role"] == "user":
                with st.chat_message("user"):
                    st.markdown(chat["content"])
            elif chat["role"] == "assistant":
                with st.chat_message("assistant"):
                    st.markdown(chat["content"])
                    if st.button(label="Copy", key=index):
                        pyperclip.copy(chat["content"])
                        status = st.empty()
                        status.success('Successfully copied!', icon="✅")
                        time.sleep(5)
                        status.empty()

        if prompt:
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                assistant = st.empty()

                in_progress = ""
                for message in st.session_state["chat"].stream_completion(prompt):
                    in_progress += message
                    assistant.markdown(in_progress)

                if st.button(label="Copy", key=len(st.session_state["chat"].history)-1):
                    pyperclip.copy(chat["content"])
                    status = st.empty()
                    status.success('Successfully copied!', icon="✅")
                    time.sleep(5)
                    status.empty()


    controls = st.empty()
    memory, model, specs = controls.tabs([
        "Memory",
        "Model",
        "Specs"
    ])

    with specs.container():
        st.write("Max tokens: ", st.session_state["chat"].settings.max_tokens)

    with memory.container():
        st.write(f"Chat history tokens:", st.session_state['chat'].token_count)
        st.progress(
            value=st.session_state["chat"].token_count / st.session_state["chat"].history_allocation,
            text="Remaining tokens"
        )

    c1, c2 = memory.columns(2)
    m1, m2 = model.columns(2)

    st.session_state["chat"].settings.make = m1.selectbox(
        "Make",
        ("openai", "llama")
    )

    if st.session_state["chat"].settings.make == "openai":
        st.session_state["chat"].settings.model = m2.selectbox(
            "Model",
            ("gpt-3.5-turbo-16k-0613", "gpt-4-0613")
        )
        if model := st.session_state["chat"].settings.model == "gpt-4-0613":
            st.session_state["chat"].settings.max_tokens = 8192
        elif model == "gpt-3.5-turbo-16k-0613":
            st.session_state["chat"].settings.max_tokens = 16000

    if c1.button("Clean memory"):
        c1.warning("Would you like to save first", icon="⚠️")
        st.session_state.clean_memory = True

    if st.session_state.clean_memory:
        if c1.button("Save & Reset"):
            c1.success('Successfully reset! Type in a new message.', icon="✅")
            st.session_state["chat"].reset()
            st.session_state.clean_memory = False
            time.sleep(5)
            controls.empty()

        if c1.button("Reset Only"):
            c1.success('Successfully reset! Type in a new message.', icon="✅")
            st.session_state["chat"].reset()
            st.session_state.clean_memory = False
            time.sleep(5)
            controls.empty()

    if c2.button("Save"):
        pass

if __name__ == "__main__":
    main()