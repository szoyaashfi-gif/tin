"""Offline contract checks for the employee-analysis workflow."""

import json
from pathlib import Path


ROOT = Path(__file__).parents[1] / "workflow_packages/people.employee_analysis"
MANIFEST = ROOT / "workflow.json"
PROMPT = ROOT / "PROMPT.md"
SKILL = ROOT / "skills/employee-analysis/SKILL.md"


def test_manifest_is_bounded_and_on_demand():
    definition = json.loads(MANIFEST.read_text())["definition"]
    assert definition["key"] == "people.employee_analysis"
    assert definition["executor"] == "codex.procedure"
    assert definition["schedule_modes"] == ["on_demand"]
    assert definition["input_schema"]["required"] == ["project_id"]
    assert definition["input_schema"]["additionalProperties"] is False
    assert definition["input_schema"]["properties"]["project_id"]["format"] == "uuid"
    assert definition["input_schema"]["properties"]["focus"]["maxLength"] == 1000
    assert definition["input_schema"]["properties"]["source_hint"]["maxLength"] == 500
    assert definition["procedure"]["workspace"] == {"kind": "project.state"}
    assert definition["procedure"]["sandbox"]["egress"] == "fenced"
    assert definition["procedure"]["sandbox"]["timeout_seconds"] == 600
    assert definition["procedure"]["output"]["path"] == "reports/EMPLOYEE_ANALYSIS.md"
    assert definition["procedure"]["output"]["max_bytes"] == 30000


def test_declared_skill_exists_and_has_privacy_boundaries():
    definition = json.loads(MANIFEST.read_text())["definition"]
    for path in definition["procedure"]["skill_files"]:
        assert (ROOT / path).exists()

    prompt = PROMPT.read_text()
    skill = SKILL.read_text()
    combined = f"{prompt}\n{skill}"

    for phrase in (
        "aggregate or anonymized",
        "Do not expose names",
        "Do not identify individual employees",
        "infer sensitive personal traits",
        "insufficient evidence",
        "EMPLOYEE_ANALYSIS.md",
    ):
        assert phrase in combined
