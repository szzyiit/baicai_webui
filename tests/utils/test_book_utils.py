from pathlib import Path
from unittest.mock import patch

import pytest

from baicai_webui.utils import (
    create_chapter_selector,
    find_selected_chapter_file,
    get_chapter_from_url_params,
    update_chapter_url_param,
)


class TestBookUtils:
    """测试书籍工具函数"""

    def test_get_chapter_from_url_params_no_chapters(self):
        """测试没有可用章节时的情况"""
        result, info = get_chapter_from_url_params([], "默认章节")
        assert result == "默认章节"
        assert info == ""

    def test_get_chapter_from_url_params_default_chapter(self):
        """测试使用默认章节的情况"""
        chapters = ["第1章", "第2章", "第3章"]
        result, info = get_chapter_from_url_params(chapters, "第1章")
        assert result == "第1章"
        assert info == ""

    def test_get_chapter_from_url_params_exact_match(self):
        """测试精确匹配的情况"""
        chapters = ["第1章", "第2章", "第3章"]
        with patch("streamlit.query_params") as mock_params:
            mock_params.get.return_value = "第2章"
            result, info = get_chapter_from_url_params(chapters, "第1章")
            assert result == "第2章"
            assert info == ""

    def test_get_chapter_from_url_params_fuzzy_match(self):
        """测试模糊匹配的情况"""
        chapters = ["第1章 机器学习基础", "第2章 深度学习", "第3章 强化学习"]
        with patch("streamlit.query_params") as mock_params:
            mock_params.get.return_value = "机器学习"
            result, info = get_chapter_from_url_params(chapters, "第1章")
            assert result == "第1章 机器学习基础"
            assert "模糊匹配成功" in info

    def test_get_chapter_from_url_params_decode_failure(self):
        """测试URL解码失败的情况"""
        chapters = ["第1章", "第2章", "第3章"]
        with patch("streamlit.query_params") as mock_params:
            mock_params.get.return_value = "invalid%chapter"
            with patch("urllib.parse.unquote", side_effect=Exception("Decode error")):
                result, info = get_chapter_from_url_params(chapters, "第1章")
                assert result == "第1章"
                assert "解码失败" in info

    def test_update_chapter_url_param_same_chapter(self):
        """测试相同章节时不需要更新URL"""
        with patch("streamlit.query_params") as mock_params:
            result = update_chapter_url_param("第1章", "第1章")
            assert result is False
            mock_params.__setitem__.assert_not_called()

    def test_update_chapter_url_param_different_chapter(self):
        """测试不同章节时需要更新URL"""
        with patch("streamlit.query_params") as mock_params:
            result = update_chapter_url_param("第2章", "第1章")
            assert result is True
            mock_params.__setitem__.assert_called_once_with("chapter", "第2章")

    def test_create_chapter_selector(self):
        """测试章节选择器创建"""
        chapters = ["第1章", "第2章", "第3章"]
        current_chapter = "第2章"

        with patch("streamlit.subheader") as mock_subheader:
            with patch("streamlit.selectbox") as mock_selectbox:
                mock_selectbox.return_value = "第3章"

                result = create_chapter_selector(chapters, current_chapter)

                mock_subheader.assert_called_once_with("选择要学习的章节")
                mock_selectbox.assert_called_once()
                assert result == "第3章"

    def test_find_selected_chapter_file_found(self):
        """测试找到章节文件"""
        # 创建真实的Path对象而不是Mock对象
        chapters = [
            Path("第1章.md"),
            Path("第2章.md"),
            Path("第3章.md")
        ]

        result = find_selected_chapter_file(chapters, "第2章")
        assert result == chapters[1]

    def test_find_selected_chapter_file_not_found(self):
        """测试未找到章节文件"""
        chapters = [
            Path("第1章.md"),
            Path("第2章.md"),
            Path("第3章.md")
        ]

        result = find_selected_chapter_file(chapters, "第4章")
        assert result is None

    def test_find_selected_chapter_file_empty_chapters(self):
        """测试空章节列表"""
        result = find_selected_chapter_file([], "第1章")
        assert result is None


if __name__ == "__main__":
    pytest.main([__file__])
