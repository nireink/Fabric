# CODEX-DASHBOARD-01

## GYPPORT® PLATFORM OS

Track: Dashboard Engine
Step: DASHBOARD-01 — Dashboard Composition Foundation Audit
Mode: Read Only
Agent: Codex
Status: Ready for Execution

---

# FOUNDATION

This STEP belongs exclusively to the Dashboard Engine track.

Repository Recovery is CLOSED.

Foundation v3 is the governing authority.

This STEP SHALL NOT modify production code.

This STEP SHALL NOT reorganize Studio.

This STEP SHALL NOT create new architecture.

This STEP SHALL NOT expand the project scope.

Its purpose is ONLY to audit the current Dashboard Engine composition.

---

# READ FIRST

Read in this exact order:

1. AGENTS.md
2. Reglas.md
3. docs/architecture/PLATFORM_FOUNDATION.md
4. docs/architecture/STRUCTURE_CANONICAL.md
5. docs/architecture/BOUNDARY_RULES.md
6. docs/architecture/ACTIVE_TRACKS.md

These documents are authoritative.

---

# AUTHORIZED BOUNDARY

You may inspect ONLY:

platform_os/studio/engine/core/ui/dashboard/

platform_os/studio/contracts/dashboard/

platform_os/studio/contracts/registry/

platform_os/studio/channel/browser/shell/vitest.config.js

platform_os/studio/channel/browser/shell/package.json

Do NOT inspect:

platform_os/studio/journey/

platform_os/studio/module/

platform_os/studio/server/

developer_platform/

desktop/

mobile/

---

# REQUIRED INVENTORY

Identify every Dashboard Engine component.

At minimum verify:

DashboardBuilder

DashboardSchema

DashboardTypes

DashboardValidator

DashboardRegistry

Dashboard Contracts

Registry Contracts

Contract Harness

Vitest Configuration

For every component report:

- File
- Owner
- Responsibility
- Current Status
- Dependencies
- Consumers
- Validation Status

---

# FOUNDATION COMPLIANCE

Determine whether the current Dashboard Engine satisfies:

- Single ownership
- Single responsibility
- Boundary isolation
- Contract ownership
- Registry ownership
- Dashboard ownership
- Foundation v3

Report every violation if one exists.

Do NOT propose implementation.

---

# VALIDATION

Verify:

- Dashboard contracts
- Registry contracts
- Contract Harness
- Vitest configuration

Do NOT create new tests.

Do NOT modify contracts.

Do NOT execute fixes.

---

# REQUIRED OUTPUT

Return exactly:

1. Repository root

2. Branch

3. Dashboard Engine tree

4. Dashboard component inventory

5. Ownership table

6. Dependency graph

7. Validation summary

8. Foundation v3 compliance

9. Missing architectural pieces

10. Recommended execution order

11. Recommended next STEP

---

# STRICT PROHIBITIONS

Do NOT:

- modify code
- create files
- rename files
- stage
- commit
- push

Do NOT leave the Dashboard Engine boundary.

Stop after the report.