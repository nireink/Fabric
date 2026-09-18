# GYPPORT AI KNOWN FINDING COMPLETION POLICY

PROJECT=GYPPORT
DOCUMENT_TYPE=CANONICAL_AI_GOVERNANCE_KNOWLEDGE
RULE_ID=GYPPORT_AI_KNOWN_FINDING_COMPLETION_POLICY
STATUS=OWNER_APPROVED_BASELINE
SCOPE=CLAUDE_CODE_CODEX_CHATGPT_AND_OTHER_GYPPORT_EXECUTION_AGENTS

RECOMMENDED_PATH=
D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT\Fabric\Knowledge\AI\GYPPORT_AI_KNOWN_FINDING_COMPLETION_POLICY.md

---

## 1. PURPOSE

GYPPORT does not accept vague technical deferral as a substitute for completing
work correctly.

When an issue, gap, inconsistency, missing guard, traceability defect, security
risk, broken invariant, or necessary correction is discovered during an
authorized STEP, the default behavior is to resolve it in the current work
cycle when the solution is already supported by the accepted architecture and
is unambiguous.

Canonical principle:

```text
KNOWN_PROBLEM
→ RESOLVE_NOW

NOT:

KNOWN_PROBLEM
→ "NOT NECESSARY TODAY"
→ "FUTURE"
→ "LATER"
→ FORGOTTEN
→ EXPENSIVE REWORK
```

The goal is to avoid accumulating small unresolved defects that later force
larger redesigns or destructive changes.

---

## 2. PROHIBITED VAGUE DEFERRAL LANGUAGE

Agents must not close a STEP with phrases such as:

```text
"not necessary today"
"can be done later"
"future improvement"
"we can revisit this"
"follow-up someday"
"nice to have later"
"out of scope for now"
```

when the finding:

- is directly relevant to the current work;
- is required for correctness;
- is required for security;
- is required for data integrity;
- is required to preserve the accepted domain model;
- is required to prevent predictable rework;
- can be corrected safely with the already-approved architecture.

Canonical:

```text
VAGUE_DEFERRAL_OF_KNOWN_IN_SCOPE_PROBLEM=NO
```

---

## 3. FOUR VALID FINDING DISPOSITIONS

Every material finding must end in exactly one of these states.

### A. RESOLVED_NOW

Use when:

- the issue is real;
- the solution is unambiguous;
- the solution is already supported by the accepted architecture/model;
- the change is within the authorized STEP or the Owner explicitly expands the
  STEP.

Required:

```text
DISPOSITION=RESOLVED_NOW
IMPLEMENT=
TEST=
DOCUMENT=
```

---

### B. ACCEPTED_NON_DEFECT_WITH_ENFORCEMENT

Use only when evidence proves the finding is not actually a defect.

Do not merely say "not a problem."

Preserve the conclusion now with the smallest appropriate enforcement:

- regression test;
- invariant/contract test;
- code assertion;
- canonical documentation;
- permission-set guard;
- schema constraint if already supported and explicitly authorized.

Required:

```text
DISPOSITION=ACCEPTED_NON_DEFECT_WITH_ENFORCEMENT
WHY_NOT_A_DEFECT=
ENFORCEMENT_ADDED_OR_ALREADY_PRESENT=
```

A known structural limitation that could become dangerous later should not be
left only as prose if a cheap existing-model guard can prevent misuse now.

---

### C. OWNER_DECISION_REQUIRED_NOW

Use when:

- more than one legitimate solution exists;
- the solution changes architecture/security/product semantics;
- a new role/table/column/scope/concept is required;
- external verification policy must be chosen;
- the Owner must accept risk or behavior.

Required workflow:

```text
FINDING
→ BOUNDED READ-ONLY DIAGNOSIS
→ STOP
→ PRESENT OPTIONS
→ WAIT FOR OWNER
→ OWNER CHOOSES
→ RESUME THE SAME WORK CYCLE
→ COMPLETE
```

Do not convert the finding into an indefinite future STEP merely to close the
current STEP.

---

### D. EXTERNAL_DEPENDENCY_BLOCKED_NOW

Use only when the required resolution depends on something genuinely not
available to the agent/project now, such as:

- missing official external integration;
- unavailable credential/certificate;
- external approval;
- unavailable authoritative data source;
- third-party outage or legal prerequisite.

Required:

```text
DISPOSITION=EXTERNAL_DEPENDENCY_BLOCKED_NOW
EXTERNAL_DEPENDENCY=
WHY_INTERNAL_WORK_CANNOT_COMPLETE_IT=
WHAT_CAN_BE_COMPLETED_NOW=
EXACT_TRIGGER_TO_RESUME=
OWNER_ACKNOWLEDGEMENT_REQUIRED=YES
```

Do as much safe internal completion as possible now.

Do not fabricate the unavailable external capability.

---

## 4. COMPLETE THE CURRENT PROBLEM BEFORE OPENING THE NEXT ONE

Default:

```text
DO_NOT_OPEN_NEXT_MAJOR_STEP_WITH_KNOWN_UNRESOLVED_CURRENT_FINDING=YES
```

If a finding is directly part of the current foundation, complete it before
moving to another module.

Example:

```text
Security foundation
→ known traceability gap
→ fix traceability now
→ then freeze security foundation
→ then return to Expenses / Fuel Stations
```

Not:

```text
Security foundation
→ known traceability gap
→ mark "05E later"
→ move to Expenses
→ rediscover security dependency months later
```

---

## 5. STOP GATES STILL APPLY

This policy does NOT authorize agents to improvise.

It works together with:

```text
GYPPORT_AI_AGENT_AUTONOMY_STOP_GATES.md
```

Difference:

```text
AUTONOMY_STOP_GATES
= unexpected/ambiguous issue → STOP AND ASK

KNOWN_FINDING_COMPLETION_POLICY
= after the decision is clear → DO NOT DEFER; FINISH IT NOW
```

Canonical:

```text
STOP_BEFORE_UNAPPROVED_REPAIR=YES
RESUME_AFTER_OWNER_DECISION=YES
COMPLETE_AFTER_DECISION=YES
```

---

## 6. NO AUTO-INVENTION TO "FINISH NOW"

"Resolve now" does NOT mean "invent now."

Forbidden:

- inventing a replacement role;
- inventing a table because code needs one;
- inventing an authorization scope;
- inventing fake verification;
- inventing an SRI response;
- rewriting accepted architecture to remove a test failure.

If current architecture cannot support the needed resolution:

```text
OWNER_DECISION_REQUIRED_NOW
```

The Owner chooses the new direction before implementation.

---

## 7. UNEXPECTED TEST FAILURES

If an unexpected failure appears:

```text
STOP
→ diagnose boundedly
→ ask Owner if decision is needed
```

Once proven to be a mechanical execution/environment issue with a single
already-authorized correction, complete that correction in the same work cycle.

Do not create a separate future debt item for a problem that can be closed now.

---

## 8. PREEXISTING TECHNICAL DEBT

Preexisting debt is not automatically in scope.

But if it directly blocks or invalidates the current STEP:

```text
PREEXISTING_BUT_BLOCKING
→ OWNER DECISION NOW
```

If it is truly unrelated and non-blocking:

```text
PREEXISTING_UNRELATED
→ preserve untouched
→ record exact evidence
```

Do not "clean it up helpfully."

Do not use "preexisting" to ignore a problem that the current STEP actually
depends on.

---

## 9. STRUCTURAL LIMITATIONS

When an audit finds a structural limitation but proves it is not a current
defect, choose one of two dispositions:

```text
A. ACCEPTED_NON_DEFECT_WITH_ENFORCEMENT
B. OWNER_DECISION_REQUIRED_NOW
```

Do not write:

```text
"today it is not necessary to change"
```

without deciding whether the limitation is intentionally accepted and guarded.

Example:

If TENANT_USER permissions are safe today but the resolver cannot identify
permission provenance, add or preserve a contract/invariant that prevents
Organization-administration permissions from entering TENANT_USER when that can
be done using the existing model.

If that requires a new architecture, stop and ask.

---

## 10. FOLLOW-UP STEPS

A separate follow-up STEP is allowed only when one of these is true:

1. the Owner explicitly chooses to split the work;
2. the work is independently valuable and not required to make the current
   foundation correct;
3. a genuine external dependency blocks completion;
4. isolating the implementation is required for repository/worktree safety and
   the Owner approves the split.

Required:

```text
FOLLOWUP_CREATED_BY_EXPLICIT_OWNER_DECISION=YES
```

Agents must not create "05D later", "05E later", etc. only to make the current
STEP appear complete.

---

## 11. OWNER DECISION DIALOG

When a decision is required now:

```text
STATUS=OWNER_DECISION_REQUIRED

FINDING=
WHY_IT_MATTERS=
EVIDENCE=

CAN_RESOLVE_WITH_EXISTING_MODEL=YES/NO

OPTIONS=

A.
IMPACT=
RISK=

B.
IMPACT=
RISK=

C.
IMPACT=
RISK=

OTHER=
Owner may give another instruction.

RECOMMENDED_OPTION=

IF_OWNER_SELECTS_OPTION=
Resume this same work cycle and complete the selected resolution.

WAITING_FOR_OWNER_INSTRUCTION=YES
```

---

## 12. STEP CLOSURE GATE

A STEP may be marked COMPLETE only if all material findings are classified.

Required final fields:

```text
KNOWN_FINDINGS_TOTAL=

RESOLVED_NOW=
ACCEPTED_NON_DEFECT_WITH_ENFORCEMENT=
OWNER_DECISION_REQUIRED_NOW=
EXTERNAL_DEPENDENCY_BLOCKED_NOW=

UNCLASSIFIED_FINDINGS=0
```

For Owner Acceptance:

```text
UNRESOLVED_IN_SCOPE_FINDINGS=0
```

unless the Owner explicitly accepted an external block or an intentional split.

---

## 13. GYPPORT-SPECIFIC EXAMPLES

### Bad

```text
created_by_user_id is not populated.
We can do it later.
```

### Correct

```text
created_by_user_id is part of the current Organization-control traceability
foundation and the existing DB column already exists.

If plumbing is straightforward and model-consistent:
→ implement now.

If it reveals a domain-model ambiguity:
→ STOP and ask now.
```

### Bad

```text
Initial Organization OWNER activation can be a future STEP.
```

### Correct

```text
The current security foundation is not complete until the first legitimate
Organization OWNER activation path has a disposition.

If an existing safe verification path exists:
→ implement now.

If official/external verification is required and unavailable:
→ report EXTERNAL_DEPENDENCY_BLOCKED_NOW or ask the Owner to choose an explicit
  MVP verification policy now.

Do not silently defer it.
```

---

## 14. RELATION TO OTHER GYPPORT AI POLICIES

Use together:

```text
GYPPORT_AI_AGENT_USAGE_EFFICIENCY_KNOWLEDGE.md
= work efficiently

GYPPORT_AI_AGENT_AUTONOMY_STOP_GATES.md
= stop before unapproved decisions/repairs

GYPPORT_AI_KNOWN_FINDING_COMPLETION_POLICY.md
= once a finding is known and disposition is clear, do not defer it
```

All three are mandatory for substantial GYPPORT implementation and audit work.

---

## 15. CANONICAL SUMMARY

```text
GYPPORT_AI_KNOWN_FINDING_COMPLETION_POLICY

KNOWN_IN_SCOPE_PROBLEM=RESOLVE_NOW

VAGUE_DEFERRAL=NO
"NOT_NECESSARY_TODAY"=PROHIBITED_FOR_KNOWN_IN_SCOPE_PROBLEM
"FUTURE"=PROHIBITED_AS_DEFAULT_DISPOSITION
"LATER"=PROHIBITED_AS_DEFAULT_DISPOSITION

AUTO_INVENTION_TO_FINISH_NOW=NO

AMBIGUOUS_SOLUTION
→ STOP
→ OPTIONS
→ OWNER DECISION
→ RESUME
→ COMPLETE

NON_DEFECT
→ ACCEPT_EXPLICITLY
→ GUARD/TEST/DOCUMENT NOW

EXTERNAL_BLOCK
→ NAME IT
→ COMPLETE ALL INTERNAL WORK NOW
→ DEFINE EXACT RESUME TRIGGER

DO_NOT_CLOSE_STEP_WITH_UNRESOLVED_IN_SCOPE_FINDING=YES

FOLLOWUP_REQUIRES_EXPLICIT_OWNER_DECISION=YES

STEP_ACCEPTANCE_REQUIRES:
UNCLASSIFIED_FINDINGS=0
UNRESOLVED_IN_SCOPE_FINDINGS=0
```
