# GM AI Workspace — Audit Remediation v0.1

```text
TRACK=GM-IA-COLLABORATION-WORKSPACE-01
SOURCE_AUDIT=06_CLAUDE_CODE_READ_ONLY_AUDIT
SOURCE_VERDICT=BLOCKED
WORKFLOW_DISPOSITION=RETURNED_FOR_CHANGES
RETURN_TO_STEP=05_CHATGPT_WORK_HANDOFF_VERIFIABLE
SCOPE_VERSION_BEFORE=v0.1
SCOPE_VERSION_AFTER=v0.1
SCOPE_CHANGE=NON_MATERIAL_CORRECTION
IMPLEMENTATION_AUTHORIZED=NO
```

## Propósito

Este paquete completa evidencia operativa que faltaba en el track. No cambia las capacidades, exclusiones, tecnologías, rutas de implementación ni criterios de aceptación del alcance v0.1.

## Cruce de la auditoría

### Aceptado como bloqueo previo a aprobación

1. Formalizar las intervenciones 02 y 04 de Claude Chat.
2. Crear `TRACK_STATE.md`, `SCOPE.md`, `CONTEXT_PACK.md` y `SOURCE_MANIFEST.json` en la raíz del track.
3. Crear `dialog/events.jsonl` con la secuencia verificable y el retorno por cambios.

### Reclasificado como trabajo de implementación

1. Los tres fixtures sintéticos deben ser implementados por Codex dentro de `Modules\gm-ai-workspace\tests\fixtures`; no deben existir en el track productivo como precondición de la aprobación.
2. Las pruebas de path traversal, symlinks/junctions, hashes, secretos y no mutación son pruebas obligatorias de la intervención 07 y criterios de la auditoría final 08; su ausencia antes de implementar no es un defecto del handoff.
3. La aprobación de Eduardo debe permanecer ausente hasta que la reauditoría read-only acepte el alcance exacto. No se crea ni se infiere una aprobación en este paquete.

## Instalación manual

Copiar el contenido de `place-at-track-root` dentro de:

```text
D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT\Fabric\gm-ai-boxghost\
tracks\GM-IA-COLLABORATION-WORKSPACE-01\
```

La copia agrega los archivos faltantes en sus rutas canónicas. No sustituya ni elimine las intervenciones 01, 03, 05 o 06 existentes.

Después, Claude Code debe hacer una reauditoría read-only limitada a confirmar esta corrección. Todavía no corresponde autorizar a Codex.
