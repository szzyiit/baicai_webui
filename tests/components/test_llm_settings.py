import pytest
import streamlit as st
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root))

from baicai_webui.components.llm_settings import render_llm_settings


def test_llm_settings():
    """Test LLM settings component."""
    # Initialize required session state
    st.session_state.llm_settings = {"model": "gpt-3.5-turbo", "temperature": 0.7, "max_tokens": 1000}

    # Test rendering
    try:
        render_llm_settings()
    except Exception as e:
        pytest.fail(f"Failed to render LLM settings: {str(e)}")
