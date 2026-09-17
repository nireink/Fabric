# GM_EXPENSES_CONTROLLED_COMMIT_GATE_23 — record (2026-09-17)

```text
TRACK=GM_EXPENSES_RELEASE_READINESS
STEP=GM_EXPENSES_CONTROLLED_COMMIT_GATE_23
MODE=READ_ONLY_PRECOMMIT_AUDIT -> EXPLICIT_PATH_STAGING -> COMMIT -> POST_COMMIT_PROOF
PROMPT_SOURCE=Fabric/Knowledge/00-GYPPORT-UNIVERSE/steps/GM-EXPENSES-RELEASE-READINESS/GM_EXPENSES_CONTROLLED_COMMIT_GATE_23.md
STATUS=COMMITTED_LOCALLY_WAITING_OWNER_REVIEW
PUSH_PERFORMED=NO   SHARED_DEV_MODIFIED=NO   DEPLOYMENT_PERFORMED=NO   OWNER_CASE_MODIFIED=NO
```

## 1. Pre-commit baseline (§1) — matched exactly

```text
Modules/gm-expenses  master                                      545eae0fb287f8e04f7f1b4ac73780304ec53f22
Gystigo              feature/gm-fleets-minimum-vehicle-master-01  bcb959158b781e3fcd876bacc6fcf0f1f1c79b9f
Fabric               main                                         bbdd66a0c5a1c9cbb21293beb74c3e5e61cc5de0
```

## 2. Dirty-worktree re-audit (§4)

The audit was taken from the filesystem, not from an earlier count. Full table:
`dirty-worktree-classification.md`; the staging lists it produced: `accepted-paths/`.

```text
CURRENT_DIRTY_PATHS_TOTAL=72   (+2 over STEP 22A: the 22B prompt and its evidence folder)
ACCEPTED_PATHS_TOTAL=57        (gm-expenses 18, Gystigo 23, Fabric 16)
UNRELATED_WIP_PATHS_TOTAL=15   (Gystigo 5, Fabric 10)
UNKNOWN_PATHS=0
GENERATED_RUNTIME=0            (no build output is tracked in any of the three repositories)
```

The STEP 23 records themselves (this folder and the stored prompt) were created during the gate and are committed with
Fabric as its evidence.

## 3. Evidence validity before committing (§7, §9)

```text
gm-expenses   newest accepted byte 17:35:05, module suite ran 17:35:3x  -> TESTED_BYTES_UNCHANGED=YES (reused 773/773)
Studio        three files changed after the 17:31 run (ExpenseCaseListPage.jsx, expenseService.js,
              ChooseCaseForAdvancePage.jsx) -> RERUN: 648/648 in 53 files at 18:13, ESLint clean
Host          its own sources unchanged since 17:34, but the module jar it links against was rebuilt from the commit
              -> RERUN after the install: 106/106, flywayMax 64 (host-expenses-realdb-result-post-commit.json)
V64 rehearsal reused: the migration byte has not changed since the rehearsal
Responsive    reused: 1280 / 768 / 375 / 320 with no horizontal overflow (STEP 22A)
INVALIDATED_TEST_EVIDENCE=NO
```

## 4. V64 proof (§8)

```text
V64_SHA256=95dc6f57abf5609c198634c1fb036682d4cd512af0a9c06cc272338992c5fd21   bytes=7568
V64_MTIME=2026-09-17 16:34:18   REHEARSAL_RUN=2026-09-17 16:42:17
V64_BYTES_UNCHANGED_SINCE_REHEARSAL=YES
STAGED_BLOB_SHA256=95dc6f57abf5609c198634c1fb036682d4cd512af0a9c06cc272338992c5fd21  (no normalization; blob a5b33da)
PRESENT   case_business_date, case_sequence, case_number, expense_case_number_sequence, ROW_NUMBER() backfill,
          uq_case_tenant_business_number, uq_case_tenant_date_sequence, both immutability triggers
ABSENT    any write to settlement_balance_event, advance_settlement, expense or expense_advance; tax_subject;
          organization. "establishment", "RUC" and "document_sequences" appear only in the header comment that says
          they take no part.
```

## 5. Secret scan (§10)

```text
SECRET_SCAN=PASS   (69 accepted files scanned for literal passwords, secrets, tokens, jdbc credentials, private keys)
ONLY_MATCH=ExpenseCaseHttpApiTest.java:1573, the pre-existing synthetic registration password of a throwaway
           @example.test account in the isolated test database - unchanged by this work and not a credential.
```

## 6. The three commits

```text
GM_EXPENSES  874a3e5071e46b179444730089d34afa5fe0e742  tree 88b76271e60819d7cd5531d6ac3127b068e3f3dc
             18 files, +1029 -38   unrelated staged = 0   worktree clean afterwards
             feat(expenses): case business number and reconciliation semantics

MODULE_INSTALL from the committed HEAD: mvnw -o clean install -DskipTests = PASS
             gm-expenses-0.1.0-SNAPSHOT.jar installed 18:15:34,
             sha256 4a887b4c009c56f733e0488857513a91d46fcb68a89ab478ac119fcad64c12f4,
             carrying CaseNumber, BusinessDatePort, CaseNumberSequencePort, JdbcCaseNumberSequenceRepository and
             SettlementBalanceEvent. The Host suite then passed 106/106 against exactly that jar.

GYSTIGO      0293ff45e94b2ebbec67e792fea28e7b80bc8901
             23 files, +1440 -183   unrelated staged = 0
             feat(expenses): expense case business number in the API, V64 and Studio

FABRIC       committed third with this record, the canonical documentation, the append-only Reglas entries, the stored
             Owner prompts 19 to 23, the BoxGhost evidence of 19, 20, 20A, 21, 22, 22A, 22B and 23, and CURRENT_STEP.
```

## 7. Unrelated WIP preserved (§5, §16)

```text
Gystigo  README.md (deleted in the worktree), src/application/AuthPage.css,
         src/application/onboarding/ShortRegisterPage.jsx, fixtures/HeaderBrandingFixture.jsx,
         fixtures/header-branding.html
Fabric   Knowledge/AI/, Knowledge/Architecture/GYPPORT_REGLAS_CANONICAS_ARQUITECTURA_DOMINIO_UIX.md,
         Knowledge/Derived/, Knowledge/Security/, Knowledge/UIX/, Knowledge/gm-accounting/,
         Knowledge/gm-expenses/03-application/, 04-integration/, 05-implementation/, Knowledge/gm-expenses/README.md
```

None of them was staged, deleted, restored, modified, normalized or moved. They stay dirty on purpose.

## 8. Runtime after the gate — deliberately still the old one

```text
SHARED_DEV_VERSION=V63            OFFICIAL_BACKEND=gystigo-backend:4.1.0-java25-gm-expenses-mvp-bcb9591 (STEP 18)
WORKING_COMMITTED_SOURCE_SUPPORTS_CASE_NUMBER=YES
RUNNING_BACKEND_SUPPORTS_CASE_NUMBER=NO
OWNER_CASE_MODIFIED=NO            (its two RETURN_REGISTERED events still total USD 300.00)
NEXT_STEP=GM_EXPENSES_SHARED_DEV_V64_DEPLOYMENT_24
```

## 9. Line endings (Reglas, controlled-commit rule)

Three evidence files were written by PowerShell with CRLF and Git normalized them to LF on staging, which the
canonical rule accepts. Their hashes, as the rule requires:

```text
FILE=FINAL-CASE-CARD-NUMBERING-ALIGNMENT-22A-2026-09-17/host-expenses-realdb-result.json
  PRE_STAGE_WORKTREE_SHA256=de5d4550f634a0d26344f56005be4e4c3dc2310d41979cf9885ef2f5bdc3052d
  STAGED_BLOB_SHA256=9dfd7c33730df6a79f76f976883b06947345c637d01a17ac26bd6fb3cffde6ef
  NORMALIZATION=CRLF_TO_LF
FILE=FINAL-MVP-CLOSURE-22-2026-09-17/host-expenses-realdb-result.json
  PRE_STAGE_WORKTREE_SHA256=5c7cdad6a8e88e4bbb99fdecfda7b6ac8cbcaa7f9e73849c635d5291a2f1217b
  STAGED_BLOB_SHA256=4333231128cf63f6d89a2d51b840a87c8ed6e1420e1234c1160e58b7655c0acc
  NORMALIZATION=CRLF_TO_LF
FILE=CONTROLLED-COMMIT-GATE-23-2026-09-17/host-expenses-realdb-result-post-commit.json
  PRE_STAGE_WORKTREE_SHA256=e7d0e5792d091f760d203eb5d7ac8191c34e34dd59226cca72594895f16908dc
  STAGED_BLOB_SHA256=e8280a45db2b7a0a68262890aca4d976fc355c4292f777af6eb31a4a2b07ec6c
  NORMALIZATION=CRLF_TO_LF
```
