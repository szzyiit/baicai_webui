import streamlit as st

from baicai_webui.components.model import get_page_llm


def show():
    st.title("Book")

    # Get configured LLM instance with configuration UI
    llm = get_page_llm(
        config_id="book",
        title="Book 模型配置",
        info_text="配置用于 Book 功能的模型参数",
    )
    # Now you can use the llm instance for your page functionality
    # Example:
    # response = llm.invoke("你好")
    # st.write(response)

show()