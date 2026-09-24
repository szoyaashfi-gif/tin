"""Offline contract checks for the beginner-start workflow."""

import json
from pathlib import Path


ROOT = Path(__file__).parents[1] / "workflow_packages/product.beginner_start"
MANIFEST = ROOT / "workflow.json"
PROMPT = ROOT / "PROMPT.md"
SKILL = ROOT / "skills/beginner-start/SKILL.md"


def test_manifest_is_simple_and_bounded():
    definition = json.loads(MANIFEST.read_text())["definition"]
    assert definition["key"] == "product.beginner_start"
    assert definition["executor"] == "codex.procedure"
    assert definition["schedule_modes"] == ["on_demand"]
    assert definition["input_schema"]["required"] == ["project_id"]
    assert definition["input_schema"]["additionalProperties"] is False
    assert definition["input_schema"]["properties"]["project_id"]["format"] == "uuid"
    assert definition["input_schema"]["properties"]["focus"]["maxLength"] == 1000
    assert definition["procedure"]["workspace"] == {"kind": "project.state"}
    assert definition["procedure"]["sandbox"]["timeout_seconds"] == 600
    assert definition["procedure"]["sandbox"]["egress"] == "fenced"
    assert definition["procedure"]["output"]["path"] == "reports/BEGINNER_START.md"
    assert definition["procedure"]["output"]["max_bytes"] == 20000


def test_declared_skill_exists_and_is_beginner_focused():
    definition = json.loads(MANIFEST.read_text())["definition"]
    for path in definition["procedure"]["skill_files"]:
        assert (ROOT / path).exists()

    prompt = PROMPT.read_text()
    skill = SKILL.read_text()
    combined = f"{prompt}\n{skill}"

    for phrase in (
        "complete beginner",
        "first 3-5 steps",
        "Beginner glossary",
        "Your first small task",
        "Do not invent commands",
        "Do not browse the public web",
        "BEGINNER_START.md",
    ):
        assert phrase in combined
