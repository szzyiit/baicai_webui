import pytest
import streamlit as st
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root))

from baicai_webui.pages.ml import show


def test_ml_page():
    """Test ML page functionality."""
    try:
        show()
    except Exception as e:
        pytest.fail(f"Failed to render ML page: {str(e)}")
