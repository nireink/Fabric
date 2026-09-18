# GM_EXPENSES_PERMANENT_EXPEDIENTE_SEQUENCE_V65_25 — record (2026-09-17)

```text
TRACK=GM_EXPENSES_RELEASE_READINESS
STEP=GM_EXPENSES_PERMANENT_EXPEDIENTE_SEQUENCE_V65_25
MODE=AUDIT_CURRENT_V64_MODEL -> IMPLEMENT_V65 -> VERIFY -> DISPOSABLE_REHEARSAL -> OWNER_REVIEW
PROMPT_SOURCE=Fabric/Knowledge/00-GYPPORT-UNIVERSE/steps/GM-EXPENSES-RELEASE-READINESS/GM_EXPENSES_PERMANENT_EXPEDIENTE_SEQUENCE_V65_25.md
STATUS=READY_FOR_OWNER_REVIEW
FILES_STAGED=0  COMMITS_CREATED=0  PUSH_PERFORMED=NO  SHARED_DEV_MODIFIED=NO  DEPLOYMENT_PERFORMED=NO
```

## 1. Baseline and audit (§8, §37)

```text
gm-expenses master 874a3e5071e46b179444730089d34afa5fe0e742   Gystigo feature/gm-fleets-minimum-vehicle-master-01
0293ff45e94b2ebbec67e792fea28e7b80bc8901   Fabric main 018ea843b6bbb86f4e47c3ad43edb42ac7f7ffe5   Shared DEV V64
EXISTING_CASE_SEQUENCE_FIELD=expense_case.case_sequence (SMALLINT UNSIGNED, 1..9999 per tenant + business date)
EXISTING_CASE_NUMBER_FIELD=expense_case.case_number (CHAR(12) STORED, generated from the date and case_sequence)
EXISTING_BUSINESS_DATE_FIELD=expense_case.case_business_date (DATE)
EXISTING_DAILY_COUNTER_TABLE=expense_case_number_sequence (tenant_id, case_business_date, last_sequence)
CASE_CREATION_TRANSACTION_BOUNDARY=ExpenseCaseService.create (@Transactional, inside the idempotency guard)
V64_SHA256_BEFORE=95dc6f57abf5609c198634c1fb036682d4cd512af0a9c06cc272338992c5fd21
V64_SHA256_AFTER=95dc6f57abf5609c198634c1fb036682d4cd512af0a9c06cc272338992c5fd21   V64_UNCHANGED=YES (empty git diff)
```

## 2. The model

```text
UUID               technical identity, routes only
expense_sequence   permanent number of the Case inside its TENANT            -> EXP. NN   (new, V65)
case_sequence      the Case's number within TENANT + BUSINESS_DATE           -> composes the ID (V64, unchanged)
case_number        YYYYMMDD#### = case_business_date + case_sequence         -> ID: ...   (V64, unchanged)
```

The two sequences are two counters and never one: `expense_sequence` takes no part in `case_number`, and
`case_sequence` no longer decides EXP. A new business day restarts only `case_sequence`.

## 3. What changed

```text
V65          expense_case.expense_sequence INT UNSIGNED NOT NULL, CHECK >= 1, UNIQUE (tenant_id, expense_sequence);
             expense_case_permanent_sequence (tenant_id PK, last_sequence, updated_at), CHECK >= 1;
             deterministic backfill by tenant, created_at, expense_case_id; counter seeded at each tenant's maximum;
             trg_expense_case_expense_sequence_immutable and trg_case_permanent_sequence_no_delete
             sha256 8ed3c20b1b45af4f832623992882612f4fe78d8327b31d8cb3a90a245e1962b4
gm-expenses  ExpenseSequence (value object), ExpenseSequencePort, JdbcExpenseSequenceRepository (the V64 upsert pattern
             on its own tenant-keyed counter); ExpenseCase carries expenseSequence; ExpenseCaseService allocates it inside
             the creating transaction, the tenant's permanent row first; JdbcExpenseCaseRepository writes and reads it;
             CaseNumber javadoc corrected
Host         ExpenseCaseConfig wires the port; the Case payload (list and detail) adds expenseSequence and keeps
             caseSequence, caseNumber, businessDate and the UUID
Studio       expenseSequenceOf() replaces caseSequenceOf(); caseTitle() reads expenseSequence with no daily fallback -
             a payload without it shows no EXP; fixtures carry both numbers; card comment corrected
```

Transaction semantics (§17): both counters are advanced in the creating transaction. A creation that rolls back also
rolls its counter back, so the committed permanent numbers run without holes; a committed number is never handed out
again, because the next allocation always reads the committed counter under the row lock.

## 4. Tests

```text
GM_EXPENSES=780/780 in 86 classes (773 + ExpenseSequenceTest 3 + 4 service scenarios: keeps counting across business
            days, a retroactive business date still takes the next number, another tenant counts from one, closing the
            Case keeps its number)
HOST_REAL_DB=107/107, flywayMax=65 (106 + the permanent-sequence race); the payload assertions add expenseSequence
            1 then 2, list == detail, another tenant 1. The only later edit in the Host's module dependency was a
            javadoc: CaseNumber.class is byte-identical before and after it.
HOST_TARGETED=thePermanentSequenceSurvivesAConcurrentRaceAndWhatItAssignedIsImmutable - 8 threads on their own
            connections, tenant-keyed row: 8 distinct allocations 1..8, counter = 8, no duplicate; UPDATE of
            expense_sequence refused by the database
STUDIO=649/649 in 53 files (EXP from expenseSequence, no daily fallback, sort and filter never renumber, date
            independence EXP. 07 / 202609170003 then EXP. 08 / 202609180001, 1 -> EXP. 01, 100 -> EXP. 100,
            101 -> EXP. 101); ESLint clean
```

## 5. V64 -> V65 rehearsal on a disposable copy of today's Shared DEV (§34, §35)

Migrated by the Host application's own Flyway, exactly as a deployment would (log extract:
`v65-rehearsal-flyway-extract.txt`; full result: `v65-rehearsal-result.txt`).

```text
RESTORED=Shared DEV at V64, 35 Cases; plus 5 synthetic Cases in a synthetic tenant for the order rule
Migrating schema to version "65 - gm expenses case permanent sequence" -> now at v65 (1.259 s)
FLYWAY_MAX=65  FAILED=0  V65_SUCCESS=1
TOTAL_CASES=40  WITH_EXPENSE_SEQUENCE=40  NULL_EXPENSE_SEQUENCE=0  DUPLICATE_TENANT_EXPENSE_SEQUENCE=0
ORDER_MISMATCHES=0 against ROW_NUMBER() OVER (PARTITION BY tenant ORDER BY created_at, expense_case_id), every tenant
TENANTS=12  COUNTER_ROWS=12  COUNTER_GAPS=0
SYNTHETIC  A 10:00 (business date 17) -> EXP 1 | B 11:00 (date 13) -> EXP 2 | C 12:00 (date 17) -> EXP 3
           D and E, same created_at -> EXP 4 and 5 by technical id
FINANCIAL_CHECKSUMS_IDENTICAL=YES   BUSINESS_NUMBERS_AND_CREATED_AT_UNCHANGED=YES   V64_HISTORY_ROW_UNCHANGED=YES
EXPENSE_SEQUENCE_IMMUTABLE=YES   COUNTER_CONTINUES_AFTER_BACKFILL=6   COUNTER_DELETE_REFUSED=YES
```

The Owner's tenant, in real creation order:

```text
EXP 1 Viaje los encuentros 202608310001 | EXP 2 Viaje A Loja 202608310002 | EXP 3 Viaje Zamora 202609010001
EXP 4 SUSCRIPCION IA 202609020001 | EXP 5 Compra Camaras 202609030001 | EXP 6 PRUEBA20260909 202609100001
EXP 7 Viaje Loja 202609130001 | EXP 8 Compra Filtro 202609170001 | EXP 9 VIAJE QUITO 202609170002
OWNER_CASE 437a92bf = Compra Filtro -> expense_sequence 8 (EXP. 08), business date 2026-09-17, case_sequence 1,
                     ID 202609170001; its two RETURN_REGISTERED events still total USD 300.00
```

The prompt's illustration placed Compra Filtro at EXP. 02; the Owner's own rule - "the exact historical assignment
MUST follow real creation order" - makes it EXP. 08, because seven Cases of that tenant were created before it.

## 6. Source control

```text
CURRENT_DIRTY_PATHS=43 (gm-expenses 9, Gystigo 16, Fabric 18 incl. this evidence folder)  UNKNOWN=0  FILES_STAGED=0
STEP_24 uncommitted deployment evidence kept: its prompt, its evidence folder and CURRENT_STEP.md (refreshed here)
UNRELATED_WIP=15, untouched
```
