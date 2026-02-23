#!/bin/bash
#
# check-teammate-idle.sh
# Agent Teams hook: keeps teammate working when predecessor has completed
# v2.0: se→fe/be split, cr→qa absorbed. Flow: be→fe→qa→re
#
# Usage: check-teammate-idle.sh <agent_role> <wi_id> <deliverables_dir>
#
# Exit codes:
#   0 = allow idle (predecessor not done yet)
#   2 = keep working (predecessor done, this agent should be active)
#

set -e

AGENT_ROLE="${1:?Error: agent_role required (fe|qa|re)}"
WI_ID="${2:?Error: WI ID required}"
DELIVERABLES_DIR="${3:?Error: deliverables directory required}"

echo ""
echo "Idle Check: ${AGENT_ROLE} for ${WI_ID}"
echo "-------------------------------------------"

case "${AGENT_ROLE}" in
  fe)
    # fe is blocked until be completes (type/service files exist)
    CHANGED_FILES=$(git diff --name-only HEAD 2>/dev/null || echo "")
    BE_FILES=$(echo "${CHANGED_FILES}" | grep -E '(types|services|mocks)' || echo "")
    if [ -n "${BE_FILES}" ]; then
      echo "UNBLOCKED: be has completed type/service changes"
      echo "ACTION: fe should begin UI implementation now"
      exit 2
    else
      echo "BLOCKED: be has not yet completed"
      echo "STATUS: fe should remain idle"
      exit 0
    fi
    ;;

  qa)
    # qa is blocked until fe completes (component/page files exist)
    CHANGED_FILES=$(git diff --name-only HEAD 2>/dev/null || echo "")
    FE_FILES=$(echo "${CHANGED_FILES}" | grep -E '(components|pages|\.tsx)' || echo "")
    if [ -n "${FE_FILES}" ]; then
      echo "UNBLOCKED: fe has completed component changes"
      echo "ACTION: qa should begin quality review now"
      exit 2
    else
      echo "BLOCKED: fe has not yet completed"
      echo "STATUS: qa should remain idle"
      exit 0
    fi
    ;;

  re)
    # re is blocked until qa completes (qa report exists)
    QA_FILE=$(find "${DELIVERABLES_DIR}" -name "${WI_ID}-qa-report.md" 2>/dev/null || echo "")
    if [ -n "${QA_FILE}" ] && [ -s "${QA_FILE}" ]; then
      echo "UNBLOCKED: qa report exists"
      echo "ACTION: re should begin testing now"
      exit 2
    else
      echo "BLOCKED: qa review not yet completed"
      echo "STATUS: re should remain idle"
      exit 0
    fi
    ;;

  *)
    echo "INFO: Agent '${AGENT_ROLE}' has no idle check configured"
    exit 0
    ;;
esac
