# Agent Coordination Protocol

## 1. Objetivo

Coordinar a Eduardo, ChatGPT Work, Claude Chat, Claude Code y Codex mediante handoffs explícitos y evidencia verificable. La aplicación registra y presenta el proceso; no reemplaza la autoridad humana.

## 2. Orden obligatorio

Se aplica el workflow descrito en `TRACK_AND_WORKFLOW_MODEL.md`:

```text
01 ChatGPT Work -> propuesta
02 Claude Chat -> revisión crítica
03 ChatGPT Work -> ajuste
04 Claude Chat -> consolidación
05 ChatGPT Work -> handoff verificable
06 Claude Code -> auditoría read-only
07 Codex -> implementación aprobada
08 Claude Code -> auditoría final
09 Claude Chat -> consolidación final
Owner gate -> Eduardo
```

## 3. Paquete de entrada obligatorio

Antes de actuar, el agente entrante lee:

1. `TRACK_STATE.md`;
2. `CONTEXT_PACK.md`;
3. `SCOPE.md` y su versión;
4. decisiones y aprobaciones vigentes;
5. handoff anterior;
6. evidencia directamente relevante;
7. reglas canónicas referenciadas.

Luego confirma:

```text
TRACK_ID
WORKFLOW_ID
CURRENT_STEP
CURRENT_OWNER
REVISION
SCOPE_VERSION
SOURCE_HASHES_VERIFIED
```

## 4. Contrato de salida

Cada intervención contiene:

```text
INTERVENTION_ID
AGENT
ROLE
INPUT_REFS
INPUT_HASHES
FINDINGS
DECISIONS_ACCEPTED_OR_CHALLENGED
OUTPUTS
VERDICT
NEXT_OWNER
NEXT_STEP
IMPLEMENTATION_AUTHORIZED=YES|NO
```

Un agente no reescribe la intervención de otro. Las correcciones se registran como una nueva intervención o revisión enlazada.

## 5. Ownership y exclusión conceptual

- `CURRENT_OWNER` designa un responsable del siguiente resultado.
- Solo ese actor produce la intervención principal del paso.
- Otros actores pueden aportar evidencia, pero no cambiar estado ni alcance en paralelo.
- Un cambio de ownership requiere evento explícito.
- En el primer slice, una incoherencia se reporta; no se bloquea ni modifica físicamente el track.

No se implementa un lock distribuido en v0.1. La exclusión es documental y auditable.

## 6. Aprobaciones

- Solo Eduardo aprueba el alcance de modificación.
- Solo Eduardo autoriza staging, commit o push cuando corresponda.
- Ningún agente interpreta silencio como aprobación.
- No se pide nuevamente una aprobación válida para el mismo `scope_ref` y hash.
- Un cambio material crea una nueva versión y una nueva compuerta.

El formato se define en `APPROVAL_MODEL.md`.

## 7. Retornos

`RETURNED_FOR_CHANGES` debe incluir motivo, actor, timestamp, evidencia y evaluación de la versión de alcance. Las reglas completas están en `TRACK_AND_WORKFLOW_MODEL.md`.

## 8. Jerarquía de evidencia

Cuando existan contradicciones:

1. repositorio, archivos y pruebas ejecutables;
2. evidencia archivo/línea y hashes;
3. auditoría independiente de Claude Code;
4. informe de implementación de Codex;
5. revisiones conversacionales;
6. recuerdos o resúmenes sin evidencia directa.

Las decisiones canónicas aprobadas limitan la interpretación, pero no convierten una afirmación técnica falsa en evidencia real.

## 9. Responsabilidades

| Actor | Responsabilidad | No puede |
|---|---|---|
| Eduardo | Aprobar alcance y autorizar Git | Ser sustituido por inferencia de una IA |
| ChatGPT Work | Organizar, cruzar y preparar handoffs | Implementar fuera del alcance aprobado |
| Claude Chat | Revisar y consolidar conceptualmente | Autorizar por Eduardo |
| Claude Code | Auditar read-only contra evidencia real | Modificar durante la auditoría |
| Codex | Implementar el changeset aprobado | Ampliar el alcance o autorizar Git |

## 10. Primer slice

La UI muestra workflow, owner, revisiones, retornos, decisiones y aprobaciones. El backend valida inconsistencias. No cambia estados, no crea aprobaciones y no escribe eventos.

## 11. Referencias

- Estados, retornos y versiones: `TRACK_AND_WORKFLOW_MODEL.md`.
- Aprobaciones: `APPROVAL_MODEL.md`.
- Archivos de entrada: `BOXGHOST_STRUCTURE.md`.
- Alcance de implementación: `GM_AI_WORKSPACE_IMPLEMENTATION_SCOPE_v0.1.md`.
