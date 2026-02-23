---
module: ts-impl-rules
tier: 1
inject: conditional
target_agents: [se, cr]
condition: typescript
---

# TypeScript Implementation Rules

Rules for TypeScript implementation in NestJS (server) and Expo/React Native (mobile) projects.

---

## TS-1: Naming Conventions

| Context | Convention | Examples |
|---------|-----------|----------|
| Variables, functions | `camelCase` | `tripId`, `getUserProfile` |
| Interfaces, types, DTO classes | `PascalCase` | `UserProfile`, `CreateTripDto` |
| DTO fields (API boundary) | `snake_case` | `start_date!: string` |
| Enum values | `UPPER_SNAKE_CASE` | `TRIP_CREATE`, `PACKING_ADD` |
| URL path parameters | `camelCase` | `/trips/:tripId/itinerary/:dayIndex` |
| URL path segments | `kebab-case` | `/packing-list`, `/duty-free` |

Violation = CR MAJOR.

## TS-2: API Boundary Rule (Critical)

The API layer (request body, response body, query parameters) uses `snake_case` exclusively. Internal TypeScript code uses `camelCase`.

Conversion happens at:
- **Server (NestJS):** DTO fields are `snake_case`. Controllers convert to internal `camelCase` types when passing to services.
- **Mobile (React Native):** Internal state uses `camelCase`. API call sites convert to `snake_case` before sending.

### Server DTO Example

```typescript
// DTO (API boundary) -- snake_case
export class CreateTripDto {
  @IsDateString()
  start_date!: string;       // snake_case in DTO

  @IsDateString()
  end_date!: string;
}

// Controller -- converts to internal type
const trip: CreateTripInput = {
  startDate: dto.start_date,  // camelCase internally
  endDate: dto.end_date,
};
```

### Mobile API Call Example

```typescript
// Internal interface -- camelCase
interface CreateTripInput {
  startDate: string;
  endDate: string;
}

// API call -- convert to snake_case
await api.post('/trips', {
  start_date: input.startDate,
  end_date: input.endDate,
});
```

## TS-3: Architecture Patterns

- **MA single touchpoint:** Both users and workers exchange final agreements only through MA.
- **Context isolation first:** Output explosions (exploration, logs, bulk summaries) are isolated to Subagents.
- **Dual outputs:** All task outputs are managed as 2 sets: User-facing and Agent-facing.

## TS-4: Design System Reuse

- SE prioritizes reuse of existing design system components. Creating new UI elements without checking the design system is prohibited.
- When SE needs UI elements not in the design system, immediately request from UV. Do not create temporary patches.

## TS-5: Testing Patterns

- Co-locate test files: `helpers.ts` alongside `helpers.test.ts`.
- Use `*.test.ts` or `*.spec.ts` naming convention.
- Follow Arrange/Act/Assert structure in all tests.
- Coverage thresholds: 80% lines, 70% branches, 80% functions.

## TS-6: TDD Cycle

1. **Red:** Write a failing test first (define expected behavior before implementation).
2. **Green:** Write minimal code to pass the test.
3. **Refactor:** Improve code quality while keeping tests green.

## TS-7: Security

- No hardcoded secrets in TypeScript source.
- Use environment variables via NestJS ConfigService (server) or Expo constants (mobile).
- 100% test coverage required for security-sensitive code (auth, authorization, data sanitization).
