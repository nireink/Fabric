# AI Collaboration

**Organization:** ISAGRUB CORPORACIÓN C.L. — GYPPORT®

**Classification:** AI Governance — Shared

**Status:** ALIGNED WITH APPROVED CANONICAL STANDARD

**Effective date:** 2026-07-30

**Owner and final authority:** Eduardo Luis Burgasi Pullaguari

## Purpose

This document is the permanent, concise entry point for collaboration among
the AI participants used by GYPPORT®. It defines their authority, mandatory
order, boundaries, and handoffs.

The detailed and controlling operating procedure is:

`Fabric/Knowledge/00-GYPPORT-UNIVERSE/ai-collaboration/GYPPORT_AI_COLLABORATION_EXECUTION_ORDER_v1.0.md`

If this summary and the canonical operating procedure ever differ, the
approved canonical operating procedure prevails.

## Permanent Rules

1. Eduardo initiates the activity by deciding that a topic will be addressed
   and defining its objective or business need.

2. Eduardo has final authority over architecture, governance, security,
   canonical data, product scope, base technology, ownership boundaries, the
   exact implementation scope, and protected Git operations.

3. ChatGPT develops the initial proposal, receives the architectural critique,
   and produces a revised proposal. It must not present assumptions as verified
   repository evidence or approve decisions reserved to Eduardo.

4. Claude Chat performs the conceptual and architectural critique, then
   produces the provisional decision. It may define the proposed model, target
   file structure, contracts, pseudocode, or suggested content that Codex would
   later implement, but it must not modify the repository or replace
   independent technical verification.

5. ChatGPT Work coordinates the operational workflow, crosses the preceding
   interventions, and prepares the `TECHNICAL_VERIFICATION_HANDOFF`. It
   translates the provisional decision into a precise, verifiable scope
   without introducing unreviewed architecture.

6. Claude Code independently verifies the proposed model and scope against the
   real repository before implementation. This intervention is read-only and
   must identify the exact files, dependencies, conflicts, tests, and
   technically implementable boundary.

7. Eduardo approves the exact implementation scope once, after the
   pre-implementation verification. That approval remains valid for the same
   unchanged scope and must not be requested repeatedly.

8. Codex confirms the authorized repository state, implements only the scope
   approved by Eduardo, runs the required tests, and documents evidence. Codex
   must not redesign the approved solution or approve its own implementation.

9. Claude Code independently audits the implementation against the approved
   scope, real files, Git diff, and reproducible tests. This
   post-implementation intervention is read-only.

10. Claude Chat performs the architectural and functional closure using the
    approved proposal and the independent implementation audit.

11. ChatGPT Work crosses all final evidence and issues the closure
    recommendation. It must distinguish implementation, audit, architectural
    closure, owner approval, commit, and push.

12. Only Eduardo may authorize staging, commit, or push. Approval of the
    implementation scope does not by itself authorize any of these protected
    Git operations.

13. No AI may expand an approved boundary, modify protected files, or move work
    into another track without explicit authorization.

14. No autonomous negotiation between AIs is permitted. Each intervention must
    produce a self-contained result that Eduardo can review and transfer to the
    next participant.

15. One active track does not authorize changes in another track.

16. Toolchain and Platform OS evolve independently unless their integration is
    explicitly authorized.

17. Approved canonical documentation governs intent and authority. The current
    filesystem, code, configuration, Git state, executable contracts, and
    reproduced tests establish the actual technical state.

18. AI chat history is supporting context, not canonical governance and not
    proof of repository state.

## Mandatory Execution Order

Before intervention 1, Eduardo declares that the topic will be addressed. This
initiates the activity but does not authorize repository modification.

### Phase 1 — Conceptual Exchange

1. **ChatGPT — `INITIAL_PROPOSAL`**

   Organizes the available corpus, synthesizes the problem, and proposes the
   initial model.

2. **Claude Chat — `ARCHITECTURAL_CRITIQUE`**

   Critically reviews the initial proposal, challenges its assumptions, and
   identifies architectural, functional, security, data, and maintainability
   risks.

3. **ChatGPT — `REVISED_PROPOSAL`**

   Crosses the critique with the original corpus and produces a corrected,
   more precise proposal.

4. **Claude Chat — `PROVISIONAL_DECISION`**

   Performs the second conceptual review and consolidates the provisional
   architectural decision. When required, it defines the proposed file model,
   contracts, pseudocode, or suggested content for later implementation by
   Codex. It does not write to the repository.

### Phase 2 — Verifiable Technical Scope

5. **ChatGPT Work — `TECHNICAL_VERIFICATION_HANDOFF`**

   Crosses the four conceptual interventions and converts the provisional
   decision into a concrete read-only verification assignment for Claude Code.

6. **Claude Code — Independent pre-implementation verification**

   Verifies the proposal against the real repository, files, dependencies,
   contracts, tests, Git state, and protected boundaries.

Claude Code must issue one of these verdicts:

- `READY_FOR_OWNER_SCOPE_APPROVAL`
- `READY_WITH_FINDINGS`
- `BLOCKED`
- `RETURN_TO_DECISION`

`READY_WITH_FINDINGS` may progress only when the findings are expressly
included in the exact scope presented to Eduardo.

### Phase 3 — Single Owner Gate

7. **Eduardo — One-time approval of the exact implementation scope**

Eduardo approves or rejects the exact scope that Codex may implement. Once
approved, the same unchanged scope must not be submitted for approval again.

If later evidence requires changing files, behavior, contracts, dependencies,
or boundaries outside that approved scope, the expansion must return to the
appropriate earlier intervention and be presented as a new or revised scope.

This gate authorizes implementation only. It does not authorize staging,
commit, or push.

### Phase 4 — Implementation

8. **Codex — Implementation and tests within the approved scope**

Codex implements the files approved by Eduardo, executes the applicable tests,
records the real diff and evidence, and stops without staging, commit, or push
unless Eduardo has separately authorized those Git operations.

Codex must issue one of these results:

- `IMPLEMENTED_READY_FOR_AUDIT`
- `PARTIALLY_BLOCKED`
- `NOT_IMPLEMENTED`

### Phase 5 — Independent Post-Implementation Audit

9. **Claude Code — Independent read-only audit**

Claude Code verifies the real implementation against:

- the scope approved by Eduardo;
- the files and contracts actually modified;
- the Git diff;
- the required tests and reproducible evidence;
- the architectural and security boundaries.

Claude Code must issue one of these verdicts:

- `ACCEPTED`
- `ACCEPTED_WITH_FINDINGS`
- `REJECTED`

### Phase 6 — Architectural and Operational Closure

10. **Claude Chat — Architectural and functional closure**

Claude Chat determines whether the accepted implementation satisfies the
provisional decision and the intended product outcome.

11. **ChatGPT Work — Final evidence cross-check and closure recommendation**

ChatGPT Work crosses:

- the initial and revised proposals;
- both Claude Chat conceptual interventions;
- the technical verification;
- Eduardo's exact approval;
- the Codex implementation report;
- the Claude Code post-implementation audit;
- the Claude Chat architectural and functional closure;
- the actual Git state reported in the evidence.

ChatGPT Work then recommends one of:

- `READY_FOR_OWNER_CLOSURE_DECISION`
- `READY_WITH_FINDINGS`
- `RETURN_FOR_CORRECTION`
- `BLOCKED`

ChatGPT Work does not authorize staging, commit, or push.

## Protected Git Operations

Staging, commit, and push are separate protected operations.

- Approval of the implementation scope authorizes Codex to implement only.
- Acceptance by Claude Code confirms the audit result only.
- Architectural closure by Claude Chat confirms architectural and functional
  alignment only.
- A closure recommendation by ChatGPT Work is not a Git authorization.
- Only Eduardo may authorize staging, commit, or push, and the authorization
  must state which operation or operations are permitted.

## Abbreviated Route

Work may begin at intervention 5 only when an approved ADR, authorized STEP,
current executable contract, or unequivocal written owner decision already
contains the complete conceptual decision that interventions 1 through 4 would
otherwise produce.

The abbreviated route does not permit omission of:

1. ChatGPT Work's `TECHNICAL_VERIFICATION_HANDOFF`.
2. Claude Code's pre-implementation read-only verification.
3. Eduardo's one-time approval of the exact implementation scope.
4. Codex implementation and validation.
5. Claude Code's independent post-implementation audit.
6. Claude Chat's architectural and functional closure.
7. ChatGPT Work's final evidence cross-check and closure recommendation.

An existing approval remains valid only for its exact unchanged scope. The
abbreviated route must not create a duplicate approval gate.

## Mandatory Stop Conditions

The workflow must stop when:

- The repository, branch, or `HEAD` differs materially from the verified
  handoff.
- Local changes collide with the proposed or approved scope.
- The implementation boundary or protected files are unclear.
- The one-time owner approval for the exact scope is missing.
- Claude Code returns `BLOCKED`, `RETURN_TO_DECISION`, or `REJECTED`.
- Implementation would require expanding the active track.
- Evidence cannot be reproduced.
- Codex discovers that the approved scope cannot be implemented without
  changing unapproved files, contracts, dependencies, or behavior.

A stop does not cancel an approval already granted for the unaffected portion
of the exact scope. Any expansion or materially changed scope requires a new
decision; the original unchanged scope must not be approved again.

## Canonical Record

`AIs_Dialog_v2.md` is a chronological collaboration log. It may summarize and
link each intervention, but it must not replace the canonical procedure or
duplicate complete technical reports. Since 2026-09-15 it lives in the operational
memory, at `Fabric/gm-ai-boxghost/imports/GYPPORT-CANONICAL-MEMORY-FOUNDATION-01/gypport-storage/IAs Agents/GYPPORT Lineamientos Desarrollo ERP/AIs_Dialog_v2.md`,
and a new dialog log belongs in `Fabric/gm-ai-boxghost/tracks/<TRACK-ID>/dialog/`.

New work must not use earlier six- or eight-iteration models. Those models are
retained only as `HISTORICAL_WORKFLOW`.
