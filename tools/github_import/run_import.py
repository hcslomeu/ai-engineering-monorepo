#!/usr/bin/env python3
"""Entry point for GitHub project import."""

import argparse
from pathlib import Path

from .importer import ProjectImporter


def main():
    parser = argparse.ArgumentParser(
        description="Import work packages into GitHub Issues"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without executing",
    )
    parser.add_argument(
        "--include-done",
        action="store_true",
        help="Include work packages marked as done",
    )

    args = parser.parse_args()

    owner = "hcslomeu"
    repo = "ai-engineering-monorepo"
    json_file = Path(__file__).parent / "work_packages.json"

    importer = ProjectImporter(owner, repo, dry_run=args.dry_run)
    importer.load_from_json(json_file)
    importer.run_import(skip_done=not args.include_done)


if __name__ == "__main__":
    main()
