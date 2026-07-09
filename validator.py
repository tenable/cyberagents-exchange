#!/usr/bin/env python

from datetime import date
from pathlib import Path
from typing import Literal, Type

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
    tier: Literal["unreviewed", "community-reviewed", "certified"]
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


class Agent(Entry):
    """Agent Exchange Entry"""

    type: Literal["agent", "tool", "mcp-server"]
    framework: str


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

    if error_count > 0:
        console.print(f"{error_count} Issues Identified")
        exit(1)


if __name__ == "__main__":
    cli()
