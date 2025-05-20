import pytest
import streamlit as st
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root))

from baicai_webui.components.stepper import StepperBar


def test_stepper():
    """Test stepper component."""
    try:
        steps = [("Step 1", lambda: None, "graph1"), ("Step 2", lambda: None, "graph2")]
        stepper = StepperBar(steps, 0)
        stepper()
    except Exception as e:
        pytest.fail(f"Failed to render stepper: {str(e)}")
