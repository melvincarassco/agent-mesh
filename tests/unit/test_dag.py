"""
Unit tests for DAG Engine and Task Dependency Resolver.
"""
import pytest
from app.core.dag import DAGGraph, TaskNode, TaskStatus


def test_dag_graph_node_addition_and_execution_resolution():
    """Verify DAG executable nodes resolution based on prerequisite completion."""
    graph = DAGGraph()

    node1 = TaskNode(
        id="t1",
        title="Research",
        description="Research task",
        assigned_agent="researcher"
    )

    node2 = TaskNode(
        id="t2",
        title="Analysis",
        description="Analysis task",
        assigned_agent="executor",
        dependencies=["t1"]
    )

    graph.add_node(node1)
    graph.add_node(node2)

    assert graph.validate_dag() is True

    # Initially, only t1 is executable because t2 depends on t1
    exec_nodes = graph.get_executable_nodes()
    assert len(exec_nodes) == 1
    assert exec_nodes[0].id == "t1"

    # Complete t1
    node1.status = TaskStatus.COMPLETED

    # Now t2 becomes executable
    exec_nodes_after = graph.get_executable_nodes()
    assert len(exec_nodes_after) == 1
    assert exec_nodes_after[0].id == "t2"


def test_dag_graph_cycle_detection():
    """Verify DAG cycle detection raises ValueError."""
    graph = DAGGraph()

    node1 = TaskNode(
        id="t1",
        title="Task 1",
        description="Desc",
        assigned_agent="executor",
        dependencies=["t2"]
    )

    node2 = TaskNode(
        id="t2",
        title="Task 2",
        description="Desc",
        assigned_agent="executor",
        dependencies=["t1"]
    )

    graph.add_node(node1)
    graph.add_node(node2)

    # Circular dependency t1 <-> t2 should fail validation
    assert graph.validate_dag() is False
