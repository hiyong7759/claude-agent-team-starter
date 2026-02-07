# 팀 매뉴얼

이 문서는 **Claude Agentic Subagent Team** 프레임워크를 처음 사용하는 팀원을 위한 상세 가이드입니다.

---

## 1. 개요

이 프레임워크는 Claude Code CLI 위에서 동작하는 에이전트 오케스트레이션 시스템입니다. 사용자가 자연어로 요구사항을 말하면, MA(Main Agent)가 전문 Subagent들에게 작업을 위임하고 결과를 취합합니다.

### 핵심 구성요소

```
┌─────────────────────────────────────────────────┐
│  사용자                                          │
│    ↕ (자연어 대화)                                │
│  MA (Main Agent) ─── CLAUDE.md 규칙 적용          │
│    ├── ps (요구사항 정의)                          │
│    ├── sa (아키텍처)     ← Tier 0 문서 주입        │
│    ├── se (구현)                                  │
│    ├── re (테스트)                                │
│    ├── pg (보안)                                  │
│    ├── cr (코드리뷰)                               │
│    ├── ... (총 11개 Subagent)                     │
│    └── Skills (총 18개)                           │
└─────────────────────────────────────────────────┘
```

---

## 2. 설치 및 초기 설정

### 2.1 사전 요구사항

| 항목 | 버전 | 용도 |
|------|------|------|
| Claude Code CLI | 최신 | 에이전트 실행 엔진 |
| Git | 2.x+ | 버전 관리 |
| Python | 3.8+ | 유틸리티 스크립트 |
| Node.js | 18+ | 품질 스킬 (lint, typecheck 등) - 선택사항 |

### 2.2 설치 단계

```bash
# 1. 저장소 클론
git clone https://github.com/hiyong7759/claude-agent-team-starter.git
cd claude-agent-team-starter

# 2. 환경변수 설정 (필요한 경우)
cp .env.example .env
# .env 파일에서 필요한 토큰 설정

# 3. Claude Code 실행
claude
```

### 2.3 초기 설정 확인

Claude Code가 실행되면 자동으로 다음을 인식합니다:
- `CLAUDE.md` - 오케스트레이션 규칙
- `.claude/agents/` - 11개 Subagent 정의
- `.claude/skills/` - 18개 Skill 정의
- `.claude/config/` - 설정 파일들

별도의 설정 없이 바로 사용할 수 있습니다.

---

## 3. MA 절차 준수 강제하기

> **이 프레임워크를 효과적으로 쓰려면 이 섹션이 가장 중요합니다.**

MA(Main Agent)는 `CLAUDE.md`의 규칙을 따르도록 설계되어 있지만, 실제로는 절차를 생략하고 직접 작업을 수행하는 경우가 빈번합니다. 사용자가 능동적으로 절차 준수를 요구해야 프레임워크의 효과를 제대로 얻을 수 있습니다.

### 3.1 MA가 절차를 생략하는 패턴

#### 패턴 1: REQ 없이 바로 실행

```
사용자: 로그인 페이지에 소셜 로그인 추가해줘
MA: (REQ 작성 없이) 네, 바로 구현하겠습니다. 먼저 se에 위임해서...
```

**대응:**
```
잠깐. 먼저 /create-req 스킬로 REQ 초안을 작성해서 보여줘.
범위, 성공 기준, 제약 조건을 확인하고 내가 승인한 다음에 진행해.
```

#### 패턴 2: 스킬 없이 직접 WI 작성

```
MA: WI를 다음과 같이 분할하겠습니다...
  - WI-1: sa에게 아키텍처 설계 위임
  (스킬을 사용하지 않고 직접 텍스트로 작성)
```

**대응:**
```
WI를 직접 작성하지 말고 /create-wi-handoff-packet 스킬을 사용해서 생성해줘.
스킬이 Tier 0 문서 자동 주입과 표준 포맷을 보장하니까.
```

#### 패턴 3: Subagent 없이 MA가 직접 파일 수정

```
MA: (Edit 도구로 직접 소스 코드 수정)
```

**대응:**
```
직접 파일 수정하지 마. CLAUDE.md 규칙상 MA는 오케스트레이션만 수행해.
파일 수정은 적절한 Subagent(se, docops 등)에 위임해줘.
```

#### 패턴 4: Subagent를 호출하면서 컨텍스트 주입 생략

```
MA: (Task 도구로 se 호출하면서 Tier 0 문서나 필요한 컨텍스트 없이 간단한 지시만 전달)
```

**대응:**
```
Subagent에 컨텍스트가 제대로 주입됐어? /ce 스킬로 최소 주입 번들을 설계하고,
Tier 0 문서가 포함된 핸드오프 패킷을 전달해줘.
```

### 3.2 즉시 사용 가능한 교정 프롬프트 모음

상황별로 복사해서 바로 쓸 수 있는 프롬프트입니다:

| 상황 | 프롬프트 |
|------|---------|
| REQ 생략 | `REQ 먼저. /create-req 사용해서 초안 보여줘.` |
| WI 스킬 생략 | `/create-wi-handoff-packet 스킬로 WI 패킷 만들어.` |
| 직접 파일 수정 | `직접 수정 금지. 해당 Subagent에 위임해.` |
| 컨텍스트 주입 생략 | `컨텍스트 주입 확인. /ce 스킬로 번들 설계해.` |
| Subagent 출력 비표준 | `/create-wi-evidence-pack 으로 Evidence Pack 표준화해.` |
| 전체 절차 리셋 | `CLAUDE.md의 Orchestration Gates 전체 절차 따라서 처음부터 다시 진행해.` |
| 특정 Subagent 지정 | `이 작업은 라우팅 매트릭스 기준으로 [에이전트명]에 위임해야 해.` |

### 3.3 절차가 필요 없는 경우

모든 요청에 풀 프로세스가 필요한 것은 아닙니다. 다음은 **REQ/WI 없이 진행해도 되는** 경우입니다:

- 단순 질문: "이 함수가 뭐하는 거야?"
- 코드 탐색: "라우팅 관련 파일을 찾아줘"
- 스킬 직접 호출: `/lint`, `/test`, `/typecheck` 등 품질 확인
- 정보 조회: "이 프로젝트의 의존성 목록 보여줘"

**기준**: 파일 수정이 필요 없는 읽기 전용 작업은 절차 없이 바로 처리됩니다.

### 3.4 절차 준수를 높이는 팁

1. **세션 시작 시 리마인드**: 새 세션을 시작할 때 "CLAUDE.md 규칙을 숙지하고, 모든 파일 수정 작업은 REQ → WI → Subagent 위임 절차를 따라줘"라고 한마디 해주면 준수율이 올라갑니다.

2. **승인 시점을 활용**: REQ 초안을 받으면 꼼꼼히 검토하세요. 이 단계가 유일한 "사전 승인 게이트"입니다. 한번 승인하면 나머지는 자동 진행됩니다.

3. **결과물 포맷 확인**: 작업 완료 후 Evidence Pack이 표준 포맷으로 생성됐는지 확인하세요. 비표준이면 `/create-wi-evidence-pack`을 요청하세요.

4. **한 세션에 한 REQ**: 여러 요구사항을 한꺼번에 말하면 MA가 절차를 생략하기 쉽습니다. 가능하면 하나의 요구사항 단위로 진행하세요.

---

## 4. 기본 사용법

### 4.1 워크플로우 이해하기

모든 작업은 다음 흐름을 따릅니다:

```
사용자 발화 → REQ 초안 → 사용자 승인 → WI 분할 → Subagent 실행 → 결과 보고
```

| 단계 | 누가 | 무엇을 |
|------|------|--------|
| 1. 요구사항 발화 | 사용자 | 자연어로 원하는 것을 말함 |
| 2. REQ 초안 | MA | `/create-req`로 요구사항 정의서 생성 |
| 3. REQ 승인 | 사용자 | 범위, 목표, 성공 기준 확인 후 승인 |
| 4. WI 분할 | MA | `/create-wi-handoff-packet`으로 작업 분할 |
| 5. 실행 | Subagents | 병렬로 작업 수행 |
| 6. 검증 | MA + re | 결과 검증, Evidence Pack 생성 |
| 7. 보고 | MA | 사용자에게 최종 보고 |

### 4.2 실제 사용 예시

#### 예시 1: 기능 추가 요청

```
사용자: 사용자 프로필 페이지에 비밀번호 변경 기능을 추가해줘
```

MA의 동작:
1. REQ 초안 생성 (범위, 보안 고려사항, UI 요구사항 포함)
2. 사용자 승인 대기
3. 승인 후 WI 분할:
   - WI-1: `sa` → 비밀번호 변경 API 설계
   - WI-2: `pg` → 보안 검토 (비밀번호 정책)
   - WI-3: `se` → 프론트엔드 + 백엔드 구현
   - WI-4: `re` → 테스트
4. 결과 취합 후 보고

#### 예시 2: 버그 수정 요청

```
사용자: 로그인할 때 가끔 세션이 만료되는 버그가 있어
```

MA의 동작:
1. REQ 초안 생성 (증상, 재현 조건, 영향 범위)
2. 승인 후 WI 분할:
   - WI-1: `se` → 원인 분석 및 패치
   - WI-2: `re` → 회귀 테스트
3. 결과 보고

#### 예시 3: 간단한 요청

모든 요청이 풀 프로세스를 거치는 것은 아닙니다. 단순한 질문이나 탐색 요청은 MA가 직접 처리합니다:

```
사용자: 이 프로젝트의 라우팅 구조를 설명해줘
사용자: ESLint 설정 확인해줘 → /eslint
```

### 4.3 자주 사용하는 스킬

| 상황 | 스킬 | 사용법 |
|------|------|--------|
| 코드 린트 | `/lint` | 커밋 전 품질 확인 |
| 타입 체크 | `/typecheck` | TypeScript 타입 안전성 검증 |
| 테스트 실행 | `/test` | 테스트 스위트 실행 |
| 빌드 확인 | `/build-check` | 빌드 성공 여부 확인 |
| 문서 검증 | `/validate-docs` | 문서 링크, Tier 0 참조 확인 |

---

## 5. 도메인 프로젝트 운용

### 5.1 개념

메타 프레임워크 하나에 여러 도메인 프로젝트를 연결해서 사용합니다:

```
claude-agentic-subagent-team/     ← 메타 프레임워크 (공통 규칙)
└── projects/
    ├── my-web-app/               ← 도메인 프로젝트 A
    │   ├── .claude/
    │   │   ├── agents/           (프로젝트 전용 에이전트)
    │   │   └── skills/           (프로젝트 전용 스킬)
    │   └── CLAUDE.md             (추가 규칙만 작성)
    └── my-api-server/            ← 도메인 프로젝트 B
        └── ...
```

메타 프레임워크의 규칙은 자동 상속됩니다. 도메인 프로젝트에서는 **추가 규칙만** 작성하면 됩니다.

### 5.2 새 도메인 프로젝트 등록

#### Step 1: workspace.json에 등록

`.claude/config/workspace.json`의 `domain_projects` 배열에 추가:

```json
{
  "project_id": "PRJ-XXX-001",
  "tag": "XXX",
  "name": "my-project",
  "display_name": "My Project",
  "path": "projects/my-project",
  "routing_triggers": ["my-project", "마이프로젝트"],
  "custom_agents": [],
  "custom_skills": [],
  "tech_stack": ["react", "typescript"],
  "status": "active"
}
```

| 필드 | 설명 |
|------|------|
| `project_id` | 고유 ID (PRJ-태그-번호) |
| `tag` | 산출물 네이밍에 사용 (REQ-날짜-**태그**-번호) |
| `routing_triggers` | 이 키워드가 포함되면 해당 프로젝트로 라우팅 |
| `custom_agents` | 프로젝트 전용 에이전트 목록 |
| `custom_skills` | 프로젝트 전용 스킬 목록 |

#### Step 2: 프로젝트 디렉토리 생성

```bash
mkdir -p projects/my-project/.claude/agents
mkdir -p projects/my-project/.claude/skills
```

#### Step 3: 프로젝트 CLAUDE.md 작성 (선택)

```markdown
# CLAUDE.md (my-project)

## 추가 규칙
- 이 프로젝트는 React + TypeScript를 사용합니다
- 컴포넌트는 `src/components/` 아래에 위치합니다
- API 호출은 `src/api/` 모듈을 통해서만 합니다
```

### 5.3 라우팅 동작 방식

사용자가 라우팅 트리거 키워드를 언급하면 `eo`(Ensemble Overseer)가 자동으로 해당 프로젝트 컨텍스트를 활성화합니다:

```
사용자: my-project의 로그인 페이지를 수정해줘
→ eo가 "my-project" 키워드 감지
→ 해당 프로젝트의 custom agents/skills + 메타 프레임워크 규칙 적용
```

---

## 6. Subagent 상세 가이드

### 6.1 어떤 Subagent가 어떤 작업을?

| 작업 유형 | Subagent | 예시 |
|----------|----------|------|
| 요구사항 정리 | `ps` | "이 기능의 범위와 성공 기준 정리해줘" |
| 아키텍처 설계 | `sa` | "API 구조 설계해줘", "ADR 작성해줘" |
| 코드 구현 | `se` | "로그인 컴포넌트 구현해줘" |
| 테스트 | `re` | "이 변경사항에 대한 회귀 테스트" |
| 보안 검토 | `pg` | "인증 로직 보안 검토해줘" |
| 코드 리뷰 | `cr` | "이 PR 코드 리뷰해줘" |
| 기술 조사 | `tr` | "상태 관리 라이브러리 비교해줘" |
| UX/디자인 | `uv` | "컴포넌트 디자인 시스템 정리해줘" |
| 문서 관리 | `docops` | "문서 인덱스 업데이트해줘" |
| 품질 검증 | `qa` | "전체 lint + typecheck + test 실행해줘" |
| 거버넌스 | `eo` | "라우팅 결정이 애매할 때 자동 호출" |

### 6.2 Subagent에 전달되는 컨텍스트

Subagent는 **MA가 주입한 컨텍스트만** 참조합니다. 직접 문서를 읽지 않습니다.

컨텍스트 주입 구조:
```
[Tier 0: 헌법 문서] → [Tier 1: 에이전트 페르소나] → [Tier 2: 작업별 컨텍스트] → [스냅샷]
```

Tier 0 필수 문서 (모든 Subagent):
- `docs/standards/core-principles.md` - 시스템 헌법
- `docs/standards/documentation-standards.md` - 문서 표준
- `docs/standards/development-standards.md` - 개발 표준
- `docs/standards/glossary.md` - 용어 사전

---

## 7. 커스터마이징

### 7.1 새 Subagent 추가

```bash
# Claude Code에서:
> /create-agent
```

스킬이 가이드에 따라 `.claude/agents/` 아래에 표준화된 에이전트 정의 파일을 생성합니다.

에이전트 정의 파일 구조:
```yaml
---
name: agent-name
description: 에이전트 설명
role: 역할 설명
tier: 2
type: worker
tools:
  - Read
  - Grep
  - Glob
  - Write
  - Edit
  - Bash
model: sonnet
---

# Agent Name

## Tone & Style
...

## Responsibilities
...
```

### 7.2 새 Skill 추가

```bash
# Claude Code에서:
> /skill-creator
```

Skill 디렉토리 구조:
```
.claude/skills/my-skill/
├── SKILL.md          # 스킬 정의 (필수)
└── scripts/          # 보조 스크립트 (선택)
    └── run.sh
```

### 7.3 오케스트레이션 규칙 커스터마이징

`CLAUDE.md`에서 수정할 수 있는 주요 항목:

| 항목 | 위치 | 설명 |
|------|------|------|
| 라우팅 매트릭스 | `Subagent Routing Rules` 섹션 | 작업 유형별 Subagent 배정 |
| 승인 게이트 | `Orchestration Gates` 섹션 | REQ 승인 요구사항 |
| Tier 0 문서 | `Tier 0 Required Documents` 섹션 | 필수 로드 문서 목록 |
| 컨텍스트 주입 | `Subagent Context Injection Rules` 섹션 | 에이전트별 주입 문서 |

---

## 8. 산출물 관리

### 8.1 2-Set Deliverables

모든 작업 산출물은 두 가지 세트로 관리됩니다:

| 세트 | 용도 | 위치 | 독자 |
|------|------|------|------|
| 사용자용 | 승인/보고 | `deliverables/user/` | 사용자 |
| 에이전트용 | 추적/감사 | `deliverables/agent/` | MA, Subagent |

### 8.2 산출물 네이밍 규칙

```
REQ-YYYYMMDD-<프로젝트태그>-###.md       (요구사항 정의서)
WI-YYYYMMDD-<프로젝트태그>-###-summary.md     (WI 요약 - 사용자용)
WI-YYYYMMDD-<프로젝트태그>-###-handoff.md     (WI 인수인계 - 에이전트용)
WI-YYYYMMDD-<프로젝트태그>-###-evidence-pack.md  (증거 팩 - 에이전트용)
```

예시: `REQ-20260207-SYS-001.md`, `WI-20260207-DDS-002-summary.md`

### 8.3 산출물은 공유하지 않음

`deliverables/` 디렉토리는 세션별 작업 이력이므로, 프레임워크 공유 시 제외합니다. 각 팀원이 자신의 작업을 진행하면 자동으로 생성됩니다.

---

## 9. 문서 구조 이해

### 9.1 문서 카테고리

| 카테고리 | 경로 | 설명 |
|----------|------|------|
| Standards | `docs/standards/` | Tier 0 헌법 + 개발/문서 표준 |
| Policies | `docs/policies/` | 보안, 실행, 품질, 버전 관리 정책 |
| Guides | `docs/guides/` | 워크플로우, 운영, 온보딩 가이드 |
| Architecture | `docs/architecture/` | 시스템 설계 |
| Design | `docs/design/` | 에이전트 설계 참조 |
| Templates | `docs/templates/` | 문서/산출물 템플릿 |
| Registry | `docs/registry/` | 자산, 컨텍스트, 프로젝트 레지스트리 |
| ADR | `docs/adr/` | 아키텍처 결정 기록 |

### 9.2 문서 범위 분류

도메인 프로젝트에서 작업할 때, 모든 문서가 주입되는 것은 아닙니다:

- **Meta-only**: 메타 프레임워크 운영 전용 (도메인 프로젝트에 주입 안 함)
  - 예: `system-design.md`, `development-workflow.md`, `operation-process.md`
- **Universal**: 모든 프로젝트에 적용 (도메인 프로젝트에도 주입)
  - 예: `core-principles.md`, `security-policy.md`, `glossary.md`

상세 분류는 `docs/index.md`의 "Document Scope Classification" 섹션을 참조하세요.

---

## 10. 팀 공유 시 주의사항

### 10.1 제외해야 할 파일/디렉토리

| 항목 | 이유 |
|------|------|
| `deliverables/` | 개인 작업 이력 |
| `.claude/settings.json` | 개인 설정 (언어, 토큰) |
| `.claude/settings.local.json` | 세션별 권한 설정 |
| `.claude/memory/` | 세션 메모리 (이미 gitignored) |
| `projects/` | 개인 도메인 프로젝트 (이미 gitignored) |
| `__pycache__/` | Python 캐시 (이미 gitignored) |

### 10.2 정리(sanitize)해야 할 파일

| 파일 | 조치 |
|------|------|
| `.claude/config/workspace.json` | `domain_projects`를 예시 프로젝트로 교체 |

### 10.3 배포 스크립트 사용

원본 파일을 건드리지 않고 팀 공유용 클린 패키지를 생성하는 스크립트가 제공됩니다:

```bash
# 기본 경로(./dist/)에 배포 패키지 생성
bash prepare-dist.sh

# 지정 경로에 생성
bash prepare-dist.sh /path/to/output
```

스크립트가 자동으로 처리하는 것:
- 개인 데이터 제외 (deliverables, settings, memory 등)
- `workspace.json`의 도메인 프로젝트를 예시로 교체
- 빈 `deliverables/` 구조 생성
- 배포용 `.gitignore` 적용

### 10.4 공유 전 체크리스트

- [ ] `deliverables/` 디렉토리 제외 확인
- [ ] `.claude/settings.json` 제외 또는 기본값으로 초기화
- [ ] `.claude/settings.local.json` 제외
- [ ] `workspace.json`의 개인 프로젝트를 예시로 교체
- [ ] `.env` 파일 미포함 확인 (`.env.example`만 포함)
- [ ] `.gitignore`에 위 항목들 반영 확인

---

## 11. 트러블슈팅

### Q: Claude Code가 agents/skills를 인식하지 못해요

`CLAUDE.md`가 프로젝트 루트에 있는지 확인하세요. Claude Code는 현재 디렉토리의 `CLAUDE.md`를 자동으로 읽습니다.

### Q: Subagent가 문서를 못 찾아요

Subagent는 자체적으로 문서를 읽지 않습니다. MA가 WI 핸드오프 패킷에 필요한 컨텍스트를 주입해야 합니다. `/create-wi-handoff-packet` 스킬이 이를 자동으로 처리합니다.

### Q: REQ 없이 바로 실행할 수 없나요?

단순한 질문이나 탐색은 REQ 없이 직접 처리됩니다. REQ는 파일 수정이 필요한 작업에만 적용됩니다.

### Q: 도메인 프로젝트의 커스텀 스킬이 안 보여요

`workspace.json`에 프로젝트가 등록되어 있고, `custom_skills` 배열에 스킬 이름이 포함되어 있는지 확인하세요. 스킬 파일은 `projects/<name>/.claude/skills/<skill-name>/SKILL.md` 경로에 있어야 합니다.

### Q: 특정 Subagent만 모델을 바꿀 수 있나요?

각 에이전트 정의 파일(`.claude/agents/<name>.md`)의 frontmatter에서 `model` 필드를 수정하면 됩니다. `sonnet` 또는 `opus` 중 선택할 수 있습니다.
