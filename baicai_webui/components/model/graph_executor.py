from typing import Any, Dict

import streamlit as st
from baicai_base.services import LLM
from baicai_dev.agents.graphs.action_builder import ActionBuilder
from baicai_dev.agents.graphs.baseline_builder import BaselineBuilder
from baicai_dev.agents.graphs.dl_builder.dl_builder import DLBuilder
from baicai_dev.agents.graphs.ml_graph import MLGraph
from baicai_dev.agents.graphs.optimization_builder import OptimizationBuilder
from baicai_dev.agents.graphs.workflow_builder import WorkflowBuilder
from baicai_dev.utils.data import TaskType
from baicai_dev.utils.setups import create_dl_config


class GraphExecutor:
    """Handles execution of ML and DL graphs"""

    @staticmethod
    def execute_ml_graph(
        config: Dict[str, Any],
        code_interpreter=None,
        auto=False,
        start_builder="baseline_builder",
        baseline_codes=None,
        workflow_codes=None,
        actions=None,
        llm_params=None,
    ):
        """Execute ML graph with given configuration"""
        # 验证必要参数
        configurable = config.get("configurable", config)  # 如果没有 configurable 字段，使用原始配置
        required_fields = ["path", "target"]
        missing_fields = [field for field in required_fields if not configurable.get(field)]
        if missing_fields:
            raise ValueError(f"缺少必要的配置参数: {', '.join(missing_fields)}")

        try:
            # Create LLM instance with provided parameters or defaults from env
            llm_instance = None
            if llm_params:
                llm_instance = LLM(**llm_params).llm

            if auto:
                graph = MLGraph(
                    config=config,
                    start_builder=start_builder,
                    code_interpreter=code_interpreter,
                    need_helper=True,
                    llm=llm_instance,
                )
                return graph
            else:
                if start_builder == "baseline_builder":
                    graph = BaselineBuilder(
                        config=config, need_helper=True, code_interpreter=code_interpreter, llm=llm_instance
                    )
                elif start_builder == "action_builder":
                    graph = ActionBuilder(
                        config=config,
                        need_helper=True,
                        code_interpreter=code_interpreter,
                        baseline_codes=baseline_codes,
                        llm=llm_instance,
                    )
                elif start_builder == "workflow_builder":
                    graph = WorkflowBuilder(
                        config=config,
                        need_helper=True,
                        code_interpreter=code_interpreter,
                        baseline_codes=baseline_codes,
                        actions=actions,
                        llm=llm_instance,
                    )
                elif start_builder == "optimization_builder":
                    graph = OptimizationBuilder(
                        config=config,
                        need_helper=True,
                        code_interpreter=code_interpreter,
                        workflow_codes=workflow_codes,
                        llm=llm_instance,
                    )
                return graph
        except Exception as e:
            raise ValueError(f"配置参数错误: {str(e)}")

    @staticmethod
    def execute_dl_graph(config: Dict[str, Any], code_interpreter=None, llm_params=None):
        """Execute DL graph with given configuration"""
        try:
            # Create LLM instance with provided parameters or defaults from env
            llm_instance = None
            if llm_params:
                llm_instance = LLM(**llm_params).llm

            # 使用create_dl_config创建标准配置
            dl_config = create_dl_config(config)

            # 创建DLBuilder并返回其app
            builder = DLBuilder(config=dl_config, need_helper=True, code_interpreter=code_interpreter, llm=llm_instance)
            return builder
        except Exception as e:
            raise ValueError(f"配置参数错误: {str(e)}")

    @staticmethod
    def get_graph_for_task(task_type: str):
        """Get appropriate graph executor for task type"""
        task_map = {
            TaskType.VISION.value: GraphExecutor.execute_dl_graph,
            TaskType.VISION_CSV.value: GraphExecutor.execute_dl_graph,
            TaskType.VISION_FUNC.value: GraphExecutor.execute_dl_graph,
            TaskType.VISION_RE.value: GraphExecutor.execute_dl_graph,
            TaskType.VISION_MULTI_LABEL.value: GraphExecutor.execute_dl_graph,
            TaskType.VISION_SINGLE_LABEL.value: GraphExecutor.execute_dl_graph,
            TaskType.NLP.value: GraphExecutor.execute_dl_graph,
            TaskType.COLLABORATIVE.value: GraphExecutor.execute_dl_graph,
            TaskType.ML.value: GraphExecutor.execute_ml_graph,
            TaskType.NLP_SENTIMENT_TRAINER.value: GraphExecutor.execute_dl_graph,
            TaskType.NLP_SENTIMENT_INFERENCE.value: GraphExecutor.execute_dl_graph,
            TaskType.NLP_NER_INFERENCE.value: GraphExecutor.execute_dl_graph,
            TaskType.NLP_SEMANTIC_MATCH_INFERENCE.value: GraphExecutor.execute_dl_graph,
        }

        return task_map.get(task_type)

    @staticmethod
    def get_llm_params():
        """Get LLM parameters from environment variables"""
        import os

        # Check if environment variables are set
        provider = os.environ.get("LLM_PROVIDER")
        if not provider:
            return None

        llm_params = {
            "provider": provider,
            "model_name": os.environ.get("LLM_MODEL_NAME"),
            "base_url": os.environ.get("LLM_BASE_URL"),
        }

        # Add temperature if available
        temp_str = os.environ.get("LLM_TEMPERATURE")
        if temp_str:
            try:
                llm_params["temperature"] = float(temp_str)
            except (ValueError, TypeError):
                pass

        return llm_params


def create_graph_executor():
    """Create or get graph executor from session state"""
    if "graph_executor" not in st.session_state:
        st.session_state.graph_executor = GraphExecutor()
    return st.session_state.graph_executor
