import streamlit as st
from streamlit_flow import streamlit_flow
from streamlit_flow.elements import StreamlitFlowEdge, StreamlitFlowNode
from streamlit_flow.layouts import TreeLayout
from streamlit_flow.state import StreamlitFlowState

page_map = {
    "0": "home",
    "1": "ml",
    "2": "vision",
    "3": "nlp",
}


def reset_session_state():
    """Reset session state variables used by the AI assistant to their initial values."""
    st.session_state.messages = []
    st.session_state.message_placeholders = {}

    st.session_state.tutor_messages = []
    st.session_state.tutor_message_placeholders = {}


def button_graph():
    nodes = [
        StreamlitFlowNode(
            id="0",
            pos=(100, 100),
            data={"content": "项目1"},
            node_type="input",
            source_position="right",
            draggable=False,
        ),
        StreamlitFlowNode("1", (350, 50), {"content": "项目2"}, "default", "right", "left", draggable=False),
        StreamlitFlowNode("2", (350, 150), {"content": "项目3"}, "default", "right", "left", draggable=False),
        StreamlitFlowNode("3", (600, 100), {"content": "项目4"}, "output", target_position="left", draggable=False),
    ]

    edges = [
        StreamlitFlowEdge("0-1", "0", "1", animated=True),
        StreamlitFlowEdge("1-2", "0", "2", animated=True),
        StreamlitFlowEdge("2-3", "1", "3", animated=True),
        StreamlitFlowEdge("3-4", "2", "3", animated=True),
    ]

    if "click_interact_state" not in st.session_state:
        st.session_state.click_interact_state = StreamlitFlowState(nodes, edges)

    updated_state = streamlit_flow(
        "ret_val_flow",
        st.session_state.click_interact_state,
        fit_view=True,
        get_node_on_click=True,
        get_edge_on_click=True,
    )

    # st.write(f"Clicked on: {updated_state.nodes[int(updated_state.selected_id)].data['content']}")

    st.session_state.redirect_to = updated_state.selected_id

    # Check for redirect flag from button_graph component
    if "redirect_to" in st.session_state and st.session_state["redirect_to"]:
        page = page_map[st.session_state["redirect_to"]]
        st.session_state.page = page
        reset_session_state()
        st.session_state.redirect_to = None
        st.rerun()
