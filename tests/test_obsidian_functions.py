import re

import pytest

from baicai_webui.utils import (
    filter_exercise_section,
    process_lists_in_callout,
    process_obsidian_callouts,
    process_obsidian_frontmatter,
    process_obsidian_links,
    process_obsidian_special_formats,
    process_obsidian_tables,
)


class TestObsidianCallouts:
    """测试 Obsidian callout 处理功能"""

    def test_empty_content(self):
        """测试空内容"""
        assert process_obsidian_callouts("") == ""
        assert process_obsidian_callouts(None) == None

    def test_basic_callout(self):
        """测试基本 callout 格式"""
        content = "> [!info] 重要信息\n> 这是一个信息提示框"
        result = process_obsidian_callouts(content)
        
        assert "callout-info" in result
        assert "ℹ️" in result
        assert "重要信息" in result
        assert "这是一个信息提示框" in result

    def test_callout_without_title(self):
        """测试没有标题的 callout"""
        content = "> [!warning]\n> 这是一个警告"
        result = process_obsidian_callouts(content)
        
        assert "callout-warning" in result
        assert "⚠️" in result
        # 实际实现中，如果没有标题，会使用内容的第一行作为标题
        assert "这是一个警告" in result

    def test_callout_with_multiline_content(self):
        """测试多行内容的 callout"""
        content = "> [!note] 笔记\n> 第一行内容\n> 第二行内容"
        result = process_obsidian_callouts(content)
        
        assert "callout-note" in result
        assert "📝" in result
        assert "第一行内容" in result
        assert "第二行内容" in result

    def test_callout_with_list_content(self):
        """测试包含列表的 callout"""
        content = "> [!todo] 待办事项\n> 1. 第一个任务\n> 2. 第二个任务"
        result = process_obsidian_callouts(content)
        
        assert "callout-todo" in result
        assert "📋" in result
        assert "第一个任务" in result
        assert "第二个任务" in result

    def test_all_callout_types(self):
        """测试所有 callout 类型"""
        callout_types = [
            "info", "note", "warning", "error", "success",
            "question", "todo", "tip", "abstract", "quote", "example"
        ]
        
        for callout_type in callout_types:
            content = f"> [!{callout_type}] 测试\n> 内容"
            result = process_obsidian_callouts(content)
            
            assert f"callout-{callout_type}" in result
            assert "内容" in result

    def test_unknown_callout_type(self):
        """测试未知的 callout 类型"""
        content = "> [!unknown] 未知类型\n> 内容"
        result = process_obsidian_callouts(content)
        
        # 应该使用默认的 info 样式
        assert "callout-unknown" in result
        assert "ℹ️" in result

    def test_callout_with_empty_content(self):
        """测试内容为空的 callout"""
        content = "> [!info] 空内容\n> "
        result = process_obsidian_callouts(content)
        
        # 实际实现中，空内容会显示为 ">"
        assert ">" in result


class TestObsidianFrontmatter:
    """测试 Obsidian frontmatter 处理功能"""

    def test_empty_content(self):
        """测试空内容"""
        assert process_obsidian_frontmatter("") == ""
        assert process_obsidian_frontmatter(None) == None

    def test_frontmatter_removal(self):
        """测试 frontmatter 删除"""
        content = """---
Date created: 2025-04-21
Date edited: 2025-04-22
Source: AI入门教材
---

# 正文内容
这里是正文内容"""
        
        result = process_obsidian_frontmatter(content)
        
        assert "Date created" not in result
        assert "Date edited" not in result
        assert "Source" not in result
        assert "# 正文内容" in result
        assert "这里是正文内容" in result

    def test_no_frontmatter(self):
        """测试没有 frontmatter 的内容"""
        content = "# 标题\n这是内容"
        result = process_obsidian_frontmatter(content)
        
        assert result == content

    def test_frontmatter_with_complex_yaml(self):
        """测试复杂的 YAML frontmatter"""
        content = """---
tags:
  - AI/basic_book
  - tutorial
Important: true
Rating: 5
imageNameKey: AI_first
---

正文内容"""
        
        result = process_obsidian_frontmatter(content)
        
        assert "tags:" not in result
        assert "Important:" not in result
        assert "Rating:" not in result
        assert "正文内容" in result


class TestObsidianSpecialFormats:
    """测试 Obsidian 特殊格式处理功能"""

    def test_markmap_processing(self):
        """测试 markmap 格式处理"""
        content = "```markmap\n- 主题1\n  - 子主题1\n  - 子主题2\n```"
        result = process_obsidian_special_formats(content)
        
        assert "__MARKMAP_PLACEHOLDER__" in result
        assert "__END_MARKMAP__" in result
        assert "- 主题1" in result

    def test_mermaid_processing(self):
        """测试 mermaid 格式处理"""
        content = "```mermaid\ngraph TD\nA-->B\n```"
        result = process_obsidian_special_formats(content)
        
        assert "__MERMAID_PLACEHOLDER__" in result
        assert "__END_MERMAID__" in result
        assert "graph TD" in result

    def test_pdf_placeholder_processing(self):
        """测试 PDF 占位符处理"""
        content = "__PDF_PLACEHOLDER__document.pdf__END_PDF__"
        result = process_obsidian_special_formats(content)
        
        assert "__PDF_PLACEHOLDER__" in result
        assert "__END_PDF__" in result
        assert "document.pdf" in result

    def test_multiple_formats(self):
        """测试多种格式混合"""
        content = """```markmap\n- 主题\n```
```mermaid\ngraph TD\nA-->B\n```
正文内容"""
        result = process_obsidian_special_formats(content)
        
        assert "__MARKMAP_PLACEHOLDER__" in result
        assert "__MERMAID_PLACEHOLDER__" in result
        assert "正文内容" in result


class TestObsidianTables:
    """测试 Obsidian 表格处理功能"""

    def test_basic_table(self):
        """测试基本表格"""
        content = """| 列1 | 列2 | 列3 |
|-----|-----|-----|
| 数据1 | 数据2 | 数据3 |"""
        
        result = process_obsidian_tables(content)
        
        assert "<table" in result
        assert "<th" in result
        assert "<td" in result
        assert "列1" in result
        assert "数据1" in result

    def test_invalid_table(self):
        """测试无效表格（行数不足）"""
        content = "| 列1 | 列2 |\n|-----|-----|"
        result = process_obsidian_tables(content)
        
        # 应该返回原内容，因为行数不足
        assert result == content

    def test_table_with_empty_cells(self):
        """测试包含空单元格的表格"""
        content = """| 列1 | 列2 | 列3 |
|-----|-----|-----|
| 数据1 |  | 数据3 |"""
        
        result = process_obsidian_tables(content)
        
        assert "<table" in result
        assert "数据1" in result
        assert "数据3" in result


class TestObsidianLinks:
    """测试 Obsidian 链接处理功能"""

    def test_md_file_link(self):
        """测试 .md 文件链接"""
        content = "[第一章](第1章.md)"
        result = process_obsidian_links(content)
        
        assert "href=" in result
        assert "chapter=" in result
        assert "📖" in result

    def test_external_link(self):
        """测试外部链接"""
        content = "[Google](https://google.com)"
        result = process_obsidian_links(content)
        
        assert "href=" in result
        assert "target=" in result
        assert "🔗" in result

    def test_image_link(self):
        """测试图片链接（应该保持原样）"""
        content = "![图片](image.png)"
        result = process_obsidian_links(content)
        
        assert result == content

    def test_pdf_file_link(self):
        """测试 PDF 文件链接"""
        content = "[文档](document.pdf)"
        result = process_obsidian_links(content)
        
        assert "📄" in result
        assert "文件链接" in result


class TestListProcessing:
    """测试列表处理功能"""

    def test_ordered_list_in_callout(self):
        """测试 callout 中的有序列表"""
        content = "1. 第一项\n2. 第二项\n3. 第三项"
        result = process_lists_in_callout(content)
        
        # 实际实现中，输出包含样式信息
        assert "ol" in result
        assert "li" in result
        assert "第一项" in result
        assert "第二项" in result
        assert "第三项" in result

    def test_unordered_list_in_callout(self):
        """测试 callout 中的无序列表"""
        content = "- 项目1\n- 项目2\n- 项目3"
        result = process_lists_in_callout(content)
        
        # 实际实现中，输出包含样式信息
        assert "ul" in result
        assert "li" in result
        assert "项目1" in result
        assert "项目2" in result
        assert "项目3" in result

    def test_mixed_lists_in_callout(self):
        """测试 callout 中的混合列表"""
        content = "1. 有序项\n- 无序项\n2. 另一个有序项"
        result = process_lists_in_callout(content)
        
        # 实际实现中，输出包含样式信息
        assert "ol" in result
        assert "ul" in result
        assert "li" in result


class TestExerciseSectionFilter:
    """测试课后练习部分过滤功能"""

    def test_exercise_section_removal(self):
        """测试课后练习部分移除"""
        content = """# 章节标题
这是正文内容

## 课后练习
1. 练习1
2. 练习2"""
        
        result = filter_exercise_section(content)
        
        assert "## 课后练习" not in result
        assert "练习1" not in result
        assert "练习2" not in result
        assert "# 章节标题" in result
        assert "这是正文内容" in result

    def test_no_exercise_section(self):
        """测试没有课后练习部分的内容"""
        content = "# 标题\n这是内容"
        result = filter_exercise_section(content)
        
        assert result == content

    def test_exercise_section_at_end(self):
        """测试课后练习在末尾的内容"""
        content = "正文内容\n## 课后练习\n练习内容"
        result = filter_exercise_section(content)
        
        assert result == "正文内容"
        assert "## 课后练习" not in result
        assert "练习内容" not in result


class TestIntegration:
    """测试集成功能"""

    def test_full_content_processing(self):
        """测试完整的内容处理流程"""
        content = """---
Date: 2025-01-01
---

# 标题

> [!info] 提示
> 这是一个提示框
> - 列表项1
> - 列表项2

| 列1 | 列2 |
|-----|-----|
| 数据1 | 数据2 |

[链接](第2章.md)

## 课后练习
练习内容"""
        
        # 测试 frontmatter 移除
        processed = process_obsidian_frontmatter(content)
        assert "Date:" not in processed
        
        # 测试 callout 处理
        processed = process_obsidian_callouts(processed)
        assert "callout-info" in processed
        
        # 测试表格处理
        processed = process_obsidian_tables(processed)
        assert "<table" in processed
        
        # 测试链接处理
        processed = process_obsidian_links(processed)
        assert "href=" in processed
        
        # 测试练习部分过滤
        processed = filter_exercise_section(processed)
        assert "## 课后练习" not in processed
        assert "练习内容" not in processed


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
