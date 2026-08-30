"""
DAG Engine & Task Dependency Resolver Module.
Provides Directed Acyclic Graph validation, topological execution ordering, and state management.
"""
from enum import Enum
from typing import Any, Dict, List, Optional, Set
from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskNode(BaseModel):
    """Atomic Task Node within a DAG workflow execution tree."""
    id: str = Field(..., description="Unique task node identifier")
    title: str = Field(..., description="Human-readable task title")
    description: str = Field(..., description="Detailed instructions for assigned agent")
    assigned_agent: str = Field(..., description="Agent role (planner, researcher, executor, critic)")
    dependencies: List[str] = Field(default_factory=list, description="IDs of prerequisite task nodes")
    status: TaskStatus = Field(default=TaskStatus.PENDING, description="Current execution state")
    input_data: Dict[str, Any] = Field(default_factory=dict, description="Task execution inputs")
    output_data: Optional[Dict[str, Any]] = Field(default=None, description="Task execution result payload")
    error: Optional[str] = Field(default=None, description="Error message if task failed")
    retry_count: int = Field(default=0, description="Current retry attempt count")
    max_retries: int = Field(default=3, description="Maximum retry limit")


class DAGGraph(BaseModel):
    """Directed Acyclic Graph containing workflow tasks and dependencies."""
    nodes: Dict[str, TaskNode] = Field(default_factory=dict, description="Map of task ID to TaskNode")

    def add_node(self, node: TaskNode) -> None:
        """Adds a task node to the DAG graph."""
        self.nodes[node.id] = node

    def validate_dag(self) -> bool:
        """Validates that the task dependency graph contains zero cycles (Kahn's Algorithm)."""
        in_degree: Dict[str, int] = {node_id: 0 for node_id in self.nodes}
        
        for node in self.nodes.values():
            for dep in node.dependencies:
                if dep not in self.nodes:
                    raise ValueError(f"Task '{node.id}' depends on non-existent task '{dep}'")
                in_degree[node.id] += 1

        queue = [node_id for node_id, degree in in_degree.items() if degree == 0]
        visited_count = 0

        while queue:
            curr = queue.pop(0)
            visited_count += 1
            for node in self.nodes.values():
                if curr in node.dependencies:
                    in_degree[node.id] -= 1
                    if in_degree[node.id] == 0:
                        queue.append(node.id)

        return visited_count == len(self.nodes)

    def get_executable_nodes(self) -> List[TaskNode]:
        """Returns pending nodes whose dependencies are all completed."""
        executable: List[TaskNode] = []
        for node in self.nodes.values():
            if node.status != TaskStatus.PENDING:
                continue

            deps_satisfied = True
            for dep_id in node.dependencies:
                dep_node = self.nodes.get(dep_id)
                if not dep_node or dep_node.status != TaskStatus.COMPLETED:
                    deps_satisfied = False
                    break

            if deps_satisfied:
                executable.append(node)

        return executable

    def is_complete(self) -> bool:
        """Returns true if all nodes in the DAG have reached a terminal state (COMPLETED or FAILED)."""
        return all(
            node.status in (TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED)
            for node in self.nodes.values()
        )
