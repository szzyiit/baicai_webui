from pathlib import Path
import re
import base64

import streamlit as st

from baicai_webui.components.model import get_page_llm


def extract_chapter_number(filename):
    """从文件名中提取章节数字"""
    match = re.search(r"第(\d+)章", filename)
    if match:
        return int(match.group(1))
    return 0


def get_available_chapters(book_path):
    """获取可用的章节列表，排除结构文件，按章节数字排序"""
    if not book_path.exists():
        return []

    md_files = list(book_path.glob("*.md"))
    # 过滤掉结构文件，并按章节数字排序
    chapters = [f for f in md_files if f.name != "结构.md"]
    # 按章节数字排序（1, 2, 3, ..., 12）
    chapters.sort(key=lambda x: extract_chapter_number(x.name))
    return chapters


def process_markdown_images(content, book_path):
    """处理 Markdown 内容中的图片，将相对路径转换为可显示的格式，保留原始尺寸设置"""
    if not content:
        return content

    def replace_image(match):
        alt_text = match.group(1)
        image_path = match.group(2)

        # 检查 alt_text 是否包含尺寸信息（如 "50", "500" 等）
        width = None
        height = None

        # 尝试从 alt_text 中提取尺寸信息
        if alt_text.isdigit():
            # 如果 alt_text 是纯数字，认为是宽度
            width = int(alt_text)
        elif "x" in alt_text.lower():
            # 如果包含 x，可能是 "100x200" 格式
            try:
                parts = alt_text.lower().split("x")
                if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                    width = int(parts[0])
                    height = int(parts[1])
            except:
                pass

        # 如果是相对路径，构建绝对路径
        if image_path.startswith("attachments/"):
            absolute_path = book_path / image_path

            # 检查文件是否存在
            if absolute_path.exists():
                # 获取文件扩展名
                file_ext = absolute_path.suffix.lower()

                # 构建样式字符串
                style_parts = []
                if width:
                    style_parts.append(f"width: {width}px")
                if height:
                    style_parts.append(f"height: {height}px")
                else:
                    # 如果没有设置高度，保持宽高比
                    style_parts.append("height: auto")

                # 确保图片不会超出容器
                style_parts.append("max-width: 100%")

                style_str = "; ".join(style_parts)

                # 对于支持的图片格式，返回 HTML img 标签
                if file_ext in [".png", ".jpg", ".jpeg", ".webp"]:
                    # 使用 base64 编码图片数据
                    try:
                        with open(absolute_path, "rb") as f:
                            image_data = f.read()
                            base64_data = base64.b64encode(image_data).decode()
                            mime_type = f"image/{file_ext[1:]}" if file_ext != ".jpg" else "image/jpeg"
                            return f'<img src="data:{mime_type};base64,{base64_data}" alt="{alt_text}" style="{style_str}">'
                    except Exception:
                        # 如果 base64 编码失败，返回文件路径信息
                        return f"<p><strong>图片加载失败:</strong> {alt_text}</p>"

                elif file_ext == ".svg":
                    # 对于 SVG 文件，使用 object 标签或 iframe 来确保完整显示
                    try:
                        # 将 SVG 文件转换为 base64 编码
                        with open(absolute_path, "rb") as f:
                            svg_data = f.read()
                            svg_base64 = base64.b64encode(svg_data).decode()

                        # 使用 object 标签显示 SVG，这样可以确保完整显示
                        if width and height:
                            return f'<object data="data:image/svg+xml;base64,{svg_base64}" type="image/svg+xml" width="{width}" height="{height}" style="{style_str}"></object>'
                        elif width:
                            return f'<object data="data:image/svg+xml;base64,{svg_base64}" type="image/svg+xml" width="{width}" style="{style_str}"></object>'
                        else:
                            # 如果没有指定尺寸，使用 SVG 的原始尺寸
                            return f'<object data="data:image/svg+xml;base64,{svg_base64}" type="image/svg+xml" style="{style_str}"></object>'

                    except Exception as e:
                        # 如果 SVG 处理失败，尝试直接读取内容
                        try:
                            svg_content = absolute_path.read_text(encoding="utf-8")
                            # 确保 SVG 有正确的 viewBox 属性
                            if "viewBox" not in svg_content and "<svg" in svg_content:
                                # 如果没有 viewBox，尝试添加一个
                                svg_match = re.search(r"<svg([^>]*)>", svg_content)
                                if svg_match:
                                    svg_attrs = svg_match.group(1)
                                    # 提取宽度和高度
                                    width_match = re.search(r'width="(\d+)"', svg_attrs)
                                    height_match = re.search(r'height="(\d+)"', svg_attrs)
                                    if width_match and height_match:
                                        w = width_match.group(1)
                                        h = height_match.group(1)
                                        viewbox_attr = f' viewBox="0 0 {w} {h}"'
                                        svg_content = re.sub(
                                            r"<svg([^>]*)>", f"<svg\\1{viewbox_attr}>", svg_content, count=1
                                        )

                            # 添加样式到 SVG
                            if width or height:
                                style_attr = f' style="{style_str}"'
                                svg_content = re.sub(r"<svg([^>]*)>", f"<svg\\1{style_attr}>", svg_content, count=1)

                            return svg_content
                        except Exception:
                            return f"<p><strong>SVG 加载失败:</strong> {alt_text}</p>"

                else:
                    return f"<p><strong>不支持的图片格式:</strong> {alt_text} ({file_ext})</p>"
            else:
                return f"<p><strong>图片文件不存在:</strong> {alt_text}</p>"

        # 如果是其他路径（如 HTTP 链接），保持原样
        return match.group(0)

    # 使用正则表达式替换图片引用
    processed_content = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", replace_image, content)

    return processed_content


def load_chapter_content(md_path, book_path):
    """加载章节内容并处理图片"""
    if not md_path.exists():
        return None, f"未找到文档: {md_path.name}"

    try:
        content = md_path.read_text(encoding="utf-8")
        # 处理图片
        processed_content = process_markdown_images(content, book_path)
        return processed_content, None
    except Exception as exc:
        return None, f"读取文档失败: {exc}"


def show():
    st.title("AI 入门教材学习")

    # Get configured LLM instance with configuration UI
    _llm = get_page_llm(
        config_id="book",
        title="Book 模型配置",
        info_text="配置用于 Book 功能的模型参数",
    )

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

    # 章节选择器
    st.subheader("选择要学习的章节")

    # 创建章节名称列表（用于下拉菜单）
    chapter_names = [chapter.name for chapter in chapters]

    # 添加默认选项
    default_index = 0  # 默认选择第一章

    # 创建下拉菜单
    selected_chapter_name = st.selectbox(
        "请选择章节：", options=chapter_names, index=default_index, help="从下拉菜单中选择要阅读的章节"
    )

    # 找到选中的章节文件
    selected_chapter = next((chapter for chapter in chapters if chapter.name == selected_chapter_name), None)

    # 显示选中的章节内容
    if selected_chapter:
        st.subheader(f"{selected_chapter_name}")

        # 加载章节内容并处理图片
        content, error = load_chapter_content(selected_chapter, book_path)

        if content:
            # 显示章节内容（包含处理后的图片）
            st.markdown(content, unsafe_allow_html=True)

            # 添加章节导航
            st.markdown("---")
            st.markdown("### 章节导航")

            # 显示当前章节在列表中的位置
            current_index = chapter_names.index(selected_chapter_name)
            total_chapters = len(chapters)

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                if current_index > 0:
                    prev_chapter = chapter_names[current_index - 1]
                    if st.button(f"上一章: {prev_chapter}", key="prev_btn"):
                        st.session_state.selected_chapter = prev_chapter
                        st.rerun()
                else:
                    st.button("上一章", disabled=True, key="prev_btn_disabled")

            with col2:
                st.info(f"第 {current_index + 1} 章 / 共 {total_chapters} 章")

            with col3:
                if current_index < total_chapters - 1:
                    next_chapter = chapter_names[current_index + 1]
                    if st.button(f"下一章: {next_chapter}", key="next_btn"):
                        st.session_state.selected_chapter = next_chapter
                        st.rerun()
                else:
                    st.button("下一章", disabled=True, key="next_btn_disabled")

            with col4:
                if st.button("刷新内容", key="refresh_btn"):
                    st.rerun()

        else:
            st.error(f"{error}")

    # 显示所有可用章节列表
    with st.expander("查看所有可用章节", expanded=False):
        st.markdown("### 完整章节列表")
        for i, chapter in enumerate(chapters, 1):
            chapter_num = extract_chapter_number(chapter.name)
            if chapter.name == selected_chapter_name:
                st.markdown(f"**{chapter_num}. {chapter.name}** (当前阅读)")
            else:
                st.markdown(f"{chapter_num}. {chapter.name}")

        st.info(f"共找到 {len(chapters)} 个章节文件")


# 初始化会话状态
if "selected_chapter" not in st.session_state:
    st.session_state.selected_chapter = None

show()
