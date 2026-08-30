"""
Workflow Orchestrator Engine.
Manages DAG execution loop, agent worker dispatches, and step state streaming.
"""
import asyncio
import logging
import uuid
from typing import AsyncGenerator, Dict, Any, Optional

from app.core.dag import DAGGraph, TaskNode, TaskStatus
from app.services.agents.planner import PlannerAgent
from app.services.agents.researcher import ResearcherAgent
from app.services.agents.executor import ExecutorAgent
from app.services.agents.critic import CriticAgent

logger = logging.getLogger(__name__)


class WorkflowOrchestrator:
    """Engine orchestrating multi-agent DAG execution and streaming events."""

    def __init__(self) -> None:
        self._workflows: Dict[str, Dict[str, Any]] = {}
        self._agents = {
            "planner": PlannerAgent(),
            "researcher": ResearcherAgent(),
            "executor": ExecutorAgent(),
            "critic": CriticAgent(),
        }

    async def initialize_workflow(self, goal: str) -> str:
        """Initializes workflow, runs Planner Agent, and constructs DAG dependency graph."""
        workflow_id = f"wf-{uuid.uuid4().hex[:8]}"
        
        logger.info(f"Initializing workflow '{workflow_id}' for goal: '{goal}'")
        
        planner = self._agents["planner"]
        plan_result = await planner.run({"goal": goal})
        
        graph = DAGGraph.model_validate(plan_result["dag_graph"])

        self._workflows[workflow_id] = {
            "workflow_id": workflow_id,
            "goal": goal,
            "status": "RUNNING",
            "plan_summary": plan_result["plan_summary"],
            "graph": graph,
            "execution_log": []
        }

        return workflow_id

    def get_workflow(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves workflow execution status and graph state."""
        return self._workflows.get(workflow_id)

    async def run_workflow_stream(self, workflow_id: str) -> AsyncGenerator[Dict[str, Any], None]:
        """Executes DAG tasks step-by-step and yields real-time SSE progress events."""
        wf = self._workflows.get(workflow_id)
        if not wf:
            yield {"event": "error", "message": f"Workflow {workflow_id} not found"}
            return

        graph: DAGGraph = wf["graph"]

        yield {
            "event": "workflow_started",
            "workflow_id": workflow_id,
            "goal": wf["goal"],
            "plan_summary": wf["plan_summary"]
        }

        while not graph.is_complete():
            executable_nodes = graph.get_executable_nodes()
            
            if not executable_nodes:
                # Check for deadlocks or waiting tasks
                if any(n.status == TaskStatus.RUNNING for n in graph.nodes.values()):
                    await asyncio.sleep(0.1)
                    continue
                else:
                    logger.warning(f"Workflow {workflow_id} reached terminal state with unexecuted tasks.")
                    break

            for node in executable_nodes:
                node.status = TaskStatus.RUNNING
                yield {
                    "event": "task_started",
                    "task_id": node.id,
                    "task_title": node.title,
                    "agent": node.assigned_agent
                }

                agent = self._agents.get(node.assigned_agent, self._agents["executor"])
                
                # Gather prerequisite output data from completed dependencies
                prereq_data = {}
                for dep_id in node.dependencies:
                    dep_node = graph.nodes.get(dep_id)
                    if dep_node and dep_node.output_data:
                        prereq_data[dep_id] = dep_node.output_data

                try:
                    task_input = {
                        "description": node.description,
                        "prerequisite_data": prereq_data
                    }
                    output = await agent.run(task_input)
                    
                    node.status = TaskStatus.COMPLETED
                    node.output_data = output
                    
                    yield {
                        "event": "task_completed",
                        "task_id": node.id,
                        "task_title": node.title,
                        "agent": node.assigned_agent,
                        "output": output
                    }

                except Exception as exc:
                    logger.error(f"Task {node.id} failed: {exc}")
                    node.retry_count += 1
                    if node.retry_count >= node.max_retries:
                        node.status = TaskStatus.FAILED
                        node.error = str(exc)
                        yield {
                            "event": "task_failed",
                            "task_id": node.id,
                            "error": str(exc)
                        }
                    else:
                        node.status = TaskStatus.PENDING

        wf["status"] = "COMPLETED" if all(n.status == TaskStatus.COMPLETED for n in graph.nodes.values()) else "FAILED"

        yield {
            "event": "workflow_finished",
            "workflow_id": workflow_id,
            "final_status": wf["status"]
        }


_orchestrator_singleton = WorkflowOrchestrator()


def get_orchestrator() -> WorkflowOrchestrator:
    """Returns singleton instance of WorkflowOrchestrator."""
    return _orchestrator_singleton
