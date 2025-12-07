<script>
// Hide navigation sidebar on homepage only
(function() {
  if (window.location.pathname === '/' || window.location.pathname.match(/^\/[^\/]*\/?$/)) {
    var style = document.createElement('style');
    style.textContent = `
      .md-sidebar--primary,
      .md-nav--primary {
        display: none !important;
        visibility: hidden !important;
        width: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
      }
      .md-main__inner {
        max-width: 100% !important;
      }
      .md-content {
        margin-left: 0 !important;
        max-width: 100% !important;
        padding-left: 1rem !important;
      }
    `;
    document.head.appendChild(style);
    
    // Also directly hide elements
    setTimeout(function() {
      var sidebar = document.querySelector('.md-sidebar--primary');
      var nav = document.querySelector('.md-nav--primary');
      if (sidebar) sidebar.style.display = 'none';
      if (nav) nav.style.display = 'none';
    }, 100);
  }
})();
</script>

# Welcome

**aipartnerupflow** is a Python framework for orchestrating and executing tasks. It manages when tasks run, how they depend on each other, and ensures everything executes in the right order.

## Key Features

- **Simple Task Management** - Create, organize, and execute tasks with ease
- **Dependency Handling** - Tasks automatically wait for their dependencies to complete
- **Flexible Execution** - Support for custom tasks, LLM agents (CrewAI), and more
- **Production Ready** - Built-in storage, streaming, and API support
- **Extensible** - Easy to add custom task types and integrations

---

## Quick Start

**New to aipartnerupflow?** Get up and running in 5 minutes!

[Quick Start Guide](getting-started/quick-start.md){ .md-button .md-button--primary }

[Core Concepts](getting-started/concepts.md){ .md-button }

[Examples](examples/basic_task.md){ .md-button }

---

## Documentation Sections

<div class="grid cards" markdown>

-   __Getting Started__

    ---

    Learn the fundamentals and get started quickly

    [Getting Started →](getting-started/index.md)

-   __User Guides__

    ---

    Complete guides for using aipartnerupflow

    [Guides →](guides/task-orchestration.md)

-   __API Reference__

    ---

    Complete API documentation for Python and HTTP

    [API Reference →](api/python.md)

-   __Architecture__

    ---

    System architecture and design principles

    [Architecture →](architecture/overview.md)

-   __Development__

    ---

    Contributing and extending the framework

    [Development →](development/setup.md)

-   __Examples__

    ---

    Code examples and common patterns

    [Examples →](examples/basic_task.md)

</div>

---

## Popular Guides

### For Users

- **[Task Orchestration](guides/task-orchestration.md)** - Complete guide to task orchestration, dependencies, and priorities
- **[Custom Tasks](guides/custom-tasks.md)** - Guide to creating custom tasks with ExecutableTask interface
- **[CLI](guides/cli.md)** - Complete CLI usage guide
- **[API Server](guides/api-server.md)** - API server setup and usage guide
- **[Best Practices](guides/best-practices.md)** - Best practices and recommendations

### For Developers

- **[Python API](api/python.md)** - Core Python library API reference (TaskManager, ExecutableTask, TaskTreeNode, etc.)
- **[HTTP API](api/http.md)** - A2A Protocol Server HTTP API reference
- **[Extending](development/extending.md)** - Guide for extending the framework (custom executors, extensions, hooks)
- **[Contributing](development/contributing.md)** - Contribution guidelines and process

### Architecture & Design

- **[Architecture Overview](architecture/overview.md)** - System architecture and design principles
- **[Directory Structure](architecture/directory-structure.md)** - Directory structure and naming conventions
- **[Naming Convention](architecture/naming-convention.md)** - Naming conventions for extensions
- **[Extension Registry Design](architecture/extension-registry-design.md)** - Extension registry design (Protocol-based architecture)
- **[Configuration](architecture/configuration.md)** - Database table configuration

### Examples & Tutorials

- **[Basic Task](examples/basic_task.md)** - Basic task examples and common patterns
- **[Task Tree](examples/task-tree.md)** - Task tree examples with dependencies and priorities
- **[Real World Examples](examples/real-world.md)** - Real-world use cases and examples
- **[First Steps Tutorial](getting-started/tutorials/tutorial-01-first-steps.md)** - Complete beginner tutorial

---

## Learning Paths

### New to aipartnerupflow?

1. **[Core Concepts](getting-started/concepts.md)** (5 min) - Learn the fundamental ideas
2. **[Quick Start](getting-started/quick-start.md)** (10 min) - Build your first task
3. **[First Steps Tutorial](getting-started/tutorials/tutorial-01-first-steps.md)** - Complete beginner tutorial

### Ready to Build?

1. **[Task Orchestration Guide](guides/task-orchestration.md)** - Deep dive into task management
2. **[Custom Tasks Guide](guides/custom-tasks.md)** - Create your own task types
3. **[Examples](examples/basic_task.md)** - Copy-paste ready examples

### Production Ready?

1. **[Best Practices](guides/best-practices.md)** - Production recommendations
2. **[API Reference](api/python.md)** - Complete API documentation
3. **[Architecture Overview](architecture/overview.md)** - Understand the system design

---

## Additional Resources

- [GitHub Repository](https://github.com/aipartnerup/aipartnerupflow) - Source code and issues
- [PyPI Package](https://pypi.org/project/aipartnerupflow/) - Install from PyPI
- [Protocol Documentation](protocol/01-overview.md) - A2A Protocol specification

---

## Need Help?

Check out our [FAQ](guides/faq.md) for common questions and answers.
