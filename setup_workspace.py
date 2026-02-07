#!/usr/bin/env python3
"""
루트 실행용 래퍼.

프로젝트 복원 스크립트 본체: `.claude/scripts/setup_workspace.py`
"""

from __future__ import annotations

import runpy
from pathlib import Path


if __name__ == "__main__":
    script = Path(__file__).resolve().parent / ".claude" / "scripts" / "setup_workspace.py"
    runpy.run_path(str(script), run_name="__main__")

