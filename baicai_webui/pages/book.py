import re
from pathlib import Path

import streamlit as st
from streamlit_markmap import markmap
from streamlit_mermaid import st_mermaid
from streamlit_pdf_viewer import pdf_viewer

from baicai_webui.utils import (
    get_available_chapters,
    get_callout_css,
    load_chapter_content,
)


def show():
    st.title("AI 入门教材学习")

    # 注入 callout 的 CSS 样式
    st.markdown(get_callout_css(), unsafe_allow_html=True)

    # Get portable path to AI_intro_book folder
    current_file = Path(__file__)
    book_path = current_file.parent.parent.parent / "AI_intro_book"

    # 检查书籍路径是否存在
    if not book_path.exists():
        st.error(f"未找到 AI_intro_book 文件夹: {book_path}")
        st.info("请确保 AI_intro_book 文件夹存在于项目根目录中。")
        return

    # 获取可用章节
    chapters = get_available_chapters(book_path)

    if not chapters:
        st.warning("AI_intro_book 文件夹中没有找到可用的章节文件。")
        return

    # 创建章节名称列表（用于下拉菜单），去除 .md 扩展名
    chapter_names = [chapter.name.replace(".md", "") for chapter in chapters]

    # 从 URL 参数获取当前章节，如果没有则使用默认值
    default_chapter = chapter_names[0] if chapter_names else ""
    current_chapter = st.query_params.get("chapter", default_chapter)

    # 如果从URL参数获取到章节，尝试解码并匹配
    if current_chapter and current_chapter != default_chapter:
        try:
            import urllib.parse

            # 尝试解码URL参数
            decoded_chapter = urllib.parse.unquote(current_chapter)

            # 尝试精确匹配
            if decoded_chapter in chapter_names:
                current_chapter = decoded_chapter
            else:
                # 尝试模糊匹配，查找包含该章节名称的章节
                matched_chapter = None
                for chapter_name in chapter_names:
                    if decoded_chapter in chapter_name or chapter_name in decoded_chapter:
                        matched_chapter = chapter_name
                        break

                if matched_chapter:
                    current_chapter = matched_chapter
                    st.write(f"✅ 模糊匹配成功: `{decoded_chapter}` → `{matched_chapter}`")
                else:
                    # 如果仍然无法匹配，使用默认章节
                    current_chapter = default_chapter
                    st.write(f"❌ 匹配失败，使用默认章节: `{default_chapter}`")
        except Exception as e:
            # 如果解码失败，使用默认章节
            current_chapter = default_chapter
            st.write(f"❌ 解码失败: {e}，使用默认章节: `{default_chapter}`")

    # 如果 URL 中的章节不在可用章节列表中，使用默认章节
    if current_chapter not in chapter_names:
        current_chapter = default_chapter

    # 获取当前章节在列表中的索引
    current_index = chapter_names.index(current_chapter) if current_chapter in chapter_names else 0

    # 章节选择器
    st.subheader("选择要学习的章节")

    # 创建下拉菜单，使用当前选中的章节
    selected_chapter_name = st.selectbox(
        "请选择章节：", options=chapter_names, index=current_index, help="从下拉菜单中选择要阅读的章节"
    )

    # 如果选择的章节与当前 URL 参数不同，更新 URL
    if selected_chapter_name != current_chapter:
        st.query_params["chapter"] = selected_chapter_name
        st.rerun()

    # 找到选中的章节文件
    selected_chapter = next(
        (chapter for chapter in chapters if chapter.name.replace(".md", "") == selected_chapter_name), None
    )

    # 显示选中的章节内容
    if selected_chapter:
        # 显示章节标题
        st.subheader(selected_chapter_name)

        # 加载章节内容并处理图片
        content, error = load_chapter_content(selected_chapter, book_path)

        if content:
            # 处理 markmap、mermaid 和 PDF 占位符并渲染内容
            processed_content = content

            # 定义占位符模式
            markmap_placeholder_pattern = r"__MARKMAP_PLACEHOLDER__(.*?)__END_MARKMAP__"
            mermaid_placeholder_pattern = r"__MERMAID_PLACEHOLDER__(.*?)__END_MERMAID__"
            pdf_placeholder_pattern = r"__PDF_PLACEHOLDER__(.*?)__END_PDF__"

            # 用于生成唯一 key 的计数器
            mermaid_counter = 0
            markmap_counter = 0
            pdf_counter = 0

            # 首先分割 markmap 占位符
            markmap_parts = re.split(markmap_placeholder_pattern, processed_content, flags=re.DOTALL)

            # 处理每个部分
            for i, part in enumerate(markmap_parts):
                if i % 2 == 0:  # 普通内容，需要进一步检查是否包含 mermaid 和 PDF
                    if part.strip():
                        # 检查这部分是否包含 mermaid 占位符
                        mermaid_parts = re.split(mermaid_placeholder_pattern, part, flags=re.DOTALL)

                        # 交替显示内容和 mermaid
                        for j, mermaid_part in enumerate(mermaid_parts):
                            if j % 2 == 0:  # 普通内容，需要进一步检查是否包含 PDF
                                if mermaid_part.strip():
                                    # 检查这部分是否包含 PDF 占位符
                                    pdf_parts = re.split(pdf_placeholder_pattern, mermaid_part, flags=re.DOTALL)

                                    # 交替显示内容和 PDF
                                    for k, pdf_part in enumerate(pdf_parts):
                                        if k % 2 == 0:  # 普通内容
                                            if pdf_part.strip():
                                                st.markdown(pdf_part, unsafe_allow_html=True)
                                        else:  # PDF 内容
                                            if pdf_part.strip():
                                                pdf_counter += 1
                                                try:
                                                    pdf_path = Path(pdf_part.strip())
                                                    if pdf_path.exists():
                                                        pdf_viewer(str(pdf_path), height=400, key=f"pdf_{pdf_counter}")
                                                    else:
                                                        st.error(f"PDF 文件不存在: {pdf_path}")
                                                except Exception as e:
                                                    st.error(f"PDF 加载失败: {e}")
                            else:  # mermaid 内容
                                if mermaid_part.strip():
                                    mermaid_counter += 1
                                    st_mermaid(mermaid_part.strip(), height=400, key=f"mermaid_{mermaid_counter}")
                else:  # markmap 内容
                    if part.strip():
                        markmap_counter += 1
                        # markmap 函数不支持 key 参数，但我们可以通过其他方式确保唯一性
                        markmap(part.strip(), height=400)

        else:
            st.error(f"{error}")


show()
