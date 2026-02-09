"""GitHub CLI wrapper for repository automation."""

import json
import subprocess
from dataclasses import dataclass


class GitHubCLIError(Exception):
    """Exception raised for GitHub CLI errors."""

    def __init__(self, message: str, command: str = "", stderr: str = ""):
        super().__init__(message)
        self.command = command
        self.stderr = stderr


@dataclass
class CommandResult:
    """Result of a CLI command execution."""

    stdout: str
    stderr: str
    return_code: int

    @property
    def success(self) -> bool:
        """Check if command succeeded."""
        return self.return_code == 0

    def json(self) -> dict:
        """Parse stdout as JSON."""
        return json.loads(self.stdout)


class GitHubCLI:
    """Wrapper for GitHub CLI operations."""

    def __init__(self, owner: str, repo: str, dry_run: bool = False):
        """
        Initialise the GitHub CLI wrapper.

        Args:
            owner: GitHub username or organisation
            repo: Repository name
            dry_run: If True, print commands without executing
        """
        self.owner = owner
        self.repo = repo
        self.dry_run = dry_run
        self.repo_full = f"{owner}/{repo}"

    def _run(self, args: list[str]) -> CommandResult:
        """Execute a gh CLI command."""
        full_command = ["gh"] + args

        if self.dry_run:
            print(f"[DRY RUN] Would execute: {' '.join(full_command)}")
            return CommandResult(stdout="", stderr="", return_code=0)

        try:
            result = subprocess.run(
                full_command,
                capture_output=True,
                text=True,
                check=False,
            )

            return CommandResult(
                stdout=result.stdout.strip(),
                stderr=result.stderr.strip(),
                return_code=result.returncode,
            )

        except FileNotFoundError:
            raise GitHubCLIError(
                "GitHub CLI (gh) not found. Install from: https://cli.github.com/",
                command=" ".join(full_command),
            ) from None

    def _run_or_raise(self, args: list[str], error_message: str) -> CommandResult:
        """Execute a command and raise on failure."""
        result = self._run(args)

        if not result.success:
            raise GitHubCLIError(
                f"{error_message}: {result.stderr}",
                command=" ".join(["gh"] + args),
                stderr=result.stderr,
            )

        return result

    def list_labels(self) -> list[dict]:
        """Get all labels in the repository."""
        result = self._run_or_raise(
            ["label", "list", "--repo", self.repo_full, "--json", "name,color,description"],
            "Failed to list labels",
        )

        return result.json() if result.stdout else []

    def create_label(self, name: str, color: str, description: str = "") -> bool:
        """
        Create a new label.

        Returns:
            True if created, False if already exists
        """
        args = [
            "label",
            "create",
            name,
            "--repo",
            self.repo_full,
            "--color",
            color,
        ]

        if description:
            args.extend(["--description", description])

        result = self._run(args)

        if result.success:
            return True
        elif "already exists" in result.stderr.lower():
            return False
        else:
            raise GitHubCLIError(
                f"Failed to create label '{name}': {result.stderr}",
                command=" ".join(["gh"] + args),
                stderr=result.stderr,
            )

    def list_milestones(self) -> list[dict]:
        """Get all milestones in the repository."""
        result = self._run_or_raise(
            ["api", f"repos/{self.repo_full}/milestones", "--jq", ".[].title"],
            "Failed to list milestones",
        )

        if not result.stdout:
            return []

        return [{"title": title} for title in result.stdout.split("\n") if title]

    def create_milestone(self, title: str, description: str = "") -> bool:
        """
        Create a new milestone.

        Returns:
            True if created, False if already exists
        """
        existing = self.list_milestones()
        if any(m["title"] == title for m in existing):
            return False

        args = [
            "api",
            f"repos/{self.repo_full}/milestones",
            "--method",
            "POST",
            "--field",
            f"title={title}",
        ]

        if description:
            args.extend(["--field", f"description={description}"])

        result = self._run(args)

        if result.success:
            return True
        else:
            raise GitHubCLIError(
                f"Failed to create milestone '{title}': {result.stderr}",
                command=" ".join(["gh"] + args),
                stderr=result.stderr,
            )

    def list_issues(self, state: str = "all") -> list[dict]:
        """Get all issues in the repository."""
        result = self._run_or_raise(
            [
                "issue",
                "list",
                "--repo",
                self.repo_full,
                "--state",
                state,
                "--json",
                "number,title,state,labels",
                "--limit",
                "200",
            ],
            "Failed to list issues",
        )

        return result.json() if result.stdout else []

    def create_issue(
        self,
        title: str,
        body: str,
        labels: list[str] | None = None,
        milestone: str | None = None,
    ) -> dict:
        """
        Create a new issue.

        Returns:
            Dictionary with 'number' and 'url' of created issue
        """
        args = [
            "issue",
            "create",
            "--repo",
            self.repo_full,
            "--title",
            title,
            "--body",
            body,
        ]

        if labels:
            for label in labels:
                args.extend(["--label", label])

        if milestone:
            args.extend(["--milestone", milestone])

        result = self._run_or_raise(args, f"Failed to create issue '{title}'")

        return {
            "url": result.stdout,
            "number": int(result.stdout.split("/")[-1]) if result.stdout else 0,
        }
