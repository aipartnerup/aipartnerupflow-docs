# Execution Lifecycle

The Execution Lifecycle defines how a Task transitions between states and how the system manages execution order.

## State Machine

A Task transitions through the following states:

1.  **Pending** (`pending`): The task is created but not yet started. It may be waiting for dependencies or a worker slot.
2.  **In Progress** (`in_progress`): The task is currently being executed by an Executor.
3.  **Terminal States**:
    *   **Completed** (`completed`): The task finished successfully. `result` field is populated.
    *   **Failed** (`failed`): The task encountered an error. `error` field is populated.
    *   **Cancelled** (`cancelled`): The task was manually stopped.

### State Transitions

```mermaid
graph LR
    Pending --> InProgress
    InProgress --> Completed
    InProgress --> Failed
    InProgress --> Cancelled
    Pending --> Cancelled
    Failed --> Pending: Re-execution
```

## Execution Logic

### 1. Priority
Tasks are executed based on their `priority` field.
*   **Order**: Ascending (ASC). Lower numbers execute first.
*   **Standard Values**:
    *   `0`: Urgent
    *   `1`: High
    *   `2`: Normal (Default)
    *   `3`: Low

### 2. Dependency Resolution
A task cannot start until all its dependencies are satisfied.
*   **Satisfied**: The dependent task is in `completed` state.
*   **Waiting**: If a dependency is `pending` or `in_progress`, the task waits.
*   **Failure**: If a dependency is `failed`, the dependent task cannot proceed (unless specific error handling is defined).

### 3. Re-execution
The protocol supports re-execution of tasks.
*   **Failed Tasks**: Can be reset to `pending` to retry execution.
*   **Cascading**: If a task is re-executed, all tasks that depend on it must also be re-verified or re-executed to ensure consistency.
