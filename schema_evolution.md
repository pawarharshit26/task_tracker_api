# Pragya API — Schema Evolution Discussion (Living Notes)

## Context
User paused project after backend models were defined. Built React prototype (`tmp/Journel (3)/`) showing intended UX. Now walking through gaps between prototype and current backend schema, locking decisions one at a time. **Not implementing yet — discussion phase.**

Reference docs:
- `pragya_api/CLAUDE.md` — current architecture
- `pragya_api/ChatGPT-Portfolio website development.md` — original design philosophy
- `pragya_api/tmp/Journel (3)/` — React prototype (HTML + JSX, demo data only)

## Locked Decisions

### 1. Minimum Viable Effort (MVE)
Add `mve_minutes: Mapped[int | None]` to `DailyCommitment`.
- Service computes default at write time: `max(5, round(expected_minutes / 3))`
- Stored as concrete value in DB, not nullable-with-COALESCE
- User can override
- No retroactive recompute (MVE is a promise frozen on that day)
- Rationale: psychological floor for discipline; "showed up = success" semantics

### 2. Track cadence + paused
Add to `Track`:
- `cadence_per_week: Mapped[int | None]` (null = no target; daily = 7)
- `is_paused: Mapped[bool]` default False
- `paused_at: Mapped[datetime | None]`
Rationale: Cadence is intent at Track level (mirrors DailyCommitment intent at day level). Paused tracks excluded from suggestions/cadence checks but retained.

### 3. Phase status — hybrid (dates + lifecycle enum)
Add to `Phase`:
- `lifecycle: Mapped[PhaseLifecycle]` default `DRAFT` — values: `DRAFT, ACTIVE, PAUSED, COMPLETE, ABANDONED`
- `outcome: Mapped[str | None]` — "what success looks like" text
- Keep `start_date` / `end_date` as schedule
Constraint: partial unique index — only 1 phase per goal where `lifecycle = ACTIVE`.
Display status = combine lifecycle + dates (e.g. lifecycle=ACTIVE & today > end_date → "overdue active").
Rationale: dates express schedule, lifecycle expresses user intent. Captures abandoned ≠ complete ≠ paused.

### 4. Theme visuals — preset_key
Add to `Theme`:
- `preset_key: Mapped[str]` — opaque string (e.g. "career", "art", "health")
Frontend owns `THEME_PRESETS` map → resolves preset_key to glyph + color (theme-aware for dark/light).
DB stays semantic, not presentational. Cheap migration to full custom (glyph + color_hex columns) later if needed.

### 5. Block migration — hybrid by entity
Per-entity rules:
| Entity | Block usage |
|---|---|
| Vision | None — plain `title` + `description` text |
| Theme | None |
| Track | None |
| Goal | Blocks for `why` / long notes. Keep `title` + `horizon: str \| None` plain. Drop `description` text → blocks. |
| Phase | Blocks for scope/notes. Keep `title` + `outcome: str \| None` plain. |
| DailyCommitment | None — plain `intent: str(255)` (discipline guardrail; concise) |
| ExecutionLog | Hybrid — plain `actual_minutes`, `energy_level (1-5)`, `note: str \| None` (short factual) + blocks for rich reflection |

Schema deltas:
- `ExecutionLog`: ADD `actual_minutes`, `energy_level`, `note`. DROP `actual_output`, `reflection` (replaced by note + blocks).
- `Goal`: DROP `description` (move to blocks). ADD `horizon: str | None`.
- `Phase`: ADD `outcome: str | None`.
- `Block` model already exists (polymorphic `owner_type` + `owner_id`). Block service started in prior session — needs finishing + migration row.

Frontend: TipTap recommended for block editor (per design doc).

### 6. Reflection cadence — both levels (DailyReflection + ExecutionLog)
New entity:
```python
class Mood(enum.Enum):
    VERY_LOW, LOW, NEUTRAL, HIGH, VERY_HIGH

class DailyReflection(Base):
    id: uuid.UUID
    user_id: FK -> user.id
    date: Date
    mood: Mood | None
    __table_args__ = (UniqueConstraint("user_id", "date"),)
```
- Day-level reflection is primary surface (matches prototype + design doc Level 7).
- Mood lives here, not per-commitment.
- Blocks attached via `owner_type="daily_reflection"`.
- ExecutionLog keeps short `note` for per-commitment factual; ExecutionLog blocks remain *available* (deep dive) but not *required*.
- WeeklyReflection later aggregates DailyReflections cleanly.

## Final Schema Deltas Summary

**New entity:** `DailyReflection`

**Modified entities:**
- `DailyCommitment`: + `mve_minutes: int | None`
- `Track`: + `cadence_per_week: int | None`, + `is_paused: bool`, + `paused_at: datetime | None`
- `Phase`: + `lifecycle: PhaseLifecycle enum`, + `outcome: str | None` (partial unique index on `(goal_id) where lifecycle=ACTIVE`)
- `Theme`: + `preset_key: str`
- `Goal`: + `horizon: str | None`, − `description` (→ blocks)
- `ExecutionLog`: + `actual_minutes: int | None`, + `energy_level: int | None`, + `note: str | None`, − `actual_output`, − `reflection` (→ blocks)

**Block ownership extends to:** `goal`, `phase`, `execution_log`, `daily_reflection`.

## Out of Scope (Discussion Only)
User explicitly stated: not implementing now, just discussing. No code, migrations, or services to be generated from this doc. This file is a decisions ledger for when implementation resumes.

## Status — Schema Applied (2026-04-30)

Models edited and a single fresh **initial** Alembic migration generated and applied. Prior two migrations
(`166799f70db9_initial`, `746c29dbfce6_created_schema_vision_tracker`) were deleted; the DB was
nuked (`DROP SCHEMA public CASCADE`) and rebuilt from one autogen run so migration history matches
current model state with zero historical churn.

- Migration: `app/migrations/versions/ae1fac635ff8_initial.py` (down_revision = `None`)
- Postgres types created: `phase_lifecycle`, `mood`
- Tables: `user`, `auth_token`, `vision`, `theme`, `track`, `goal`, `phase`, `daily_commitment`,
  `execution_log`, `daily_reflection`, `block`
- Partial unique index: `ix_phase_one_active_per_goal` on
  `phase(goal_id) WHERE lifecycle = 'ACTIVE'::phase_lifecycle`
- Check constraint: `ck_execution_log_energy_level_range` (`energy_level` NULL or 1–5)
- Unique constraint: `uq_daily_reflection_user_date` on `daily_reflection(user_id, date)`
- `block` polymorphic owner_type Literal: `goal | phase | execution_log | daily_reflection`

Implementation notes:
- `DailyCommitment.expected_minutes` added (implicit prerequisite for MVE formula
  `max(5, round(expected_minutes / 3))`).
- Enum columns sit inside `create_table(...)`, so SQLAlchemy auto-issues `CREATE TYPE` —
  no need to pre-create types via `Enum.create()`. (That manual pre-create was only needed earlier
  when `add_column` was used on an existing table; gone in this single-migration approach.)
- `CheckConstraint` is captured by autogen because it's part of a fresh `create_table`. Alembic's
  known limitation only applies to detecting check constraints added to *existing* tables.
- Migration is replay-safe: `alembic downgrade base && alembic upgrade head` reproduces full state.

Next: build services + APIs per `CLAUDE.md` "Adding a New Feature" pattern.
