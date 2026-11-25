#!/usr/bin/env python3
"""Extract English questions from release_evidences.json."""

import argparse
import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = PROJECT_ROOT / "data" / "release_evidences.json"
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "questions_en.json"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract every question_en value into a JSON array."
    )
    parser.add_argument(
        "input", nargs="?", type=Path, default=DEFAULT_INPUT,
        help=f"input JSON file (default: {DEFAULT_INPUT})",
    )
    parser.add_argument(
        "output", nargs="?", type=Path, default=DEFAULT_OUTPUT,
        help=f"output JSON file (default: {DEFAULT_OUTPUT})",
    )
    args = parser.parse_args()

    with args.input.open(encoding="utf-8") as source_file:
        evidences = json.load(source_file)

    if not isinstance(evidences, dict):
        raise ValueError("Expected the input JSON to be an object keyed by evidence ID.")

    questions = [
        evidence["question_en"]
        for evidence in evidences.values()
        if isinstance(evidence, dict) and isinstance(evidence.get("question_en"), str)
    ]

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as output_file:
        json.dump(questions, output_file, ensure_ascii=False, indent=2)
        output_file.write("\n")

    print(f"Extracted {len(questions)} questions to {args.output}")


if __name__ == "__main__":
    main()
