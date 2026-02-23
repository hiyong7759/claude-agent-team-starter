# Claude Agentic Subagent Team

[Claude Code](https://docs.anthropic.com/en/docs/claude-code)에 최적화된 **에이전트 오케스트레이션 프레임워크**입니다. **MA (Main Agent) + Subagents + Skills** 아키텍처를 통해 1인 개발에서도 속도, 일관성, 재사용성을 확보합니다.

## 이 프레임워크를 왜 쓰나요?

Claude Code를 사용하는 개발자가 반복적으로 겪는 문제들:
- **컨텍스트 폭발**: 탐색 로그와 대량 출력이 메인 대화를 오염시킴
- **일관성 부재**: 세션마다 품질과 스타일이 달라짐
- **반복 작업**: REQ 작성, 코드 리뷰, 테스트 같은 절차를 매번 새로 수행

이 프레임워크의 해결 방식:
- **11개 전문 Subagent**가 격리된 컨텍스트에서 작업 수행
- **19개 재사용 Skill**이 반복 절차를 표준화
- **Tier 0 규칙 모듈**이 모든 작업의 일관성을 보장
- **2-Set Deliverables**로 사용자용 요약과 에이전트용 감사 추적을 분리

## v2.0 주요 변경사항

### 왜 바뀌었나?

#### 문제 1: 컨텍스트 주입 비효율

이전 버전은 원칙, 정책, 표준, 가이드, 보안 등 **10개 카테고리에 50개 이상의 문서**(~4,800줄)로 규칙이 분산되어 있었습니다. 이로 인해:

- **에이전트가 규칙을 빈번하게 무시**: 방대하고 두리뭉실하게 작성된 문서가 한꺼번에 주입되면서, 에이전트가 핵심 규칙을 놓치거나 우선순위를 판단하지 못하는 경우가 발생
- **불필요한 컨텍스트 낭비**: 하나의 문서 안에서도 특정 작업에 필요한 부분은 일부인데, 문서 전체가 주입되어 토큰 비용 증가
- **상호 혼동 발생**: 여러 문서에 걸쳐 유사한 내용이 다른 표현으로 존재하면서 에이전트가 어떤 규칙을 따라야 할지 혼란

#### 문제 2: 에이전트 역할의 세분화 부족

기존 `se`(Software Engineer)는 프론트엔드와 백엔드를 모두 담당하는 범용 구현자였고, `cr`(Code Reviewer)은 코드 리뷰만 전담했습니다. 실제 운용 경험에서:

- `se`가 한 번에 FE+BE를 모두 처리하면 출력이 비대해지고 품질이 떨어짐
- FE/BE 간 **타입 계약(shared contract)** 이 깨지는 경우가 빈번
- `cr`과 `qa`의 역할이 중복되어 리뷰 단계가 비효율적

### bkit 벤치마킹과 적용

[bkit](https://github.com/popup-studio-ai/bkit-claude-code)은 PDCA 기반 Claude Code 플러그인(16 에이전트, 5계층 Hook)입니다. bkit에서 참고한 핵심 개념과 적용:

| bkit 개념 | 우리 프레임워크 적용 |
|-----------|---------------------|
| CTO-Led Agent Teams | `impl-team` (be → fe → qa → re 자율 협업) |
| Frontend/Backend 아키텍트 분리 | `se` → `fe` + `be` 분리 |
| TaskCompleted/TeammateIdle 훅 | 품질 게이트 훅 (deliverable 검증) |
| 모델별 역할 배분 (Opus/Sonnet/Haiku) | 에이전트 모델 최적화 |
| Context Engineering 3계층 | 모듈형 주입 매트릭스 (Tier 0/1/2) |

### bkit vs 이 프레임워크

**bkit의 장점 (우리의 단점)**
- 플러그인 설치 한 줄로 즉시 사용 가능 → 우리는 저장소 클론 + 구조 이해 필요
- 5계층 Hook으로 컨텍스트 자동 주입 → 우리는 MA가 수동으로 주입 관리
- 241개 유틸리티 함수 내장 → 우리는 스크립트 수가 적음

**우리의 장점 (bkit의 단점)**
- **토큰 비용 통제**: bkit은 PDCA Check-Act 반복(최대 5회)이 사용자 인지 없이 자동 실행되어, 의도와 맞지 않는 방향으로 반복할 경우 불필요한 토큰 소모가 급증. 우리는 REQ 승인 게이트에서 사용자가 방향을 확인한 후에만 실행
- 규칙 모듈 13개가 `docs/rules/`에 투명하게 노출 → bkit은 플러그인 내부 로직이라 수정 어려움
- 에이전트/스킬/규칙을 자유롭게 추가/삭제/수정 → bkit은 플러그인 설정 범위 내에서만 변경
- 2-Set Deliverables로 감사 추적(user/agent 분리) → bkit은 상태 파일 기반 (`.bkit/`)
- 다중 도메인 프로젝트 운용 (workspace.json 라우팅) → bkit은 단일 프로젝트 중심

**선택 기준**
- 빠른 도입, 자동화 우선 → **bkit** (단, 토큰 비용 모니터링 필요)
- 비용 통제, 규칙 직접 제어, 다중 프로젝트 → **이 프레임워크**

### 개선 결과 요약

| 영역 | 이전 | 이후 |
|------|------|------|
| 문서 구조 | 10개 카테고리, 50+파일, ~4,800줄 | `docs/rules/` 13개 모듈, ~800줄 (**60-80% 감소**) |
| 구현 에이전트 | `se` (FE+BE 통합) | `fe` + `be` (shared contract 기반 분리) |
| 리뷰 에이전트 | `cr` + `qa` (중복) | `qa` (리뷰+린트+교차검증 통합) |
| 실행 모드 | subagent 순차만 | subagent + team 모드 선택 |
| 산출물 경로 | `deliverables/user\|agent/` | `deliverables/<PRJ>/<YYYYMMDD>/user\|agent/` |

---

## MA 절차 준수 가이드 (중요)

이 프레임워크의 핵심은 **MA가 정해진 절차(게이트)를 지키는 것**입니다. 하지만 MA가 절차를 생략하고 직접 파일을 수정하거나, 스킬/Subagent를 사용하지 않고 작업을 진행하는 경우가 있습니다.

### MA가 절차를 생략하는 대표적인 상황

| 상황 | 올바른 절차 | MA가 생략하는 행동 |
|------|------------|-------------------|
| 파일 수정 요청 | REQ → 승인 → WI → Subagent 위임 | 직접 파일 수정 |
| 요구사항 정리 | `/create-req` 스킬 사용 | 구두로 요약만 하고 넘어감 |
| Subagent 위임 전 | `/create-wi-handoff-packet` 스킬 사용 | 스킬 없이 직접 Task 호출 |
| 프론트엔드 구현 | `fe` Subagent에 위임 | MA가 직접 코드 작성 |
| 백엔드 구현 | `be` Subagent에 위임 | MA가 직접 코드 작성 |
| 문서 수정 | `docops` Subagent에 위임 | MA가 직접 문서 편집 |

### 절차를 생략할 때 사용자가 할 수 있는 대응

MA가 절차를 생략하려 할 때, 아래 문구를 사용해서 올바른 절차를 요구하세요:

**REQ 없이 실행하려 할 때:**
```
잠깐, REQ 먼저 작성해줘. /create-req 사용해서 정리하고 내 승인 받은 다음에 진행해.
```

**스킬 없이 Subagent를 호출하려 할 때:**
```
WI 핸드오프 패킷 먼저 만들어. /create-wi-handoff-packet 스킬 사용해서.
```

**Subagent 없이 직접 수정하려 할 때:**
```
직접 수정하지 말고 적절한 Subagent에 위임해. CLAUDE.md의 라우팅 매트릭스 따라서.
```

**전체 절차를 리마인드 시킬 때:**
```
CLAUDE.md의 Orchestration Gates 규칙을 다시 확인하고 절차대로 진행해줘.
```

자세한 대응 방법과 예시는 [팀 매뉴얼 - MA 절차 강제](MANUAL.md#3-ma-절차-준수-강제하기)를 참조하세요.

## 아키텍처

```
사용자  -->  MA (Main Agent)  -->  Subagents (병렬 전문화)
                |
           REQ 초안 작성
                |
           사용자 승인
                |
           WI 분할 (모드 판단: subagent / team)
                |
           위임 & 실행
```

**MA**는 유일한 사용자 접점입니다. 의도 파악, 컨텍스트 엔지니어링, Subagent 위임, 최종 보고를 담당합니다. **Subagents**는 격리된 컨텍스트에서 실행되는 전문 작업자입니다. **Skills**는 MA나 Subagent가 호출하는 표준화된 절차 패키지입니다.

### 표준 워크플로우 (7단계)

1. 사용자가 자연어로 요구사항을 말함
2. MA가 `/create-req`로 REQ(요구사항 정의서) 초안 작성 (실행 모드 판단 포함)
3. 사용자가 REQ 승인
4. MA가 WI(작업 항목) 분할:
   - **subagent 모드**: `/create-wi-handoff-packet`으로 개별 WI 생성
   - **team 모드**: `/spawn-impl-team`으로 팀 생성 + WI 자동 배정
5. Subagent들이 WI를 병렬 실행
6. MA가 결과를 수집하고 Evidence Pack 생성
7. MA가 사용자에게 보고, 산출물 아카이브

## 빠른 시작

### 사전 요구사항

- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code) 설치 및 설정 완료
- Git
- Python 3.8+ (워크스페이스 스크립트용)

### 설치

```bash
# 1. 저장소 클론
git clone https://github.com/hiyong7759/claude-agent-team-starter.git
cd claude-agent-team-starter

# 2. (선택) 환경변수 템플릿 복사
cp .env.example .env
# 필요한 토큰이 있으면 .env 편집

# 3. 프로젝트 디렉토리에서 Claude Code 실행
claude
```

끝입니다. Claude Code가 자동으로 `CLAUDE.md`를 읽고 agents/skills를 인식합니다.

### 첫 사용

자연어로 원하는 것을 말하면 됩니다:

```
> 로그인 페이지를 추가하고 싶어
```

MA가 다음을 수행합니다:
1. 승인을 위한 REQ 초안 작성 (실행 모드 자동 판단)
2. 승인 후 WI로 분할
3. 적합한 Subagent에 위임 (sa: 아키텍처, be: 백엔드, fe: 프론트엔드, re: 테스트)
4. 결과를 취합해 보고

## Subagents (11개)

| Agent | 역할 | 모델 | 설명 |
|-------|------|------|------|
| `ps` | Product Strategist | sonnet | REQ 초안 작성, 의도 명확화 |
| `eo` | Ensemble Overseer | sonnet | 라우팅, 거버넌스, 자산 승격 |
| `sa` | Software Architect | opus | 아키텍처 결정, ADR |
| `fe` | Frontend Engineer | sonnet | UI 컴포넌트, 페이지, 클라이언트 로직 |
| `be` | Backend Engineer | sonnet | 타입, 서비스, 목 데이터, 비즈니스 로직 |
| `re` | Reliability Engineer | sonnet | 테스트, 회귀 검증 |
| `pg` | Privacy Guardian | opus | 보안, 권한 검토 |
| `tr` | Technology Researcher | sonnet | 기술 조사, 대안 비교 |
| `uv` | UX/UI Virtuoso | sonnet | UX 디자인, 디자인 시스템 |
| `docops` | Documentation Ops | haiku | 문서 관리, 드리프트 감지 |
| `qa` | Quality Assurance | opus | 자동 검증 + 코드 리뷰 + FE-BE 교차 검증 |

> `fe`/`be`는 공유 계약(shared contract)을 통해 협업합니다. `be`가 `src/types/`, `src/services/`에 타입과 서비스를 정의하면, `fe`가 이를 소비하는 구조입니다.

## Skills (19개)

### 워크플로우 스킬
| 스킬 | 설명 |
|------|------|
| `/create-req` | 사용자 발화를 REQ 초안으로 정규화 (실행 모드 판단 포함) |
| `/create-wi-handoff-packet` | 표준화된 WI 인수인계 패킷 생성 (subagent 모드) |
| `/spawn-impl-team` | fe+be+qa+re 구현 팀 생성 (team 모드) |
| `/create-wi-evidence-pack` | Subagent 출력을 Evidence Pack으로 표준화 |
| `/ce` | Context Engineering - 최소 주입 번들 설계 |
| `/pe` | Prompt Engineering - Subagent 지시 강화 |

### 품질 스킬
| 스킬 | 설명 |
|------|------|
| `/lint` | 코드/문서 품질 검증 (Markdown, JSON, Python) |
| `/typecheck` | 타입 체크 (TypeScript tsc, Python mypy) |
| `/eslint` | ESLint 코드 린팅 |
| `/prettier` | 코드 포맷팅 검증 |
| `/test` | 테스트 실행 |
| `/test-coverage` | 테스트 커버리지 분석 |
| `/build-check` | 빌드 검증 |
| `/validate-docs` | 문서 무결성 검증 |

### 관리 스킬
| 스킬 | 설명 |
|------|------|
| `/create-agent` | 표준화된 Subagent 정의 생성 |
| `/skill-creator` | Skill 생성 가이드 |
| `/manage-hooks` | Git 훅 관리 |
| `/sync-docs-index` | 문서 인덱스 동기화 |
| `/react-best-practices` | React/Next.js 성능 최적화 가이드라인 |

## 디렉토리 구조

```
claude-agentic-subagent-team/
├── CLAUDE.md                     # 메인 오케스트레이션 규칙 (Claude Code가 읽음)
├── README.md                     # 이 파일
├── MANUAL.md                     # 상세 사용 매뉴얼
├── setup_workspace.py            # 워크스페이스 설정 스크립트
│
├── .claude/
│   ├── agents/                   # 11개 Subagent 정의 (fe/be 분리, qa=cr 흡수)
│   ├── skills/                   # 19개 재사용 Skill
│   ├── config/
│   │   ├── workspace.json        # 프로젝트 레지스트리 & 라우팅
│   │   ├── context-injection-rules.json  # 문서 주입 엔진
│   │   ├── module-injection-matrix.json  # 에이전트별 모듈 매핑
│   │   └── team-definitions.json         # 팀 구성 정의
│   ├── scripts/                  # 유틸리티 스크립트
│   └── hooks/                    # Git/Agent 훅
│
├── docs/                         # 시스템 문서 (정적)
│   ├── rules/                    # 13개 규칙 모듈 (Tier 0 + agent-specific)
│   ├── templates/                # 문서/산출물 템플릿
│   ├── registry/                 # 자산/컨텍스트 레지스트리
│   ├── adr/                      # 아키텍처 결정 기록
│   └── index.md                  # 문서 진입점
│
├── deliverables/                 # 작업 산출물 (동적, 공유 시 제외)
│   └── <PRJ>/<YYYYMMDD>/        # 프로젝트+날짜별 계층 구조
│       ├── user/                 # REQ-*.md, WI-*-summary.md
│       └── agent/                # WI-*-handoff.md, WI-*-evidence-pack.md
│
└── projects/                     # 도메인 프로젝트 (gitignored)
    └── <your-project>/           # 여기에 도메인 프로젝트 추가
```

## 도메인 프로젝트 추가하기

이 프레임워크는 메타 프레임워크와 함께 여러 도메인 프로젝트를 지원합니다:

1. `.claude/config/workspace.json`에 프로젝트 등록
2. `projects/` 아래에 프로젝트 디렉토리 생성
3. `projects/<name>/.claude/`에 프로젝트 전용 agents/skills 추가
4. 자동 컨텍스트 전환을 위한 라우팅 트리거 설정

자세한 내용은 [팀 매뉴얼](MANUAL.md)을 참조하세요.

## 커스터마이징

### 새 Subagent 추가

```bash
# 내장 스킬 사용
> /create-agent
```

### 새 Skill 추가

```bash
# 내장 스킬 사용
> /skill-creator
```

### 오케스트레이션 규칙 수정

`CLAUDE.md`를 편집해서 조정할 수 있습니다:
- 라우팅 매트릭스 (어떤 Subagent가 어떤 작업을 담당하는지)
- 승인 게이트 (어떤 작업에 사용자 확인이 필요한지)
- 컨텍스트 주입 규칙 (각 Subagent가 받는 문서)
- 실행 모드 (subagent vs team 모드 선택 기준)

## 문서

- **[문서 인덱스](docs/index.md)** - 전체 문서 맵
- **[팀 매뉴얼](MANUAL.md)** - 상세 설정 및 사용 가이드
- **[워크플로우 규칙](docs/rules/workflow-rules.md)** - 표준 7단계 워크플로우
- **[핵심 규칙](docs/rules/hard-rules.md)** - 시스템 헌법 (Tier 0)
- **[출력 계약](docs/rules/output-contracts.md)** - 에이전트 출력 표준

## 핵심 개념

| 개념 | 설명 |
|------|------|
| **MA** | Main Agent - 오케스트레이터이자 유일한 사용자 접점 |
| **REQ** | Requirements Definition - 실행 전 확정된 요구사항 범위 |
| **WI** | Work Item - 담당자, 입력, 출력, 완료 조건이 있는 실행 단위 |
| **Tier 0** | 항상 로드되는 규칙 모듈 (hard-rules + output-contracts) |
| **Evidence Pack** | 재현 단계가 포함된 표준화된 Subagent 출력 |
| **2-Set Deliverables** | 사용자용(요약) + 에이전트용(감사 추적) |
| **fe/be** | Frontend/Backend 분리 에이전트 (구 se를 대체) |
| **impl-team** | 실험적 팀 모드 (be → fe → qa → re 자율 협업) |
