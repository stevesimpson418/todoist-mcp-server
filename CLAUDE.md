# CLAUDE.md — Project Intelligence

## Project Overview

Todoist MCP server built with FastMCP. Wraps both the Todoist REST v2 and Sync API v1
for comprehensive task management through Claude. Runs locally via stdio transport —
API token stays on the user's machine.

## Tech Stack

- **Language:** Python 3.12+
- **Package manager:** uv (never use pip directly)
- **MCP framework:** FastMCP 2.0+
- **Todoist APIs:** todoist-api-python (REST v2), httpx (Sync API v1 batch ops)
- **Linting/formatting:** Ruff (config in ruff.toml)
- **Testing:** pytest + pytest-cov + pytest-asyncio
- **Git hooks:** Lefthook (ruff, markdownlint, shellcheck, shfmt, commitlint)
- **CI:** GitHub Actions (lint + test matrix)

## Project Structure

```text
src/todoist_mcp_server/       # Source code (src layout)
  server.py                   # Entry point — FastMCP init + tool registration
  tools.py                    # MCP tool definitions (register_todoist_tools)
  client.py                   # Todoist API client (REST v2 + Sync v1 batch)
  exceptions.py               # Custom exception classes
tests/                        # Pytest test suite
  conftest.py                 # Shared fixtures
  test_tools.py               # Tool registration and delegation tests
  test_client.py              # REST v2 client tests
  test_batch.py               # Sync API batch operation tests
```

## Key Commands

```bash
uv sync --dev                                                    # Install all deps
uv run pytest -v                                                 # Run tests
uv run pytest --cov=todoist_mcp_server --cov-report=term-missing # Coverage
uv run ruff check src/ tests/                                    # Lint
uv run ruff format src/ tests/                                   # Format
lefthook install                                                 # Install git hooks
```

## Conventions

- **Commits:** Conventional Commits format — `type(scope): description`
- **Line length:** 100 characters
- **Quotes:** Double quotes (enforced by ruff)
- **Imports:** Sorted by isort via ruff, first-party package declared in ruff.toml
- **Tests:** Mirror source structure, use fixtures in conftest.py
- **Entry point:** `server.py:main()` — registered as console script in pyproject.toml

## Architecture Pattern

1. `server.py` creates the FastMCP instance and calls `register_todoist_tools(mcp)`
2. `tools.py` defines all MCP tools using `@mcp.tool()` decorators inside `register_todoist_tools()`
3. `client.py` wraps the Todoist APIs (keeps tool definitions thin)
4. `exceptions.py` defines domain-specific exceptions

Tools should be thin wrappers that delegate to the client. Keep business logic in the client.

## Notable: Graceful Degradation

The server starts without Todoist tools if `TODOIST_API_TOKEN` is not set. This allows
Claude to load the server without errors even when unconfigured.

## Development Workflow

- **New features:** Use `/feature-dev:feature-dev` if available — it handles codebase
  analysis, architecture planning, and guided implementation.
- **Branching:** Create a feature branch (`feat/<description>`) before starting work.
- **TDD:** Write tests alongside code. Run `uv run pytest -v` early and often.
- **Review cycle:** Run `/pr-review-toolkit:review-pr code` before every commit.
  Run `/pr-review-toolkit:review-pr all parallel` before pushing or creating a PR.
- **Releases:** Tag-triggered. Push a `v*` tag to create a GitHub release with
  an auto-generated changelog (`git tag v0.2.0 && git push origin v0.2.0`).
