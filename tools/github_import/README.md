# GitHub Project Import Tool

Automates the creation of GitHub Issues, Labels, and Milestones from a structured JSON file.

## Overview

This tool reads work package definitions from `work_packages.json` and creates corresponding GitHub Issues with proper labels, milestones, and formatted descriptions.

## Prerequisites

- Python 3.10+
- [GitHub CLI (`gh`)](https://cli.github.com/) installed and authenticated
- Repository write access

## Usage

### Dry Run (Preview)

See what would be created without making changes:

```bash
python3 -m tools.github_import.run_import --dry-run
```

### Full Import

Create all issues, labels, and milestones:

```bash
python3 -m tools.github_import.run_import
```

### Include Completed Items

By default, work packages with `"status": "done"` are skipped. To include them:

```bash
python3 -m tools.github_import.run_import --include-done
```

## Configuration

### work_packages.json Structure

```json
{
  "project": "Project Name",
  "phases": [
    {
      "id": "phase-1",
      "name": "Phase Name",
      "estimate_hours": { "min": 10, "max": 15 },
      "work_packages": [
        {
          "id": "WP-001",
          "title": "Work Package Title",
          "status": "todo",
          "estimate_hours": 3,
          "priority": "P0-Critical",
          "labels": ["python", "infrastructure"],
          "milestone": "Phase Name",
          "description": "Detailed description",
          "skills": ["skill-1", "skill-2"],
          "dependencies": ["WP-000"]
        }
      ]
    }
  ]
}
```

### Adding New Work Packages

1. Edit `work_packages.json`
2. Add entries to the appropriate phase
3. Run the import (existing issues are not duplicated)

### Customising Labels

Label colours are defined in `importer.py` in the `LABEL_COLORS` dictionary. Add new labels as needed:

```python
LABEL_COLORS = {
    "new-label": "HEX_COLOR",
    ...
}
```

## Module Structure

```
tools/github_import/
├── __init__.py
├── models.py        # WorkPackage and Phase data models
├── cli.py           # GitHub CLI wrapper
├── importer.py      # Import orchestration
├── run_import.py    # Entry point
├── work_packages.json
└── README.md
```

## Output

The tool provides progress feedback and a summary:

```
📂 Loaded 4 phases with 31 work packages

🏷️  Creating 45 labels...
   ✅ ai
   ⏭️  bug (already exists)

🎯 Creating 4 milestones...
   ✅ Foundation

📝 Creating 31 issues...
   ⏭️  WP-001 (already done)
   ✅ WP-002: py-core Shared Library

==================================================
📊 IMPORT SUMMARY
==================================================
   Labels:     42 created, 3 skipped
   Milestones: 4 created, 0 skipped
   Issues:     30 created, 1 skipped, 0 failed
==================================================
```
