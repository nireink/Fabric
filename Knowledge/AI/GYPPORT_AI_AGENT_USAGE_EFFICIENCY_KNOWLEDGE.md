# GYPPORT AI AGENT USAGE EFFICIENCY KNOWLEDGE

PROJECT=GYPPORT
DOCUMENT_TYPE=CANONICAL_AI_OPERATING_KNOWLEDGE
RULE_ID=GYPPORT_AI_AGENT_USAGE_EFFICIENCY
STATUS=OWNER_APPROVED_BASELINE
SCOPE=CHATGPT_CLAUDE_CODE_CODEX_AND_OTHER_GYPPORT_AGENTS

RECOMMENDED_PATH=
D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT\Fabric\Knowledge\AI\GYPPORT_AI_AGENT_USAGE_EFFICIENCY_KNOWLEDGE.md

---

## 1. PURPOSE

Optimize AI-agent execution cost, context usage, latency, and quota consumption
without reducing architectural rigor, security evidence, or project continuity.

Canonical principle:

```text
EVIDENCE_DENSITY > CONTEXT_VOLUME
TARGETED_VERIFICATION > EXHAUSTIVE_REPETITION
PRESERVE_DECISIONS > PRESERVE_CHAT_TRANSCRIPT
```

Optimization removes redundant execution, not required evidence.

---

## 2. AUTHORITY

This document controls execution efficiency only. It does NOT override Owner
decisions, authorized STEP scope, architecture governance, approved ADRs,
security rules, repository evidence, or canonical domain ownership.

```text
CORRECTNESS_WINS=YES
SECURITY_WINS=YES
OWNER_DECISION_WINS=YES
```

---

## 3. DEFAULT EXECUTION MODE

```text
AUDIT_TARGETED_FIRST=YES
PARALLEL_SUBAGENTS_DEFAULT=0
MAX_PARALLEL_SUBAGENTS=2
DO_NOT_REREAD_UNCHANGED_FILES=YES

TARGETED_TESTS_BEFORE_FULL_SUITE=YES
FULL_SUITE_RUNS_MAX=1

PASSING_TEST_LOGS_SUMMARY_ONLY=YES
INTERMEDIATE_REPORTS=SHORT
FULL_FINDINGS_ONLY_AT_END=YES

DOCKER_REBUILD_AFTER_CODE_STABLE=YES
LIVE_BROWSER_VERIFICATION_RUNS=1

STOP_ON_OWNER_DECISION=YES
NO_SPECULATIVE_IMPLEMENTATION=YES
NO_AUTO_SCOPE_EXPANSION=YES
```

A deviation requires a concrete reason tied to the current STEP.

---

## 4. SESSION STRATEGY

Preferred:

```text
ONE_MAJOR_STEP_PER_SESSION=YES
```

A session may contain phases of the same STEP:

```text
AUDIT
→ DESIGN CHECKPOINT
→ IMPLEMENTATION
→ TARGETED TESTS
→ FINAL VERIFICATION
→ HANDOFF
```

Do not keep unrelated modules or unrelated STEPs in one long session merely to
preserve transcript context.

### Context thresholds

These are operational thresholds, not correctness limits:

```text
CONTEXT_UNDER_150K=NORMAL
CONTEXT_150K_TO_250K=REVIEW_SESSION_SHAPE
CONTEXT_ABOVE_250K=COMPACT_AT_NEXT_NATURAL_BOUNDARY
CONTEXT_ABOVE_500K=AVOID_NEW_SCOPE
```

Do not interrupt a critical atomic action solely to compact context.

### `/compact`

Use `/compact` when the same STEP continues but a major phase is complete.

Good boundaries:

```text
AUDIT_COMPLETE
→ /compact
→ IMPLEMENTATION

IMPLEMENTATION_COMPLETE
→ /compact
→ FINAL_VERIFICATION
```

### New session / `/clear`

Prefer a new session or `/clear` when:

```text
STEP_CHANGES=YES
MODULE_CHANGES=YES
TRACK_CHANGES=YES
CURRENT_GOAL_IS_COMPLETE=YES
```

Before changing session, create a compact canonical handoff.

The next session should recover state from the current STEP/handoff,
AGENTS.md, CLAUDE.md when applicable, CHATGPT.md when applicable,
Fabric/Knowledge, and repository evidence.

Do not use raw transcript length as project memory.

---

## 5. SUBAGENT STRATEGY

```text
PARALLEL_SUBAGENTS_DEFAULT=0
MAX_PARALLEL_SUBAGENTS=2
```

Use subagents only when their work is genuinely independent, bounded, useful,
and unlikely to duplicate the same repository evidence.

Good:

```text
SUBAGENT_A=inspect RBAC resolver
SUBAGENT_B=inspect DB migration history
```

Bad:

```text
4 agents
→ overlapping repository audit
→ overlapping file reads
→ long independent reports
```

If rate limiting or quota pressure appears:

```text
DO_NOT_RETRY_FANOUT=YES
RETURN_TO_SINGLE_AGENT_TARGETED_MODE=YES
```

---

## 6. OUTPUT STRATEGY

Default:

```text
INTERMEDIATE_STATUS=COMPACT
PASSING_LOGS=SUMMARY_ONLY
REPEATED_CONTEXT_EXPLANATION=NO
FULL_REPORT=ONCE_AT_END
```

Intermediate checkpoints should normally contain only:

```text
WHAT_WAS_CHECKED
KEY_FINDING
BLOCKER_IF_ANY
NEXT_ACTION
```

Do not paste entire successful Maven, Docker, browser, SQL, or test logs unless
the evidence is specifically needed. For failures, include the smallest useful
failing excerpt.

---

## 7. SEARCH AND FILE-READ STRATEGY

Preferred sequence:

```text
rg / targeted search
→ inspect matching files
→ inspect direct dependencies
→ expand only when evidence requires it
```

Canonical:

```text
SEARCH_FIRST_READ_SECOND=YES
DO_NOT_REREAD_UNCHANGED_FILES=YES
NO_FULL_REPO_SCAN_BY_DEFAULT=YES
```

---

## 8. IMPLEMENTATION STRATEGY

Preferred:

```text
AUDIT
→ FINDINGS CHECKPOINT
→ IMPLEMENT ONLY CONFIRMED DESIGN
```

Canonical:

```text
NO_SPECULATIVE_IMPLEMENTATION=YES
NO_AUTO_SCOPE_EXPANSION=YES
DO_NOT_REDESIGN_ACCEPTED_BASELINE=YES
```

If the audit reaches a real product, authority, or architecture fork:

```text
STATUS=OWNER_DECISION_REQUIRED
```

Stop before spending quota implementing alternatives.

Examples:

- Tenant-wide OWNER vs Organization-scoped OWNER
- automatic authority transfer
- new cross-module ownership
- new security scope model
- irreversible migration strategy

---

## 9. TEST STRATEGY

Preferred order:

```text
1. COMPILE
2. TARGETED_UNIT_TESTS
3. TARGETED_INTEGRATION_TESTS
4. REAL_DB_ACCEPTANCE_IF_REQUIRED
5. ONE_FINAL_FULL_SUITE
```

```text
FULL_SUITE_RUNS_MAX=1
```

Exception: a final full suite may be rerun after repairing a failure discovered
by that final suite.

Do not repeatedly rerun unchanged green suites.

---

## 10. DATABASE STRATEGY

Preferred:

```text
VERIFY_REAL_SCHEMA
→ VERIFY_LATEST_MIGRATION
→ TARGETED_SQL
→ DISPOSABLE_DB_ACCEPTANCE
```

Do not assume migration version from memory.

For high-risk DB behavior, prefer disposable MySQL acceptance over repeatedly
mutating shared DEV state.

Shared DEV mutations must be explicit, bounded, and reported.

---

## 11. DOCKER AND BROWSER STRATEGY

```text
DOCKER_REBUILD_AFTER_CODE_STABLE=YES
LIVE_BROWSER_VERIFICATION_RUNS=1
```

Do not rebuild containers after every minor source edit.

Use browser verification for final UX/integration confidence, not as the first
debugging tool.

---

## 12. GIT STRATEGY

Preferred:

```text
git status
git diff -- targeted paths
git add exact paths
```

Canonical:

```text
PATH_SPECIFIC_STAGING=YES
PRESERVE_PREEXISTING_WIP=YES
NO_PUSH_WITHOUT_AUTHORIZATION=YES
```

---

## 13. HANDOFF STRATEGY

At the end of a substantial STEP, create a compact handoff containing only
durable state.

Recommended:

```text
TRACK=
STEP=
STATUS=

HEADS=
SCHEMA_VERSION=

OWNER_DECISIONS=
IMPLEMENTED=
NOT_IMPLEMENTED=

TESTS=
KNOWN_RISKS=
PENDING_DECISIONS=

NEXT_EXACT_ACTION=
```

Do not use a full chat transcript as the handoff.

Store reusable cross-project knowledge in `Fabric\Knowledge`.

---

## 14. QUOTA-AWARE EXECUTION MODES

### NORMAL

```text
SUBAGENTS=0
TARGETED_AUDIT=YES
TARGETED_TESTS=YES
FULL_SUITE_FINAL=YES
```

### CONSERVATIVE

Use when the session is becoming large or recent usage is high.

```text
SUBAGENTS=0
NO_BROAD_AUDIT=YES
INTERMEDIATE_OUTPUT=MINIMAL
NO_REPEATED_FULL_TESTS=YES
COMPACT_AT_PHASE_BOUNDARY=YES
```

### CRITICAL

Use when limits are close and the current work is not atomic.

```text
STOP_NEW_SCOPE=YES
CREATE_HANDOFF=YES
CONTINUE_IN_NEW_SESSION_WHEN_AVAILABLE=YES
```

Never compromise correctness or security merely to conserve quota.

---

## 15. OBSERVED USAGE LESSONS

Recent GYPPORT Claude Code usage showed:

```text
VERY_LARGE_CONTEXT
+
SUBAGENT_INTENSIVE_EXECUTION
+
VERY_LARGE_INTERMEDIATE_OUTPUT
=
DISPROPORTIONATE_USAGE
```

High cache reuse helps, but extremely long sessions still have meaningful cost.

Preferred optimization target:

```text
REDUCE_REDUNDANT_CONTEXT
REDUCE_DUPLICATE_AGENT_WORK
REDUCE_VERBOSE_INTERMEDIATE_OUTPUT
PRESERVE_HIGH_VALUE_EVIDENCE
```

The goal is not to reduce reasoning quality.

---

## 16. MODULE NAVIGATION KNOWLEDGE

When a STEP concerns product navigation, module hierarchy, sidebar structure,
sections, or local tabs/navigation, also apply:

```text
D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT\Fabric\Knowledge\UIX\GYPPORT_MODULE_NAVIGATION_HIERARCHY.md
```

Do not repeat the full navigation policy inside every STEP.

---

## 17. PROMPT GENERATION RULE

AGENTS.md, CLAUDE.md, and CHATGPT.md should point to this document.

Therefore normal substantial STEPs do NOT need to paste this entire policy.

A STEP may simply state:

```text
APPLY_GYPPORT_AI_AGENT_USAGE_EFFICIENCY_KNOWLEDGE=YES
```

and include exceptions only when the STEP genuinely requires them.

If the external Knowledge file is unavailable, the minimum rules embedded in
AGENTS.md / CLAUDE.md / CHATGPT.md remain the fallback.

---

## 18. CANONICAL SUMMARY

```text
GYPPORT_AI_AGENT_USAGE_EFFICIENCY

ONE_MAJOR_STEP_PER_SESSION=YES

CONTEXT_UNDER_150K=NORMAL
CONTEXT_150K_TO_250K=REVIEW_SESSION_SHAPE
CONTEXT_ABOVE_250K=COMPACT_AT_NEXT_NATURAL_BOUNDARY
CONTEXT_ABOVE_500K=AVOID_NEW_SCOPE

PARALLEL_SUBAGENTS_DEFAULT=0
MAX_PARALLEL_SUBAGENTS=2

SEARCH_FIRST_READ_SECOND=YES
DO_NOT_REREAD_UNCHANGED_FILES=YES

AUDIT_TARGETED_FIRST=YES
NO_SPECULATIVE_IMPLEMENTATION=YES
STOP_ON_OWNER_DECISION=YES

INTERMEDIATE_REPORTS=SHORT
PASSING_TEST_LOGS_SUMMARY_ONLY=YES
FULL_FINDINGS_ONLY_AT_END=YES

TARGETED_TESTS_BEFORE_FULL_SUITE=YES
FULL_SUITE_RUNS_MAX=1

DOCKER_REBUILD_AFTER_CODE_STABLE=YES
LIVE_BROWSER_VERIFICATION_RUNS=1

PATH_SPECIFIC_STAGING=YES
PRESERVE_PREEXISTING_WIP=YES

COMPACT_AT_PHASE_BOUNDARIES=YES
NEW_SESSION_WHEN_OBJECTIVE_CHANGES=YES

HANDOFF_COMPACT_AND_CANONICAL=YES
```
