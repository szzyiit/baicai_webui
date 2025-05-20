import pytest
import streamlit as st
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root))

from baicai_webui.components.button_graph import button_graph


def test_button_graph():
    """Test button graph component."""
    try:
        button_graph()
    except Exception as e:
        pytest.fail(f"Failed to render button graph: {str(e)}")
