# GYPPORT_PRE_COMMIT_ENV_UI_AUDIT_HARDENING_13 — Owner prompt

```text
TRACK=GM_EXPENSES_RELEASE_READINESS
STEP=GYPPORT_PRE_COMMIT_ENV_UI_AUDIT_HARDENING_13
MODE=AUDIT_FIRST_THEN_TARGETED_IMPLEMENTATION
OWNER_AUTHORIZATION=YES
DATE=2026-09-17
FINAL_12_BASELINE=accepted for migrations and Case-level financial behavior (section 21)
OWNER_DECISIONS=no global Windows datasource may default to Shared DEV; Conciliado and Uso are two independent indicators; all currently created business data is TEST/EXAMPLE DATA; known OBSERVADO test expense preferred final state RECHAZADO (local 3310 only)
REQUIRED_BASELINES=GYPPORT-PKG2D-CROSS-TENANT-GLOBAL-ACCOUNT-VERIFIED-BASELINE-2026-09-16
FULL_HISTORICAL_REGRESSION_RERUN=NO
```

The Owner's prompt follows verbatim.

---

GYPPORT® — PRE-COMMIT SAFETY + FINAL EXPENSES UX/AUDIT CORRECTIONS

TRACK=
GM_EXPENSES_RELEASE_READINESS

STEP=
GYPPORT_PRE_COMMIT_ENV_UI_AUDIT_HARDENING_13

MODE=
AUDIT_FIRST_THEN_TARGETED_IMPLEMENTATION

OWNER_AUTHORIZED=YES

PURPOSE=

Before the controlled MVP commit, close three targeted items:

A. Remove the unsafe global Windows datasource reference to Shared DEV.

B. Render two independent ExpenseCase progress indicators:
   Conciliado and Uso.

C. Resolve the known OBSERVADO test-data inconsistency and prove that current
   production code cannot create OBSERVADO without immutable review history.

Do NOT migrate Shared DEV.
Do NOT commit.
Do NOT push.

============================================================
PART A — LOCAL ENVIRONMENT SAFETY
============================================================

1. CURRENT RISK
============================================================

A Windows USER-level:

    SPRING_DATASOURCE_URL

currently points to Shared DEV:

    localhost:3308

The local launcher overrides it with:

    localhost:3310/gypport_runtime_local

This is unsafe because another launcher, IDE or:

    mvn spring-boot:run

could accidentally inherit Shared DEV.

OWNER RULE:

NO global Windows User/Machine datasource configuration may make Shared DEV
the default datasource for normal development.

============================================================
2. AUDIT ENVIRONMENT SCOPES
============================================================

Read-only inspect:

Process:
    SPRING_DATASOURCE_URL
    SPRING_DATASOURCE_USERNAME
    SPRING_DATASOURCE_PASSWORD

User:
    same

Machine:
    same

Also inspect explicit project-local references to:

    localhost:3308
    gypport-mysql-dev
    Shared DEV DB name

in:

- local PowerShell launchers;
- project scripts;
- IDE launch configs if available;
- Maven/Spring run helpers;
- Docker env configuration.

Never print password values.

Report secrets only as:

    PRESENT
    ABSENT
    AMBIGUOUS

============================================================
3. REMOVE UNSAFE USER-LEVEL SHARED DEV INHERITANCE
============================================================

If USER:

    SPRING_DATASOURCE_URL

is confirmed to point to Shared DEV:

remove it from Windows User scope.

Also clear it from the current process.

If USER-level username/password variables are clearly Shared-DEV-specific:

remove those too.

If ownership is ambiguous:

do NOT remove them.
Report and stop that sub-action.

Do NOT silently change Machine-level variables.

If Machine scope points at Shared DEV:

report it for Owner decision.

============================================================
4. LOCAL RUNTIME EXPLICIT CONFIGURATION
============================================================

Local development runtime must use explicit process-local configuration:

    ENV=LOCAL_EDUARDO
    DB_HOST=127.0.0.1
    DB_PORT=3310
    DB_NAME=gypport_runtime_local

Credentials must be provided through the existing safe local mechanism.

Do NOT persist them as general Windows User environment variables.

============================================================
5. LOCAL STARTUP SAFETY GUARD
============================================================

Harden the local launcher.

Before starting Java, display only:

    ENV
    DB_HOST
    DB_PORT
    DB_NAME

Never passwords.

Abort startup if the resolved local datasource contains:

    :3308
    gypport-mysql-dev
    Shared DEV DB identifier

Error:

    "Local runtime refused to start because the datasource points to Shared DEV."

This guard is mandatory.

============================================================
6. ENVIRONMENT VERIFICATION
============================================================

After correction prove:

    plain shell inherits Shared DEV datasource = NO

Local backend:

    :8080
        → DB :3310 only

Connections to 3310:
    > 0

Connections to 3308 from local backend:
    0

Local DB:
    V63

Shared DEV:
    V43
    unchanged

/auth/me unauthenticated:
    401

login endpoint:
    reachable

============================================================
PART B — TWO INDEPENDENT PROGRESS BARS
============================================================

7. OWNER VISUAL REQUIREMENT
============================================================

The ExpenseCase card must have TWO independent visual indicators.

Not:

    Conciliado [bar]
    Uso 87%     no bar

Required:

    Conciliado      │BAR│
    100%

    Uso             │BAR│
    87%

Both get their own compact progress track.

============================================================
8. CONCILIADO
============================================================

CLOSED Case with:

    pending reconciliation = 0

shows:

    Conciliado
    100%

and:

    bar fill = 100%

For OPEN Cases:

do NOT invent an arbitrary intermediate mathematical percentage.

If no canonical progressive percentage exists:

    Conciliado
    Pendiente

and render an empty conciliation bar.

Do NOT falsely show 100%.

============================================================
9. USO
============================================================

Usage:

    usagePercent = used / delivered

when:

    delivered > 0

Preserve real numeric result:

    29%
    87%
    110%

If:

    delivered == 0

show:

    Uso 0%

and an empty usage bar.

If:

    usagePercent > 100

example:

    Uso 110%

text remains:

    110%

visual bar is clamped to:

    100%

No overflow.

============================================================
10. REQUIRED CARD EXAMPLES
============================================================

A. Compra Teléfono CLOSED:

    delivered 300
    used 260
    justified 260
    returned 40
    pending 0

Show:

    Conciliado 100%
    full bar

    Uso 87%
    87% bar

B. Viaje Loja CLOSED:

    delivered 679
    used 200
    justified 200
    returned 499
    reimbursed 20

Show:

    Conciliado 100%
    Uso 29%

with TWO bars.

C. OPEN overuse:

    delivered 1000
    used 1100

Show:

    Conciliado Pendiente
    empty conciliation bar

    Uso 110%
    visually full usage bar

D. No delivered Advance:

    Uso 0%
    empty usage bar

============================================================
11. RESPONSIVE
============================================================

Test:

    desktop
    768px
    375px
    320px

Both concepts must remain visible.

No horizontal overflow.

The two compact vertical indicators may stack if required on narrow screens.

============================================================
PART C — OBSERVADO HISTORY INTEGRITY
============================================================

12. KNOWN TEST RECORD
============================================================

Known Expense:

    5E63494AA2564C1E847CD54A6ED67A51

Current:

    state = OBSERVADO

but:

    OBSERVED history event = missing

OWNER CLASSIFICATION:

All currently created business data is TEST/EXAMPLE DATA designed to simulate
real-world scenarios.

Therefore this record may be treated as DEV TEST DATA.

Do NOT treat it as immutable production history.

============================================================
13. FIRST DETERMINE ROOT CAUSE
============================================================

Audit all CURRENT production paths that can transition Expense to:

    OBSERVADO

Determine whether current code can produce:

    Expense = OBSERVADO
    but no OBSERVED review event

Expected modern invariant:

    transition to OBSERVADO
    AND
    immutable OBSERVED history insertion

occur inside the SAME transaction.

If one fails:

    whole transaction rolls back.

Return:

    CURRENT_CODE_CAN_REPRODUCE=YES/NO

============================================================
14. AUDIT CURRENT REVIEW TRANSACTION
============================================================

Trace:

Host endpoint
    ↓
application use case
    ↓
domain transition
    ↓
Expense repository write
    ↓
review-history repository write
    ↓
transaction boundary

Prove actor comes from:

    authenticated GLOBAL UserAccount

and timestamp comes from:

    system clock / canonical Clock

Do not use Person/Responsible as audit actor.

============================================================
15. AUDIT FIELDS
============================================================

Report actual current coverage.

Expense entity/audit:

- tenant_id
- created_at
- created_by_user_account_id
- updated_at if present
- updated_by if present

Review history:

- id
- tenant_id
- expense_id
- event_type
- actor_user_account_id
- occurred_at
- reason_code
- detail
- created_at/source if present

Identify genuine audit gaps.

Do NOT add arbitrary columns just because this list contains them.

Use the existing audit/event model wherever possible.

============================================================
16. FUTURE-PROOFING RULE
============================================================

If CURRENT code can reproduce the inconsistent state:

THIS IS A RELEASE BLOCKER.

Fix it.

Required:

    Expense OBSERVADO + OBSERVED history

must be atomic.

Add tests that deliberately cause history persistence failure and prove:

    Expense does not remain OBSERVADO.

If current code CANNOT reproduce it:

classify the known row as:

    LEGACY_DEV_TEST_DATA

and do NOT add a permanent legacy product workflow merely for it.

============================================================
17. KNOWN TEST EXPENSE REGULARIZATION
============================================================

OWNER DECISION:

For this known TEST expense, preferred final state:

    RECHAZADO

because it is no longer useful as an unresolved OBSERVADO blocker.

However:

do NOT silently UPDATE its state.

Do NOT fake a historical rejection date.

Do NOT fake a historical reviewer.

First determine whether the current canonical review/application path safely
allows OBSERVADO → RECHAZADO.

If YES:

perform a real current-time rejection/regularization using:

    actor = authenticated Owner UserAccount
    timestamp = current system time
    reason = existing safe reason code

detail clearly identifying:

    "Regularización de dato de prueba creado antes del historial canónico de revisión."

The event represents a REAL regularization action now.

It does NOT represent a fabricated historical rejection.

If OBSERVADO → RECHAZADO is NOT a valid canonical transition:

do NOT add that transition merely for this test row.

Instead propose/use the smallest controlled DEV-data cleanup mechanism that:

- changes the test record to terminal RECHAZADO;
- records who performed the cleanup;
- records when;
- records why;
- keeps before/after evidence;
- does not masquerade as normal business history.

If that requires a new permanent production feature or migration:

STOP for Owner approval instead.

============================================================
18. LOCAL ONLY
============================================================

Any known-row regularization in this STEP applies ONLY to:

    local isolated DB :3310

Do NOT modify Shared DEV :3308.

The corresponding Shared DEV example-data cleanup can be handled separately
after the release migration or in an explicit DEV cleanup STEP.

============================================================
19. MODERN TESTS
============================================================

Prove with synthetic data:

A.
Submit Expense.

B.
Observe Expense.

Require:

    state = OBSERVADO
    OBSERVED event exists.

C.
OBSERVED event:

    actor = authenticated UserAccount
    timestamp = canonical current time
    reason/detail persisted.

D.
Force history persistence failure.

Require:

    transaction rollback
    Expense NOT OBSERVADO.

E.
Normal OBSERVADO correction remains valid.

F.
RECHAZADO remains terminal.

G.
Tenant isolation.

============================================================
20. DO NOT REOPEN OTHER ACCEPTED DOMAINS
============================================================

Do NOT change:

- V62
- V63
- Case-level rendition
- multiple Advances
- return/reimbursement
- Case closure financial rules
- FIFO removal
- reports financial equations

============================================================
21. FINAL_12 BASELINE
============================================================

FINAL_12 remains accepted for migrations and Case-level financial behavior.

If backend changes only in review-history atomicity:

run affected:

- gm-expenses review tests
- Host review real-DB tests
- relevant Studio contracts

Do not repeat V43→V63 migration rehearsal unless migration bytes change.

Use VERIFIED_BASELINE_REUSE.

============================================================
22. CANONICAL DOCUMENTATION
============================================================

Append/document:

A. Environment safety rule:

    Local development must never inherit Shared DEV datasource globally.

B. UI rule:

    Conciliado and Uso are independent indicators.

C. Review integrity rule:

    Modern OBSERVADO requires immutable OBSERVED event atomically.

If the known record is classified legacy test data:

document it as DEV cleanup evidence, not as a normal product state-machine rule.

Reglas.md remains append-only.

============================================================
23. REQUIRED REPORT
============================================================

Return:

STATUS=
READY_FOR_OWNER_PRE_COMMIT_HARDENING_REVIEW

STEP=
GYPPORT_PRE_COMMIT_ENV_UI_AUDIT_HARDENING_13

ENVIRONMENT:
USER_SHARED_DEV_DATASOURCE_REMOVED=
MACHINE_SHARED_DEV_DATASOURCE_FOUND=
LOCAL_LAUNCHER_TARGET=
LOCAL_SHARED_DEV_START_GUARD=
PLAIN_SHELL_INHERITS_SHARED_DEV=
BACKEND_CONNECTIONS_3310=
BACKEND_CONNECTIONS_3308=
LOCAL_DB_VERSION=V63
SHARED_DEV_VERSION=V43

DUAL_BARS:
DUAL_PROGRESS_INDICATORS=
CLOSED_CONCILIATED_BAR=
USAGE_BAR=
USAGE_110_TEXT_PRESERVED=
ZERO_DELIVERED_USAGE=
RESPONSIVE_RESULTS=

REVIEW_INTEGRITY:
KNOWN_EXPENSE_CLASSIFICATION=
CURRENT_CODE_CAN_CREATE_OBSERVED_WITHOUT_HISTORY=
OBSERVE_TRANSACTION_ATOMIC=
OBSERVED_ACTOR_SOURCE=
OBSERVED_TIMESTAMP_SOURCE=
AUDIT_FIELDS=
AUDIT_GAPS=
KNOWN_TEST_EXPENSE_ACTION=
KNOWN_TEST_EXPENSE_FINAL_STATE=
HISTORICAL_ACTOR_FABRICATED=NO
HISTORICAL_TIMESTAMP_FABRICATED=NO

TEST_RESULTS=

BACKEND_FINANCIAL_RULES_CHANGED=NO
MIGRATION_CREATED=NO

SHARED_DEV_MODIFIED=NO
FILES_STAGED=0
COMMITS=NONE
PUSH_PERFORMED=NO

READY_FOR_CONTROLLED_COMMIT_GATE=YES/NO

STOP_FOR_OWNER_REVIEW=YES
