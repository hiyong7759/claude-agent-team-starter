---
module: naming-rules
tier: 1
inject: conditional
target_agents: [se, cr, uv]
---

# Cross-Language Naming Rules

Universal naming conventions enforced across all languages and layers.

---

## NM-1: Naming Convention Table

| Context | Convention | Examples |
|---------|-----------|----------|
| **Python** -- variables, functions, files | `snake_case` | `process_data`, `trip_id`, `user_profile.py` |
| **TypeScript** -- variables, functions, interfaces, internal types | `camelCase` / `PascalCase` | `tripId`, `UserProfile`, `NliRequestContext` |
| **API Request/Response JSON** -- all field names | **`snake_case`** | `start_date`, `screen_id`, `travel_style` |
| **NestJS DTO** -- class field names (API boundary) | **`snake_case`** | `start_date!: string`, `trip_id?: string` |
| **Database columns** (PostgreSQL) | `snake_case` | `created_at`, `owner_id`, `destination_city` |
| **URL path parameters** | `camelCase` | `/trips/:tripId/itinerary/:dayIndex` |
| **URL path segments** | `kebab-case` | `/packing-list`, `/duty-free`, `/quick-phrases` |
| **DTO class names** | `PascalCase` | `CreateTripDto`, `UpdateProfileDto` |
| **TypeScript enum values** | `UPPER_SNAKE_CASE` | `TRIP_CREATE`, `PACKING_ADD` |

Violation = CR MAJOR. All naming must follow this table.

## NM-2: API Boundary Conversion Rule

The API layer uses `snake_case` exclusively. Internal TypeScript uses `camelCase`. Conversion happens at DTO (server) and API call site (mobile). See `ts-impl-rules.md` TS-2 for code examples.

## NM-3: Rationale

- **API `snake_case`**: REST API industry standard, consistent with PostgreSQL column names, language-agnostic.
- **TypeScript internal `camelCase`**: Language convention, enforced by ESLint/Prettier.
- **Boundary conversion**: Keeps each layer idiomatic while maintaining a clear contract.

## NM-4: Enforcement

- `cr` agent checks naming violations during code review. Any violation is classified as MAJOR.
- `se` agent must apply these conventions during implementation without exception.
- `uv` agent must follow these conventions in design system component naming and prop definitions.
