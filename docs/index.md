# aipartnerupflow

**Task Orchestration and Execution Framework**

Welcome to the aipartnerupflow documentation! This framework provides a unified task orchestration system that supports execution of multiple task types, from traditional API calls to LLM-based agent crews.

## What is aipartnerupflow?

aipartnerupflow is a **task orchestration and execution framework** designed to:

- **Orchestrate tasks**: Manage complex task trees with dependencies and priorities
- **Unified execution**: Support multiple task types through a single interface
- **Flexible architecture**: Core orchestration with optional LLM support via CrewAI
- **Production-ready**: Built-in storage, streaming, and A2A Protocol support

## Core Principles

### Pure Orchestration Core

The core of aipartnerupflow is **pure orchestration** with no LLM dependencies:

- Task orchestration specifications (TaskManager)
- Core interfaces (ExecutableTask, BaseTask, TaskStorage)
- Storage (DuckDB default, PostgreSQL optional)
- **NO CrewAI dependency** (available via `[crewai]` extra)

### Optional Features

- **[crewai]**: LLM-based agent crews via CrewManager
- **[a2a]**: A2A Protocol Server for agent-to-agent communication
- **[cli]**: Command-line interface tools
- **[postgres]**: PostgreSQL storage support

## Quick Start

### Installation

```bash
# Core library (pure orchestration)
pip install aipartnerupflow

# With CrewAI support
pip install aipartnerupflow[crewai]

# Everything
pip install aipartnerupflow[all]
```

### Basic Usage

```python
from aipartnerupflow import TaskManager, TaskTreeNode, create_session

# Create database session and task manager
db = create_session()
task_manager = TaskManager(db)

# Create and execute tasks
root_task = await task_manager.task_repository.create_task(
    name="root_task",
    user_id="user_123",
    priority=2
)

task_tree = TaskTreeNode(root_task)
result = await task_manager.distribute_task_tree(task_tree)
```

## Documentation Structure

- **[Getting Started](getting-started/installation.md)**: Installation and quick start guides
- **[User Guide](user-guide/overview.md)**: How to use aipartnerupflow
- **[Architecture](architecture/overview.md)**: System design and architecture
- **[Development](development/development.md)**: Contributing and development guides
- **[API Reference](api/core.md)**: API documentation

## Key Features

### Task Orchestration

- **TaskManager**: Task tree orchestration, dependency management, priority scheduling
- **Unified Execution**: All task types unified through the `ExecutableTask` interface
- **Storage**: Task state persistence (DuckDB/PostgreSQL)

### Task Execution Types

- **Custom Tasks**: Implement `ExecutableTask` for your own task types
- **CrewManager**: LLM-based task execution via CrewAI
- **BatchManager**: Batch orchestration container for multiple crews

### Protocol Support

- **A2A Protocol**: Standard protocol for agent-to-agent communication
- **Streaming**: Real-time progress updates via SSE/WebSocket
- **Multiple Transports**: HTTP, SSE, WebSocket support

## Resources

- **GitHub**: [aipartnerup/aipartnerupflow](https://github.com/aipartnerup/aipartnerupflow)
- **PyPI**: [aipartnerupflow](https://pypi.org/project/aipartnerupflow/)
- **Website**: [aipartnerup.com](https://aipartnerup.com)

## License

Apache-2.0

