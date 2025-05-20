import pytest
import streamlit as st
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root))

from baicai_webui.components.image_viewer import ImageViewer


def test_image_viewer():
    """Test image viewer component."""
    try:
        viewer = ImageViewer("test_image.jpg")
        viewer.show()
    except Exception as e:
        pytest.fail(f"Failed to render image viewer: {str(e)}")
