#!/usr/bin/env python3
"""
测试 Obsidian 格式处理函数的逻辑
不依赖 streamlit，只测试核心功能
"""

import re


def process_obsidian_callouts(content):
    """处理 Obsidian 特有的 callout 格式，转换为美观的 HTML 样式"""
    if not content:
        return content

    # Obsidian callout 的正则表达式模式
    # 匹配 > [!type] title 格式，支持多行内容
    callout_pattern = r"> \[!([^\]]+)\]\s*([^\n]*)\n((?:> [^\n]*\n?)+)"

    def replace_callout(match):
        callout_type = match.group(1).lower()
        title = match.group(2).strip()
        content_lines = match.group(3).strip()

        # 处理多行内容，移除每行开头的 "> " 并合并
        content_text = "\n".join(
            [
                line[2:].strip() if line.startswith("> ") else line.strip()
                for line in content_lines.split("\n")
                if line.strip()
            ]
        )

        # 定义不同类型的 callout 样式
        callout_styles = {
            "info": {"icon": "ℹ️", "color": "#3b82f6"},
            "note": {"icon": "📝", "color": "#059669"},
            "warning": {"icon": "⚠️", "color": "#d97706"},
            "error": {"icon": "❌", "color": "#dc2626"},
            "success": {"icon": "✅", "color": "#059669"},
            "question": {"icon": "❓", "color": "#7c3aed"},
            "todo": {"icon": "📋", "color": "#059669"},
            "tip": {"icon": "💡", "color": "#0891b2"},
            "abstract": {"icon": "📚", "color": "#7c2d12"},
            "quote": {"icon": "💬", "color": "#6b7280"},
            "example": {"icon": "🔍", "color": "#7c3aed"},
        }

        # 获取样式，如果没有找到对应的类型，使用默认样式
        style = callout_styles.get(callout_type, callout_styles["info"])

        # 构建 HTML，使用 CSS 类
        html = f"""
        <div class="callout callout-{callout_type}">
            <div class="callout-header">
                <span class="callout-icon">{style["icon"]}</span>
                {title if title else callout_type.title()}
            </div>
            <div class="callout-content">
                {content_text}
            </div>
        </div>
        """

        return html

    # 使用正则表达式替换 callout
    processed_content = re.sub(callout_pattern, replace_callout, content, flags=re.DOTALL)

    return processed_content


def process_obsidian_frontmatter(content):
    """处理 Obsidian 的 frontmatter（文件头部元数据）"""
    if not content:
        return content

    # 匹配 frontmatter 格式：以 --- 开始和结束的 YAML 内容
    frontmatter_pattern = r"^---\s*\n(.*?)\n---\s*\n"

    def replace_frontmatter(match):
        frontmatter_content = match.group(1).strip()
        lines = frontmatter_content.split("\n")

        # 提取有用的信息
        metadata = {}
        for line in lines:
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()
                if (
                    value
                    and not value.startswith("[")
                    and not value.startswith("false")
                    and not value.startswith("true")
                ):
                    metadata[key] = value

        # 如果有有用的元数据，显示在页面顶部
        if metadata:
            html_parts = [
                '<div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 1rem; margin: 1rem 0; font-size: 0.9em;">'
            ]
            html_parts.append('<div style="color: #64748b; margin-bottom: 0.5rem; font-weight: 600;">📋 文档信息</div>')

            for key, value in metadata.items():
                if key.lower() in [
                    "date created",
                    "date edited",
                    "source",
                    "description",
                    "tags",
                    "important",
                    "rating",
                    "imagenamekey",
                ]:
                    display_key = {
                        "date created": "创建日期",
                        "date edited": "编辑日期",
                        "source": "来源",
                        "description": "描述",
                        "tags": "标签",
                        "important": "重要性",
                        "rating": "评分",
                        "imagenamekey": "图片键名",
                    }.get(key.lower(), key)

                    if key.lower() == "tags":
                        # 处理标签格式
                        if value.startswith("[") and value.endswith("]"):
                            tags = value[1:-1].split(",")
                            tags = [tag.strip() for tag in tags if tag.strip()]
                            value = " ".join(
                                [
                                    f'<span style="background: #e0e7ff; color: #3730a3; padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.8em; margin-right: 0.5rem;">{tag}</span>'
                                    for tag in tags
                                ]
                            )
                        else:
                            value = f'<span style="background: #e0e7ff; color: #3730a3; padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.8em;">{value}</span>'
                    elif key.lower() in ["date created", "date edited"]:
                        # 格式化日期
                        try:
                            from datetime import datetime

                            date_obj = datetime.strptime(value, "%Y-%m-%d")
                            value = date_obj.strftime("%Y年%m月%d日")
                        except:
                            pass
                    elif key.lower() == "important":
                        # 处理重要性
                        if value.lower() == "true":
                            value = '<span style="color: #dc2626; font-weight: 600;">重要</span>'
                        elif value.lower() == "false":
                            value = '<span style="color: #6b7280;">普通</span>'

                    html_parts.append(f'<div style="margin: 0.25rem 0;"><strong>{display_key}:</strong> {value}</div>')

            html_parts.append("</div>")
            return "".join(html_parts)

        return ""  # 如果没有有用的元数据，返回空字符串

    # 应用转换
    content = re.sub(frontmatter_pattern, replace_frontmatter, content, flags=re.DOTALL)

    return content


def test_callout_processing():
    """测试 callout 处理"""
    print("=== 测试 Callout 处理 ===")

    test_content = """
# 测试文档

> [!info] 重要信息
> 这是一个信息提示框

> [!warning] 警告
> 这是一个警告提示框

> [!question] 思考问题
> 请思考以下问题：
> 1. 第一个问题
> 2. 第二个问题

> [!todo] 待办事项
> 需要完成的任务列表
"""

    result = process_obsidian_callouts(test_content)
    print("处理结果:")
    print(result)
    print("\n" + "=" * 50 + "\n")


def test_frontmatter_processing():
    """测试 frontmatter 处理"""
    print("=== 测试 Frontmatter 处理 ===")

    test_content = """---
Date created: 2025-04-21
Date edited: 2025-04-22
Source: AI入门教材
Description: 人工智能基础知识
tags:
  - AI/basic_book
  - tutorial
Important: true
Rating: 5
imageNameKey: AI_first
---

# 正文内容
这里是正文内容
"""

    result = process_obsidian_frontmatter(test_content)
    print("处理结果:")
    print(result)
    print("\n" + "=" * 50 + "\n")


if __name__ == "__main__":
    print("开始测试 Obsidian 格式处理功能...\n")

    test_callout_processing()
    test_frontmatter_processing()

    print("所有测试完成！")
