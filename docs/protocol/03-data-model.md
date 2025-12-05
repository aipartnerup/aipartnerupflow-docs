# Data Model

The Data Model defines the standard JSON structure for objects exchanged between components. Adherence to this schema ensures interoperability.

## Task Schema

A Task is represented as a JSON object with the following fields:

| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `id` | String (UUID) | Yes | Unique identifier for the task. |
| `parent_id` | String (UUID) | No | ID of the parent task (if part of a hierarchy). |
| `name` | String | Yes | Name or method identifier of the task. |
| `status` | String | Yes | Current state: `pending`, `in_progress`, `completed`, `failed`, `cancelled`. |
| `priority` | Integer | No | Execution priority. Lower value = Higher priority. Default: `2`. |
| `inputs` | Object (JSON) | No | **Runtime** input parameters for the executor. |
| `schemas` | Object (JSON) | No | **Configuration** and method definition. Defines *what* to run and *how*. |
| `result` | Object (JSON) | No | Execution result (populated when status is `completed`). |
| `error` | String | No | Error message (populated when status is `failed`). |
| `dependencies` | Array | No | List of dependencies that must be satisfied before execution. |

### Inputs vs Schemas

It is critical to distinguish between `inputs` and `schemas`:

*   **`schemas`**: Defines the **Method** and **Static Configuration**. It tells the system *which* executor to use and provides configuration that doesn't change between runs (e.g., model name, weights, validation rules).
    *   `method`: The key used to look up the executor in the `ExecutorRegistry`.
    *   `input_schema`: JSON Schema defining what `inputs` are valid.
    *   `input_data`: Static configuration data.
*   **`inputs`**: Defines the **Runtime Data**. It contains the actual data to be processed (e.g., a URL to crawl, a specific text to analyze).

### Example JSON

```json
{
  "id": "task-crawl-001",
  "name": "Crawl Website",
  "status": "pending",
  "priority": 1,
  
  // Runtime Data (The "Variable" part)
  "inputs": {
    "url": "https://example.com"
  },

  // Configuration (The "Static" part)
  "schemas": {
    "type": "local",
    "method": "web_crawler",
    "input_schema": {
      "type": "object",
      "required": ["url"],
      "properties": {
        "url": { "type": "string" }
      }
    }
  }
}
```

## External Resources & Executor Registration

The protocol supports extending functionality via **External Resources**.

*   **Custom Executors**: Users can implement custom logic (e.g., inheriting from `crew_manager` or other base classes).
*   **Registration**: These custom executors must be registered with the `ExecutorRegistry` using the `method` name defined in `schemas`.

### Registration Example (Python)

```python
from aipartnerupflow.core.extensions import executor_registry

@executor_registry.register("my_custom_analyzer")
class MyCustomAnalyzer:
    async def execute(self, inputs):
        # Implementation handling external resources
        pass
```

In the Task JSON, you would then reference this:

```json
{
  "schemas": {
    "method": "my_custom_analyzer"
  }
}
```

## Dependency Schema

Dependencies define the execution order. A task can depend on the completion of other tasks.

| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `id` | String (UUID) | Yes | ID of the task to depend on. |
| `required` | Boolean | No | If `true`, the dependent task must complete successfully. Default: `true`. |

## Task Tree Node

For hierarchical representation (e.g., when distributing a flow), tasks are wrapped in a Tree Node structure.

```json
{
  "task": { ...Task Object... },
  "children": [
    { ...TaskTreeNode Object... }
  ]
}
```
