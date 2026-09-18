# GM_EXPENSES_SHARED_DEV_DEPLOYMENT_18 — evidence recovery record (2026-09-18)

```text
RECORD_KIND=DERIVED_RECOVERY_INDEX - written 2026-09-18 by GM_EXPENSES_STEP18_EVIDENCE_RECOVERY_31; not the STEP 18 record
ORIGINAL_STEP=GM_EXPENSES_SHARED_DEV_DEPLOYMENT_18 (2026-09-17)
ORIGINAL_PROMPT=Fabric/Knowledge/00-GYPPORT-UNIVERSE/steps/GM-EXPENSES-RELEASE-READINESS/GM_EXPENSES_SHARED_DEV_DEPLOYMENT_18.md (recovered EXACT)
ORIGINAL_RECORD=recovered-from-restricted/evidence/evidence/DEPLOYMENT_18_RECORD.md (byte-exact)
RECOVERED_FILES=96   RECOVERY_HASH_MISMATCHES=0   INDEX=RECOVERY_INDEX.tsv
```

## 1. What this folder holds

| Layer | Where | What it is |
|---|---|---|
| ORIGINAL HISTORICAL EVIDENCE | `recovered-from-restricted/evidence/evidence/DEPLOYMENT_18_RECORD.md` | the record STEP 18 wrote on 2026-09-17, byte-exact (8,995 bytes, SHA-256 `48b6bdeff910...`, full value in the index) |
| RECOVERED COPY | the other 95 files under `recovered-from-restricted/` | STEP 18's own outputs - build logs, database fingerprints, deployment logs, pre-checks, smoke outputs, tooling - byte-exact, under their original relative paths |
| DERIVED RECOVERY INDEX | this record and `RECOVERY_INDEX.tsv` | written 2026-09-18: source and destination of every file, both SHA-256 values, the match and the kind |

Nothing in this folder was reconstructed from memory. Only the one file marked above is the original record.

## 2. Why STEP 18's evidence was not in BoxGhost

STEP 18's prompt (recovered, exact) says "This STEP must NOT: ... modify Fabric" and puts the backup in a restricted
location - "never Git; never Fabric". STEP 18 therefore kept its whole evidence set beside the dump, in
`GYPPORT_STORAGE/Restricted/Gystigo/shared-dev-deployment-18-2026-09-17/`, and its record ends "No source, Fabric or
documentation change". (FACT, from the recovered prompt and the original record)

## 3. Sources and classification

```text
RESTRICTED folder      97 files   1 dump (C, restricted only) + 96 evidence files (B, recovered here)
SESSION SCRATCHPAD s18 96 files   95 byte-identical to the restricted copies (D, not copied) + 1 compiled .pyc of s18_db.py (E)
SESSION TRANSCRIPT     the STEP 18 Owner prompt (recovered EXACT, stored in steps/)
COMMITTED FABRIC       later records citing STEP 18 facts (section 7); no STEP 18 evidence file was already in Fabric (A=0)
UNVERIFIABLE=0   UNKNOWN=0
```

The per-file classification and the sensitivity counts are committed with STEP 31, in
`../HISTORICAL-EVIDENCE-RECOVERY-31-2026-09-18/classification.tsv` and `sensitivity-scan.tsv`.

## 4. Why the 96 files may live in Fabric (FACT, checked 2026-09-18 without printing any value)

- Pattern scan of all 96 files: 0 generated-password lines, 0 credential variable values, 0 password hashes, 0 tokens,
  0 session cookies, 0 URL credentials, 0 private keys. The only e-mail addresses are `@example.test` ones.
- Four pattern matches were reviewed without printing any value. Three files match the name "Viaje Loja" once each.
  It is the smoke's synthetic "S18 Viaje Loja" Case, not an Owner Case. One line in `s18-deploy-smoke.ps1` matches a
  password pattern: it builds a fresh random password on each run ('<prefix>' + NewGuid) for the synthetic
  `@example.test` accounts.
- Database fingerprints (`db/`), produced by `tooling/s18_db.py`:
  - schema hashes, per-table row counts, Flyway history, trigger definers and gm-expenses content checksums;
  - the legacy audit: identifiers, statuses, amounts and timestamps, the same shape as FINAL_12's committed
    `f12-dev-legacy.txt`;
  - audit and event counts.
- Pre-checks: server status counters, schema names and the process list (users root and event_scheduler, no statement
  text).
- `old-backend-container-nonsecret.json` holds 13 environment variable names and no value.
- The backend and migration logs were captured with `grep -v -i "generated security password"`: session transcript lines
  4447 and 4506, and `tooling/s18-migrate.sh` line 35. Only Spring's generic sentence "This generated password is for
  development use only" remains, never a password.
- The four application log lines after the smoke carry four identifiers, all of them the smoke's own entities. Every
  word in them is either in the backend sources or in the smoke tool.

## 5. The dump - restricted pointer only

```text
RESTRICTED_LOGICAL_LOCATION=GYPPORT_STORAGE/Restricted/Gystigo/shared-dev-deployment-18-2026-09-17/core_business_dev_V43_20260917T162128Z.sql
BYTES=838347
SHA256=eb5f88d8d37a1fdb28f079ade99582e20f319635081c0af3dc8cb36840d13c56
ORIGINATING_STEP=GM_EXPENSES_SHARED_DEV_DEPLOYMENT_18
CLASSIFICATION=SENSITIVE_ARCHIVE (Shared DEV V43 schema and data: accounts, business and personal data)
MATCHES_THE_ORIGINAL_RECORD=YES (BACKUP_SHA256 and 838,347 bytes, record lines 42-43)
NOT_COPIED=YES (not into Fabric, not into Git)
```

## 6. STEP 18 as its record states it (FACT)

```text
STATUS=READY_FOR_OWNER_REAL_LOGIN_SMOKE
SOURCES=gm-expenses 545eae0, Gystigo bcb9591, Fabric baseline commit bbdd66a (GYPPORT-GM-EXPENSES-MVP-RELEASE-VERIFIED-BASELINE-2026-09-17)
IMAGE=gystigo-backend:4.1.0-java25-gm-expenses-mvp-bcb9591, sha256:9e3ff62f02d670bd003408a5d3631f4e17daa0cf0dbb00b887c0266e99048f81,
      built 16:20Z from git-archive exports of the committed heads
BACKUP=16:21Z, Shared DEV core_business_dev at V43 (27 Flyway rows, 0 failed), restore-verified on a disposable server
MIGRATION=V43 -> V63, 20 applied, 0 failed (16:24:38Z-16:24:58Z)
OFFICIAL_DEV_BACKEND=gypport-backend-dev recreated on the new image (section "Official DEV backend (16:26:20Z)")
SMOKE=37/37 PASS, 0 server 5xx (16:28:55Z-16:29:05Z)
LEGACY_DATA=unchanged, not cleaned
```

## 7. Byte-identical twins and later records (DERIVED 2026-09-18; STEP 18 is not rewritten)

```text
TWINS=18 of the 96 files have byte-identical content elsewhere in Fabric
  12 non-empty   identical to FINAL_12 rehearsal outputs (pre-migration and restore fingerprints of columns, counts, triggers,
                 Flyway and gm-expenses checksums; the post-migration gm-expenses checksum; the zero-tenant period summary).
                 The original record states it itself: "Identical to FINAL_12" (lines 51-53) and "Post-migration integrity
                 (identical to the FINAL_12 rehearsal)" (line 62).
   6 empty       0-byte files (4 routine lists, mysqldump stderr, restore output), equal to every empty file
  Recovered here under STEP 18's own names: a twin elsewhere is another STEP's record, not STEP 18's.

LATER RECORDS (consistency checks only)
  MVP-FROZEN baseline line 156           "V43 -> V63 (STEP 18)"                                    consistent
  MVP-FROZEN baseline line 237           STEP 18 "has no stored prompt or evidence folder in Fabric"  closed by STEP 31
  STEP 19 prompt line 9                  Owner real-login smoke "after GM_EXPENSES_SHARED_DEV_DEPLOYMENT_18" consistent
  20A record lines 25-26                 image sha256:9e3ff62f..., "built 2026-09-17T16:20Z by STEP 18" consistent
  22 record line 130                     deployed image ...-gm-expenses-mvp-bcb9591                consistent
  22B record lines 54 and 59             image label gypport.step=GM_EXPENSES_SHARED_DEV_DEPLOYMENT_18 consistent
  23 record line 108                     SHARED_DEV_VERSION=V63, OFFICIAL_BACKEND=...-bcb9591 (STEP 18) consistent
  30 record lines 51 and 115             the restricted STEP 18 folder, its dump and evidence tree  consistent
```

None of the later work - V64 and V65, the EXP numbering, Total a conciliar, the reverso - is attributed to STEP 18.
Its evidence stays as it was on 2026-09-17.

## 8. Line endings

Twenty-one recovered files use CRLF. The working-tree copies are byte-exact. Git stores them with LF under the
workspace attributes (`text=auto eol=lf`, `core.attributesfile`). Reglas.md accepts this in its 2026-09-17 entry
"Regla de fin de línea en commits controlados": the hashes in `RECOVERY_INDEX.tsv` remain valid as evidence from
before the conversion. STEP 31's record lists both hashes for each of the 21 files. The original record
`DEPLOYMENT_18_RECORD.md` uses LF and is stored exactly as written.
