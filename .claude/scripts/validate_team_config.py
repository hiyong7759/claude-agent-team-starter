#!/usr/bin/env python3
"""
Team Configuration Validator

Validates team-definitions.json structure and semantic integrity.

Usage:
    python3 .claude/scripts/validate_team_config.py [path_to_config]

    If path is omitted, defaults to .claude/config/team-definitions.json

Exit codes:
    0 - Validation passed
    1 - Validation failed
"""

import json
import sys
from pathlib import Path
from typing import List

VALID_AGENTS = [
    "ps", "eo", "sa", "se", "re", "pg", "tr", "uv", "docops", "qa", "cr"
]


class TeamConfigValidator:
    """Validates team-definitions.json for structural and semantic correctness."""

    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.errors: List[str] = []
        self.data = None

    def validate(self) -> bool:
        """Run all validation checks. Returns True if all pass."""
        if not self._load_json():
            return False

        self._check_top_level_keys()
        self._check_teams()

        return len(self.errors) == 0

    def _load_json(self) -> bool:
        """Check 1: File exists and is valid JSON."""
        if not self.config_path.exists():
            self.errors.append(f"File not found: {self.config_path}")
            return False

        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                self.data = json.load(f)
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON: {e}")
            return False

        return True

    def _check_top_level_keys(self) -> None:
        """Check 2: Required top-level keys exist."""
        required_keys = ["version", "teams"]
        for key in required_keys:
            if key not in self.data:
                self.errors.append(f"Missing required top-level key: '{key}'")

    def _check_teams(self) -> None:
        """Check 3-7: Validate each team definition."""
        if "teams" not in self.data:
            return

        teams = self.data["teams"]
        if not isinstance(teams, dict):
            self.errors.append("'teams' must be an object")
            return

        for team_id, team_def in teams.items():
            self._check_team(team_id, team_def)

    def _check_team(self, team_id: str, team_def: dict) -> None:
        """Validate a single team definition."""
        prefix = f"Team '{team_id}'"

        # Check 3: Required team keys
        required_team_keys = [
            "display_name", "members", "feedback_loops", "quality_gates"
        ]
        for key in required_team_keys:
            if key not in team_def:
                self.errors.append(f"{prefix}: missing required key '{key}'")

        # Check members
        members = team_def.get("members", [])
        if not isinstance(members, list):
            self.errors.append(f"{prefix}: 'members' must be an array")
            return

        member_agents = set()
        expected_order = 1

        for i, member in enumerate(members):
            if not isinstance(member, dict):
                self.errors.append(
                    f"{prefix}: member at index {i} must be an object"
                )
                continue

            agent = member.get("agent")

            # Check 4: Agent is in the valid agent list
            if agent is not None:
                if agent not in VALID_AGENTS:
                    self.errors.append(
                        f"{prefix}: member agent '{agent}' is not a valid "
                        f"agent. Valid agents: {VALID_AGENTS}"
                    )
                member_agents.add(agent)
            else:
                self.errors.append(
                    f"{prefix}: member at index {i} missing 'agent' key"
                )

            # Check 5: Order is sequential (1, 2, 3, ...)
            order = member.get("order")
            if order is not None:
                if order != expected_order:
                    self.errors.append(
                        f"{prefix}: member '{agent}' has order {order}, "
                        f"expected {expected_order}"
                    )
                expected_order += 1
            else:
                self.errors.append(
                    f"{prefix}: member at index {i} missing 'order' key"
                )

        # Check feedback loops
        feedback_loops = team_def.get("feedback_loops", [])
        if isinstance(feedback_loops, list):
            for j, loop in enumerate(feedback_loops):
                if not isinstance(loop, dict):
                    self.errors.append(
                        f"{prefix}: feedback_loop at index {j} must be "
                        f"an object"
                    )
                    continue

                # Check 6: from/to agents are team members
                for direction in ("from", "to"):
                    agent = loop.get(direction)
                    if agent is not None:
                        if agent not in member_agents:
                            self.errors.append(
                                f"{prefix}: feedback_loop[{j}].{direction} "
                                f"'{agent}' is not a member of this team. "
                                f"Members: {sorted(member_agents)}"
                            )
                    else:
                        self.errors.append(
                            f"{prefix}: feedback_loop[{j}] missing "
                            f"'{direction}' key"
                        )

                # Check 7: max_iterations is a positive integer
                max_iter = loop.get("max_iterations")
                if max_iter is not None:
                    if not isinstance(max_iter, int) or max_iter <= 0:
                        self.errors.append(
                            f"{prefix}: feedback_loop[{j}].max_iterations "
                            f"must be a positive integer, got {max_iter}"
                        )
                else:
                    self.errors.append(
                        f"{prefix}: feedback_loop[{j}] missing "
                        f"'max_iterations' key"
                    )


def main():
    """Main entry point."""
    # Determine config path
    if len(sys.argv) > 1:
        config_path = Path(sys.argv[1])
    else:
        # Default: relative to repo root (script is in .claude/scripts/)
        repo_root = Path(__file__).parent.parent.parent
        config_path = repo_root / ".claude" / "config" / "team-definitions.json"

    validator = TeamConfigValidator(config_path)

    if validator.validate():
        print(f"PASS: {config_path.name} is valid")
        sys.exit(0)
    else:
        for error in validator.errors:
            print(f"FAIL: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
