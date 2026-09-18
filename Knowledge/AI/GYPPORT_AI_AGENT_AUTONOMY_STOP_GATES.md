# GYPPORT AI AGENT AUTONOMY AND STOP GATES

PROJECT=GYPPORT
DOCUMENT_TYPE=CANONICAL_AI_GOVERNANCE_KNOWLEDGE
RULE_ID=GYPPORT_AI_AGENT_AUTONOMY_STOP_GATES
STATUS=OWNER_APPROVED_BASELINE
SCOPE=CLAUDE_CODE_CODEX_CHATGPT_AND_OTHER_GYPPORT_EXECUTION_AGENTS

RECOMMENDED_PATH=
D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT\Fabric\Knowledge\AI\GYPPORT_AI_AGENT_AUTONOMY_STOP_GATES.md

---

## 1. PURPOSE

GYPPORT allows AI agents to execute an explicitly authorized STEP with useful
autonomy, but autonomy does NOT include permission to silently repair,
redesign, reinterpret, or invent solutions when unexpected findings appear.

Canonical principle:

```text
AUTONOMY = EXECUTE THE APPROVED PLAN
AUTONOMY != INVENT THE NEXT PLAN
AUTONOMY != SILENT SELF-REPAIR
AUTONOMY != ARCHITECTURAL DECISION AUTHORITY
```

When the real repository, database, tests, runtime, or architecture produces an
unexpected finding, the agent must STOP and return control to the Owner.

---

## 2. OWNER AUTHORITY

The Owner retains final authority over:

- architecture
- data model
- domain ownership
- security model
- authorization scope
- migrations
- destructive changes
- new roles / permissions / concepts
- cross-module contracts
- product semantics
- acceptance of residual risk
- repair strategy after unexpected failures

The agent may recommend options.

The agent may NOT select and execute a new option on the Owner's behalf unless
the current STEP explicitly pre-authorized that exact option and condition.

```text
OWNER_DECISION_AUTHORITY=ABSOLUTE
```

---

## 3. AUTONOMY BOUNDARY

An agent may continue autonomously only while ALL of the following remain true:

```text
CURRENT_STEP_EXPLICITLY_AUTHORIZED=YES
CURRENT_ACTION_WITHIN_STEP_SCOPE=YES
MODEL_MATCHES_EXPECTED_EVIDENCE=YES
NO_NEW_ARCHITECTURE_REQUIRED=YES
NO_UNEXPECTED_SECURITY_FINDING=YES
NO_UNEXPECTED_DATA_MODEL_CONFLICT=YES
NO_UNEXPECTED_MIGRATION_RISK=YES
NO_UNEXPECTED_TEST_FAILURE_REQUIRING_NEW_DESIGN=YES
NO_SCOPE_EXPANSION_REQUIRED=YES
```

If any becomes false:

```text
STOP_REQUIRED=YES
```

---

## 4. GREEN / YELLOW / RED EXECUTION MODEL

### GREEN — CONTINUE

The agent may proceed without asking again when the action is already explicitly
inside the authorized STEP and no unexpected condition appears.

Examples:

- read the files named or directly relevant to the STEP;
- run the authorized targeted tests;
- implement the already-approved design;
- update tests to match an explicitly approved contract;
- stage only the authorized paths;
- produce the requested report.

```text
GREEN_ACTION=CONTINUE
```

### YELLOW — STOP AND ASK

A YELLOW condition means the work may have a reasonable solution, but the
solution is not already approved.

Examples:

- an unexpected test fails;
- a runtime dependency is different from the audit assumption;
- an existing table/field has different semantics than expected;
- a current API contract blocks the approved implementation;
- two valid repair alternatives exist;
- a broader file/repository change is required;
- a migration appears necessary but was not authorized;
- a preexisting defect is discovered;
- the proposed implementation would require changing an accepted invariant.

```text
YELLOW_ACTION=STOP_AND_REQUEST_INSTRUCTION
```

The agent must NOT repair first and report afterward.

### RED — STOP IMMEDIATELY

A RED condition means continuing could create architectural, security, data, or
product risk.

Examples:

- cross-tenant or cross-organization authorization leak;
- data-loss or destructive migration risk;
- need for a new security scope;
- need for a new table/column/role to fill a modeling gap;
- contradiction with an Owner-approved decision;
- irreversible change with ambiguous consequences;
- credentials/secrets exposure;
- unexplained production/shared-DEV mutation;
- an operation would broaden permissions or authority.

```text
RED_ACTION=STOP_IMMEDIATELY
```

No workaround may be implemented.

---

## 5. NO SILENT REPAIR RULE

The agent must not convert an unexpected failure into a self-directed repair
task.

Forbidden pattern:

```text
run test
→ unexpected failure
→ infer cause
→ edit production code
→ edit migration
→ rerun
→ discover another issue
→ repair again
→ report everything at the end
```

Required pattern:

```text
run test
→ unexpected failure
→ investigate only enough to identify the cause
→ STOP
→ report evidence
→ present bounded options
→ WAIT FOR OWNER
```

```text
AUTO_REPAIR_AFTER_UNEXPECTED_FAILURE=NO
```

---

## 6. NO INVENTED SOLUTION RULE

When the current model lacks a capability, the agent must not invent one merely
to complete the STEP.

Do NOT automatically create:

- new roles
- replacement roles
- new tables
- new columns
- new scope types
- new membership concepts
- new lifecycle states
- new authority concepts
- new verification mechanisms
- new background processes
- new fallback permissions
- new "temporary" architecture that becomes permanent

Examples of prohibited behavior:

```text
"OWNER is too broad, so I created MEMBER."
```

```text
"Current verification is missing, so I used password confirmation as authority."
```

```text
"The schema lacks the relation, so I added a new table."
```

unless the Owner explicitly authorized that exact change.

```text
FILL_ARCHITECTURE_GAPS_BY_INVENTION=NO
```

---

## 7. POPUP-STYLE OWNER DECISION GATE

When the agent stops, the response should behave like a clear decision dialog.

Use this structure:

```text
STATUS=OWNER_DECISION_REQUIRED

FINDING=
<one concise description>

WHY_IT_MATTERS=
<security / architecture / data / product consequence>

EVIDENCE=
<exact files, query, schema, test, runtime evidence>

CURRENT_WORK_STATE=
FILES_CHANGED=
DB_CHANGED=
COMMITS_CREATED=
PUSH_PERFORMED=NO

OPTIONS=

A. <option>
   IMPACT=
   RISK=

B. <option>
   IMPACT=
   RISK=

C. <option>
   IMPACT=
   RISK=

RECOMMENDED_OPTION=
<recommendation with reason>

OTHER=
Owner may provide another instruction.

WAITING_FOR_OWNER_INSTRUCTION=YES
```

The recommendation is advisory only.

The agent must not execute the recommended option until the Owner chooses.

---

## 8. USER-FACING QUESTION STYLE

When a decision is required, prefer a short, explicit choice instead of a long
narrative.

Example:

```text
I found that MEMBER did not exist in the approved model.

Choose how to proceed:

1. Audit whether MEMBER can be removed using the existing schema. [Recommended]
2. Keep MEMBER temporarily and document it as technical debt.
3. Stop this STEP with no further changes.
4. Other.

No changes will be made until you choose.
```

For security-sensitive choices:

```text
DEFAULT_IF_NO_RESPONSE=STOP
```

---

## 9. INVESTIGATION AFTER A FAILURE

After an unexpected error, the agent may perform a bounded read-only diagnosis
before stopping, but only enough to answer:

```text
WHAT_FAILED=
WHY_IT_FAILED=
WHETHER_IT_IS_PREEXISTING=
WHETHER_CURRENT_STEP_CAUSED_IT=
WHAT_BOUNDARY_IS_AFFECTED=
```

The diagnosis must not turn into an unapproved repair.

```text
DIAGNOSE_BEFORE_STOP=BOUNDED_READ_ONLY
REPAIR_BEFORE_OWNER_DECISION=NO
```

---

## 10. TEST FAILURE POLICY

### Expected failure

A test intentionally written first to prove an already-approved change may fail
before implementation.

This is not an unexpected stop condition if the STEP explicitly uses that
workflow.

### Unexpected failure

If a test outside the expected change fails, or the failure implies a new
architectural/security/data issue:

```text
STOP=YES
AUTO_FIX=NO
```

The agent must report the smallest reproducible evidence.

---

## 11. DATABASE AND MIGRATION STOP GATES

Before any new migration not already explicitly authorized:

```text
WHY_MIGRATION_REQUIRED=
CAN_EXISTING_SCHEMA_SUPPORT_IT=
NEW_TABLES=
NEW_COLUMNS=
DATA_REWRITE=
DESTRUCTIVE_EFFECT=
ROLLBACK_OR_FORWARD_RECOVERY=
```

If a migration is being proposed merely because the code design created a gap:

```text
STOP=YES
```

Database modeling must lead the implementation, not be reshaped silently to fit
an improvised application workaround.

```text
DATABASE_MODEL_FIRST
DOMAIN_MODEL_SECOND
SECURITY_MODEL_THIRD
APPLICATION_IMPLEMENTATION_AFTER
```

---

## 12. SECURITY STOP GATES

Immediately stop when discovering:

- tenant-scope authority leaking into Organization scope;
- Organization A permission authorizing Organization B;
- hidden UI being relied on as security;
- membership/context being treated as authorization;
- self-attestation becoming authority;
- account authentication being treated as corporate authority;
- last-admin/last-owner protection failure;
- new privilege escalation path;
- new platform-to-customer authority leak.

Required status:

```text
STATUS=SECURITY_OWNER_DECISION_REQUIRED
```

No speculative remediation.

---

## 13. SCOPE EXPANSION RULE

If implementing the STEP requires touching an additional module/repository or
opening a new domain concern that was not authorized:

```text
SCOPE_EXPANSION_REQUIRED=YES
STOP_REQUIRED=YES
```

The agent must report:

```text
WHY_NEW_SCOPE_IS_REQUIRED=
REPOSITORIES_AFFECTED=
FILES_EXPECTED=
MINIMUM_CHANGE=
ALTERNATIVES=
```

and wait.

---

## 14. PREEXISTING WORK RULE

If unrelated dirty files, concurrent edits, or unexplained DEV data are found:

```text
DO_NOT_TOUCH=YES
DO_NOT_CLEAN_UP_AUTOMATICALLY=YES
```

If they block the STEP:

```text
STOP_AND_REPORT=YES
```

The agent may not "helpfully" clean another session's work.

---

## 15. COMMIT AND PUSH RULE

A local commit does not convert an unresolved decision into an accepted design.

If an Owner decision is required before the implementation is valid:

```text
DO_NOT_COMMIT_NEW_REPAIR=YES
```

unless the STEP explicitly asked for a checkpoint commit of already-authorized
work.

Always:

```text
PUSH_WITHOUT_OWNER_AUTHORIZATION=NO
```

---

## 16. OWNER REVIEW CHECKPOINTS

For large or security-sensitive STEPs, use explicit checkpoints:

```text
CHECKPOINT_1=AUDIT_COMPLETE
CHECKPOINT_2=DESIGN_CONFIRMED
CHECKPOINT_3=IMPLEMENTATION_COMPLETE
CHECKPOINT_4=FINAL_VERIFICATION
CHECKPOINT_5=OWNER_ACCEPTANCE
```

If the audit changes the assumed design:

```text
STOP_AT_CHECKPOINT_1=YES
```

Do not continue merely because implementation permission existed for the
original design.

---

## 17. RELATION TO EFFICIENCY POLICY

This document works together with:

```text
Fabric\Knowledge\AI\GYPPORT_AI_AGENT_USAGE_EFFICIENCY_KNOWLEDGE.md
```

Efficiency rules reduce unnecessary work.

This document limits autonomous decision-making.

```text
EFFICIENCY_POLICY
= HOW TO WORK WITH LESS WASTE

AUTONOMY_STOP_GATES
= WHEN THE AGENT MUST STOP AND RETURN CONTROL
```

Efficiency must never be used as justification to skip an Owner decision.

---

## 18. RELATION TO AGENTS / CLAUDE / CHATGPT

`AGENTS.md`, `CLAUDE.md`, and `CHATGPT.md` should reference this policy.

Prompts should not need to repeat the entire document.

For substantial implementation STEPs, a short declaration is enough:

```text
APPLY_GYPPORT_AI_AGENT_AUTONOMY_STOP_GATES=YES
```

If the external file is unavailable, the agent must use the minimum embedded
rule:

```text
UNEXPECTED_FINDING
→ STOP
→ REPORT
→ OPTIONS
→ WAIT FOR OWNER
```

---

## 19. CANONICAL SUMMARY

```text
GYPPORT_AI_AGENT_AUTONOMY_STOP_GATES

AUTONOMY_EXECUTES_APPROVED_PLAN_ONLY=YES

AUTO_REPAIR_AFTER_UNEXPECTED_FAILURE=NO
AUTO_ARCHITECTURE_INVENTION=NO
AUTO_SCOPE_EXPANSION=NO

UNEXPECTED_FINDING=STOP
UNEXPECTED_TEST_FAILURE=STOP
SECURITY_CONTRADICTION=STOP
DATA_MODEL_CONTRADICTION=STOP
NEW_SCHEMA_PRIMITIVE_REQUIRED=STOP
NEW_ROLE_OR_SCOPE_REQUIRED=STOP

BOUNDED_READ_ONLY_DIAGNOSIS_ALLOWED=YES

OWNER_DECISION_DIALOG_REQUIRED=YES
OPTIONS_MAY_BE_RECOMMENDED=YES
RECOMMENDED_OPTION_AUTO_EXECUTED=NO

DEFAULT_IF_NO_OWNER_RESPONSE=STOP

PUSH_WITHOUT_OWNER_AUTHORIZATION=NO

WORKFLOW=
EXECUTE
→ UNEXPECTED FINDING
→ DIAGNOSE BOUNDEDLY
→ STOP
→ REPORT EVIDENCE
→ PRESENT OPTIONS
→ WAIT FOR OWNER
```
