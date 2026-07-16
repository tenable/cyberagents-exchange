#!/usr/bin/env python

import re
from datetime import date, datetime
from pathlib import Path
from typing import Literal, Type, get_args

import frontmatter
from pydantic import AnyUrl, BaseModel, HttpUrl, TypeAdapter, model_validator
from rich.console import Console
from typer import Typer


class Entry(BaseModel):
    """Base Exchange Entry Front-matter Model"""

    name: str
    author: str
    github_url: HttpUrl
    description: str
    license: str
    tier: Literal["contributed", "community-reviewed", "certified"]
    tags: list[str]
    integrations: list[
        Literal[
            "Anthropic",
            "AWS",
            "Azure",
            "Cisco",
            "CrowdStrike",
            "Fortinet",
            "GCP",
            "KnowBe4",
            "Microsoft Sentinel",
            "Netskope",
            "NVD",
            "PagerDuty",
            "Palo Alto",
            "Qualys",
            "Rapid7",
            "SentinelOne",
            "ServiceNow",
            "Snyk",
            "Splunk",
            "Tenable",
            "Wiz",
        ]
    ]
    date_added: date
    contribution_agreement_date: datetime | None = None
    visibility: Literal["example"] | None = None
    last_reviewed: date | None = None
    works_with_tenable_hexa_mcp: bool | None = None
    cta: Literal["T1"] | None = None

    @model_validator(mode="after")
    def cta_requires_hexa_mcp(self):
        if self.cta and not self.works_with_tenable_hexa_mcp:
            raise ValueError("cta requires works_with_tenable_hexa_mcp to be true")
        return self


class Agent(Entry):
    """Agent Exchange Entry"""


class Skill(Entry):
    """Skill Exchange Entry"""

    compatible_platforms: list[
        Literal[
            "Claude Code",
            "Claude Desktop",
            "Claude Cowork",
            "Cline",
            "Codex",
            "Cursor",
            "Gemini CLI",
            "GitHub Copilot",
            "Windsurf",
        ]
    ]
    invocation: str


class MCPTool(BaseModel):
    """MCP Tool sub-object"""

    name: str
    description: str


class MCPPrompt(MCPTool):
    """MCP Prompt sub-object"""


class MCPResource(BaseModel):
    """MCP Resource sub-object"""

    name: AnyUrl
    description: str


class MCPServer(Entry):
    """MCP Server Entry"""

    compatible_clients: list[
        Literal[
            "Antigravity",
            "ChatGPT",
            "Claude Code",
            "Claude Desktop",
            "Cline",
            "Codex",
            "Continue",
            "Cursor",
            "Gemini CLI",
            "VS Code Copilot",
            "Windsurf",
        ]
    ]
    tools_exposed: list[MCPTool]
    resources_exposed: list[MCPResource]
    prompts_exposed: list[MCPPrompt]
    transport: Literal["stdio", "http", "both"]
    auth_method: Literal["api-key", "none", "oauth2", "token"]
    runtime: Literal["binary", "bun", "go", "node", "python", "rust"]


class PlaybookAgent(BaseModel):
    """Playbook Agent sub-object"""

    name: str
    role: str
    type: Literal["exchange", "github", "info", "vendor"]
    ref: str | None = None


class StandardPlaybook(Entry):
    """Standard multi-agent playbook."""

    playbook_type: Literal["standard"]
    agents_used: list[PlaybookAgent]

    @model_validator(mode="after")
    def no_vendor_agents(self):
        if any(a.type == "vendor" for a in self.agents_used):
            raise ValueError("Only sponsored playbooks may include vendor-type agents")
        return self


class SponsoredPlaybook(Entry):
    """Sponsored vendor-partnered playbook with co-branding."""

    playbook_type: Literal["sponsored"]
    agents_used: list[PlaybookAgent]
    logo: HttpUrl


class N8nPlaybook(Entry):
    """n8n workflow playbook with Mermaid diagram."""

    playbook_type: Literal["n8n"]
    workflow_diagram: str
    agents_used: list[PlaybookAgent] | None = None

    @model_validator(mode="after")
    def no_vendor_agents(self):
        if self.agents_used and any(a.type == "vendor" for a in self.agents_used):
            raise ValueError("Only sponsored playbooks may include vendor-type agents")
        return self


Playbook = StandardPlaybook | SponsoredPlaybook | N8nPlaybook
PlaybookAdapter = TypeAdapter(Playbook)


console = Console()
cli = Typer()


def validate_markdown_frontmatter(filepath: Path, schema: Type[Entry] | TypeAdapter) -> None:
    """Performs validation of the markdown frontmatter based on the provided schema."""
    if filepath.suffix not in [".md", ".mdown", ".markdown"]:
        raise ValueError(f"{filepath} doesn't have a valid markdown suffix.")
    page = frontmatter.load(filepath.open())
    if isinstance(schema, TypeAdapter):
        schema.validate_python(dict(page))
    else:
        schema.model_validate(dict(page))


def _extract_literals_from_field(model: Type[BaseModel], field_name: str) -> set[str]:
    """Extract the allowed Literal values for a field from a Pydantic model."""
    field_info = model.model_fields[field_name]
    annotation = field_info.annotation
    # Handle list[Literal[...]]
    if hasattr(annotation, "__args__"):
        for arg in get_args(annotation):
            literal_args = get_args(arg)
            if literal_args:
                return set(literal_args)
    # Handle plain Literal[...]
    literal_args = get_args(annotation)
    if literal_args:
        return set(literal_args)
    return set()


def _validate_contributing_md(path: Path) -> list[str]:
    """Check that values mentioned in CONTRIBUTING.md are valid per the current vocabulary."""
    contributing = path / "CONTRIBUTING.md"
    if not contributing.exists():
        return []

    content = contributing.read_text()
    errors = []

    # Aggregate playbook_type values across all playbook models
    playbook_type_values = set()
    for model in (StandardPlaybook, SponsoredPlaybook, N8nPlaybook):
        playbook_type_values |= _extract_literals_from_field(model, "playbook_type")

    vocabulary_checks: list[tuple[str, set[str]]] = [
        ("transport", _extract_literals_from_field(MCPServer, "transport")),
        ("runtime", _extract_literals_from_field(MCPServer, "runtime")),
        ("auth_method", _extract_literals_from_field(MCPServer, "auth_method")),
        ("playbook_type", playbook_type_values),
    ]

    for field, valid_values in vocabulary_checks:
        # Match patterns like: - `field` — ... `value`, `value`
        pattern = rf"- `{field}`.*?—(.*?)$"
        for match in re.finditer(pattern, content, re.MULTILINE):
            line = match.group(1)
            mentioned = set(re.findall(r"`([^`]+)`", line))
            invalid = mentioned - valid_values
            for val in sorted(invalid):
                errors.append(
                    f"CONTRIBUTING.md mentions `{val}` for `{field}` "
                    f"but it is not in the validator vocabulary"
                )

    # Validate specific inline value lists like: must be `x`, `y`, or `z`
    field_map = {field: valid for field, valid in vocabulary_checks}
    must_be_pattern = r"- `(\w+)` must be (.*?)$"
    for match in re.finditer(must_be_pattern, content, re.MULTILINE):
        field_name = match.group(1)
        values_text = match.group(2)
        mentioned = set(re.findall(r"`([^`]+)`", values_text))

        if field_name in field_map:
            invalid = mentioned - field_map[field_name]
            for val in sorted(invalid):
                errors.append(
                    f"CONTRIBUTING.md lists `{val}` as a valid `{field_name}` value "
                    f"but it is not in the validator vocabulary"
                )

    return errors


@cli.command()
def validate(path: Path = Path(".")):
    """
    Validates the exchange directories.
    """
    error_count = 0
    for loc, schema in (
        (path.joinpath("agents"), Agent),
        (path.joinpath("mcp-servers"), MCPServer),
        (path.joinpath("skills"), Skill),
        (path.joinpath("playbooks"), PlaybookAdapter),
    ):
        if not loc.is_dir():
            raise FileExistsError(f"{loc} is not a directory.")
        for fname in loc.iterdir():
            try:
                validate_markdown_frontmatter(fname, schema)
            except Exception as err:
                error_count += 1
                console.print(f"[red]✘[/red] {fname} is not valid!\n[red]{err}[/red]")
            else:
                console.print(f"[green]✔[/green] {fname} is valid.")

    # Validate CONTRIBUTING.md references match current vocabulary
    for err in _validate_contributing_md(path):
        error_count += 1
        console.print(f"[red]✘[/red] {err}")

    if error_count > 0:
        console.print(f"{error_count} Issues Identified")
        exit(1)


if __name__ == "__main__":
    cli()
