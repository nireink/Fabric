---
track_id: GM-IA-COLLABORATION-WORKSPACE-01
scope_version: v0.1
scope_status: APPROVED_FOR_IMPLEMENTATION
implementation_authorized: true
owner_approval_recorded: true
sensitivity: INTERNAL
---

# Alcance vigente v0.1

La autoridad del alcance implementable es:

```text
interventions/chatgpt-work/05-handoff-verifiable/
GM_AI_WORKSPACE_IMPLEMENTATION_SCOPE_v0.1.md
```

Sus siete especificaciones normativas asociadas permanecen en la misma intervención 05. Este archivo raíz no las duplica: identifica la versión vigente y su estado de gobernanza.

## Inclusiones

- Primer slice local de solo lectura.
- Backend `READ + VALIDATE + REPORT`.
- Frontend de visualización.
- Lectura segura de tracks preexistentes en `Fabric\gm-ai-boxghost`.
- Validación de rutas, estructura, hashes, referencias, límites, workflow, aprobaciones existentes y patrones sintéticos de secretos.
- Fixtures sintéticos, bootstrap no productivo y pruebas implementados dentro de `Modules\gm-ai-workspace`.

## Exclusiones

- Escritura, edición, movimiento o eliminación en BoxGhost productivo.
- MySQL u otro índice persistente.
- Captura o importación de sesiones.
- Mutaciones de aprobaciones, workflow, lifecycle, owner o scope.
- Multiusuario e integraciones en tiempo real.
- Migración del ZIP histórico y limpieza de duplicados.
- Staging, commit, push o despliegue.

## Estado de aprobación

```text
CLAUDE_CODE_FINAL_VERIFICATION=ACCEPTED
FINAL_VERIFICATION_SHA256=6ca464613c810b6c5ff41f20eb479dbd18fffc7dedc2725ded4de604a17f501e
CORRECTION_TYPE=NON_MATERIAL
EDUARDO_SCOPE_APPROVAL=GRANTED
OWNER_REAPPROVAL_REQUIRED=NO
CURRENT_INTERVENTION=07_CODEX_IMPLEMENTATION
```
