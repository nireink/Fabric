# GM_EXPENSES_V65_CONTROLLED_COMMIT_GATE_26 — record (2026-09-17)

```text
TRACK=GM_EXPENSES_RELEASE_READINESS
STEP=GM_EXPENSES_V65_CONTROLLED_COMMIT_GATE_26
MODE=CONTINUE_FROM_CURRENT_STEP -> VERIFY_EXISTING_V65_WORK -> CONTROLLED_COMMIT -> STOP_BEFORE_DEPLOYMENT
PROMPT_SOURCE=Fabric/Knowledge/00-GYPPORT-UNIVERSE/steps/GM-EXPENSES-RELEASE-READINESS/GM_EXPENSES_V65_CONTROLLED_COMMIT_GATE_26.md
STATUS=COMMITTED_LOCALLY_WAITING_OWNER_REVIEW
REIMPLEMENTED_FROM_SCRATCH=NO  PUSH_PERFORMED=NO  DEPLOYMENT_PERFORMED=NO  SHARED_DEV_MODIFIED=NO  OWNER_CASE_MODIFIED=NO
```

## 1. Continuity (§0, §2, §3)

```text
CURRENT_STEP_FOUND=GM_EXPENSES_V65_EXP_DISPLAY_CORRECTION_25A, READY_FOR_OWNER_REVIEW
PREVIOUS_STEP_25_FOUND=YES (prompt, evidence folder PERMANENT-EXPEDIENTE-SEQUENCE-V65-25-2026-09-17)
PREVIOUS_STEP_25A_FOUND=YES (prompt, evidence folder V65-EXP-DISPLAY-CORRECTION-25A-2026-09-17)
BASELINE gm-expenses master 874a3e5071e4..., Gystigo feature/gm-fleets-minimum-vehicle-master-01 0293ff45e94b...,
         Fabric main 018ea843b6bb... - all as expected, nothing staged
EXISTING_V65_IMPLEMENTATION_PRESENT=YES - verified in the bytes: ExpenseSequence, ExpenseSequencePort,
         JdbcExpenseSequenceRepository (tenant-keyed upsert), the allocation in ExpenseCaseService, expense_sequence in the
         repository, V65 (column, tenant+sequence unique key, created_at/id backfill, immutability trigger), the payload's
         expenseSequence, the permanent-sequence race test, and Studio's expenseSequenceOf / caseTitle on the card and
         the detail heading with the ID still read from caseNumber
```

## 2. Evidence reuse (§4, §5)

```text
V64_SHA256=95dc6f57abf5609c198634c1fb036682d4cd512af0a9c06cc272338992c5fd21 (unchanged)   V64_UNCHANGED=YES
V65_SHA256=8ed3c20b1b45af4f832623992882612f4fe78d8327b31d8cb3a90a245e1962b4 = staged blob = rehearsed file
MODULE   newest source 20:55:21 < green run 20:56:49            -> 780/780 REUSED
HOST     newest source 20:48:46 < green run 20:53:45            -> 107/107 REUSED
         its module jar (installed 20:49:21) versus the build from the committed 39a2adf: 261 of 261 classes
         byte-identical, so the Host evidence applies to the committed bytes as they are
STUDIO   newest source 21:04:52 < green run 21:04:55            -> 652/652 and ESLint REUSED
V65      mtime 20:47:26 < rehearsal 20:55:38                     -> V64 -> V65 rehearsal and concurrency REUSED
TESTED_BYTES_UNCHANGED=YES
SECRET_SCAN=PASS (53 accepted files; the only match is the untouched synthetic registration password of an
         @example.test account in ExpenseCaseHttpApiTest, outside this change)
```

## 3. Worktree (§6)

Full table: `dirty-worktree-classification.md`; staging lists: `accepted-paths/`.

```text
CURRENT_DIRTY_PATHS=46   ACCEPTED_PATHS=31   UNRELATED_WIP_PATHS=15   UNKNOWN_PATHS=0   GENERATED_RUNTIME=0
A  V65 implementation (gm-expenses 9, Gystigo V65 + Host + tests + Studio V65 parts)
B  STEP 25A Studio correction (ExpenseCaseDetailPage.jsx, fixtures and contracts it extended)
C  STEP 24 deployment evidence (its prompt, its evidence folder, CURRENT_STEP.md)
D  STEP 25 / 25A documentation and evidence (Reglas.md, the two baselines, prompts, evidence folders)
E  unrelated WIP: Gystigo 5 (README deletion, AuthPage.css, ShortRegisterPage.jsx, the branding fixture pair),
   Fabric 10 (untracked Knowledge folders)
```

## 4. The commits

```text
GM_EXPENSES  39a2adf4dfff0196208a1f80719be1c12c047ac2   9 files, +236 -25   unrelated staged 0   worktree clean
             feat(expenses): permanent expediente sequence per tenant
             BUILD from the committed HEAD: mvnw -o clean install -DskipTests = PASS,
             jar sha256 34df3b9528f98028524ed7d2c4531411cc10b4c50a443a7709933f6cb4e22776
GYSTIGO      5eed5d692342cc889f2afff7a6c4f7f6b5cca1dc   12 files, +371 -84  unrelated staged 0
             feat(expenses): permanent expediente numbering in V65, the API and Studio
FABRIC       committed third with this record, the STEP 24, 25, 25A and 26 prompts and evidence, Reglas.md, the two
             gm-expenses baselines and CURRENT_STEP
```

## 5. Runtime after the gate — deliberately unchanged

```text
SHARED_DEV_VERSION=64   V65_DEPLOYED=NO   OFFICIAL_BACKEND=gystigo-backend:4.1.0-java25-gm-expenses-v64-0293ff4
REAL_APP_EXPECTED_TO_SHOW_EXP_BEFORE_DEPLOYMENT=NO - 8080 sends no expenseSequence until V65 is deployed
RUNTIME_OBSERVATION=the three DEV containers (backend, MySQL, Mailpit) were started again at 2026-09-18T02:32Z with
                    restart count 0 - the same backend container created by STEP 24 on the same V64 image, restarted with
                    Docker or the host, not redeployed; Shared DEV read-only check: Flyway 64, no expense_sequence column
AFTER DEPLOYMENT, by real creation order: Compra Filtro EXP. 08 (ID 202609170001), VIAJE QUITO EXP. 09 (ID 202609170002)
OWNER_CASE_MODIFIED=NO (its two RETURN_REGISTERED events still total USD 300.00)
NEXT_STEP=GM_EXPENSES_V65_SHARED_DEV_DEPLOYMENT_27
```

## 6. Line endings and whitespace (Reglas, controlled-commit rule)

Four evidence files were written by PowerShell with CRLF and Git normalized them to LF on staging, which the
canonical rule accepts:

```text
FILE=PERMANENT-EXPEDIENTE-SEQUENCE-V65-25-2026-09-17/host-expenses-realdb-result.json
  PRE_STAGE_WORKTREE_SHA256=da171bda653dbf7c96fb7d971ce9a8d315641c60c376c5b4c7cf6526d4971aca
  STAGED_BLOB_SHA256=2c07fafe7433ebe1df5bc03d1ee63041709530f5c0ac6ba3b15ef95a79c56027
  NORMALIZATION=CRLF_TO_LF
FILE=SHARED-DEV-V64-DEPLOYMENT-24-2026-09-17/artifact-proof.txt
  PRE_STAGE_WORKTREE_SHA256=5b5d77ea21d78972cbb7859843c09f15a1e87bf92c646cb1f91ea0652625be37
  STAGED_BLOB_SHA256=c05c5981848f4dde1412992cfd880a7bd40304a502288484392df3c439ec6453
  NORMALIZATION=CRLF_TO_LF
FILE=SHARED-DEV-V64-DEPLOYMENT-24-2026-09-17/reversal-capability-results.txt
  PRE_STAGE_WORKTREE_SHA256=f07999f8be112225ed1075916d2b1865ba4312a38a6f3bcfe3af961f9e55cf00
  STAGED_BLOB_SHA256=93ef79b10be17f9e11aae2ee9e1a38809d7d67de28b7b1e83f6daac2fad098e0
  NORMALIZATION=CRLF_TO_LF
FILE=SHARED-DEV-V64-DEPLOYMENT-24-2026-09-17/smoke-results.txt
  PRE_STAGE_WORKTREE_SHA256=001fc390621cd2de91ea824ab9f22da0b14d5a8b00f5a12c5005470749dfe8d0
  STAGED_BLOB_SHA256=7c0b70f5f30b336aa68cc927ac259e3ce91a5898d5bf4860945be7c9516cf5d6
  NORMALIZATION=CRLF_TO_LF
```

`git diff --cached --check` flags three lines of trailing whitespace, all inside captured program output
committed byte-exact as evidence: the Flyway log extract of the V65 rehearsal (a log line cut at 220 columns),
a Spring warning line in the STEP 24 migration log, and a FAIL line of the STEP 24 reversal smoke whose detail
was empty. The authored documents are clean - the extra blank line at the end of the persistence baseline was
removed before this commit.
