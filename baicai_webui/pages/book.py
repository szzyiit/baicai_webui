from pathlib import Path

import streamlit as st

from baicai_webui.components.model import get_page_llm


def show():
    st.title("Book")

    # Get configured LLM instance with configuration UI
    _llm = get_page_llm(
        config_id="book",
        title="Book 模型配置",
        info_text="配置用于 Book 功能的模型参数",
    )
    # Now you can use the llm instance for your page functionality
    # Example:
    # response = llm.invoke("你好")
    # st.write(response)

    # Render a fixed Markdown file from an absolute path
    # Replace this path with your actual Markdown file path
    md_path = Path("/Users/yugeng/Library/CloudStorage/OneDrive-sziit.edu.cn/Documents/AI/4. Store/AI book/第1章 你好，人工智能！.md")

    st.subheader("📖 章节内容预览")
    if md_path.exists():
        try:
            content = md_path.read_text(encoding="utf-8")
            st.markdown(content, unsafe_allow_html=True)
        except Exception as exc:
            st.error(f"读取文档失败: {exc}")
    else:
        st.info(f"未找到文档: {md_path}. 请在代码中将 md_path 修改为实际 Markdown 路径。")


show()