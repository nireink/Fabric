# gm-expenses — Knowledge Index

```text
MODULE=gm-expenses
GM_EXPENSES_MVP_STATUS=FROZEN_OWNER_ACCEPTED_PUSHED
CURRENT_AUTHORITY=GYPPORT-GM-EXPENSES-MVP-FROZEN-OWNER-ACCEPTED-2026-09-17
FROZEN_SOURCE=gm-expenses 39a2adf4dfff0196208a1f80719be1c12c047ac2 (master), Gystigo 5eed5d692342cc889f2afff7a6c4f7f6b5cca1dc (master)
SHARED_DEV=Flyway V65
MVP_CHANGES=only through a new explicit Owner track
```

This README is an index. It specifies nothing itself: every rule it points to lives in the document named, and
where an older document differs from the frozen baseline, the frozen baseline governs.

## Current authority

1. [Frozen MVP baseline](../00-GYPPORT-UNIVERSE/verification-baselines/GYPPORT_GM_EXPENSES_MVP_FROZEN_OWNER_ACCEPTED_2026-09-17.md)
   — the accepted source heads, numbering model, financial semantics, invariants and verification evidence.
2. [Domain baseline](01-domain/GYPPORT_GM_EXPENSES_DOMAIN_BASELINE_v1.0.md) and
   [Persistence baseline](02-persistence/GYPPORT_GM_EXPENSES_PERSISTENCE_BASELINE_v1.0.md) — born in the initial
   development and maintained through the MVP track; their latest sections cover V64 and V65.
3. The gm-expenses entries of [`Reglas.md`](../00-GYPPORT-UNIVERSE/Reglas.md), including the MVP freeze of 2026-09-17.

## Historical design documents (initial development)

Owner-accepted outputs of `GM-EXPENSES-INITIAL-DEVELOPMENT-01` / `WP_00_CANONICAL_DESIGN_BASELINE_PUBLICATION`
(2026-08-26 to 2026-08-28). Each carries the `HISTORICAL INITIAL-DEVELOPMENT BASELINE` banner and describes the design
stage, not the frozen MVP.

- [03-application](03-application/GYPPORT_GM_EXPENSES_APPLICATION_ARCHITECTURE_BASELINE_v1.0.md) — package model,
  transaction model, idempotency, commands
- [04-integration](04-integration/GYPPORT_GM_EXPENSES_CROSS_REPOSITORY_INTEGRATION_BASELINE_v1.0.md) — security and
  tenant context, Host and sibling-module integration state as of 2026-08-26
- [05-implementation](05-implementation/GYPPORT_GM_EXPENSES_IMPLEMENTATION_CONSTRAINTS_v1.0.md) — the rules given to
  implementation agents in the initial development

## Operational evidence

- [BoxGhost track `GM-EXPENSES-RELEASE-READINESS`](../../gm-ai-boxghost/tracks/GM-EXPENSES-RELEASE-READINESS/) — the
  record and evidence of every release STEP
- [Stored Owner prompts](../00-GYPPORT-UNIVERSE/steps/GM-EXPENSES-RELEASE-READINESS/)

## Where the module lives

| Concern | Location |
|---|---|
| Domain, Application and Infrastructure Java | `Modules/gm-expenses` (master) |
| Flyway migrations | `Gystigo/database/modules/gm-expenses/migration` (V11, V12, V15–V20, V23–V25, V33–V35, V62–V65) |
| Host API and Studio | `Gystigo` (master) |
| This index | `Fabric/Knowledge/gm-expenses` |

## Original purpose (WP_00 publication, 2026-08-26)

This folder is the canonical, Owner-approved design input for the `gm-expenses`
module. It exists so that any future implementation work package — for any
agent, human or AI — can proceed **without depending on chat history** with
ChatGPT (architectural conductor), Codex (implementation agent), or Claude
Code (independent read-only auditor).

```text
CHAT_HISTORY_IS_NOT_IMPLEMENTATION_SOURCE_OF_TRUTH=YES
THESE_DOCUMENTS_ARE_CANONICAL_DESIGN_BASELINE=YES
```

Everything in these five documents reflects the **final** state of Phases
A–D after reconciliation. Discarded intermediate alternatives, superseded
naming, and rejected proposals are deliberately not reproduced here — only
outcomes. Where a rejected alternative is mentioned at all, it is only to
state the final rule unambiguously (e.g. "VENCIDO is not a lifecycle state"),
never as a record of the debate that led there.

This publication is documentation-only. No Java, no `pom.xml`, no SQL
migration, and no change to the `gm-expenses` or `Gystigo` repositories was
made or authorized as part of producing it.

## Provenance of the original publication

Produced through independent cross-repository, read-only inspection of
`gm-expenses`, `gm-entities`, `gm-organizations`, `gm-fleet`, `Gystigo`, the
`gypport-engineering-template`, and `Fabric/Knowledge`, reconciled against
Owner decisions. No repository state was assumed without direct verification.
