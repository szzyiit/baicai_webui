import pytest
import streamlit as st
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))


@pytest.fixture(autouse=True)
def setup_streamlit():
    """Setup Streamlit session state for each test."""
    # Clear session state before each test
    for key in list(st.session_state.keys()):
        del st.session_state[key]

    # Initialize required session state variables
    st.session_state.messages = []
    st.session_state.message_placeholders = {}
    st.session_state.tutor_messages = []
    st.session_state.tutor_message_placeholders = {}
    st.session_state.page = "home"
