"""Offline contract checks for the contributed customer-language procedure."""

import json
from pathlib import Path


ROOT = Path(__file__).parents[1] / "workflow_packages/research.customer_language"
MANIFEST = ROOT / "workflow.json"
PROMPT = ROOT / "PROMPT.md"
SKILL = ROOT / "skills/customer-language/SKILL.md"


def test_manifest_declares_bounded_project_artifact_procedure():
    definition = json.loads(MANIFEST.read_text())["definition"]
    assert definition["key"] == "research.customer_language"
    assert definition["executor"] == "codex.procedure"
    assert definition["schedule_modes"] == ["on_demand"]
    assert definition["input_schema"]["additionalProperties"] is False
    assert definition["input_schema"]["properties"]["focus"]["maxLength"] == 2000
    assert definition["input_schema"]["properties"]["source_hint"]["maxLength"] == 1000
    assert definition["procedure"]["workspace"] == {"kind": "project.state"}
    assert definition["procedure"]["sandbox"]["egress"] == "fenced"
    assert definition["procedure"]["sandbox"]["timeout_seconds"] == 900
    assert definition["procedure"]["output"]["path"] == "reports/CUSTOMER_LANGUAGE.md"
    assert definition["procedure"]["output"]["max_bytes"] == 40000


def test_declared_resources_exist_and_skill_has_safety_boundaries():
    definition = json.loads(MANIFEST.read_text())["definition"]
    for path in definition["procedure"]["skill_files"]:
        assert (ROOT / path).exists()
    prompt = PROMPT.read_text()
    skill = SKILL.read_text()
    combined = f"{prompt}\n{skill}"
    for phrase in (
        "Do not publish",
        "Do not browse the public web",
        "email addresses",
        "phone numbers",
        "reports/CUSTOMER_LANGUAGE.md",
    ):
        assert phrase in combined
    assert "project.state" in json.dumps(definition)