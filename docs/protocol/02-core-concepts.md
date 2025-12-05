# Core Concepts

This section defines the fundamental concepts of the AI Partner Up Flow Protocol. Understanding these concepts is essential for implementing the protocol in any language.

## Flow

A **Flow** represents a complete workflow or process. It is structured as a hierarchical tree of **Tasks**.

*   **Structure**: A Flow is a Directed Acyclic Graph (DAG) where tasks are nodes and dependencies define the edges.
*   **Root Task**: Every flow has a single root task. Complex flows are built by adding children to this root task.

## Task

A **Task** is the atomic unit of execution within a Flow.

*   **Definition**: A task is defined by its `name` (what to do) and `inputs` (data to work on).
*   **Identity**: Each task has a unique `id` (UUID) that persists across the network.
*   **State**: A task has a well-defined state (e.g., `pending`, `in_progress`, `completed`).

## Executor

An **Executor** is the component responsible for performing the actual work defined by a Task.

*   **Role**: It takes a Task's `inputs`, performs the operation, and produces a `result`.
*   **Types**: Executors can be simple functions, API calls, or complex agents (LLMs).
*   **Abstraction**: The protocol defines *how* to invoke an executor, but not *what* the executor does internally.

## Node

A **Node** is a participant in the network that implements the protocol.

*   **Capabilities**: A node can submit flows, execute tasks, or store results.
*   **Interoperability**: Nodes running different language implementations (Python, Go, Rust) can communicate as long as they adhere to the Data Protocol.
