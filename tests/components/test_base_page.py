import pytest
import streamlit as st
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root))

from baicai_webui.components.base_page import BasePage
from baicai_dev.utils.data.task_type import TaskType


def mock_data_uploader():
    """Mock data uploader function for testing."""
    return {"configurable": {"from_web_ui": True}}


def test_base_page():
    """Test BasePage class functionality."""

    class TestPage(BasePage):
        def show(self):
            return "test"

    page = TestPage(task_type=TaskType.ML, data_uploader_func=mock_data_uploader)
    assert hasattr(page, "show")
    assert page.show() == "test"
