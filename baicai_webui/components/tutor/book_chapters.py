import pandas as pd
import streamlit as st

chapter_template = {
    "book_name": "AI 基础",
    "chapters": [
        {
            "id": 1,
            "name": "AI 数学基础",
            "summary": "AI 数学基础是 AI 学习的基础，主要介绍 AI 数学基础的基本概念和基本原理。",
            "keywords": ["平均数", "方差", "矩阵", "向量", "中位数"],
        },
        {
            "id": 2,
            "name": "线性回归",
            "summary": "线性回归是 AI 学习的基础，主要介绍线性回归的基本概念和基本原理。",
            "keywords": ["线性回归", "最小二乘法", "梯度下降", "正则化"],
        },
        {
            "id": 3,
            "name": "逻辑回归",
            "summary": "逻辑回归是 AI 学习的基础，主要介绍逻辑回归的基本概念和基本原理。",
            "keywords": ["逻辑回归", "最大似然估计", "梯度下降", "正则化"],
        },
        {
            "id": 4,
            "name": "神经网络",
            "summary": "神经网络是 AI 学习的基础，主要介绍神经网络的基本概念和基本原理。",
            "keywords": ["神经网络", "反向传播", "梯度下降", "正则化"],
        },
        {
            "id": 5,
            "name": "决策树",
            "summary": "决策树是 AI 学习的基础，主要介绍决策树的基本概念和基本原理。",
            "keywords": ["决策树", "信息增益", "基尼不纯度", "剪枝"],
        },
    ],
}

survey_result_template = {
    "summary": {
        "type": "低动机-低效能-被动型",
        "description": "学生在内在动机和学习行为上表现极低，自我效能感偏低，外在动机和学习压力中等，整体学习状态不佳。",
    },
    "dimension_scores": {
        "intrinsic_motivation": {"question_ids": [1, 2, 3, 4, 5], "mean_score": 0.8, "level": "极低", "label": "内在动机"},
        "extrinsic_motivation": {"question_ids": [6, 7, 8], "mean_score": 2.67, "level": "中等", "label": "外在动机"},
        "self_efficacy": {"question_ids": [9, 10, 11], "mean_score": 2, "level": "偏低", "label": "自我效能感"},
        "learning_behaviors": {"question_ids": [12, 13, 14, 15], "mean_score": 1.5, "level": "极低", "label": "学习行为"},
        "learning_stress_and_challenge": {"question_ids": [16, 17, 18], "mean_score": 2, "level": "中等", "label": "学习压力和挑战"},
    },
    "problems_identified": ["缺乏内在动机", "自我效能感不足", "学习行为被动", "学习压力适中但挑战感中等"],
    "personalized_recommendations": {
        "interest_motivation": ["提供多样化的学习材料以激发兴趣", "设计实践性强的项目以增加参与感"],
        "self_efficacy_building": ["设定并完成小目标以增强成就感", "提供正面反馈，强化学生的能力认知"],
        "learning_strategy": ["建议使用主动学习策略，如定期复习和提前预习", "鼓励参与课堂讨论和小组合作"],
        "teaching_support": ["定期与学生沟通，了解学习状态和困难", "提供额外的学习资源和支持材料"],
    },
}


def select_book_chapters(book_chapters: list[dict] = None):
    """
    Select a chapter from the book
    Args:
        book_chapters: List of book chapters
    Returns:
        Selected chapter
    """
    if book_chapters is None:
        book_chapters = chapter_template

    st.title(f"{book_chapters['book_name']}")

    # Convert chapters to DataFrame
    df = pd.DataFrame(book_chapters["chapters"])
    df["keywords"] = df["keywords"].apply(lambda x: ", ".join(x))

    # Display DataFrame with selection
    st.subheader("章节列表")
    event = st.dataframe(
        df[["id", "name", "summary"]],
        column_config={"id": "章节编号", "name": "章节名称", "summary": "章节摘要"},
        hide_index=True,
        use_container_width=True,
        key="chapter_selection",
        on_select="rerun",
        selection_mode="single-row",
    )

    # Display selected chapter details
    if event.selection.rows:
        selected_index = event.selection.rows[0]
        # Create a copy of the selected row to avoid the warning
        selected_chapter = df.iloc[selected_index].copy()
        st.success(f"您选择的学习章节是：第{selected_chapter['id']}章 - {selected_chapter['name']}")
        # Convert keywords back to list
        selected_chapter["keywords"] = selected_chapter["keywords"].split(", ")
        return selected_chapter.to_dict()

    # If no chapter is selected, return the first chapter
    st.success(f"默认选择: 第{book_chapters['chapters'][0]['id']}章 - {book_chapters['chapters'][0]['name']}")
    return book_chapters["chapters"][0]
