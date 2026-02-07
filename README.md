# Claude Agentic Subagent Team

[Claude Code](https://docs.anthropic.com/en/docs/claude-code)에 최적화된 **에이전트 오케스트레이션 프레임워크**입니다. **MA (Main Agent) + Subagents + Skills** 아키텍처를 통해 1인 개발에서도 속도, 일관성, 재사용성을 확보합니다.

## 이 프레임워크를 왜 쓰나요?

Claude Code를 사용하는 개발자가 반복적으로 겪는 문제들:
- **컨텍스트 폭발**: 탐색 로그와 대량 출력이 메인 대화를 오염시킴
- **일관성 부재**: 세션마다 품질과 스타일이 달라짐
- **반복 작업**: REQ 작성, 코드 리뷰, 테스트 같은 절차를 매번 새로 수행

이 프레임워크의 해결 방식:
- **11개 전문 Subagent**가 격리된 컨텍스트에서 작업 수행
- **18개 재사용 Skill**이 반복 절차를 표준화
- **Tier 0 헌법 문서**가 모든 작업의 일관성을 보장
- **2-Set Deliverables**로 사용자용 요약과 에이전트용 감사 추적을 분리

## MA 절차 준수 가이드 (중요)

이 프레임워크의 핵심은 **MA가 정해진 절차(게이트)를 지키는 것**입니다. 하지만 MA가 절차를 생략하고 직접 파일을 수정하거나, 스킬/Subagent를 사용하지 않고 작업을 진행하는 경우가 있습니다.

### MA가 절차를 생략하는 대표적인 상황

| 상황 | 올바른 절차 | MA가 생략하는 행동 |
|------|------------|-------------------|
| 파일 수정 요청 | REQ → 승인 → WI → Subagent 위임 | 직접 파일 수정 |
| 요구사항 정리 | `/create-req` 스킬 사용 | 구두로 요약만 하고 넘어감 |
| Subagent 위임 전 | `/create-wi-handoff-packet` 스킬 사용 | 스킬 없이 직접 Task 호출 |
| 구현 작업 | `se` Subagent에 위임 | MA가 직접 코드 작성 |
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
           WI 분할
                |
           위임 & 실행
```

**MA**는 유일한 사용자 접점입니다. 의도 파악, 컨텍스트 엔지니어링, Subagent 위임, 최종 보고를 담당합니다. **Subagents**는 격리된 컨텍스트에서 실행되는 전문 작업자입니다. **Skills**는 MA나 Subagent가 호출하는 표준화된 절차 패키지입니다.

### 표준 워크플로우 (7단계)

1. 사용자가 자연어로 요구사항을 말함
2. MA가 `/create-req`로 REQ(요구사항 정의서) 초안 작성
3. 사용자가 REQ 승인
4. MA가 `/create-wi-handoff-packet`으로 WI(작업 항목) 분할
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
1. 승인을 위한 REQ 초안 작성
2. 승인 후 WI로 분할
3. 적합한 Subagent에 위임 (sa: 아키텍처, se: 구현, re: 테스트)
4. 결과를 취합해 보고

## Subagents (11개)

| Agent | 역할 | 모델 | 설명 |
|-------|------|------|------|
| `ps` | Product Strategist | sonnet | REQ 초안 작성, 의도 명확화 |
| `eo` | Ensemble Overseer | opus | 라우팅, 거버넌스, 자산 승격 |
| `sa` | Software Architect | opus | 아키텍처 결정, ADR |
| `se` | Software Engineer | opus | 구현, 리팩토링 |
| `re` | Reliability Engineer | sonnet | 테스트, 회귀 검증 |
| `pg` | Privacy Guardian | opus | 보안, 권한 검토 |
| `tr` | Technology Researcher | sonnet | 기술 조사, 대안 비교 |
| `uv` | UX/UI Virtuoso | sonnet | UX 디자인, 디자인 시스템 |
| `docops` | Documentation Ops | sonnet | 문서 관리, 드리프트 감지 |
| `qa` | Quality Assurance | sonnet | 통합 품질 검증 |
| `cr` | Code Reviewer | opus | 코드 리뷰, 베스트 프랙티스 |

## Skills (18개)

### 워크플로우 스킬
| 스킬 | 설명 |
|------|------|
| `/create-req` | 사용자 발화를 REQ 초안으로 정규화 |
| `/create-wi-handoff-packet` | 표준화된 WI 인수인계 패킷 생성 |
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
├── setup_workspace.py            # 워크스페이스 설정 스크립트
├── .env.example                  # 환경변수 템플릿
│
├── .claude/
│   ├── agents/                   # 11개 Subagent 정의
│   ├── skills/                   # 18개 재사용 Skill
│   ├── config/
│   │   ├── workspace.json        # 프로젝트 레지스트리 & 라우팅
│   │   └── context-injection-rules.json  # 문서 주입 엔진
│   ├── scripts/                  # 유틸리티 스크립트
│   └── hooks/                    # Git 훅
│
├── docs/                         # 시스템 문서 (정적)
│   ├── standards/                # Tier 0 헌법 + 표준
│   ├── policies/                 # 운영 정책
│   ├── guides/                   # 워크플로우 & 운영 가이드
│   ├── architecture/             # 시스템 설계
│   ├── design/                   # 에이전트 설계 참조
│   ├── templates/                # 문서/산출물 템플릿
│   ├── registry/                 # 자산/컨텍스트 레지스트리
│   ├── adr/                      # 아키텍처 결정 기록
│   └── index.md                  # 문서 진입점
│
├── deliverables/                 # 작업 산출물 (동적, 공유 시 제외)
│   ├── user/                     # 사용자용: REQ-*.md, WI-*-summary.md
│   └── agent/                    # 에이전트용: WI-*-handoff.md, WI-*-evidence-pack.md
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

## 문서

- **[문서 인덱스](docs/index.md)** - 전체 문서 맵
- **[팀 매뉴얼](MANUAL.md)** - 상세 설정 및 사용 가이드
- **[개발 워크플로우](docs/guides/development-workflow.md)** - 표준 7단계 워크플로우
- **[시스템 설계](docs/architecture/system-design.md)** - 아키텍처 심층 분석
- **[핵심 원칙](docs/standards/core-principles.md)** - 시스템 헌법 (Tier 0)

## 핵심 개념

| 개념 | 설명 |
|------|------|
| **MA** | Main Agent - 오케스트레이터이자 유일한 사용자 접점 |
| **REQ** | Requirements Definition - 실행 전 확정된 요구사항 범위 |
| **WI** | Work Item - 담당자, 입력, 출력, 완료 조건이 있는 실행 단위 |
| **Tier 0** | 항상 로드되는 헌법 문서 |
| **Evidence Pack** | 재현 단계가 포함된 표준화된 Subagent 출력 |
| **2-Set Deliverables** | 사용자용(요약) + 에이전트용(감사 추적) |
