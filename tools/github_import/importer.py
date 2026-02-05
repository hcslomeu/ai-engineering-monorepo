"""Project importer for GitHub Issues automation."""

import json
from pathlib import Path

from .cli import GitHubCLI, GitHubCLIError
from .models import Phase, WorkPackage


LABEL_COLORS: dict[str, str] = {
    # Languages & Frameworks
    "python": "3572A5",
    "typescript": "3178C6",
    "react": "61DAFB",
    # Infrastructure & DevOps
    "infrastructure": "6B7280",
    "ci-cd": "22C55E",
    "devops": "8B5CF6",
    "docker": "2496ED",
    "terraform": "7B42BC",
    "iac": "9333EA",
    "aws": "FF9900",
    "s3": "569A31",
    "lambda": "FF9900",
    "serverless": "F97316",
    # Data Engineering
    "data-engineering": "EC4899",
    "medallion": "F97316",
    "airflow": "017CEE",
    "databricks": "FF3621",
    "bigquery": "4285F4",
    "kafka": "231F20",
    "streaming": "06B6D4",
    # AI & ML
    "ai": "8B5CF6",
    "agents": "A855F7",
    "langgraph": "7C3AED",
    "langsmith": "1E40AF",
    "crewai": "6366F1",
    "multi-agent": "8B5CF6",
    "llamaindex": "7C3AED",
    "rag": "A855F7",
    "pytorch": "EE4C2C",
    "lstm": "F43F5E",
    "deep-learning": "BE185D",
    "huggingface": "FFD21E",
    "pinecone": "000000",
    "vectordb": "6366F1",
    "embeddings": "8B5CF6",
    # Projects
    "alphawhale": "3B82F6",
    "mediguard": "DB2777",
    "railsense": "22C55E",
    # Domains
    "healthcare": "EC4899",
    "fhir": "E11D48",
    "transportation": "84CC16",
    "real-time": "14B8A6",
    # Quality & Security
    "testing": "EAB308",
    "integration": "F59E0B",
    "performance": "EF4444",
    "compliance": "DC2626",
    "security": "B91C1C",
    "pii": "DC2626",
    "privacy": "991B1B",
    # General
    "library": "F59E0B",
    "foundation": "10B981",
    "documentation": "0075CA",
    "setup": "6B7280",
    "frontend": "38BDF8",
    "whatsapp": "25D366",
    "human-in-loop": "84CC16",
    "observability": "3B82F6",
    "supabase": "3ECF8E",
    "feature-engineering": "F472B6",
}

DEFAULT_LABEL_COLOR = "6B7280"


class ProjectImporter:
    """Orchestrates importing work packages into GitHub."""

    def __init__(self, owner: str, repo: str, dry_run: bool = False):
        """
        Initialise the importer.

        Args:
            owner: GitHub username
            repo: Repository name
            dry_run: If True, preview without making changes
        """
        self.cli = GitHubCLI(owner, repo, dry_run)
        self.dry_run = dry_run
        self.phases: list[Phase] = []
        self.stats = {
            "labels_created": 0,
            "labels_skipped": 0,
            "milestones_created": 0,
            "milestones_skipped": 0,
            "issues_created": 0,
            "issues_skipped": 0,
            "issues_failed": 0,
        }

    def load_from_json(self, json_path: str | Path) -> None:
        """Load work packages from a JSON file."""
        path = Path(json_path)

        if not path.exists():
            raise FileNotFoundError(f"JSON file not found: {path}")

        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        self.phases = [Phase.from_dict(phase) for phase in data["phases"]]

        total_wp = sum(len(phase.work_packages) for phase in self.phases)
        print(f"📂 Loaded {len(self.phases)} phases with {total_wp} work packages")

    def _collect_unique_labels(self) -> set[str]:
        """Gather all unique labels from work packages."""
        labels = set()

        for phase in self.phases:
            for wp in phase.work_packages:
                labels.update(wp.labels)

        return labels

    def _collect_unique_milestones(self) -> set[str]:
        """Gather all unique milestone names."""
        return {phase.name for phase in self.phases}

    def _create_labels(self) -> None:
        """Create all required labels in GitHub."""
        labels = self._collect_unique_labels()
        print(f"\n🏷️  Creating {len(labels)} labels...")

        for label in sorted(labels):
            color = LABEL_COLORS.get(label, DEFAULT_LABEL_COLOR)

            try:
                created = self.cli.create_label(label, color)

                if created:
                    self.stats["labels_created"] += 1
                    print(f"   ✅ {label}")
                else:
                    self.stats["labels_skipped"] += 1
                    print(f"   ⏭️  {label} (already exists)")

            except GitHubCLIError as e:
                print(f"   ❌ {label}: {e}")

    def _create_milestones(self) -> None:
        """Create all required milestones in GitHub."""
        milestones = self._collect_unique_milestones()
        print(f"\n🎯 Creating {len(milestones)} milestones...")

        for milestone in sorted(milestones):
            try:
                created = self.cli.create_milestone(milestone)

                if created:
                    self.stats["milestones_created"] += 1
                    print(f"   ✅ {milestone}")
                else:
                    self.stats["milestones_skipped"] += 1
                    print(f"   ⏭️  {milestone} (already exists)")

            except GitHubCLIError as e:
                print(f"   ❌ {milestone}: {e}")

    def _create_issues(self, skip_done: bool = True) -> None:
        """Create GitHub issues for all work packages."""
        total = sum(len(p.work_packages) for p in self.phases)
        print(f"\n📝 Creating {total} issues...")

        for phase in self.phases:
            print(f"\n   Phase: {phase.name}")

            for wp in phase.work_packages:
                if skip_done and wp.status == "done":
                    self.stats["issues_skipped"] += 1
                    print(f"      ⏭️  {wp.id} (already done)")
                    continue

                try:
                    result = self.cli.create_issue(
                        title=wp.full_title,
                        body=wp.issue_body,
                        labels=wp.labels,
                        milestone=wp.milestone,
                    )

                    self.stats["issues_created"] += 1
                    print(f"      ✅ {wp.id}: {wp.title}")

                except GitHubCLIError as e:
                    self.stats["issues_failed"] += 1
                    print(f"      ❌ {wp.id}: {e}")

    def _print_summary(self) -> None:
        """Print import summary."""
        print("\n" + "=" * 50)
        print("📊 IMPORT SUMMARY")
        print("=" * 50)
        print(f"   Labels:     {self.stats['labels_created']} created, "
              f"{self.stats['labels_skipped']} skipped")
        print(f"   Milestones: {self.stats['milestones_created']} created, "
              f"{self.stats['milestones_skipped']} skipped")
        print(f"   Issues:     {self.stats['issues_created']} created, "
              f"{self.stats['issues_skipped']} skipped, "
              f"{self.stats['issues_failed']} failed")
        print("=" * 50)

        if self.dry_run:
            print("\n⚠️  DRY RUN - No changes were made to GitHub.")

    def run_import(self, skip_done: bool = True) -> None:
        """
        Run the full import process.

        Args:
            skip_done: If True, skip work packages marked as done
        """
        if not self.phases:
            print("❌ No phases loaded. Call load_from_json() first.")
            return

        print("\n🚀 Starting GitHub import...")

        self._create_labels()
        self._create_milestones()
        self._create_issues(skip_done=skip_done)
        self._print_summary()
