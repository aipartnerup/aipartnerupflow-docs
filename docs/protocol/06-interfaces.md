# Interface Protocol

The Interface Protocol defines how external clients (CLIs, Dashboards, other Agents) interact with an AI Partner Up Flow node.

The standard interface uses **JSON-RPC 2.0 over HTTP**.

## Transport

*   **Protocol**: HTTP/1.1 or HTTP/2
*   **Method**: `POST`
*   **Endpoint**: `/tasks`
*   **Content-Type**: `application/json`

## Message Format

### Request
```json
{
  "jsonrpc": "2.0",
  "method": "tasks.create",
  "params": {
    "name": "My Task",
    "inputs": { "key": "value" }
  },
  "id": "req-001"
}
```

### Response (Success)
```json
{
  "jsonrpc": "2.0",
  "result": {
    "id": "task-uuid",
    "status": "pending"
  },
  "id": "req-001"
}
```

### Response (Error)
```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32600,
    "message": "Invalid Request",
    "data": "Details..."
  },
  "id": "req-001"
}
```

## Standard Methods

A compliant node MUST support the following methods:

### Task Management

| Method | Description | Params |
| :--- | :--- | :--- |
| `tasks.create` | Create a new task or flow. | `Task` object (without ID) |
| `tasks.get` | Retrieve a task by ID. | `{"task_id": "uuid"}` |
| `tasks.update` | Update task fields. | `{"task_id": "uuid", "updates": {...}}` |
| `tasks.delete` | Delete a task. | `{"task_id": "uuid"}` |
| `tasks.list` | List tasks with filters. | `{"limit": 100, "status": "..."}` |
| `tasks.execute` | Execute a task (supports streaming). | `{"task_id": "uuid"}` |
| `tasks.cancel` | Cancel a running task. | `{"task_id": "uuid"}` |

### Task Query

| Method | Description | Params |
| :--- | :--- | :--- |
| `tasks.tree` | Get the full task hierarchy. | `{"task_id": "uuid"}` |
| `tasks.children` | Get direct children of a task. | `{"parent_id": "uuid"}` |

## CLI Reference

The `aipartnerupflow` CLI is a reference implementation of a client using this protocol.

```bash
# Example mapping
aipartnerupflow task create  ->  tasks.create
aipartnerupflow task list    ->  tasks.list
```
