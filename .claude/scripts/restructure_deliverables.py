#!/usr/bin/env python3
"""
Restructure deliverables/ from flat agent/user to project/date/agent|user hierarchy.

Usage:
    python3 .claude/scripts/restructure_deliverables.py --dry-run   # Preview
    python3 .claude/scripts/restructure_deliverables.py             # Execute
"""

import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DELIVERABLES = ROOT / "deliverables"

# Non-conforming file hardcoded mapping
HARDCODED_MAP = {
    ("agent", "FLOW-VERIFICATION-EVIDENCE.md"): ("SYS", "20260207", "agent"),
    ("user", "FLOW-VERIFICATION-SUMMARY.md"): ("SYS", "20260207", "user"),
    ("user", "DDS-TYPE-ERRORS-REPORT.md"): ("DDS", "20260206", "user"),
    ("user", "agent-facing-docs-ops-approval-20260127.md"): ("SYS", "20260127", "user"),
    ("user", "ma-subagent-injection-mechanism.md"): ("SYS", "20260131", "user"),
    ("user", "poomacy-v2-status-20260201.md"): ("PMV2", "20260201", "user"),
}

# Known project tags
KNOWN_TAGS = {"SYS", "PMV2", "DDS", "PMDDS", "USI"}

# Pattern: WI-YYYYMMDD-<TAG>-NNN-* or REQ-YYYYMMDD-<TAG>-NNN*
TAGGED_PATTERN = re.compile(
    r"^(?:WI|REQ)-(\d{8})-([A-Z][A-Z0-9]+)-\d+"
)

# Pattern: WI-YYYYMMDD-SES-XXXX-NNN-* (session tag → SYS)
SESSION_PATTERN = re.compile(
    r"^(?:WI|REQ)-(\d{8})-SES-[a-f0-9]+-\d+"
)

# Legacy pattern: WI-YYYYMMDD-NNN-* or REQ-YYYYMMDD-NNN-*
LEGACY_PATTERN = re.compile(
    r"^(?:WI|REQ)-(\d{8})-\d+"
)


def classify_file(set_type: str, filename: str):
    """
    Classify a file into (project, date, target_set).
    Returns (project, date, set_type) or None if unclassifiable.
    """
    key = (set_type, filename)
    if key in HARDCODED_MAP:
        return HARDCODED_MAP[key]

    # Try tagged pattern (WI-20260205-SYS-001-*)
    m = TAGGED_PATTERN.match(filename)
    if m:
        date, tag = m.group(1), m.group(2)
        if tag in KNOWN_TAGS:
            return (tag, date, set_type)
        # Unknown tag → SYS
        return ("SYS", date, set_type)

    # Try session pattern (WI-20260201-SES-29a7-*)
    m = SESSION_PATTERN.match(filename)
    if m:
        date = m.group(1)
        return ("SYS", date, set_type)

    # Try legacy pattern (WI-20260131-001-* or REQ-20260129-001-*)
    m = LEGACY_PATTERN.match(filename)
    if m:
        date = m.group(1)
        return ("SYS", date, set_type)

    # Unclassifiable
    return None


def build_move_plan():
    """Build list of (old_path, new_path) tuples."""
    moves = []
    unclassified = []

    for set_type in ("agent", "user"):
        src_dir = DELIVERABLES / set_type
        if not src_dir.exists():
            continue
        for filename in sorted(os.listdir(src_dir)):
            if not filename.endswith(".md"):
                continue
            old_path = src_dir / filename
            result = classify_file(set_type, filename)
            if result:
                project, date, target_set = result
                new_path = DELIVERABLES / project / date / target_set / filename
                moves.append((old_path, new_path))
            else:
                # Should not happen with our hardcoded map
                unclassified.append((set_type, filename))

    return moves, unclassified


def main():
    dry_run = "--dry-run" in sys.argv

    moves, unclassified = build_move_plan()

    if unclassified:
        print("WARNING: Unclassified files:")
        for set_type, filename in unclassified:
            print(f"  {set_type}/{filename}")
        print()

    # Collect stats
    projects = {}
    for old_path, new_path in moves:
        rel_new = new_path.relative_to(DELIVERABLES)
        parts = rel_new.parts
        project = parts[0]
        date = parts[1]
        key = f"{project}/{date}"
        projects.setdefault(key, 0)
        projects[key] += 1

    print(f"Total files to move: {len(moves)}")
    print(f"\nBreakdown by project/date:")
    for key in sorted(projects.keys()):
        print(f"  {key}: {projects[key]} files")

    if dry_run:
        print(f"\n--- DRY RUN: showing all moves ---")
        for old_path, new_path in moves:
            old_rel = old_path.relative_to(ROOT)
            new_rel = new_path.relative_to(ROOT)
            print(f"  {old_rel} → {new_rel}")
        print(f"\nDry run complete. {len(moves)} files would be moved.")
        return

    print(f"\nExecuting {len(moves)} git mv operations...")

    # Create target directories
    dirs_created = set()
    for _, new_path in moves:
        target_dir = new_path.parent
        if target_dir not in dirs_created:
            target_dir.mkdir(parents=True, exist_ok=True)
            dirs_created.add(target_dir)

    # Execute git mv
    errors = []
    for i, (old_path, new_path) in enumerate(moves):
        old_rel = old_path.relative_to(ROOT)
        new_rel = new_path.relative_to(ROOT)
        result = subprocess.run(
            ["git", "mv", str(old_rel), str(new_rel)],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            errors.append((old_rel, new_rel, result.stderr.strip()))
            print(f"  ERROR: {old_rel} → {new_rel}: {result.stderr.strip()}")
        else:
            if (i + 1) % 50 == 0:
                print(f"  Moved {i + 1}/{len(moves)}...")

    print(f"\nCompleted: {len(moves) - len(errors)} moved, {len(errors)} errors")

    if errors:
        print("\nErrors:")
        for old_rel, new_rel, err in errors:
            print(f"  {old_rel} → {new_rel}: {err}")

    # Try to remove empty old directories
    for set_type in ("agent", "user"):
        old_dir = DELIVERABLES / set_type
        if old_dir.exists():
            remaining = list(old_dir.iterdir())
            if not remaining:
                subprocess.run(["git", "rm", "-r", str(old_dir.relative_to(ROOT))],
                             cwd=ROOT, capture_output=True)
                print(f"  Removed empty directory: deliverables/{set_type}/")
            else:
                print(f"  Directory deliverables/{set_type}/ still has {len(remaining)} files")


if __name__ == "__main__":
    main()
