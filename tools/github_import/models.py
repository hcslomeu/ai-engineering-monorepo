"""Data models for GitHub project import."""

from dataclasses import dataclass, field


@dataclass
class WorkPackage:
    """Represents a work package to be created as a GitHub Issue."""

    id: str
    title: str
    description: str
    estimate_hours: int
    priority: str
    status: str
    milestone: str
    labels: list[str] = field(default_factory=list)
    skills: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)

    @property
    def full_title(self) -> str:
        """Return formatted issue title."""
        return f"{self.id}: {self.title}"

    @property
    def issue_body(self) -> str:
        """Generate GitHub issue body in Markdown format."""
        skills_list = "\n".join(f"- [ ] {skill}" for skill in self.skills)
        deps_text = ", ".join(self.dependencies) if self.dependencies else "None"

        return f"""## Description

{self.description}

## Details

| Field | Value |
|-------|-------|
| **Estimate** | {self.estimate_hours} hours |
| **Priority** | {self.priority} |
| **Milestone** | {self.milestone} |
| **Dependencies** | {deps_text} |

## Skills to Learn/Practice

{skills_list if skills_list else "- No specific skills listed"}

## Acceptance Criteria

- [ ] Implementation complete
- [ ] Tests written and passing
- [ ] Documentation updated
- [ ] Code reviewed
"""

    @classmethod
    def from_dict(cls, data: dict) -> "WorkPackage":
        """Create a WorkPackage from a dictionary."""
        return cls(
            id=data["id"],
            title=data["title"],
            description=data["description"],
            estimate_hours=data["estimate_hours"],
            priority=data["priority"],
            status=data["status"],
            milestone=data["milestone"],
            labels=data.get("labels", []),
            skills=data.get("skills", []),
            dependencies=data.get("dependencies", []),
        )


@dataclass
class Phase:
    """Represents a project phase containing multiple work packages."""

    id: str
    name: str
    estimate_hours_min: int
    estimate_hours_max: int
    work_packages: list[WorkPackage] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> "Phase":
        """Create a Phase from a dictionary."""
        work_packages = [
            WorkPackage.from_dict(wp) for wp in data.get("work_packages", [])
        ]

        return cls(
            id=data["id"],
            name=data["name"],
            estimate_hours_min=data["estimate_hours"]["min"],
            estimate_hours_max=data["estimate_hours"]["max"],
            work_packages=work_packages,
        )
