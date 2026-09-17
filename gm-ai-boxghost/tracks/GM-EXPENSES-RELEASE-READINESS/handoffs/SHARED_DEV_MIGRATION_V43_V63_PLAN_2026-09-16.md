# Shared DEV controlled migration V43 → V63 — plan (prepared, not executed)

```text
TRACK=GM_EXPENSES_RELEASE_READINESS
PREPARED_BY=GM_EXPENSES_MVP_FINAL_RELEASE_CONSOLIDATION_07 §23
DATE=2026-09-16
STATUS=PREPARED_NOT_AUTHORIZED
EXECUTION_REQUIRES=explicit Owner authorization of a dedicated migration STEP
TARGET=Shared DEV gypport-mysql-dev 127.0.0.1:3308 core_business_dev, V43 -> V63
REHEARSAL=GM_EXPENSES_RUNTIME_REHEARSAL_03 (OWNER_ACCEPTED), evidence/RUNTIME-REHEARSAL-03-2026-09-16/
```

Nothing in this document authorizes a commit, a push, a backup, a build or a migration. It records the
order the Owner fixed for the real migration and what each step must prove, using what the rehearsal
already established.

## Preconditions

- The Owner has accepted GM_EXPENSES_MVP_FINAL_RELEASE_CONSOLIDATION_07.
- The legacy Shared DEV data stays as it is. The migration never repairs, backfills, cancels or deletes
  legacy rows; their cleanup is a separate Owner-controlled STEP.
- The stale `gypport-backend-dev` container (image `gystigo-backend:4.1.0-java25`, code V42 or earlier)
  stays stopped. It is never started against the migrated schema.

## Steps and what each must prove

1. **Controlled commits of the exact rehearsed and final bytes.** One commit per repository (Gystigo,
   Modules/gm-expenses, Fabric), each with an explicit path list; never `git add .` or `git add -A`.
   Prove that the backend and migration bytes committed are the rehearsed ones: no file under
   `Gystigo/platform_os/server/src`, `Gystigo/database` or `Modules/gm-expenses/src` differs from the
   working tree that produced Host jar `CC028B88…` and gm-expenses jar `FDDAB6CF…`, and the
   V44..V63 migration files keep their SHA-256.
2. **Fresh Shared DEV backup immediately before the migration.** Read-only
   `mysqldump --single-transaction --routines --triggers --no-tablespaces --set-gtid-purged=OFF`
   into `resolve(GYPPORT_STORAGE)/Restricted/...`, recording its size and SHA-256. A restore needs root,
   because the 29 triggers are defined by `root@%`. Never restore into 3308 during a rehearsal and never
   reuse 3308 for a disposable copy.
3. **Re-check Shared DEV.** Flyway max 43, 27 history rows, 0 failed; 102 tables; per-table row counts;
   and a read-only content checksum of the 19 gm-expenses tables, taken as in `r03-postmigration.ps1`,
   to compare against after the migration.
4. **Compare with the rehearsal source fingerprint.** The per-table counts must equal
   `r03-dev-counts.txt` (SHA-256 `0bfec7e9…`). Any difference stops the migration until the Owner
   decides whether a new rehearsal on a fresh copy is required.
5. **Build the backend from the accepted commit**, from a tree whose built paths are clean. Install the
   module, then package the Host after deleting `target/gystigo-host-runtime-0.1.0-SNAPSHOT.jar` and
   its `.jar.original`; otherwise the package step reuses a stale jar. Never `mvn clean` while the
   runtime-local copy lives under `target/`.
6. **Verify the packaged hashes.** Record the Host and gm-expenses jar SHA-256; the gm-expenses jar
   nested in `BOOT-INF/lib` equals the installed module jar; the packaged V44..V63 migrations equal the
   committed files. Jar hashes may differ from the rehearsal because of build timestamps; the migration
   files may not.
7. **Migrate Shared DEV V43 → V63** with the verified backend and nothing else connected to 3308. Prove:
   20 migrations applied and 0 failed; no table lost; only additive row changes (Flyway history and the
   V61 memberships); all 19 gm-expenses tables content-identical over shared columns to the step 3
   checksum; 17 delete guards; 8 canonical categories; the V61, V62 and V63 invariants; 0 ambiguous
   legacy links. `r03-postmigration.ps1` is the model for this check.
8. **Rebuild or recreate the official DEV backend** from the accepted commit under a new image tag,
   keeping the previous image and the `gypport_expense_documents_dev_data` volume for rollback.
9. **Owner real-login smoke** in the Owner's own browser (cache-bypass reload, own credentials; no agent
   login). The Case card shows the canonical financial vocabulary; advance → delivery → expenses →
   review → return or reimbursement → Conciliar → Cerrar expediente; reports; the access log shows
   0 legacy `/settlement` calls and 0 5xx.
10. **Declare Shared DEV aligned** only after step 9 passes.

## Stop conditions

- Step 4 finds a fingerprint difference.
- Any Flyway failure, or any integrity check in step 7 fails.
- The packaged migrations differ from the committed ones (step 6).
- The Owner smoke in step 9 fails.

## Rollback

MySQL DDL is not transactional: a failed migration can leave a partially migrated schema. The rollback is
the step 2 backup restored into Shared DEV as root, with the previous backend image. After a successful
migration the previous image is not a rollback path on its own, because its code predates the schema
(inference, not tested); rolling back means restoring the backup.
