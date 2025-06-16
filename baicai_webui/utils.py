import streamlit as st
from baicai_base.configs import ConfigManager
from dotenv import load_dotenv


def guard_llm_setting():
    env_path = ConfigManager.get_env_path()
    env_exists = env_path.exists() and env_path.stat().st_size > 0

    if env_exists:
        load_dotenv(dotenv_path=env_path, override=True)
    return env_exists


def reset_session_state():
    """Reset session state variables used by the AI assistant to their initial values."""
    st.session_state.messages = []
    st.session_state.message_placeholders = {}
    st.session_state.tutor_messages = []
    st.session_state.tutor_message_placeholders = {}