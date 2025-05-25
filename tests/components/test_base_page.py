import pytest
import streamlit as st
from pathlib import Path
import sys
import asyncio
from unittest.mock import Mock, patch, AsyncMock

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root))

from baicai_webui.components.base_page import BasePage
from baicai_dev.utils.data import TaskType


@pytest.fixture
def mock_data_uploader():
    """Create a mock data uploader function."""

    def uploader():
        return {"configurable": {"from_web_ui": False}}

    return uploader


@pytest.fixture
def base_page(mock_data_uploader):
    """Create a BasePage instance for testing."""
    return BasePage(TaskType.ML, mock_data_uploader)


def test_base_page_initialization(base_page):
    """Test that BasePage initializes correctly."""
    assert base_page.task_type == TaskType.ML
    assert "code_interpreter" in st.session_state
    assert "page_state" in st.session_state
    assert "data_config" in st.session_state
    assert "graph_state" in st.session_state

    # Check page_state initialization
    page_state = st.session_state.page_state
    assert "monitor" in page_state
    assert page_state["helper_ready"] is False
    assert page_state["post_train_completed"] is False
    assert page_state["data_config"] is None
    assert page_state["pre_train_container"] is None
    assert page_state["run_post_train"] is False

    # Check graph_state initialization
    graph_state = st.session_state.graph_state
    assert graph_state["messages"] == []
    assert graph_state["dl_codes"] == []
    assert graph_state["dl_models"] == []
    assert graph_state["dl_success"] is False


def test_show_without_data(base_page):
    """Test show method when no data is uploaded."""
    # Create a mock data uploader that returns None
    base_page.data_uploader_func = lambda: None

    with patch("streamlit.warning") as mock_warning:
        base_page.show()
        mock_warning.assert_called_once_with("请上传数据")


def test_show_with_data_and_pre_train(base_page):
    """Test show method with data and pre_train function."""
    mock_pre_train = Mock()
    mock_post_train = AsyncMock()

    with patch("streamlit.button", return_value=False):
        base_page.show(pre_train=mock_pre_train, post_train=mock_post_train)
        mock_pre_train.assert_called_once()


def test_show_with_training(base_page):
    """Test show method with training process."""
    mock_monitor = Mock()
    mock_monitor.start_training = AsyncMock(return_value={"result": "success"})
    mock_monitor.app = Mock()
    mock_monitor.app.get_state = Mock(
        return_value=Mock(values={"dl_codes": ["code1"], "dl_models": ["model1"], "dl_success": True})
    )

    # Create a mock async iterator for helper_node
    class MockAsyncIterator:
        def __init__(self):
            self.items = [{"state": "update1"}, {"state": "update2"}]
            self.index = 0

        def __aiter__(self):
            return self

        async def __anext__(self):
            if self.index >= len(self.items):
                raise StopAsyncIteration
            item = self.items[self.index]
            self.index += 1
            return item

    mock_monitor.graph = Mock()
    mock_monitor.graph.helper_node = Mock(return_value=MockAsyncIterator())

    st.session_state.page_state["monitor"] = mock_monitor
    st.session_state.page_state["helper_ready"] = False

    with (
        patch("streamlit.success") as mock_success,
        patch("streamlit.button", return_value=True),
    ):
        base_page.show()
        mock_monitor.start_training.assert_called_once()
        mock_success.assert_called_once_with("训练已启动！")
        assert st.session_state.graph_state["dl_codes"] == ["code1"]
        assert st.session_state.graph_state["dl_models"] == ["model1"]
        assert st.session_state.graph_state["dl_success"] is True
        assert st.session_state.page_state["helper_ready"] is True


def test_show_with_training_error(base_page):
    """Test show method when training fails."""
    mock_monitor = Mock()
    mock_monitor.start_training = AsyncMock(side_effect=Exception("Training failed"))

    st.session_state.page_state["monitor"] = mock_monitor
    st.session_state.page_state["helper_ready"] = False

    with (
        patch("streamlit.error") as mock_error,
        patch("streamlit.button", return_value=True),
    ):
        base_page.show()
        mock_error.assert_called_once_with("训练失败：Training failed")


def test_show_with_post_train(base_page):
    """Test show method with post_train function."""
    mock_post_train = AsyncMock()
    st.session_state.page_state["run_post_train"] = True
    st.session_state.page_state["post_train_completed"] = False

    with patch("streamlit.button", return_value=False):
        base_page.show(post_train=mock_post_train)
        mock_post_train.assert_called_once()
        assert st.session_state.page_state["post_train_completed"] is True
        assert st.session_state.page_state["run_post_train"] is False
