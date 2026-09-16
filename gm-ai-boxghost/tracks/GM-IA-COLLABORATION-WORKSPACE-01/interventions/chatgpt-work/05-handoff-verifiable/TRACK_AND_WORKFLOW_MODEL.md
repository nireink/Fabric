# Track and Workflow Model

## 1. Propósito

Este documento separa el ciclo de vida del track, el workflow aplicable, el paso actual, el responsable y la revisión. El primer slice los lee, valida y muestra; no ejecuta transiciones.

## 2. Modelo

```text
TRACK_ID         = identidad estable
LIFECYCLE_STATUS = DRAFT | ACTIVE | PAUSED | CLOSED | ARCHIVED
WORKFLOW_ID       = flujo versionado aplicable
CURRENT_STEP      = paso existente dentro de WORKFLOW_ID
CURRENT_OWNER     = actor responsable del siguiente resultado
REVISION          = entero monotónico del estado declarativo
SCOPE_VERSION     = versión vigente del alcance
```

`LIFECYCLE_STATUS` describe la vida general. `CURRENT_STEP` ubica la intervención. Un evento en el timeline registra lo sucedido, pero no reemplaza el estado actual.

## 3. Workflow canónico de este track

| Orden | Step ID | Actor | Resultado esperado |
|---:|---|---|---|
| 1 | `01_CHATGPT_WORK_INITIAL_PROPOSAL` | ChatGPT Work | Propuesta inicial |
| 2 | `02_CLAUDE_CHAT_CRITICAL_REVIEW` | Claude Chat | Revisión crítica |
| 3 | `03_CHATGPT_WORK_ADJUSTMENT` | ChatGPT Work | Cruce y ajuste |
| 4 | `04_CLAUDE_CHAT_CONSOLIDATION` | Claude Chat | Consolidación |
| 5 | `05_CHATGPT_WORK_HANDOFF_VERIFIABLE` | ChatGPT Work | Alcance verificable |
| 6 | `06_CLAUDE_CODE_READ_ONLY_AUDIT` | Claude Code | Auditoría contra evidencia real |
| 7 | `07_CODEX_IMPLEMENTATION` | Codex | Implementación aprobada |
| 8 | `08_CLAUDE_CODE_FINAL_AUDIT` | Claude Code | Auditoría final independiente |
| 9 | `09_CLAUDE_CHAT_FINAL_CONSOLIDATION` | Claude Chat | Consolidación final |
| Gate | `OWNER_GATE_EDUARDO` | Eduardo | Autoridad sobre alcance y operaciones Git |

La compuerta del propietario se aplica donde el orden canónico la exija. Ningún agente puede inferirla a partir de silencio, intención o aprobación anterior de otro alcance.

## 4. Reglas de transición

1. Un agente registra la terminación de su propia intervención y el resultado entregado.
2. ChatGPT Work puede preparar el siguiente handoff previsto.
3. `CURRENT_STEP` debe existir en el `WORKFLOW_ID` declarado.
4. Un avance normal incrementa `REVISION` exactamente en uno.
5. Un salto solo es válido si el workflow lo declara o Eduardo lo autoriza expresamente con una aprobación referenciada.
6. El cierre requiere que no existan hallazgos bloqueantes o que exista una decisión explícita que los disponga.
7. `ARCHIVED` solo puede seguir a `CLOSED` y no elimina evidencia.
8. El primer slice no modifica ningún estado.

## 5. Retornos y control de ciclos

Un retorno exige un evento:

```yaml
event_type: RETURNED_FOR_CHANGES
from_step: 06_CLAUDE_CODE_READ_ONLY_AUDIT
to_step: 05_CHATGPT_WORK_HANDOFF_VERIFIABLE
reason: "Hallazgo verificable pendiente"
actor_id: claude-code
occurred_at: 2026-08-01T18:00:00Z
scope_version_before: v0.1
scope_version_after: v0.1
scope_version_assessment: NON_MATERIAL_CORRECTION
evidence_refs:
  - audits/claude-code/AUDIT.md
```

Toda devolución debe documentar motivo, actor, timestamp y evaluación de versión:

- `NON_MATERIAL_CORRECTION`: conserva la versión de alcance y registra la razón.
- `MATERIAL_SCOPE_CHANGE`: crea una nueva versión (`v0.2`, `v1.1`, etc.) y deja la anterior disponible.
- `UNDETERMINED`: bloquea el avance hasta decidir la versión.

El primer slice solo muestra los retornos registrados y detecta ciclos o versiones incoherentes. No cambia versiones ni limita automáticamente el número de retornos. Una auditoría reportará `WORKFLOW_CYCLE_REVIEW_REQUIRED` cuando el mismo par de pasos acumule tres retornos sin una decisión de disposición.

## 6. Cambio material de alcance

Es material si modifica al menos uno de estos elementos:

- capacidad incluida o excluida;
- autoridad de datos;
- superficie de escritura;
- frontera de seguridad;
- tecnología o repositorio objetivo con impacto verificable;
- criterio de aceptación;
- conjunto de archivos autorizado para modificación.

Correcciones ortográficas, referencias cruzadas o aclaraciones que no cambian obligaciones pueden conservar la versión.

## 7. Ownership

`CURRENT_OWNER` identifica quién debe producir el siguiente resultado, no quién es dueño del proyecto. El propietario final continúa siendo Eduardo.

Un cambio de owner requiere evento con actor, motivo, timestamp y paso. Si contradice el actor esperado por el workflow, necesita referencia a una decisión o aprobación válida.

## 8. Hallazgos del validador

- `UNKNOWN_WORKFLOW`;
- `UNKNOWN_STEP`;
- `INVALID_STEP_TRANSITION`;
- `REVISION_NOT_MONOTONIC`;
- `OWNER_STEP_MISMATCH`;
- `RETURN_WITHOUT_REASON`;
- `SCOPE_VERSION_ASSESSMENT_MISSING`;
- `MATERIAL_CHANGE_WITHOUT_NEW_SCOPE_VERSION`;
- `WORKFLOW_CYCLE_REVIEW_REQUIRED`;
- `OWNER_APPROVAL_NOT_FOUND`.

## 9. Referencias

- Aprobaciones y compuertas: `APPROVAL_MODEL.md`.
- Protocolo entre actores: `AGENT_COORDINATION_PROTOCOL.md`.
- Archivos del track: `BOXGHOST_STRUCTURE.md`.
