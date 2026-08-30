"""
Planner Agent Module.
Decomposes high-level objectives into dependency-managed DAG execution trees.
"""
from typing import Any, Dict
from app.core.dag import DAGGraph, TaskNode, TaskStatus
from app.services.agents.base import BaseAgent


class PlannerAgent(BaseAgent):
    """Specialist Agent responsible for architectural task decomposition."""

    def __init__(self) -> None:
        super().__init__(agent_role="planner")

    async def run(self, task_input: Dict[str, Any]) -> Dict[str, Any]:
        goal = task_input.get("goal", "Execute Workflow")
        
        prompt = (
            f"You are a Staff Systems Architect. Break down the following objective into a 3-step DAG:\n"
            f"Objective: '{goal}'\n\n"
            f"1. Research Task\n2. Analytical Execution Task\n3. Quality Critique Task"
        )
        
        # Invoke LLM for plan synthesis
        llm_response = self.invoke_model(prompt)

        # Build structured DAGGraph
        graph = DAGGraph()
        
        task1 = TaskNode(
            id="task_1_research",
            title="Gather Domain Context & Data",
            description=f"Research context and parameters for: {goal}",
            assigned_agent="researcher",
            input_data={"goal": goal}
        )
        
        task2 = TaskNode(
            id="task_2_analysis",
            title="Execute Data Analysis & Synthesis",
            description=f"Analyze research data and construct solution for: {goal}",
            assigned_agent="executor",
            dependencies=["task_1_research"],
            input_data={"goal": goal}
        )

        task3 = TaskNode(
            id="task_3_critique",
            title="Evaluate Output Quality & Constraints",
            description="Critique synthesized results against accuracy and completeness standards",
            assigned_agent="critic",
            dependencies=["task_2_analysis"],
            input_data={"goal": goal}
        )

        graph.add_node(task1)
        graph.add_node(task2)
        graph.add_node(task3)

        graph.validate_dag()

        return {
            "status": "success",
            "plan_summary": llm_response,
            "dag_graph": graph.model_dump()
        }
