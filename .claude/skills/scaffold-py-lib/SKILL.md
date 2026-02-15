---
name: scaffold-py-lib
description: Scaffold a new Python library in libs/ with standard directory structure, pyproject.toml, project.json, and Nx integration
user-invocable: true
argument-hint: "<library-name>"
---

# Skill: Scaffold Python Library

Create a new Python library in the monorepo with the standard project structure.

## When to Use

- When creating a new shared library in `libs/`
- When a new app needs a companion library

## Inputs

Library name is passed as an argument: `/scaffold-py-lib my-lib-name`

The name should use hyphens (e.g., `py-agents`). The Python package name uses underscores (e.g., `py_agents`).

## What Gets Created

```
libs/<lib-name>/
├── src/<package_name>/
│   └── __init__.py
├── tests/
│   └── test_placeholder.py
├── pyproject.toml
├── project.json
└── README.md
```

## Implementation Steps

1. **Derive names** from the argument:
   - `lib_name`: as provided (e.g., `py-agents`)
   - `package_name`: replace hyphens with underscores (e.g., `py_agents`)

2. **Create directory structure**:
   ```
   libs/<lib_name>/src/<package_name>/
   libs/<lib_name>/tests/
   ```

3. **Create `pyproject.toml`**:
   ```toml
   [tool.poetry]
   name = "<lib_name>"
   version = "0.1.0"
   description = ""
   authors = []
   readme = "README.md"
   packages = [{ include = "<package_name>", from = "src" }]

   [tool.poetry.dependencies]
   python = "^3.12"

   [build-system]
   requires = ["poetry-core"]
   build-backend = "poetry.core.masonry.api"
   ```

4. **Create `project.json`** (Nx integration):
   ```json
   {
     "name": "<lib_name>",
     "projectType": "library",
     "sourceRoot": "libs/<lib_name>/src",
     "targets": {
       "test": {
         "executor": "nx:run-commands",
         "options": {
           "command": "poetry run pytest libs/<lib_name>/tests -v",
           "cwd": "."
         }
       },
       "lint": {
         "executor": "nx:run-commands",
         "options": {
           "command": "poetry run ruff check libs/<lib_name>/",
           "cwd": "."
         }
       }
     }
   }
   ```

5. **Create `src/<package_name>/__init__.py`**:
   ```python
   """<lib_name> — [brief description]."""
   ```

6. **Create `tests/test_placeholder.py`**:
   ```python
   """Placeholder test to verify library structure."""

   def test_import():
       import <package_name>
       assert <package_name> is not None
   ```
   Note: Do NOT add `__init__.py` to the `tests/` folder (causes namespace collisions in monorepo).

7. **Create `README.md`**:
   ```markdown
   # <lib_name>

   > Part of the [ai-engineering-monorepo](../../README.md).
   ```

8. **Ask the user** if the library should be added as a path dependency to the root `pyproject.toml` or to a specific app.

## After Scaffolding

Provide the user with next steps:
- Add dependencies to `pyproject.toml`
- Run `poetry lock` at root
- Run `poetry install` to install the new library
- Replace the placeholder test with real tests

## Rules

- Always use Python 3.12+ (`^3.12`)
- Never add `__init__.py` to test directories
- Use `packages = [{ include = "<name>", from = "src" }]` layout
- Follow existing library patterns (reference `libs/py-core/` as example)