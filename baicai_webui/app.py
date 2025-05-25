import sys
from pathlib import Path

import streamlit as st

# from baicai_webui.components.llm_settings import render_llm_settings

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))


def reset_session_state():
    """Reset session state variables used by the AI assistant to their initial values."""
    st.session_state.messages = []
    st.session_state.message_placeholders = {}

    st.session_state.tutor_messages = []
    st.session_state.tutor_message_placeholders = {}


def main():
    st.set_page_config(page_title="🥬白菜人工智能平台", page_icon="🤖", layout="wide", initial_sidebar_state="expanded")

    # Initialize session state
    if "page" not in st.session_state:
        st.session_state.page = "home"

    # Sidebar navigation
    st.sidebar.title("🥬白菜人工智能平台")
    pages = {
        "主页": "home",
        "教材学习": "book",
        "小测验": "quiz",
        "计算机视觉": "vision",  # 对应 bears/mnist 配置
        "自然语言处理": "nlp",  # 对应 sentiment_classifier 配置
        "推荐系统": "collab",  # 对应 collab 配置
        "传统机器学习": "ml",  # 对应 iris/titanic/house 配置
        "大模型配置": "llm_setting",
    }

    # 根据任务导航或手动选择来设置页面
    if st.session_state.page in pages.values():
        # 找到当前页面对应的显示名称
        current_page_name = [k for k, v in pages.items() if v == st.session_state.page][0]
        selection = st.sidebar.radio(
            "选择任务类型",
            list(pages.keys()),
            index=list(pages.keys()).index(current_page_name),
        )
    else:
        selection = st.sidebar.radio("选择任务类型", list(pages.keys()))

    # 如果是手动选择，更新页面状态
    if pages[selection] != st.session_state.page:
        st.session_state.page = pages[selection]
        reset_session_state()
        st.rerun()

    # Import and show selected page
    try:
        mod = __import__(f"baicai_webui.pages.{st.session_state.page}", fromlist=["show"])
        mod.show()
    except Exception as e:
        st.error(f"Error loading page: {str(e)}")


if __name__ == "__main__":
    main()
