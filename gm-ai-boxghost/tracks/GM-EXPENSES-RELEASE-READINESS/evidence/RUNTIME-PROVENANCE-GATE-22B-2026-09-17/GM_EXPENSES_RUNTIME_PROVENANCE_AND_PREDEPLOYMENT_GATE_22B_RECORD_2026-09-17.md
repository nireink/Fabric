# GM_EXPENSES_RUNTIME_PROVENANCE_AND_PREDEPLOYMENT_GATE_22B — record (2026-09-17)

```text
TRACK=GM_EXPENSES_RELEASE_READINESS
STEP=GM_EXPENSES_RUNTIME_PROVENANCE_AND_PREDEPLOYMENT_GATE_22B
MODE=READ_ONLY_RUNTIME_AUDIT
STATUS=PROVEN
SOURCE_EDITED=NO  FILES_STAGED=0  COMMITS_CREATED=0  PUSH_PERFORMED=NO
SHARED_DEV_MODIFIED=NO  OWNER_CASE_MODIFIED=NO  NOTHING_RESTARTED=YES
```

## 1. Frontend on 5173

```text
PID=23416  node.exe  C:\Program Files\nodejs\node.exe
CMD="node" "D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT\Gystigo\node_modules\.bin\..\vite\bin\vite.js"
PARENT_CHAIN=cmd.exe /c vite  <-  npm run dev  <-  VS Code integrated PowerShell
STARTED=2026-09-17 15:31:55 (local)
```

The Vite root is not guessed from the command line - the server itself says where its files come from. The module
served at `/src/application/expenses/cases/ExpenseCaseCard.jsx` carries

```text
_jsxFileName = "D:/NZXTG7/GYPPORT/GYPPORT ERP/GYPPORT/Gystigo/platform_os/studio/channel/browser/shell/src/
                application/expenses/cases/ExpenseCaseCard.jsx"
```

and the `dev` script of that directory's package (`@gypport/platform-os-browser-shell`) is plainly `vite`, so the
process working directory - and therefore the Vite root - is that shell directory. The served `/` is that directory's
`index.html`.

What the served bytes contain (not the disk file - the bytes the browser receives):

```text
ExpenseCaseCard.jsx   imports caseTitle from caseRules.js;  const title = caseTitle(item);
                      className "expense-case-card__business-id" with children ["ID: ", item.caseNumber]
caseRules.js          exports caseSequenceOf, caseTitle, caseIdentityConsistent; caseListSequence is gone
ExpenseCaseListPage   renders ExpenseCaseCard with { item } only - no position is passed
expenseService.js     const API_BASE_URL = "http://localhost:8080"
```

The `?t=...` query strings on those modules are Vite's own HMR stamps, so the browser is being served freshly
transformed current bytes, not a stale bundle.

## 2. Backend on 8080

```text
CONTAINER=gypport-backend-dev (Docker published 127.0.0.1:8080->8080)
IMAGE=gystigo-backend:4.1.0-java25-gm-expenses-mvp-bcb9591  sha256:9e3ff62f02d6...
IMAGE_CREATED=2026-09-17T16:20:30Z    CONTAINER_STARTED=2026-09-17T16:26:21Z
LABEL gypport.source.gystigo=bcb959158b781e3fcd876bacc6fcf0f1f1c79b9f
LABEL gypport.source.gm-expenses=545eae0fb287f8e04f7f1b4ac73780304ec53f22
LABEL gypport.step=GM_EXPENSES_SHARED_DEV_DEPLOYMENT_18
LABEL gypport.baseline=GYPPORT-GM-EXPENSES-MVP-RELEASE-VERIFIED-BASELINE-2026-09-17
SPRING_DATASOURCE_URL=jdbc:mysql://mysql:3306/core_business_dev   (the Shared DEV database)
```

This is the STEP 18 deployment, built from the commit gate of STEP 17. Every STEP from 19 onward is uncommitted work
that this image cannot contain.

## 3. What that runtime can and cannot answer (§4)

The API requires authentication (`GET /api/expense-cases` and the Case detail both answer `401`, as do
`/v3/api-docs` and `/actuator/*`). No session of the Owner's was used and no credential was entered, so **no live
payload values are quoted here**. The payload shape is proven instead from two independent read-only sources:

```text
A) The running jar. /app/app.jar copied out of the container and its ExpenseCaseController.class scanned for the
   JSON field names it writes:
     PRESENT  caseId, responsibleName, reviewerName, createdAt, closedAt, financialSummary, "rendition/returns"
     ABSENT   caseNumber, caseSequence, businessDate, movements, baseToReturn, baseToReimburse, "movement-reversals"
   The controls prove the method: the fields the Owner does see are present, the fields the Owner does not see are not.

B) The database it reads. core_business_dev, read inside SET SESSION TRANSACTION READ ONLY / START TRANSACTION
   READ ONLY / ROLLBACK:
     FLYWAY_MAX=63
     expense_case columns case_business_date / case_sequence / case_number = 0
     table expense_case_number_sequence = 0
   Even a newer backend could not serve the identity from this schema until V64 runs.
```

## 4. Why the Owner's screen looks the way it does

The card's own logic explains the screen exactly:

```text
title = caseTitle(item)          -> no caseSequence and no caseNumber in the payload, so the title is just the name:
                                    "VIAJE QUITO", with no EXP. NN
{item.caseNumber && <p>ID: ...}  -> no caseNumber, so no ID line is rendered at all
date = item.businessDate ?? item.createdAt.slice(0,10)  -> no businessDate, so the date falls back to the created day,
                                    which is why "Fecha: 2026-09-17" is still there
```

The visual grouping the Owner already sees (identity block, hairline dividers, Conciliado on its rail, the Finanzas
order) is frontend-only work and it is loaded. The two missing lines are the two that need the backend.

```text
ROOT_CAUSE=NEW_STUDIO_OLD_BACKEND
```

## 5. Fixtures on 5189

```text
PID=21108  node .../vite.js  <shell directory>  --config <shell>/vite.config.js  --port 5189 --strictPort
PURPOSE=the Owner acceptance fixtures (expense-case-cards.html, expense-case-detail.html)
```

Those pages assign `expenseService.listCases` / `expenseService.getCase` to local synthetic data inside the fixture
file. They never call an API. **A green fixture proves the presentation, never the runtime**: it says nothing about
what the API on 8080 returns to the real app on 5173.

## 6. Source control and the Owner's suspicion

```text
Modules/gm-expenses  master                                       545eae0 (2026-09-17 10:44)  0 staged, 12 modified, 6 untracked
Gystigo              feature/gm-fleets-minimum-vehicle-master-01   bcb9591 (2026-09-17 10:45)  0 staged, 22 modified, 6 untracked
Fabric               main                                          bbdd66a (2026-09-17 10:54)  0 staged,  4 modified, 20 untracked
COMMITS_CREATED_SINCE_STEP_22A=0   PUSH_PERFORMED=NO
```

A search of the whole workspace for `ExpenseCaseCard.jsx` (excluding node_modules and dist) returns **exactly one
file**, in the expected working tree. The 49 other git roots under the workspace - Github, UI_Experiments,
GYPPORT-Storage, the module repositories - contain no expenses Studio files at all.

```text
ALTERNATE_WORKTREE_FOUND_WITH_STEP22_CHANGES=NO
```

## 7. Conclusion

```text
SOURCE_IMPLEMENTATION_CORRECT=YES     (no card edit is needed or was made)
DEPLOYMENT_REQUIRED=YES               (commit gate -> Shared DEV V64 -> rebuild the DEV backend from the new commits)
OWNER_CASE_MODIFIED=NO                (its two RETURN_REGISTERED events still total USD 300.00)
```
