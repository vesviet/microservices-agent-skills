#!/usr/bin/env python3
"""Generate A2A Agent Cards and registry from role definitions.

2026 upgrades:
- Emits /.well-known/agent-card.json (IANA permanent A2A 1.0 well-known URI; renamed from agent.json in A2A v0.3.0)
- Emits /.well-known/ai-catalog.json (Google AI Catalog 2026 meta-index)
- Adds 'data' to inputModes per A2A 1.0 spec update
- protocol_version stays "1.0" (donated to Linux Foundation, no version bump)
- Capability map includes security card signing awareness flag
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from common import CORE_ROOT, ROOT, SKILLS_ROOT, collect_skill_names, parse_frontmatter, section_text


ROLE_ROOT = CORE_ROOT / "roles"
REGISTRY_ROOT = CORE_ROOT / "a2a" / "registry"
WELL_KNOWN = CORE_ROOT / "a2a" / ".well-known" / "agent-registry.json"
# A2A 1.0 canonical single-agent endpoint (/.well-known/agent-card.json — IANA permanent URI)
WELL_KNOWN_AGENT = CORE_ROOT / "a2a" / ".well-known" / "agent-card.json"
# AI Catalog meta-index pointing to agent-card.json, mcp.json, OpenAPI
AI_CATALOG = CORE_ROOT / "a2a" / ".well-known" / "ai-catalog.json"
PACK_VERSION_PATH = ROOT / "VERSION"
SCHEMAS_ROOT = CORE_ROOT / "contracts" / "schemas"

CANONICAL_TAGS = {
    "agent": "agent",
    "backend": "backend",
    "frontend": "frontend",
    "platform": "platform",
    "foundation": "foundation",
    "security-data": "security",
    "documentation": "documentation",
    "education": "education",
    "meetings-analysis": "analysis",
    "repo-ops": "devops",
    "content": "content",
    "commerce": "commerce",
    "mmo": "operations",
}


def pack_version() -> str:
    if PACK_VERSION_PATH.is_file():
        return PACK_VERSION_PATH.read_text(encoding="utf-8").strip()
    return "0.0.0"


def role_files() -> list[Path]:
    return sorted(
        p for p in ROLE_ROOT.glob("*.md") if p.name not in {"README.md", "role-standard.md"}
    )


def parse_mission(body: str) -> str:
    match = re.search(r"(?m)^Mission: (.+)$", body)
    return match.group(1).strip() if match else ""


def skill_description(skill_id: str) -> str:
    """Look up the skill description from SKILL.md frontmatter."""
    for skill_path in SKILLS_ROOT.glob(f"*/{skill_id}/SKILL.md"):
        metadata, _body, _errors = parse_frontmatter(skill_path.read_text(encoding="utf-8"))
        desc = metadata.get("description", "")
        if desc:
            return desc
    return f"Skill {skill_id}."


def skill_category(skill_id: str) -> str:
    """Return the taxonomy category folder for a skill."""
    for skill_path in SKILLS_ROOT.glob(f"*/{skill_id}/SKILL.md"):
        return CANONICAL_TAGS.get(skill_path.parent.parent.name, "pack")
    return "pack"


def primary_skills(body: str) -> list[str]:
    block = section_text(body, "### Primary Skills", level_aware=True)
    return re.findall(r"(?m)^- `([a-z0-9-]+)`", block)


def contract_refs(body: str) -> list[str]:
    """Collect output contracts from Outputs Produced only (not consumer/handoff inputs)."""
    block = section_text(body, "## Outputs Produced", level_aware=True)
    # Role files may document consumed-contract ownership immediately after
    # Outputs Produced. Keep those inputs out of the agent's output schemas.
    block = re.split(r"\nContracts owned by other roles", block, maxsplit=1)[0]
    text = block if block.strip() else body
    return sorted(set(re.findall(r"contracts/schemas/([a-z0-9-]+\.json)", text)))


def build_agent_card(path: Path, known_skills: set[str]) -> dict:
    body = path.read_text(encoding="utf-8")
    slug = path.stem
    mission = parse_mission(body)
    skills = primary_skills(body)
    schemas = contract_refs(body)

    card_skills = []
    for skill_id in skills:
        if skill_id not in known_skills:
            continue
        cat = skill_category(skill_id)
        card_skills.append(
            {
                "id": skill_id,
                "name": skill_id.replace("-", " ").title(),
                "description": skill_description(skill_id),
                "tags": [cat, "pack"],
                # A2A 1.0 2026: 'data' added alongside text/json
                "inputModes": ["text", "json", "data"],
                "outputModes": ["json", "text"],
                "output_schema_refs": schemas[:3] if schemas else [],
            }
        )

    if not card_skills:
        card_skills.append(
            {
                "id": slug,
                "name": slug.replace("-", " ").title(),
                "description": mission or f"{slug} delivery role.",
                "tags": ["role"],
                "inputModes": ["text", "json", "data"],
                "outputModes": ["json"],
                "output_schema_refs": schemas,
            }
        )

    return {
        "id": f"pack://agent-skills/core/roles/{slug}",
        "contract_type": "agent-card",
        "name": slug,
        "description": mission,
        "url": f"pack://agent-skills/core/roles/{slug}.md",
        "version": pack_version(),
        # A2A 1.0 — protocol donated to Linux Foundation; version stays "1.0"
        "protocol_version": "1.0",
        "capabilities": {
            "streaming": True,
            "pushNotifications": False,
            "stateTransitionHistory": True,
            # A2A 1.0 2026: security card signing support declaration
            "securityCardSigning": False,
        },
        "authentication": {"schemes": ["pack-local"]},
        "defaultInputModes": ["text", "json", "data"],
        "defaultOutputModes": ["text", "json"],
        "skills": card_skills,
        "defaultOutputSchemas": schemas,
        "role_file": f"core/roles/{slug}.md",
        "policy_profile": slug,
    }


def main() -> int:
    known_skills = collect_skill_names()
    roles = role_files()
    REGISTRY_ROOT.mkdir(parents=True, exist_ok=True)
    WELL_KNOWN.parent.mkdir(parents=True, exist_ok=True)

    entries: list[dict] = []
    for path in roles:
        card = build_agent_card(path, known_skills)
        out = REGISTRY_ROOT / f"{path.stem}.agent-card.json"
        out.write_text(json.dumps(card, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        entries.append(
            {
                "role": path.stem,
                "agent_card": str(out.relative_to(ROOT)).replace("\\", "/"),
                "url": card["url"],
                "description": card["description"][:120],
            }
        )

    # agent-registry.json — internal multi-agent directory (project convention)
    registry = {
        "contract_type": "agent-registry",
        "pack_version": pack_version(),
        "protocol_version": "1.0",
        "generated_from": "core/roles",
        "agents": entries,
    }
    WELL_KNOWN.write_text(
        json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    # /.well-known/agent-card.json — A2A canonical single-agent card endpoint (IANA permanent)
    # Represents the pack itself as an orchestrating agent
    canonical_card = {
        "name": "agent-skills-pack",
        "description": "Agent Skills Pack — multi-role engineering skill pack for AI-assisted delivery",
        "url": "pack://agent-skills",
        "version": pack_version(),
        "protocol_version": "1.0",
        "capabilities": {
            "streaming": True,
            "pushNotifications": False,
            "stateTransitionHistory": True,
            "securityCardSigning": False,
        },
        "defaultInputModes": ["text", "json", "data"],
        "defaultOutputModes": ["text", "json"],
        "skills": [
            {
                "id": entry["role"],
                "name": entry["role"].replace("-", " ").title(),
                "description": entry["description"],
            }
            for entry in entries[:20]  # top 20 roles for discovery
        ],
    }
    WELL_KNOWN_AGENT.write_text(
        json.dumps(canonical_card, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    # /.well-known/ai-catalog.json — AI Catalog meta-index (LF Agent-Card/ai-catalog shape)
    ai_catalog = {
        "version": "1.1",
        "agents": [
            {"type": "a2a", "url": "/.well-known/agent-card.json"},
            {"type": "registry", "url": "/.well-known/agent-registry.json"},
        ],
        "mcp": [],
        "openapi": [],
    }
    AI_CATALOG.write_text(
        json.dumps(ai_catalog, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    cap_lines = [
        "# Generated capability → role map for Antigravity a2a-config.template.yaml",
        "# Regenerate: python3 core/scripts/generate-a2a-registry.py",
        "capability_role_map:",
    ]
    for entry in entries:
        role = entry["role"]
        cap_id = role.replace("_", "-")
        cap_lines.append(f"  {cap_id}: {role}")
    cap_path = ROOT / "adapters" / "antigravity" / "capability-role-map.generated.yaml"
    cap_path.write_text("\n".join(cap_lines) + "\n", encoding="utf-8")

    print(f"Generated {len(entries)} agent cards under {REGISTRY_ROOT.relative_to(ROOT)}")
    print(f"Canonical A2A endpoint: {WELL_KNOWN_AGENT.relative_to(ROOT)}")
    print(f"AI Catalog meta-index: {AI_CATALOG.relative_to(ROOT)}")
    print(f"Capability map: {cap_path.relative_to(ROOT)}")
    print(f"Registry: {WELL_KNOWN.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
