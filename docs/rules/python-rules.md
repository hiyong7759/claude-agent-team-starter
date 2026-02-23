---
module: python-rules
tier: 1
inject: conditional
target_agents: [se]
condition: python
---

# Python Implementation Rules

Rules for Python scripts in the agent orchestration framework.

---

## PY-1: File Location and Structure

- Location: `.claude/scripts/{filename}.py`
- Filename: `snake_case` (e.g., `context_manager.py`, `test_triggers.py`)
- Encoding: `utf-8` required
- Execution: Must be executable as `python3 .claude/scripts/{filename}.py` (Argparse recommended)
- Python version: 3.10 or higher

## PY-2: Style Guide (PEP 8 + Type Hints)

- Type hints required in all function signatures.
- Docstrings: Google Style Docstring.
- Comments: Comment bodies in Korean. Code itself and technical terms may use English.
- Line length: 88 characters recommended (Black formatter), up to 100 allowed.

### Example Template

```python
import os
import argparse
from typing import List, Dict, Optional

def process_data(input_list: List[str], options: Optional[Dict] = None) -> bool:
    """
    Processes the input data based on provided options.

    Args:
        input_list: A list of strings to process.
        options: Optional configuration dictionary.

    Returns:
        True if processing was successful, False otherwise.

    Raises:
        ValueError: If input_list is empty.
    """
    if not input_list:
        raise ValueError("Input list cannot be empty")

    # ... logic ...
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process Data Script")
    # ... args ...
```

## PY-3: Security Coding

- No hardcoded secrets: Never include API keys or passwords in code.
- Environment variables: Use `os.environ.get("KEY_NAME")`.
- File operations: When user approval (HITL) is needed for file writes, request explicit user confirmation.

## PY-4: Dependencies

- Prefer standard library. For external libraries, specify in `requirements.txt` and install after user approval.
- Use system Python or venv within Single Machine Runtime.

## PY-5: Testing

- Test file naming: `test_*.py` (pytest convention).
- Test location: `.claude/tests/` (centralized, preferred for system scripts).
- Follow Arrange/Act/Assert structure.
- Coverage thresholds: 80% lines, 70% branches, 80% functions.

## PY-6: Traceability

- Leave evidence pointers (file/line/command/log/path) before explanations.
- Subagent results must include evidence pointers and reproduction/test procedures.
