# GM_EXPENSES_STEP18_EVIDENCE_RECOVERY_31 — record (2026-09-18)

```text
TRACK=GM_EXPENSES_RELEASE_READINESS
STEP=GM_EXPENSES_STEP18_EVIDENCE_RECOVERY_31
MODE=READ_ONLY_DISCOVERY -> EXACT_SOURCE_RECOVERY -> HASH_AND_PROVENANCE_VERIFY -> BOXGHOST_EVIDENCE_RECONCILIATION
     -> CONTINUITY_CLOSEOUT -> CONTROLLED_FABRIC_COMMIT -> PUSH
PROMPT_SOURCE=Fabric/Knowledge/00-GYPPORT-UNIVERSE/steps/GM-EXPENSES-RELEASE-READINESS/GM_EXPENSES_STEP18_EVIDENCE_RECOVERY_31.md
STATUS=EVIDENCE_RECOVERED_AND_TRACK_CLOSED (committed with this record, then pushed as a normal fast-forward)
NATURE=historical evidence reconciliation; no source, database, runtime or application behavior changed
SOURCE_CODE_CHANGED=NO   SHARED_DEV_MODIFIED=NO   OWNER_CASE_MODIFIED=NO   REGLAS_CHANGED=NO
```

Labels follow §11 of the prompt:
- FACT: recorded by the original STEP's evidence or checked today against a repository or file.
- RECOVERED_FACT: supported by a surviving exact artifact.
- DERIVED: calculated today from immutable evidence.
- INFERENCE: plausible but not provable.

## 1. Pre-state (§2, FACT)

```text
GM_EXPENSES master 39a2adf4dfff0196208a1f80719be1c12c047ac2 = origin/master, clean
GYSTIGO     master 5eed5d692342cc889f2afff7a6c4f7f6b5cca1dc = origin/master; the 5 unrelated WIP paths (README.md deleted,
            AuthPage.css and ShortRegisterPage.jsx modified, two untracked header-branding fixtures), untouched
FABRIC      main   165bc9227d4875f35d158b91a539c9dd211d70b6 = origin/main; untracked = the 2 Owner WIP files
UNKNOWN_PATHS=0
```

## 2. STEP 18 - sources (§3 - §5)

```text
SEARCHED                                                                FOUND
GYPPORT_STORAGE/Restricted/Gystigo/shared-dev-deployment-18-2026-09-17/ 97 files: the V43 dump and an evidence/ tree of 96 files
this session's scratchpad s18/ (STEP 18's working folder)               96 files: 95 byte-identical to the restricted copies, 1 .pyc
session transcript 6bd391c2, line 4181                                  the STEP 18 Owner prompt
Fabric, committed                                                       7 files that cite STEP 18; no STEP 18 evidence file
Gystigo: tracked files, docs/, working-tree changes                     nothing
rest of GYPPORT_STORAGE, %LOCALAPPDATA%\Temp\gypport,
the 178 other session folders under the Claude temp directory           nothing named for STEP 18
```

```text
A CANONICAL_EVIDENCE_ALREADY_IN_BOXGHOST     0
B MISSING_CANONICAL_EVIDENCE_RECOVERABLE    96   the restricted evidence tree, recovered
C SENSITIVE_RAW_EVIDENCE_RESTRICTED_ONLY     1   the V43 dump: restricted pointer only
D DUPLICATE_BYTE_IDENTICAL                  95   scratchpad copies of B files, not copied again
E SUPERSEDED_DERIVED_OUTPUT                  1   compiled bytecode of s18_db.py
F UNVERIFIABLE                               0
G UNKNOWN                                    0
```

The per-file classification is `classification.tsv`. `sensitivity-scan.tsv` holds only counts for each pattern.
The three flagged files were reviewed without printing any value. So were the logs, pre-checks, the container file and
the legacy audit. The results are in section 4 of the STEP 18 recovery record. A file counts as A only when a
byte-identical copy already sits in a STEP 18 folder. The 18 twins found in other STEPs' folders are therefore noted
but still recovered: 12 are FINAL_12 outputs and 6 are empty files.

## 3. BoxGhost recovery (§6 - §8)

```text
DESTINATION=gm-ai-boxghost/tracks/GM-EXPENSES-RELEASE-READINESS/evidence/SHARED-DEV-DEPLOYMENT-18-2026-09-17/
LAYOUT=recovered-from-restricted/<original relative path>; provenance kept, nothing flattened
INDEX=RECOVERY_INDEX.tsv: ORIGINAL_SOURCE_PATH, DESTINATION_PATH, BYTES, SHA256_SOURCE, SHA256_DESTINATION, HASH_MATCH, KIND
RECOVERED=96 (1 ORIGINAL_HISTORICAL_EVIDENCE + 95 RECOVERED_COPY), 571,763 bytes   RECOVERY_HASH_MISMATCHES=0
ORIGINAL_STEP18_RECORD=DEPLOYMENT_18_RECORD.md, preserved byte-exact
RECOVERY_RECORD=GM_EXPENSES_STEP18_EVIDENCE_RECOVERY_RECORD_2026-09-18.md (DERIVED; never presented as the original)
DUMP=pointer only: logical location, file name, SHA-256 eb5f88d8..., 838,347 bytes, STEP 18, SENSITIVE_ARCHIVE
RESTRICTED_SOURCE_UNCHANGED=YES (copies only; 97 of 97 files re-hashed equal to discovery)
STEP18_HISTORY_COMPLETE=YES (the original record, the complete evidence tree and the exact prompt)
```

## 4. Prompts (§9, §10)

```text
STEP                                          TRANSCRIPT LINE  MESSAGE TIMESTAMP (UTC)   CHARS  PROMPT_TEXT_SHA256  RECOVERY
GM_EXPENSES_SHARED_DEV_DEPLOYMENT_18                4181       2026-09-17T16:08:11.892Z  11499  c8f4d30179cc...     EXACT
GM_EXPENSES_FINAL_PUSH_GATE_29                     10782       2026-09-18T04:31:09.717Z   7817  ca35e34cbf9a...     EXACT
GYPPORT_POST_MVP_WORKTREE_CLASSIFICATION_29C       11137       2026-09-18T05:14:18.240Z   5137  e52ae3ff4de1...     EXACT
GM_EXPENSES_STEP18_EVIDENCE_RECOVERY_31            11885       2026-09-18T11:34:10.287Z  14932  0aa4ed62de48...     stored at execution
STEP29_PROMPT_RECOVERY=EXACT   STEP29C_PROMPT_RECOVERY=EXACT
```

Each prompt was extracted programmatically from the Owner's message in session transcript 6bd391c2 and never
retyped. Each stored file carries the full SHA-256, the message identity and the verbatim text.
`prompt-verification.txt` records the checks (RECOVERED_FACT):
- A prompt is identified by its own header: the first line that is exactly `STEP=`, and the next line.
- Across all 110 local session transcripts, each header occurs in exactly one message.
- Each stored body re-hashes to the PROMPT_TEXT_SHA256 in its header.

A header's DATE is the UTC date of the message. This machine runs at UTC-05:00. STEP 29's message (04:31Z) was
therefore sent on 2026-09-17 at 23:31 local time, the date the 29B record gives STEP 29.

Correction made during this STEP (FACT):
- The first extraction (`tooling/store_prompts.py`) located each prompt by the text `STEP=` followed by the id.
- For STEP 31, that text also appears in the closing line of STEP 30's prompt:
  `NEXT_OPTIONAL_STEP=` followed by `GM_EXPENSES_STEP18_EVIDENCE_RECOVERY_31`.
- As a result, STEP 30's text was first written under STEP 31's file name.
- The header check found the error before anything was staged.
- The untracked file was deleted. STEP 30's prompt is already committed verbatim as
  `GM_EXPENSES_RESTRICTED_BACKUP_ARCHIVAL_30.md`.
- STEP 31's prompt was then stored from its own message (`tooling/store_prompt31.py`).
- The three recovered prompts passed the same check unchanged.

## 5. Result coverage of STEPs 29, 29B, 29C and 29D (§13)

```text
STEP 29   frozen commits pushed, Gystigo branch        29B record lines 24-28: gm-expenses master 7bad5b0..39a2adf, Fabric main
          published, no force                          1798ac4..d99e99a, Gystigo as a new remote branch at 5eed5d6, "without
                                                       force", 177-commit pre-push audit                                    COMPLETE
STEP 29B  accepted Gystigo history on master,          29B record line 9 STATUS=MASTER_INTEGRATED_FEATURE_CLOSED, line 11
          feature branch closed                        FORCE_PUSH_USED=NO; today origin has only master, at 5eed5d6        COMPLETE
STEP 29C  VS Code 36 = Fabric 31 + Gystigo 5           29D record line 20 (31 of 31 paths) and lines 23-27 (8 folders +
                                                       2 files = 10)                                                        COMPLETE
STEP 29D  Fabric 31 reconciled to 2 Owner WIP files    29D record line 8 STATUS=RECONCILED, lines 139-144 and 153; today
                                                       Fabric's untracked files are exactly those two                      COMPLETE
RESULT_HISTORY_COMPLETE=YES
```

The three gaps named in the prompt are closed: A, the STEP 18 evidence (section 3); B, the STEP 29 prompt; and C, the
STEP 29C prompt (section 4).

## 6. Agent-governance observation - closeout (§14)

```text
FINDING="Should AGENTS.md reference the three AI policies?"
DISPOSITION=ALREADY_RESOLVED_BY_CANONICAL_MEMORY_FOUNDATION
AI_GOVERNANCE_REFERENCE_WIRING=ALREADY_RESOLVED   NEW_AGENTS_EDIT_REQUIRED=NO   AGENT_GOVERNANCE_EDITED=NO
```

1. The 2026-09-08 AGENTS policy named all three AI policies (RECOVERED_FACT).
   - The archived GYPPORT_STORAGE snapshots `Gystigo/Nueva carpeta/AGENTS BACKUP_20260909.md`,
     `CHATGPT BACKUP_20260909.md` and `CLAUDE BACKUP_20260909.md` were modified on 2026-09-08 at 14:45 local time. Each
     names every policy three times. So do the later `*_BACKUP_20260910.md` copies in the same folder, modified on
     2026-09-09 at 10:21 and 2026-09-10 at 12:43.
   - Session transcript 454a94c1 read `Gystigo/AGENTS.md`, `CHATGPT.md` and `CLAUDE.md` between 2026-09-08T19:50:16Z
     and 19:50:53Z. Each returned text named all three policies.
   - `CLAUDE.md` still named them on 2026-09-10 at 12:15Z and 12:29Z (sessions baf848a7 and f606bf51).
   - Context (FACT): the versions from 09:01 to 09:23 that morning, and the "FN" copies from 15:15, name only the
     efficiency policy. The snapshots from 2026-09-10 19:06 and 2026-09-15 name none. Gystigo's history holds no
     commit that adds or removes any of the three names in AGENTS, CLAUDE or CHATGPT (`git log -S`: 0 for each).
   - Sources: `governance-snapshots.tsv` and `governance-reads.txt`.
2. Universal governance later took on the same agent rules (DERIVED).
   - `agents/AGENTS.md` line 340, the Mandatory Conflict Gate: "A finding or technical contradiction does not
     authorize an agent to resolve it autonomously".
   - The 2026-09-13 universal data-domain context, line 273: `DO_NOT_PICK_OPTION_AUTONOMOUSLY=YES`.
3. The Canonical Memory Foundation moved authoritative agent governance to Fabric (FACT).
   - `GYPPORT_MEMORY_ARCHITECTURE.md` line 18: `FABRIC_IS_SINGLE_GYPPORT_MEMORY_ROOT=YES`.
   - The canonical agent root is `Fabric/Knowledge/00-GYPPORT-UNIVERSE/agents/` (lines 282 and 360).
4. The Gystigo files became technical discovery entrypoints (FACT). Line 3 of both `Gystigo/AGENTS.md` and
   `Gystigo/CLAUDE.md` says "permanent technical entrypoint".
5. `AGENT_AUTO_DISCOVERY_ENABLED=YES` was verified (FACT):
   - `Reglas.md` line 780, in the entry at line 760 (2026-09-15);
   - `GYPPORT_CANONICAL_MEMORY_FOUNDATION_CLOSEOUT_VERIFIED_BASELINE_2026-09-15.md` line 102;
   - `GYPPORT_CANONICAL_MEMORY_FOUNDATION_VERIFIED_BASELINE_2026-09-15.md` line 549;
   - `gm-ai-boxghost/tracks/GYPPORT-CANONICAL-MEMORY-FOUNDATION-01/evidence/VALIDATION_RESULTS.md` line 81.
6. STEP 29D revalidated the three documents (FACT). Its record, lines 34-37, gives each one as
   `STILL_VALID_SUPPORTING_KNOWLEDGE`, committed under `Knowledge/AI/`, with `CONFLICTS_WITH_NEWER_OWNER_RULES=0`.

The canonical `agents/` files carry the rules themselves (point 2) rather than the three file names. The documents
remain committed supporting knowledge (point 6). No agent file was touched, and no CHATGPT.md, CODEX.md or second
CURRENT_STEP.md was created.

## 7. Continuity and rules (§15, §16)

`Fabric/tools/continuity/Set-GypportCurrentStep.ps1` regenerated the existing
`Fabric/Knowledge/00-GYPPORT-UNIVERSE/active-work/CURRENT_STEP.md` in place, with:
- GM_EXPENSES_RELEASE_READINESS=COMPLETE
- GM_EXPENSES_MVP_STATUS=FROZEN_OWNER_ACCEPTED_PUSHED
- BACKUP_ARCHIVAL_30=COMPLETE
- HISTORICAL_EVIDENCE_RECOVERY_31=COMPLETE
- the remaining independent pre-production debt, SPRING_GENERATED_PASSWORD_STARTUP_LOG
- NEXT_GM_EXPENSES_STEP=NONE

No other gm-expenses STEP was started. `Reglas.md` is unchanged (REGLAS_CHANGED=NO): recovering evidence is not a new
Owner decision.

## 8. Staging and line endings (§17, §18)

```text
STAGED=the STEP 18 evidence folder (96 recovered files, RECOVERY_INDEX.tsv, its recovery record), this folder,
       the 4 stored prompts and the existing CURRENT_STEP.md; each file named explicitly
OWNER_WIP_STAGED=0   UNKNOWN_STAGED=0   SQL_FILES_STAGED=0
```

- Twenty-one recovered files use CRLF, and Git stores them with LF under `text=auto eol=lf`. Reglas.md accepts this in
  its 2026-09-17 entry "Regla de fin de línea en commits controlados".
- `line-ending-normalization.tsv` gives each file's PRE_STAGE_WORKTREE_SHA256 and STAGED_BLOB_SHA256 with
  NORMALIZATION=CRLF_TO_LF. The tooling predicted both from the working tree, and the staged blobs confirmed them.
- Every other staged blob equals its working-tree bytes.

```text
STAGED=120 = LISTED=120   BLOB_PREDICTION_MISMATCHES=0   NORMALIZED_BLOBS=21
GIT_DIFF_CACHED_NAME_STATUS=119 A + 1 M (CURRENT_STEP.md)
OWNER_WIP=the 2 files still untracked, SHA-256 equal to the 29D pre-state manifest
```

`git diff --cached --check` flags only bytes kept exact on purpose:
- trailing whitespace in 17 recovered STEP 18 files: the seven module build logs, the Host build log, five deployment
  logs and outputs, two evidence notes and the two writer pre-checks;
- one "leftover conflict marker" at line 39 of `GYPPORT_POST_MVP_WORKTREE_CLASSIFICATION_29C.md`. It is the Owner's
  own `=======` underline of the heading PURPOSE, in the verbatim prompt.

The files written by this STEP are clean.

A credential scan of the 120 staged blobs printed counts only. Apart from two benign pattern matches, it found no
generated-password value, private key, cloud token, JWT, password hash, credential variable value, URL credential or
address outside `@example.test`. The two matches:
- line 47 of `s18-deploy-smoke.ps1` builds the synthetic account's per-run password from NewGuid;
- line 14 of `tooling/sensitivity_scan.py` is the scanner's own regular expression.

## 9. Frozen MVP (§20, read-only)

```text
GM_EXPENSES_HEAD=39a2adf4dfff0196208a1f80719be1c12c047ac2   GYSTIGO_HEAD=5eed5d692342cc889f2afff7a6c4f7f6b5cca1dc
SHARED_DEV Flyway 65, 49 versioned rows, 0 failed
OWNER_CASE: STEP 28's read-only verify-owner-reversal.sh reproduces its post-reversal-state.txt byte for byte (IDENTICAL)
DEV_CONTAINERS gypport-mysql-dev (mysql:8.4.10) and gypport-backend-dev (gystigo-backend:4.1.0-java25-gm-expenses-v65-5eed5d6), healthy
SOURCE_CODE_CHANGED=NO   SHARED_DEV_MODIFIED=NO   OWNER_CASE_MODIFIED=NO
```

## 10. Files of this STEP

```text
evidence/SHARED-DEV-DEPLOYMENT-18-2026-09-17/
  recovered-from-restricted/evidence/...           96 files, byte-exact
  RECOVERY_INDEX.tsv                                DERIVED recovery index
  GM_EXPENSES_STEP18_EVIDENCE_RECOVERY_RECORD_2026-09-18.md
evidence/HISTORICAL-EVIDENCE-RECOVERY-31-2026-09-18/
  this record, classification.tsv, sensitivity-scan.tsv, prompt-verification.txt, governance-reads.txt,
  governance-snapshots.tsv, line-ending-normalization.tsv
  tooling/  discover.py, sensitivity_scan.py, recover.py, extract_prompts.py, store_prompts.py, store_prompt31.py,
            verify_prompts.py, governance_reads.py, governance_snapshots.py, line_endings.py
Knowledge/00-GYPPORT-UNIVERSE/steps/GM-EXPENSES-RELEASE-READINESS/
  GM_EXPENSES_SHARED_DEV_DEPLOYMENT_18.md, GM_EXPENSES_FINAL_PUSH_GATE_29.md,
  GYPPORT_POST_MVP_WORKTREE_CLASSIFICATION_29C.md, GM_EXPENSES_STEP18_EVIDENCE_RECOVERY_31.md
Knowledge/00-GYPPORT-UNIVERSE/active-work/CURRENT_STEP.md (existing file, updated)
```

## 11. For the Owner

```text
GM_EXPENSES_RELEASE_READINESS=COMPLETE   GM_EXPENSES_MVP_STATUS=FROZEN_OWNER_ACCEPTED_PUSHED
ONLY_REMAINING_PRE_PRODUCTION_DEBT=SPRING_GENERATED_PASSWORD_STARTUP_LOG
NEXT_GM_EXPENSES_STEP=NONE
STOP_FOR_OWNER_REVIEW=YES
```
