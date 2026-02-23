#!/bin/bash
#
# verify-task-complete.sh
# Quality gate hook for Agent Teams: blocks task completion without required deliverables
# v2.0: se→fe/be split, cr→qa absorbed
#
# Usage: verify-task-complete.sh <agent_role> <wi_id> <deliverables_dir>
# Example: verify-task-complete.sh fe WI-20260220-PMV2-001 deliverables/PMV2/20260220/agent
#
# Exit codes:
#   0 = gate passed, allow completion
#   2 = gate failed, block completion (Agent Teams: exit 2 = prevent)
#

set -e

AGENT_ROLE="${1:?Error: agent_role required (fe|be|qa|re)}"
WI_ID="${2:?Error: WI ID required}"
DELIVERABLES_DIR="${3:?Error: deliverables directory required}"

echo ""
echo "Gate Check: ${AGENT_ROLE} completion for ${WI_ID}"
echo "-------------------------------------------"

case "${AGENT_ROLE}" in
  fe)
    # fe must have component/page file changes
    CHANGED_FILES=$(git diff --name-only HEAD 2>/dev/null || echo "")
    FE_FILES=$(echo "${CHANGED_FILES}" | grep -E '(components|pages|\.tsx)' || echo "")
    if [ -z "${FE_FILES}" ]; then
      echo "BLOCKED: fe has no component/page file changes"
      echo "Fix: fe must modify at least one component or page file"
      exit 2
    fi
    echo "PASS: fe has frontend file changes"
    echo "${FE_FILES}" | head -10
    ;;

  be)
    # be must have type/service/mock file changes
    CHANGED_FILES=$(git diff --name-only HEAD 2>/dev/null || echo "")
    BE_FILES=$(echo "${CHANGED_FILES}" | grep -E '(types|services|mocks|hooks)' || echo "")
    if [ -z "${BE_FILES}" ]; then
      echo "BLOCKED: be has no type/service/mock file changes"
      echo "Fix: be must modify at least one type, service, or mock file"
      exit 2
    fi
    echo "PASS: be has backend file changes"
    echo "${BE_FILES}" | head -10
    ;;

  qa)
    # qa must produce a quality report (replaces cr review report)
    QA_FILE=$(find "${DELIVERABLES_DIR}" -name "${WI_ID}-qa-report.md" 2>/dev/null || echo "")
    if [ -z "${QA_FILE}" ]; then
      echo "BLOCKED: qa report not found"
      echo "Expected: ${DELIVERABLES_DIR}/${WI_ID}-qa-report.md"
      echo "Fix: qa must write quality report before completing"
      exit 2
    fi
    if [ ! -s "${QA_FILE}" ]; then
      echo "BLOCKED: qa report is empty"
      exit 2
    fi
    echo "PASS: qa report exists: ${QA_FILE}"
    ;;

  re)
    # re must produce a verification report
    VERIFY_FILE=$(find "${DELIVERABLES_DIR}" -name "${WI_ID}-re-verification.md" 2>/dev/null || echo "")
    if [ -z "${VERIFY_FILE}" ]; then
      echo "BLOCKED: re verification report not found"
      echo "Expected: ${DELIVERABLES_DIR}/${WI_ID}-re-verification.md"
      echo "Fix: re must write verification report before completing"
      exit 2
    fi
    if [ ! -s "${VERIFY_FILE}" ]; then
      echo "BLOCKED: re verification report is empty"
      exit 2
    fi
    echo "PASS: re verification report exists: ${VERIFY_FILE}"
    ;;

  *)
    echo "WARNING: Unknown agent role '${AGENT_ROLE}', skipping gate check"
    exit 0
    ;;
esac

echo "-------------------------------------------"
echo "Gate passed for ${AGENT_ROLE}"
exit 0
