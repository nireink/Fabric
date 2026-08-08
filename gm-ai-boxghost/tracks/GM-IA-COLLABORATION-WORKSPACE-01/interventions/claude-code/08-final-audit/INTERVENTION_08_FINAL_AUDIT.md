# Intervención 08 — Final Read-Only Audit (Independent)

```text
INTERVENTION=08_CLAUDE_CODE_FINAL_AUDIT
TRACK=GM-IA-COLLABORATION-WORKSPACE-01
SCOPE_VERSION=v0.1
MODE=INDEPENDENT_READ_ONLY_AUDIT
AUDITED_INTERVENTION=07_CODEX_IMPLEMENTATION
```

This audit does not accept Codex's own summary
(`INTERVENTION_07_IMPLEMENTATION_HANDOFF.md`) as sufficient evidence. Every
claim in that handoff was independently re-derived in this session: source
files were read directly, tests and builds were re-run from a clean Maven/npm
invocation, the packaged JAR was rebuilt and re-hashed, and the runtime was
booted and probed with real HTTP requests. Where this audit's own numbers
happen to match the handoff's, that is because both measured the same real
artifact, not because the handoff was trusted.

---

## 1. Preparación obligatoria

Documents read before forming a verdict (all read directly this session):

- `Fabric/AGENTS.md` (only applicable AGENTS.md — none exists inside
  `Modules/gm-ai-workspace` or `Fabric/gm-ai-boxghost`)
- `TRACK_STATE.md`, `SCOPE.md`, `CONTEXT_PACK.md`, `SOURCE_MANIFEST.json`
- `approvals/apr-7c613757-a5d5-4e16-90c6-a0c17cd90907.json`
- `interventions/claude-code/06-read-only-audit/FINAL_POST_DEPLOYMENT_VERIFICATION.md`
- The eight Intervention-05 handoff specs under
  `interventions/chatgpt-work/05-handoff-verifiable/`
- `Modules/gm-ai-workspace/docs/handoffs/INTERVENTION_07_IMPLEMENTATION_HANDOFF.md`
- `Modules/gm-ai-workspace/README.md`
- `Modules/gm-ai-workspace/contracts/openapi/gm-ai-workspace-v0.1.yaml`

### Canonical state verified

```text
TRACK_STATE.md: current_step=07_CODEX_IMPLEMENTATION, current_owner=CODEX, revision=7
SCOPE.md: owner_approval_recorded=true, implementation_authorized=true
OWNER_APPROVAL_RECORDED=YES  (approvals/apr-7c613757-...json, decision=APPROVED, granted_by=eduardo)
CODEX_ALLOWED=YES            (TRACK_STATE.md front matter)
implementation_authorized=true (SCOPE.md front matter)
06->07 transition recorded   (dialog/events.jsonl evt-0010, WORKFLOW_TRANSITION 06->07)
```

`CLARIFICATION_REPORT_CORRECTED.md` was not reopened; it is superseded history
per `CONTEXT_PACK.md`'s evidence chain and `FINAL_POST_DEPLOYMENT_VERIFICATION.md`.
No re-request of Eduardo's approval was made — it is already recorded and was
only read, not re-solicited.

### SOURCE_MANIFEST.json integrity (independent SHA-256 recomputation)

```text
UNIQUE_MANIFEST_ENTRIES=20
HASH_MATCHES=20
HASH_MISMATCHES=0
MISSING_FILES=0
```

All 20 manifest entries were re-hashed twice in this session — once before the
runtime test and once after — with identical results both times, confirming
no mutation occurred during the audit itself. The declared count (20) matched
what was requested; no forcing was needed.

---

## 2. Backend audit

| Check | File:line | Result |
|---|---|---|
| Spring Boot 4.1 / Java 25 | `backend/pom.xml:8,17` (`spring-boot-starter-parent` 4.1.0, `java.version=25`) | PASS |
| 8 GET endpoints, 1:1 with OpenAPI | `backend/src/main/java/.../workspace/WorkspaceController.java:24-56` | PASS — 8 `@GetMapping`, 0 `@PostMapping`/`@PutMapping`/`@DeleteMapping`/`@PatchMapping` |
| No mutation endpoints anywhere | repo-wide grep for `@PostMapping\|@PutMapping\|@DeleteMapping\|@PatchMapping` under `backend/src` | PASS — zero matches |
| Path traversal / symlink / junction defense | `WorkspaceService.java:423-453` (`safeResolve`) | PASS — rejects absolute paths, `..` segments, null bytes; resolves `toRealPath()` and re-checks `startsWith(root)`; explicitly rejects `Files.isSymbolicLink(candidate)` |
| No JDBC/MySQL/JPA/Flyway, no persistent writes | repo-wide grep under `backend/src` | PASS — zero matches in `main`; the only `Files.write*/createDirectories/copy` calls are in `src/test/.../SyntheticFixtureSupport.java` and `WorkspaceServiceTest.java`, confined to JUnit `@TempDir` fixtures |
| Secrets/sensitive data redaction | `WorkspaceService.java:38,59-64,485-491` (`maskSecrets`, `SECRET_PATTERNS`) | PASS — 5 patterns (OpenAI-style keys, AWS AKIA, password/token/api-key kv pairs, PEM private keys, JWTs), applied to timeline lines, context, and all resource content before it leaves the service |
| Bootstrap not a public mutation surface | `WorkspaceController.java` (no bootstrap mapping exists); `tests/fixtures/bootstrap-boxghost.sh:24-29` | PASS — bootstrap is a standalone shell script, not wired into the Spring app, requires an explicit `--confirm-test-fixtures` flag, and refuses non-absolute, non-empty, and broad/production-looking destinations |
| Fixtures exclusively synthetic | `backend/src/test/java/.../WorkspaceServiceTest.java:38-40` (`TEST-COMPLETE-01`, `TEST-INVALID-01`, `TEST-MINIMAL-01`); `tests/fixtures/{valid-minimal,valid-complete,invalid-fail-closed}/` | PASS — no references to real track IDs or production BoxGhost content |
| Loopback binding | `backend/src/main/resources/application.properties:2-3` (`server.address=127.0.0.1`, `server.port=8080`) | PASS |
| CORS restricted to GET / configured origin | `SecurityConfig.java:29-40` | PASS — `setAllowedMethods(List.of("GET"))`, origin from `gm.ai.allowed-origin` (default `http://127.0.0.1:5173`) |
| Public errors carry no stack trace / path | `application.properties:5-7` (`server.error.include-message/stacktrace/binding-errors=never`); `ApiExceptionHandler.java` | PASS |

### Backend tests (re-run from a clean `mvnw test` invocation, this session)

```text
BACKEND_TESTS_TOTAL=22
BACKEND_TESTS_PASSED=21
BACKEND_TESTS_FAILED=0
BACKEND_TESTS_SKIPPED=1
BACKEND_BUILD=PASS
```

Command: `./mvnw.cmd -B test` in `Modules/gm-ai-workspace/backend` → `BUILD SUCCESS`,
`Tests run: 22, Failures: 0, Errors: 0, Skipped: 1`.

The one skipped test is
`symbolicLinkOutsideRootFailsClosedWhenPlatformAllowsCreation`
(`WorkspaceServiceTest.java:101-113`), which calls `Assumptions.abort()` when
`Files.createSymbolicLink` fails — this host does not permit unprivileged
POSIX symlink creation. The Windows-equivalent risk is covered by
`windowsJunctionOutsideRootFailsClosed` (`WorkspaceServiceTest.java:115-130`,
`@EnabledOnOs(OS.WINDOWS)`), which **did run** (it is not the skipped test —
only 1 of 22 was skipped) and asserts `mklink /J` junctions pointing outside
root are caught as `REFERENCE_OUTSIDE_ROOT`. This equivalent coverage is a
genuine substitute for the omitted generic POSIX test, not a gap.

`./mvnw.cmd -B -DskipTests package` → `BUILD SUCCESS`. The repackaged JAR was
independently re-hashed:

```text
JAR_SHA256=2121626694e5f2bfba5e785bd6e42c2df014134f07985cc578066a9020db37a1
```

This is byte-for-byte identical to the hash declared in the Intervention 07
handoff, despite being rebuilt from scratch in this session — real
corroboration, not a repeated claim.

---

## 3. Frontend audit

| Check | File:line | Result |
|---|---|---|
| React + TypeScript + Vite + Tailwind | `frontend/package.json:12-25` (`react@19.1.0`, `typescript@7.0.2`, `vite@7.0.4`, `tailwindcss@4.3.3`) | PASS |
| Display-only, no mutation controls | `frontend/src/app/App.tsx` (full file read) | PASS — no `<form>`, no submit handlers, only a text filter input (`onChange` on local state) and track-selection buttons that call `setSelected` |
| Only GET is ever issued | `frontend/src/services/api.ts:27-28` (hardcoded `method: 'GET'` in the single `get<T>` helper); repo-wide grep for `method:\s*['"](POST\|PUT\|DELETE\|PATCH)` under `frontend/src` and `frontend/tests` | PASS — zero non-GET method literals anywhere in the frontend |
| Consumes exactly the 8 contracted endpoints | `frontend/src/services/api.ts:36-45` | PASS — `health`, `tracks`, `track`, `timeline`, `context`, `decisions`, `approvals`, `findings` map 1:1 to the OpenAPI paths |
| Loading / empty / error / unauthorized / ready states | `frontend/src/app/App.tsx:23,77-82` | PASS |
| Client-side secret masking as defense in depth | `frontend/src/services/api.ts:3-25` (`maskText`/`sanitize`, same 5 pattern families as the backend) | PASS |

### Frontend tests / build (re-run this session)

```text
FRONTEND_TESTS_TOTAL=4
FRONTEND_TESTS_PASSED=4
FRONTEND_TESTS_FAILED=0
FRONTEND_BUILD=PASS
FRONTEND_MODULES_BUILT=32
NPM_VULNERABILITIES=0
```

Commands: `npm test` (vitest) → `Test Files 1 passed (1)`, `Tests 4 passed (4)`.
`npm run build` (`tsc -b && vite build`) → `32 modules transformed`, build
succeeded. `npm audit` (both with and without `--omit=dev`) → `found 0
vulnerabilities`. No `npm audit fix` or dependency updates were applied.

---

## 4. Runtime verification

Backend JAR launched directly (`java -jar ...backend-0.1.0-SNAPSHOT.jar`) with
`server.port=18080` and `gm.ai.boxghost-root` pointed at the real canonical
`Fabric/gm-ai-boxghost`, so this exercised the actual production BoxGhost tree
read-only, not a fixture copy.

```text
HEALTH=UP
MODE=READ_ONLY
APPROVAL_STATUS=VALID
```

All 8 GET endpoints hit with `curl` against `GM-IA-COLLABORATION-WORKSPACE-01`:

- `GET /api/workspace/health` → 200, `{"boxghostAvailable":true,"configured":true,"status":"UP","mode":"READ_ONLY"}`
- `GET /api/tracks` → 200, one track returned
- `GET /api/tracks/{id}` → 200, `integrity: "VALID"`, `findingsCount: 0`
- `GET /api/tracks/{id}/timeline` → 200, `total: 10` events (matches the 10 `dialog/events.jsonl` lines)
- `GET /api/tracks/{id}/context` → 200, masked context, `redacted: false`
- `GET /api/tracks/{id}/decisions` → 200, `[]`
- `GET /api/tracks/{id}/approvals` → 200, one approval, `validationStatus: "VALID"`
- `GET /api/tracks/{id}/findings` → 200, `[]`

Method / route rejection:

- `POST /api/tracks` → 405 `{"error":"METHOD_NOT_ALLOWED","status":405}`
- `POST /api/workspace/health` → 405 (same body)
- `DELETE /api/tracks/{id}` → 405 (same body)
- `GET /api/tracks/not_valid_id` (invalid track-id characters) → 400 `{"error":"INVALID_TRACK_ID","status":400}`
- `GET /api/tracks/..%2f..%2f..%2fetc` (encoded traversal in path segment) → 400, rejected by Tomcat itself before reaching the app (see Finding F-1)
- `GET /api/nonexistent` (unmapped route under `/api/**`) → 500 `{"error":"WORKSPACE_READ_FAILED","status":500}` (see Finding F-2)

No absolute path, stack trace, or secret pattern appeared in any response
body. Server was then stopped (`Stop-Process`); a follow-up `curl` confirmed
connection refused (HTTP 000).

```text
RUNTIME=PASS
READ_ONLY_BOUNDARY=PASS
OPENAPI_CONFORMANCE=PASS
```

---

## 5. Integridad y Git

```text
BRANCH=master
HEAD=84feea2f5f4cfd2a6feb446eabc495f9e3a8c33d   (matches expected)
```

- `git diff --cached --name-only` → empty, both before and after the runtime
  test. Nothing is staged.
- `git log origin/master --oneline` → same two commits as local HEAD; no
  push occurred in this session or since the Intervention 07 handoff.
- Working tree: `README.md` modified (unstaged) and the entire new
  implementation (`backend/`, `frontend/`, `config/`, `contracts/`, `docs/`,
  `tests/`, `.env.example`, `.gitignore`, `.code-workspace`) untracked —
  consistent with `STAGING=false, COMMIT=false, PUSH=false` as declared.
- No `git add`, `commit`, `push`, `reset`, `checkout`, or `clean` was run
  against `Modules/gm-ai-workspace` in this audit.
- All product changes are confined to `Modules/gm-ai-workspace`; nothing under
  `Fabric` was touched by the implementation.
- `Fabric/gm-ai-boxghost` file count: **28 files**, recomputed independently
  by full recursive listing after the runtime test — matches the handoff's
  declared count exactly. The 20 `SOURCE_MANIFEST.json` entries were
  re-verified byte-for-byte both before and after the runtime boot, with 0
  mismatches both times, directly confirming `BOXGHOST_MUTATED_BY_PRODUCT=false`
  for the portion of BoxGhost this audit itself exercised.

---

## 6. Findings

**F-1 (LOW, non-blocking).** An encoded path-traversal attempt in a URL path
segment (`/api/tracks/..%2f..%2f..%2fetc`) is rejected with HTTP 400 by
embedded Tomcat's own request-target normalization before Spring's
dispatcher — and therefore before `ApiExceptionHandler.java` — runs, so the
response body is Tomcat's stock HTML error page instead of the app's JSON
error shape. No absolute path, stack trace, or internal detail is present in
that page; the traversal is still refused. This is a cosmetic inconsistency
in error-body format for one specific malformed-request class, not a
traversal or information-disclosure defect. `WorkspaceService.safeResolve`
(`WorkspaceService.java:423-453`) still correctly fails closed for every
traversal attempt that reaches application code (verified both by the
re-run unit tests and by this session's own runtime probing).

**F-2 (LOW, non-blocking).** An unmapped route under `/api/**`
(`GET /api/nonexistent`) returns HTTP 500 `WORKSPACE_READ_FAILED` rather than
404, because Spring's handler-not-found condition is caught by the catch-all
`@ExceptionHandler(Exception.class)` in `ApiExceptionHandler.java:22-26`
instead of surfacing as a 404. The response body still leaks nothing (no
path, no stack trace), and `SecurityConfig.java:20-21` correctly denies
everything outside `/api/**`, so this is a status-code accuracy issue, not a
security or scope defect.

Neither finding violates any of the 12 acceptance criteria in the
Intervention 07 handoff, contradicts the OpenAPI contract, or exposes data.
Both are candidates for a future cleanup pass, not blockers for this gate.

```text
CRITICAL_FINDINGS=0
HIGH_FINDINGS=0
MEDIUM_FINDINGS=0
LOW_FINDINGS=2
```

---

## 7. Mutation declaration

```text
AUDITED_SOURCE_FILES_MODIFIED=NO
REPORT_ONLY_MUTATION=YES
REPORT_FILE_CREATED=YES
REPORT_FILE_PATH=D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT\Fabric\gm-ai-boxghost\tracks\GM-IA-COLLABORATION-WORKSPACE-01\interventions\claude-code\08-final-audit\INTERVENTION_08_FINAL_AUDIT.md
TRACK_STATE.md / SCOPE.md / CONTEXT_PACK.md / events.jsonl / SOURCE_MANIFEST.json: NOT MODIFIED
STAGED=NO
COMMIT_CREATED=NO
PUSH_PERFORMED=NO
```

A temporary bootstrap-fixture run (`bootstrap-boxghost.sh`) was executed
against an isolated `/tmp` destination only, to verify its guardrails, and
was deleted immediately after (`rm -rf`). A second invocation against the
real `Fabric/gm-ai-boxghost` path was run specifically to confirm it is
refused (`exit=3`, `"refusing broad or production destination"`) — no files
were written to `Fabric/gm-ai-boxghost` by that invocation. The backend JAR
was run and stopped; its process left no artifacts outside
`backend/target/` (already untracked/ignored build output).

---

## Veredicto final

```text
TRACK=GM-IA-COLLABORATION-WORKSPACE-01
INTERVENTION=08
MODE=READ_ONLY
BRANCH=master
HEAD=84feea2f5f4cfd2a6feb446eabc495f9e3a8c33d
MANIFEST_ENTRIES_COUNT=20
HASH_MATCHES=20
HASH_MISMATCHES=0
BACKEND_TESTS=21/22 (1 skipped, 0 failed)
FRONTEND_TESTS=4/4
BACKEND_BUILD=PASS
FRONTEND_BUILD=PASS
RUNTIME=PASS
READ_ONLY_BOUNDARY=PASS
OPENAPI_CONFORMANCE=PASS
BOXGHOST_EVIDENCE_MODIFIED=NO
AUDITED_SOURCE_FILES_MODIFIED=NO
REPORT_ONLY_MUTATION=YES
STAGED=NO
COMMIT_CREATED=NO
PUSH_PERFORMED=NO
CRITICAL_FINDINGS=0
HIGH_FINDINGS=0
MEDIUM_FINDINGS=0
LOW_FINDINGS=2
VERDICT=ACCEPTED
READY_FOR_INTERVENTION_09=YES
REPORT_PATH=D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT\Fabric\gm-ai-boxghost\tracks\GM-IA-COLLABORATION-WORKSPACE-01\interventions\claude-code\08-final-audit\INTERVENTION_08_FINAL_AUDIT.md
NEXT_STEP=CLAUDE_CHAT_EXECUTES_INTERVENTION_09_FINAL_CONSOLIDATION
```

The SHA-256 of this report file (necessarily computed after this file was
saved, so it is not self-embedded) is reported in the closing chat message of
this intervention, not inside this document.
