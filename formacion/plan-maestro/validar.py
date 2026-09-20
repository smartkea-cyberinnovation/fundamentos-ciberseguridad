#!/usr/bin/env python3
"""Validate this planning reference only; never execute a lab or use network access."""
from __future__ import annotations

from collections import Counter
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def read_json(path: Path) -> dict:
    def reject_constant(value: str) -> None:
        raise ValueError(f"Non-finite JSON value: {value}")

    value = json.loads(path.read_text(encoding="utf-8"), parse_constant=reject_constant)
    require(isinstance(value, dict), f"Expected JSON object: {path.name}")
    return value


def require_unique(values: list[str], label: str) -> None:
    duplicates = [key for key, count in Counter(values).items() if count != 1]
    require(not duplicates, f"Duplicate {label}: {duplicates}")


def validate_graph(areas: list[dict]) -> None:
    graph = {area["id"]: area["prerequisites"] for area in areas}
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> None:
        require(node in graph, f"Unknown prerequisite: {node}")
        require(node not in visiting, f"Cyclic prerequisites at {node}")
        if node in visited:
            return
        visiting.add(node)
        for prerequisite in graph[node]:
            visit(prerequisite)
        visiting.remove(node)
        visited.add(node)

    for node in graph:
        visit(node)


def validate_risk(risk: dict) -> dict:
    def number(value: str) -> Decimal:
        result = Decimal(value)
        require(result.is_finite() and result >= 0, "Invalid nonnegative risk input")
        return result

    base = risk["inherent"]
    frequency = number(base["frequency"])
    severity = number(base["mean_loss_per_event"])
    inherent = frequency * severity
    require(inherent == number(base["expected_annual_loss"]), "Inherent loss mismatch")
    losses: dict[str, Decimal] = {"inherent": inherent}
    for state in ("current", "target"):
        data = risk[state]
        frequency_reduction = number(data["frequency_reduction_from_inherent"])
        severity_reduction = number(data["severity_reduction_from_inherent"])
        require(frequency_reduction <= 1 and severity_reduction <= 1, "Invalid reduction")
        f = frequency * (1 - frequency_reduction)
        s = severity * (1 - severity_reduction)
        require(f == number(data["expected_frequency"]), f"{state} frequency mismatch")
        require(s == number(data["expected_mean_loss_per_event"]), f"{state} severity mismatch")
        losses[state] = f * s
        require(losses[state] == number(data["expected_annual_loss"]), f"{state} loss mismatch")
    decision = risk["incremental_decision"]
    reduction = losses["current"] - losses["target"]
    cost = number(decision["additional_annual_equivalent_cost"])
    require(cost > 0, "Positive incremental cost required")
    require(reduction == number(decision["expected_annual_reduction_from_current"]), "Incremental reduction mismatch")
    require(reduction - cost == number(decision["expected_net_annual_benefit"]), "Net benefit mismatch")
    require((reduction - cost) / cost == number(decision["expected_net_benefit_cost_ratio"]), "Benefit ratio mismatch")
    require(inherent - losses["target"] == number(decision["inherent_to_target_difference_not_incremental_benefit"]), "Total reduction mismatch")
    sensitivity = risk["sensitivity"]
    factor = (1 - number(risk["target"]["frequency_reduction_from_inherent"])) * (1 - number(risk["target"]["severity_reduction_from_inherent"]))
    for index in (0, 1):
        bound = number(sensitivity["frequency_bounds"][index]) * number(sensitivity["severity_bounds"][index])
        require(bound == number(sensitivity["inherent_loss_bounds"][index]), "Sensitivity base mismatch")
        require(bound * factor == number(sensitivity["target_loss_bounds"][index]), "Sensitivity target mismatch")
    return {key: str(value) for key, value in losses.items()}


def validate_reference(root: Path = ROOT) -> dict:
    required = ["README.md", "01-mapa-curricular.md", "02-arquitecturas.md", "03-nist-equipos.md", "04-controles-correspondencias.md", "05-gestion-riesgos.md", "06-laboratorios.md", "07-glosario-protecciones.md", "08-continuacion.md", "09-fuentes.md", "OVERVIEW.en.md", "catalogo.json", "riesgo-ejemplo.json"]
    for name in required:
        require((root / name).is_file(), f"Missing reference file: {name}")
    catalogue = read_json(root / "catalogo.json")
    require(catalogue["status"] == "planning_reference_not_runtime_catalogue", "Reference status changed")
    require(catalogue["proposed_additional_hours"] is None, "Unreviewed additional hours")
    baseline = catalogue["baseline"]
    require((baseline["modules"], baseline["laboratory_designs"], baseline["planned_hours"]) == (32, 96, 480), "Baseline counts changed")
    require(baseline["theory_hours"] + baseline["practice_hours"] == 480, "Baseline hours mismatch")
    areas = catalogue["areas"]
    area_ids = [area["id"] for area in areas]
    require_unique(area_ids, "area IDs")
    require(area_ids == [f"A{i:02d}" for i in range(1, 19)], "Expected 18 ordered areas")
    units = []
    for area in areas:
        expected = [f"{area['id']}.U{i:02d}" for i in range(1, 7)]
        require(area["unit_ids"] == expected, f"Unit IDs mismatch in {area['id']}")
        require(bool(area["title_es"]) and bool(area["title_en"]), "Missing bilingual title")
        require(all(re.fullmatch(r"M(?:0[1-9]|[12][0-9]|3[0-2])", mid) for mid in area["legacy_modules"]), "Unknown legacy module")
        units.extend(area["unit_ids"])
    require_unique(units, "unit IDs")
    validate_graph(areas)
    syllabus = (root / "01-mapa-curricular.md").read_text(encoding="utf-8")
    written_units = re.findall(r"^- \*\*(A\d{2}\.U\d{2})\.", syllabus, re.MULTILINE)
    require(written_units == units, "Syllabus and catalogue units differ")
    written_areas = re.findall(r"^## (A\d{2}) ·", syllabus, re.MULTILINE)
    require(written_areas == area_ids, "Syllabus area headings differ")
    labs = re.findall(r"^\| (LAB-\d{2}) \|", (root / "06-laboratorios.md").read_text(encoding="utf-8"), re.MULTILINE)
    require(labs == catalogue["lab_scenarios"] == [f"LAB-{i:02d}" for i in range(1, 25)], "Expected 24 laboratory designs")
    glossary = re.findall(r"^\| (G\d{3}) \|", (root / "07-glosario-protecciones.md").read_text(encoding="utf-8"), re.MULTILINE)
    require(glossary == [f"G{i:03d}" for i in range(1, 111)], "Expected 110 ordered glossary entries")
    categories = re.findall(r"^\| ((?:GV|ID|PR|DE|RS|RC)\.[A-Z]{2}) \|", (root / "03-nist-equipos.md").read_text(encoding="utf-8"), re.MULTILINE)
    expected_categories = "GV.OC GV.RM GV.RR GV.PO GV.OV GV.SC ID.AM ID.RA ID.IM PR.AA PR.AT PR.DS PR.PS PR.IR DE.CM DE.AE RS.MA RS.AN RS.CO RS.MI RC.RP RC.CO".split()
    require(categories == expected_categories, "NIST category identifiers differ")
    sources_text = (root / "09-fuentes.md").read_text(encoding="utf-8")
    sources = re.findall(r"^\| (S\d{2}) \|", sources_text, re.MULTILINE)
    require(sources == [f"S{i:02d}" for i in range(1, 35)], "Source registry identifiers differ")
    require(catalogue["glossary_entries"] == len(glossary), "Glossary count mismatch")
    require(catalogue["nist_categories"] == len(categories), "Category count mismatch")
    require(catalogue["source_registry_entries"] == len(sources), "Source count mismatch")
    local_links = 0
    for document in sorted(root.glob("*.md")):
        text = document.read_text(encoding="utf-8")
        for source in re.findall(r"\bS\d{2}\b", text):
            require(source in sources, f"Undefined source {source} in {document.name}")
        for target in re.findall(r"\]\(([^)]+)\)", text):
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            path = (document.parent / unquote(parsed.path)).resolve()
            require(path.is_relative_to(root.resolve()), f"Reference link leaves capsule: {target}")
            require(path.is_file(), f"Broken local link in {document.name}: {target}")
            local_links += 1
    losses = validate_risk(read_json(root / "riesgo-ejemplo.json"))
    files = [p for p in sorted(root.iterdir()) if p.is_file() and p.suffix in {".md", ".json", ".py"}]
    manifest = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    return {"status": "passed", "scope": "reference structure, local links, IDs and synthetic arithmetic; not native labs, external link availability, translation completeness or legal compliance", "areas": len(areas), "proposed_units": len(units), "lab_designs": len(labs), "glossary_entries": len(glossary), "nist_categories": len(categories), "sources": len(sources), "local_links_checked": local_links, "expected_annual_losses_eur": losses, "sha256": manifest}


if __name__ == "__main__":
    try:
        report = validate_reference()
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"status": "failed", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
    print(json.dumps(report, ensure_ascii=False, indent=2))
