import asyncio
import os

import streamlit as st
import torch
from baicai_base.utils.setups import setup_code_interpreter
from baicai_dev.utils.data import TaskType

from baicai_webui.components.chat import ai_assistant
from baicai_webui.components.model import create_training_monitor, result_display

torch.classes.__path__ = [os.path.join(torch.__path__[0], torch.classes.__file__)]


class BasePage:
    """Base page component for different task types"""

    def __init__(self, task_type: TaskType, data_uploader_func):
        self.task_type = task_type
        self.data_uploader_func = data_uploader_func

        if "code_interpreter" not in st.session_state:
            st.session_state.code_interpreter = setup_code_interpreter()

        # 初始化页面状态
        if "page_state" not in st.session_state:
            st.session_state.page_state = {
                "monitor": create_training_monitor(),
                "helper_ready": False,
                "post_train_completed": False,
                "data_config": None,
                "pre_train_container": None,
                "run_post_train": False,
            }

        if "data_config" not in st.session_state:
            st.session_state.data_config = None

        # Initialize graph_state in session state
        if "graph_state" not in st.session_state:
            st.session_state.graph_state = {
                "messages": [],
                "dl_codes": [],
                "dl_models": [],
                "dl_success": False,
            }

    def show(self, pre_train=None, post_train=None, title=None):
        """Display the page with common structure"""
        st.title(f"{title or self.task_type.value}")

        # Create tabs
        tab1, tab2, tab3 = st.tabs(["🤖 智能体配置", "📈结果查看", "💬 AI助手"])

        monitor = st.session_state.page_state["monitor"]

        with tab1:
            # Data upload and configuration
            data_config = self.data_uploader_func()
            if not data_config:
                st.warning("请上传数据")
                return

            data_config["configurable"]["from_web_ui"] = True

            if data_config:
                st.session_state.data_config = data_config
                if pre_train:
                    pre_train()

                # Show start training button
                if st.button("开始训练", type="primary", key="start_training_button"):
                    st.session_state.page_state["post_train_completed"] = False
                    st.session_state.page_state["run_post_train"] = True
                    try:
                        result = asyncio.run(
                            monitor.start_training(
                                task_type=self.task_type.value,
                                config=data_config,
                                code_interpreter=st.session_state.code_interpreter,
                            )
                        )
                        if result:
                            state_values = monitor.app.get_state(data_config).values
                            st.session_state.graph_state["dl_codes"] = state_values.get("dl_codes", [])
                            st.session_state.graph_state["dl_models"] = state_values.get("dl_models", [])
                            st.session_state.graph_state["dl_success"] = state_values.get("dl_success", False)
                            st.session_state.page_state["helper_ready"] = True
                            st.success("训练已启动！")
                    except Exception as e:
                        st.error(f"训练失败：{str(e)}")

        with tab2:
            # Handle post_train in a separate rerun
            if (
                st.session_state.page_state["run_post_train"]
                and post_train
                and not st.session_state.page_state["post_train_completed"]
            ):
                try:
                    asyncio.run(post_train(st.session_state.code_interpreter))
                    st.session_state.page_state["post_train_completed"] = True
                    st.session_state.page_state["run_post_train"] = False
                except Exception as e:
                    st.error(f"训练后处理失败：{str(e)}")
                    st.session_state.page_state["post_train_completed"] = True
                    st.session_state.page_state["run_post_train"] = False
            # Display results
            if st.session_state.page_state["helper_ready"]:
                result_display.display_results(st.session_state.graph_state, graph="dl")

        with tab3:
            if st.session_state.page_state["helper_ready"]:
                ai_assistant.create_ai_assistant(monitor, task_type=self.task_type.value)
            else:
                st.info("请先完成训练")
