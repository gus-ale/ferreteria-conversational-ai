import json
from pathlib import Path

from app.services.guardrails import inspect_input
from app.services.intents import classify_intent


def main() -> int:
    cases_path = Path(__file__).with_name("cases.json")
    cases = json.loads(cases_path.read_text(encoding="utf-8"))
    failures: list[str] = []

    for case in cases:
        decision = inspect_input(case["input"], max_characters=2_000)
        intent = classify_intent(case["input"])
        if decision.allowed != case["allowed"]:
            failures.append(
                f"{case['name']}: allowed={decision.allowed}, expected={case['allowed']}"
            )
        if decision.allowed and intent != case["expected_intent"]:
            failures.append(f"{case['name']}: intent={intent}, expected={case['expected_intent']}")

    if failures:
        print("EVALUACIONES FALLIDAS")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"EVALUACIONES OK: {len(cases)}/{len(cases)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
