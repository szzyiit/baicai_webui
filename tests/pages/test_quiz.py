import pytest
import streamlit as st
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root))

from baicai_webui.pages.quiz import show


def test_quiz_page():
    """Test quiz page functionality."""
    try:
        show()
    except Exception as e:
        pytest.fail(f"Failed to render quiz page: {str(e)}")
