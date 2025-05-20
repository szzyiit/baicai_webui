from pathlib import Path

import streamlit as st
import streamlit_mermaid as stmd
from baicai_base.utils.data import clear_tmp_files, get_tmp_folder

from baicai_webui.components.button_graph import button_graph
from baicai_webui.components.llm_settings import render_llm_settings
from baicai_webui.components.tutor import reset_session_state as reset_survey_session_state
from baicai_webui.components.tutor import survey_flow


def ability_navigator():
    """任务导航助手"""
    st.subheader("🧭 任务导航助手")
    st.write("请选择您想使用的任务类型：")

    # 选择任务类型
    data_type = st.radio(
        "选择任务类型",
        ["教材学习", "小测验", "计算机视觉", "自然语言处理", "表格数据处理", "了解更多"],
    )

    if data_type == "教材学习":
        st.write("👉 采用非个性化的教材学习, 您可以：")
        st.info("""
        - 了解人工智能基础知识
        - 掌握人工智能基本流程
        - 了解常用人工智能算法
        - 了解人工智能应用场景
        """)
        if st.button("👉 开始教材学习"):
            st.session_state.page = "book"
            st.rerun()

    elif data_type == "小测验":
        st.write("👉 采用个性化的测验，您可以：")
        st.info("""
        - 测试您的知识点
        - 了解您的学习情况
        - 针对性地互动进行学习
        """)
        if st.button("👉 开始小测验"):
            st.session_state.page = "quiz"
            st.rerun()

    elif data_type == "计算机视觉":
        st.write("👉 计算机视觉可以帮您完成以下任务：")
        st.info("""
        - 图片分类：识别图片中的物体类型（如猫狗识别、物体分类）
        - 物体检测：定位并识别图片中的多个物体
        - 图像分割：精确分析图片中物体的轮廓和区域
        - 人脸识别：检测和识别图片中的人脸
        """)
        if st.button("👉 开始计算机视觉任务"):
            st.session_state.page = "vision"
            st.rerun()

    elif data_type == "自然语言处理":
        st.write("👉 自然语言处理可以帮您完成以下任务：")
        st.info("""
        - 文本分类：对文章进行自动分类（如新闻分类、垃圾邮件识别）
        - 情感分析：分析文本的情感倾向（如商品评论分析）
        - 信息提取：从文本中提取关键信息（如提取人名、地名、关键词）
        - 文本摘要：自动生成文章摘要
        """)
        if st.button("👉 开始自然语言处理任务"):
            st.session_state.page = "nlp"
            st.rerun()

    elif data_type == "表格数据处理":
        st.write("👉 表格数据处理包括以下两类任务：")

        col1, col2 = st.columns(2)
        with col1:
            st.info("""
            **传统机器学习**
            - 数值预测：预测房价、销量、股票等
            - 分类预测：预测客户流失、信用评估等
            - 数据聚类：自动对数据分组
            """)
            if st.button("👉 开始机器学习任务"):
                st.session_state.page = "ml"
                st.rerun()

        with col2:
            st.info("""
            **推荐系统**
            - 商品推荐：电商商品个性化推荐
            - 内容推荐：视频、音乐、文章推荐
            - 社交推荐：好友推荐、兴趣组推荐
            """)
            if st.button("👉 开始推荐系统任务"):
                st.session_state.page = "collab"
                st.rerun()

    else:
        # 设置页面布局，减少边距
        st.markdown(
            """
            <style>
                .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                    padding-left: 1rem;
                    padding-right: 1rem;
                }
                .element-container {
                    width: 100%;
                }
                .stMarkdown {
                    width: 100%;
                }
            </style>
        """,
            unsafe_allow_html=True,
        )

        # 添加任务类型脑图
        st.write("### 🎯 人工智能常见任务")
        mermaid_chart = """
        graph LR
            AI((BaiCai AI)) --> CV(计算机视觉)
            AI --> NLP(自然语言处理)
            AI --> ML(机器学习)
            AI --> RS(推荐系统)

            CV --> CV1[图像识别]
            CV --> CV2[物体检测]
            CV1 --> CV1E[物体识别<br>商品图片分类]
            CV2 --> CV2E[无人驾驶<br>安防监控]

            NLP --> NLP1[文本分类]
            NLP --> NLP2[情感分析]
            NLP1 --> NLP1E[新闻分类<br>垃圾邮件过滤]
            NLP2 --> NLP2E[评论分析<br>舆情监控]

            ML --> ML1[预测分析]
            ML --> ML2[智能决策]
            ML1 --> ML1E[销量预测<br>股价预测]
            ML2 --> ML2E[风险评估<br>智能诊断]

            RS --> RS1[商品推荐]
            RS --> RS2[内容推荐]
            RS1 --> RS1E[电商推荐<br>个性化营销]
            RS2 --> RS2E[视频推荐<br>音乐推荐]

            classDef root fill:#0E1117,color:#fff,stroke:#31333F,stroke-width:2px
            classDef main fill:#1E88E5,color:#fff,stroke:#1565C0,stroke-width:1px
            classDef sub fill:#E3F2FD,color:#1565C0,stroke:#90CAF9,stroke-width:1px
            classDef example fill:#F5F5F5,color:#424242,stroke:#E0E0E0,stroke-width:1px

            class AI root
            class CV,NLP,ML,RS main
            class CV1,CV2,NLP1,NLP2,ML1,ML2,RS1,RS2 sub
            class CV1E,CV2E,NLP1E,NLP2E,ML1E,ML2E,RS1E,RS2E example

            linkStyle default stroke:#90CAF9,stroke-width:2px
        """
        stmd.st_mermaid(mermaid_chart)

        st.info("""
        👋 让我们详细了解每种 AI 任务类型：

        1. **计算机视觉**
           - **图像识别**
             * MNIST数字识别：手写数字自动识别的经典入门项目
             * 商品图片分类：电商平台商品自动分类、质量检测
             * 医学影像诊断：X光片分析、病理图像识别
             * 物体识别：动物、植物、商品、人脸识别
           - **物体检测**
             * 无人驾驶：道路场景识别、车辆行人检测
             * 安防监控：人流密度检测、异常行为识别
             * 工业质检：产品缺陷检测、装配线监控

        2. **自然语言处理**
           - **文本分类**
             * 新闻分类：自动对新闻文章进行主题分类
             * 垃圾邮件过滤：智能识别和过滤垃圾邮件
             * 客服工单分类：自动分类客户问题类型
           - **情感分析**
             * 评论分析：分析商品评论的情感倾向
             * 舆情监控：监测社交媒体上的品牌口碑
             * 用户反馈：分析用户满意度和情感趋势

        3. **机器学习**
           - **预测分析**
             * 销量预测：根据历史数据预测未来销量
             * 股价预测：分析市场趋势预测股票走向
             * 天气预测：结合多维数据预测天气变化
           - **智能决策**
             * 风险评估：信用卡欺诈检测、贷款风险评估
             * 智能诊断：基于数据的疾病风险预测
             * 客户分析：客户流失预警、精准营销

        4. **推荐系统**
           - **商品推荐**
             * 电商推荐：基于用户行为的商品推荐
             * 个性化营销：定制化的促销和营销策略
             * 相关商品推荐：购物场景下的商品关联推荐
           - **内容推荐**
             * 视频推荐：短视频和长视频的个性化推送
             * 音乐推荐：基于用户口味的音乐推荐
             * 新闻推荐：个性化新闻资讯推送

        每个任务类型都配备了完整的训练流程和详细的操作指南，您可以根据实际需求选择合适的任务开始尝试！
        """)


def show():
    # Check user_info folder and handle survey
    user_info_folder = get_tmp_folder("user_info")
    user_info_folder.mkdir(parents=True, exist_ok=True)

    env_folder = Path.home() / ".baicai" / "env"
    env_folder.mkdir(parents=True, exist_ok=True)

    st.title("欢迎使用🥬白菜人工智能平台")

    # Check if environment variables are set
    env_path = env_folder / ".env"
    if not env_path.exists():
        st.write("请先设置人工智能大模型")
        render_llm_settings(sidebar=False)
        st.rerun()

    # Check if survey.json exists
    survey_path = user_info_folder / "survey.json"
    if not survey_path.exists():
        # Show survey if no previous data exists
        st.write("在开始之前，请先完成我们的学习情况调查问卷。")
        survey_flow()
        return

    # If survey exists, show the clear button
    if st.sidebar.button("重新开始调查问卷"):
        clear_tmp_files("user_info")
        reset_survey_session_state()
        st.rerun()

    # 显示导航助手或主页内容
    tab1, tab2, tab3, tab4 = st.tabs(["🧭 任务导航", "📚 章节目录", "🔍 功能导航", "📚 平台介绍"])

    with tab1:
        button_graph()

    with tab2:
        st.subheader("📚 章节目录")

        # 创建章节数据结构
        chapters = [
            {
                "title": "人工智能基础",
                "icon": "🧠",
                "sections": [
                    {"title": "什么是人工智能", "duration": "15分钟", "difficulty": "入门"},
                    {"title": "人工智能的历史", "duration": "20分钟", "difficulty": "入门"},
                    {"title": "机器学习vs深度学习", "duration": "25分钟", "difficulty": "入门"},
                    {"title": "人工智能的应用场景", "duration": "30分钟", "difficulty": "入门"},
                ],
            },
            {
                "title": "机器学习基础",
                "icon": "🤖",
                "sections": [
                    {"title": "机器学习概述", "duration": "20分钟", "difficulty": "入门"},
                    {"title": "监督学习", "duration": "30分钟", "difficulty": "基础"},
                    {"title": "无监督学习", "duration": "30分钟", "difficulty": "基础"},
                    {"title": "强化学习", "duration": "35分钟", "difficulty": "进阶"},
                ],
            },
            {
                "title": "深度学习入门",
                "icon": "🧮",
                "sections": [
                    {"title": "神经网络基础", "duration": "40分钟", "difficulty": "基础"},
                    {"title": "卷积神经网络", "duration": "45分钟", "difficulty": "进阶"},
                    {"title": "循环神经网络", "duration": "45分钟", "difficulty": "进阶"},
                    {"title": "Transformer架构", "duration": "50分钟", "difficulty": "高级"},
                ],
            },
            {
                "title": "计算机视觉应用",
                "icon": "👁️",
                "sections": [
                    {"title": "图像分类入门", "duration": "30分钟", "difficulty": "基础"},
                    {"title": "目标检测技术", "duration": "40分钟", "difficulty": "进阶"},
                    {"title": "图像分割", "duration": "45分钟", "difficulty": "进阶"},
                    {"title": "计算机视觉实战", "duration": "60分钟", "difficulty": "高级"},
                ],
            },
            {
                "title": "自然语言处理",
                "icon": "🔤",
                "sections": [
                    {"title": "文本处理基础", "duration": "25分钟", "difficulty": "基础"},
                    {"title": "词嵌入技术", "duration": "35分钟", "difficulty": "进阶"},
                    {"title": "序列模型与注意力机制", "duration": "50分钟", "difficulty": "高级"},
                    {"title": "大型语言模型", "duration": "60分钟", "difficulty": "高级"},
                ],
            },
            {
                "title": "推荐系统",
                "icon": "🎯",
                "sections": [
                    {"title": "推荐系统概述", "duration": "20分钟", "difficulty": "基础"},
                    {"title": "协同过滤算法", "duration": "35分钟", "difficulty": "进阶"},
                    {"title": "基于内容的推荐", "duration": "30分钟", "difficulty": "进阶"},
                    {"title": "混合推荐系统", "duration": "40分钟", "difficulty": "高级"},
                ],
            },
        ]

        # 创建难度标签样式映射
        difficulty_styles = {
            "入门": "background-color: #a8e6cf; padding: 2px 8px; border-radius: 10px; font-size: 0.8em;",
            "基础": "background-color: #dcedc1; padding: 2px 8px; border-radius: 10px; font-size: 0.8em;",
            "进阶": "background-color: #ffd3b6; padding: 2px 8px; border-radius: 10px; font-size: 0.8em;",
            "高级": "background-color: #ffaaa5; padding: 2px 8px; border-radius: 10px; font-size: 0.8em;",
        }

        # 创建交互式章节导航
        selected_chapter = st.selectbox(
            "选择学习章节",
            options=range(len(chapters)),
            format_func=lambda x: f"{chapters[x]['icon']} {chapters[x]['title']}",
        )

        # 显示所选章节的内容
        st.write(f"### {chapters[selected_chapter]['icon']} {chapters[selected_chapter]['title']}")

        # 创建进度条
        total_sections = len(chapters[selected_chapter]["sections"])
        completed_sections = 0  # 假设用户还未完成任何章节
        progress = st.progress(completed_sections / total_sections)
        st.caption(f"学习进度: {completed_sections}/{total_sections} 完成")

        # 展示课程内容
        for i, section in enumerate(chapters[selected_chapter]["sections"]):
            with st.expander(f"{i + 1}. {section['title']}"):
                col1, col2, col3 = st.columns([5, 2, 2])

                with col1:
                    st.write("📝 **课程内容简介**")
                    # st.write(f"这是关于"{section['title']}"的学习内容，通过本节学习，您将掌握相关的核心概念和应用方法。")

                with col2:
                    st.write("⏱️ **预计用时**")
                    st.write(section["duration"])

                with col3:
                    st.write("📊 **难度等级**")
                    st.markdown(
                        f"<span style='{difficulty_styles[section['difficulty']]}'>{section['difficulty']}</span>",
                        unsafe_allow_html=True,
                    )

                # 添加学习和测验按钮
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"📚 开始学习 #{i + 1}", key=f"learn_{selected_chapter}_{i}"):
                        st.session_state.page = "lesson"
                        st.session_state.current_chapter = selected_chapter
                        st.session_state.current_section = i
                        st.rerun()
                with col2:
                    if st.button(f"✅ 章节测验 #{i + 1}", key=f"quiz_{selected_chapter}_{i}"):
                        st.session_state.page = "section_quiz"
                        st.session_state.current_chapter = selected_chapter
                        st.session_state.current_section = i
                        st.rerun()

        # 添加资源下载区
        st.write("### 📥 章节资源")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            **可下载资源:**
            * 📄 章节PPT
            * 📊 实验数据集
            * 📓 练习题与答案
            * 🧮 代码示例
            """)

        with col2:
            if st.button("📦 下载全部资源"):
                st.success("资源包下载已开始，请稍候...")

    with tab3:
        ability_navigator()

    with tab4:
        st.markdown("""
        ### 🚀 快速开始

        不知道从哪里开始？我们为您准备了三个简单步骤：
        1. 👉 使用左侧的**任务导航**，找到适合您数据类型的任务
        2. 📝 跟随交互式指南，一步步完成模型训练
        3. 🎯 获得立即可用的 AI 模型

        ### 💡 平台特色

        - 🤝 **零基础友好**
          * 交互式引导
          * 傻瓜式操作
          * 即时效果预览

        - 🛠️ **专业可靠**
          * 业界主流算法
          * 自动参数优化
          * 详细评估报告

        - ⚡ **高效便捷**
          * 快速模型训练
          * 实时训练监控
          * 一键模型部署

        ### 📊 使用流程

        1. **选择任务** ➔ 根据您的需求选择合适的 AI 任务
        2. **准备数据** ➔ 上传数据，我们会自动进行格式检查
        3. **配置模型** ➔ 按需调整参数，或使用推荐配置
        4. **开始训练** ➔ 启动训练，实时查看训练进度
        5. **应用模型** ➔ 下载模型或直接在线调用
        """)

        # 添加示例数据集
        st.subheader("🎯 快速入门项目")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.info("""
            ### 🖼️ 计算机视觉入门

            **经典项目**
            - MNIST数字识别
              手写数字自动识别，准确率95%+
            - CIFAR-10物体识别
              10类物体分类，可视化结果

            **适合人群**
            - 图像处理初学者
            - 计算机视觉爱好者
            - 深度学习入门者

            **预计耗时：** 15-30分钟
            """)

        with col2:
            st.info("""
            ### 📝 自然语言处理入门

            **经典项目**
            - 新闻分类
              自动对新闻进行多分类，准确率90%+
            - 情感分析
              分析商品评论情感倾向

            **适合人群**
            - 文本分析初学者
            - NLP技术探索者
            - 数据分析师

            **预计耗时：** 20-40分钟
            """)

        with col3:
            st.info("""
            ### 🎯 推荐系统入门

            **经典项目**
            - 电影推荐
              基于协同过滤的个性化推荐
            - 图书推荐
              结合内容的混合推荐系统

            **适合人群**
            - 推荐算法初学者
            - 电商从业者
            - 产品经理

            **预计耗时：** 30-45分钟
            """)
