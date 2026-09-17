# GM_EXPENSES_RUNTIME_REHEARSAL_03 — evidence

```text
TRACK=GM_EXPENSES_RELEASE_READINESS
STEP=GM_EXPENSES_RUNTIME_REHEARSAL_03
DATE=2026-09-16 (local, UTC-5); run 2026-09-17T00:57Z-01:07Z
STATUS=OWNER_ACCEPTED
ACCEPTANCE_SOURCE=Owner prompt GM_EXPENSES_MVP_FINAL_RELEASE_CONSOLIDATION_07 §17
PROMOTED_BY=GM_EXPENSES_MVP_FINAL_RELEASE_CONSOLIDATION_07 §20
COMMIT_STATUS=NOT_COMMITTED (evidence of an uncommitted working tree)
PUSH_STATUS=NOT_PUSHED
SHARED_DEV_STATUS=UNTOUCHED (V43; read-only queries and one mysqldump --single-transaction)
```

## Owner acceptance

```text
GM_EXPENSES_RUNTIME_REHEARSAL_03=OWNER_ACCEPTED
V43 -> V63                        PASS
20 migrations                     PASS, 0 failures
gm-expenses row integrity         PASS
real workflow smoke               14/14
reports                           PASS
tenant isolation                  PASS
old settlement calls              0
5xx                               0
Shared DEV modified               NO
```

## What was rehearsed

A disposable `mysql:8.4.10` container (`gypport-rehearsal03-a2038866`, 127.0.0.1:3312) was restored from
a read-only dump of Shared DEV (`gypport-mysql-dev`, 127.0.0.1:3308, Flyway V43). The working-tree Host
jar migrated the copy to V63 and served the runtime smoke on 127.0.0.1:18082. The container, its volume,
the backend and its work directory were removed afterwards.

```text
SOURCE                Shared DEV V43, 102 tables, 3,192 rows (r03-dev-counts.txt)
COPY_BEFORE           identical per-table counts (r03-copy-counts-before.txt has the same SHA-256)
GM_EXPENSES_JAR       FDDAB6CF81B60AFE1E1F48ABCD8BB08F2EF30729358C3732CAFD8224D2BE8C9D
HOST_JAR              CC028B886C4DF352A8A9936CCE1F44666B41B3A770EBC38FE7AC0283693057F5 (built 2026-09-17T01:00:13Z)
MIGRATION             Flyway 43 -> 63, V44..V63, 20 migrations, 8.98 s, 0 failed
TABLES / ROWS         102 -> 107 tables (none lost, 5 added); 3,192 -> 3,234 rows (+20 Flyway, +22 membership)
GM_EXPENSES_CONTENT   19/19 tables content-identical over shared columns, 0 mismatches
INVARIANTS            17 delete guards, 8 canonical categories, V61/V62/V63 checks, 0 ambiguous legacy links
RUNTIME_SMOKE         14/14 PASS (r03-runtime-smoke-results.txt)
ACCESS_LOG            0 legacy /settlement calls, 0 5xx
```

Evidence note: line 5 of `r03-runtime-smoke-results.txt` shows `confirmedBy=` empty. The script printed
a field that only the advance list returns; the check's pass condition did not use it.

## Legacy Shared DEV data recorded before migration (not repaired)

`r03-premigration-records.txt` holds the exact identifiers:

```text
LEGACY_OBSERVED_ROWS=1       OBSERVADO expense without an OBSERVED review event (tenant 1, no Case)
LEGACY_SETTLEMENT_ROWS=3     CERRADO settlements whose advances remain EN_RENDICION (tenant 1, one Case)
BORRADOR_ROWS=16             tenant 1: 3 without a Case + 10 in one Case; tenant 4: 1; tenant 70: 2
MULTI_ACTIVE_GROUPS=4        Case+currency groups with more than one financially active advance
OTHER                        3 advances without a Case, 9 legacy case->advance links, 4 expenses without a Case
TENANT_CLASSIFICATION        1 REAL_DEV_DATA; 4 and 387 TEST_DATA; 33 and 70 UNKNOWN (Owner evidence required)
```

Legacy cleanup is a separate Owner-controlled STEP.

## Sensitivity check before promotion

```text
SECRET_SCAN=PASS
LITERAL_PASSWORDS=0            synthetic account passwords are generated at run time and never written
DATABASE_PASSWORDS=0           read at run time from the disposable container environment
SESSION_COOKIES_OR_TOKENS=0    the smoke script handles cookies in memory only
DUMPS_PROMOTED=0               the Shared DEV dump stays in GYPPORT_STORAGE (Restricted); nothing here restores data
PERSONAL_DATA=0                synthetic @example.test accounts only; Shared DEV rows appear as counts and technical ids
NOT_PROMOTED                   session extracts of Owner messages (owner-messages-*.txt) and the deleted backend work directory
```

The FIX_01 Shared DEV archive this rehearsal compared against is referenced, not copied:
`resolve(GYPPORT_STORAGE)/Restricted/Gystigo/runtime-local-alignment-2026-09-16/core_business_dev_V43_20260916T171614Z.sql`
(838,347 bytes, SHA-256 7b66579e…).

## Manifest (byte-exact copies of the session scratchpad files)

| File | Bytes | SHA-256 |
|---|---:|---|
| r03-dev-counts.txt | 2336 | 0bfec7e9acf929721192cb68cef12d8808143607fc20e5d5c516b918877fb555 |
| r03-copy-counts-before.txt | 2336 | 0bfec7e9acf929721192cb68cef12d8808143607fc20e5d5c516b918877fb555 |
| r03-premigration.sql | 4182 | b737d9f05d693a82d8136d619a5c88cf0a060db22342e18830a82b0731ab9118 |
| r03-premigration-records.txt | 2352 | c5a103b4ca0cbef7c54c19ffcd37472d9ee14bd4ab89857914e3442f3c4c70be |
| r03-module-test.log | 23134 | db364c8f11e72e3178d8a6563a36c5fdedc57adf7cb07b36bbc4e91e55988491 |
| r03-module-install.log | 2090 | dfce5f9e78694d22784bee048409c3dd583047b12f4c44909e97f4567c6bcf44 |
| r03-host-package.log | 2459 | c305904c64dee7e473833ce19d78f94662e78e2268f378d82bc62797052a9b0e |
| r03-studio-contracts.log | 391 | c8279a6575fa4158c9ea0a9c0301ebc5169d2e3e503e6570efe9d90a237a4c81 |
| r03-start-backend.ps1 | 3680 | 920ebc01b8a978c4a55666d7c6187fb43674b50e924ed4cd0e7f6f24ff435ac7 |
| r03-postmigration.ps1 | 10458 | 47b706813b917ac8e2c0783c8f08a76fc0016da98092a0d60f87d1c4c9cfb528 |
| r03-postmigration-results.txt | 3629 | d7c9bc674cc9cf9f8a54a8324d882c4b7e59e7af2ea944e09074c8470a26092a |
| r03-runtime-smoke.ps1 | 18044 | a5f4c64da1d7fb4d277ded2a459be49e249e128ddc5dda25a105b3aec3a4a4d7 |
| r03-runtime-smoke-results.txt | 2202 | 4143981410544bdea2c86c2c69d83247b31d5f9183df5464d7c1e1aab2ba32df |
| r03-container-name.txt | 30 | a712d66290345a684358123a44c55753a8f79173ddf5213bb0be863995179d84 |
