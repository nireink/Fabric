# BoxGhost Structure

```text
Document_status: SPECIFICATION
Applies_to: GM AI Workspace first read-only slice
Canonical_root: D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT\Fabric\gm-ai-boxghost
```

## 1. Autoridad y frontera

`gm-ai-boxghost` es la fuente canónica de archivos, estado declarativo, capturas, intervenciones, decisiones, aprobaciones, evidencia, auditorías y paquetes de continuidad.

El primer slice:

- lee Markdown, JSON y JSONL existentes;
- valida estructura, referencias, hashes y seguridad de rutas;
- reporta hallazgos sin cambiar los archivos;
- no utiliza MySQL ni otro índice persistente;
- no crea, edita, mueve ni elimina contenido en BoxGhost.

Un índice futuro deberá ser una proyección desechable y reconstruible. Toda divergencia invalida el índice, no la fuente canónica.

## 2. Estructura mínima soportada

```text
gm-ai-boxghost\
├── global\
│   ├── WORKSPACE.md
│   ├── CURRENT_RULES.md
│   ├── CURRENT_DECISIONS.md
│   ├── CURRENT_ROLES.md
│   ├── ACTIVE_BOUNDARIES.md
│   ├── ACTIVE_ADRS.md
│   ├── PROVIDER_REGISTRY.json
│   └── SOURCE_REGISTRY.json
├── projects\
│   └── gypport\
│       ├── PROJECT_CONTEXT.md
│       ├── REPOSITORIES.json
│       └── ACTIVE_TRACKS.json
├── tracks\
│   └── <TRACK-ID>\
│       ├── TRACK_STATE.md
│       ├── CONTEXT_PACK.md
│       ├── SCOPE.md
│       ├── SOURCE_MANIFEST.json
│       ├── continuity\
│       ├── dialog\
│       │   ├── events.jsonl
│       │   ├── AIs_Dialog_v2.md
│       │   └── conversation-index.json
│       ├── captures\
│       ├── interventions\
│       ├── working-files\
│       ├── attachments\
│       ├── scope-versions\
│       ├── artifacts\
│       ├── approvals\
│       ├── decisions\
│       ├── evidence\
│       ├── audits\
│       └── exports\
├── imports\
├── objects\sha256\
├── archive\
└── backups\
```

Solo `tracks/<TRACK-ID>` es obligatorio para descubrir un track. Los directorios globales son contexto adicional y su ausencia genera un hallazgo de configuración, no la invención de datos.

## 3. Identificadores y rutas

- `TRACK-ID` usa `^[A-Z0-9][A-Z0-9-]{2,99}$`.
- Toda ruta declarada es relativa a la raíz canónica y usa `/` en JSON.
- Se rechazan rutas absolutas, `..`, segmentos vacíos, caracteres NUL y enlaces simbólicos que salgan de la raíz.
- Antes de abrir un archivo se resuelve su ruta real y se confirma que permanece dentro de la raíz configurada.
- La aplicación no sigue junctions o symlinks fuera de la raíz.

## 4. Formato mínimo de `TRACK_STATE.md`

Cabecera legible por humanos y máquina:

```yaml
---
track_id: GM-IA-COLLABORATION-WORKSPACE-01
lifecycle_status: ACTIVE
workflow_id: GYPPORT_AI_COLLABORATION_9_STEP_V1
current_step: 05_CHATGPT_WORK_HANDOFF_VERIFIABLE
current_owner: CHATGPT_WORK
revision: 5
scope_version: v0.1
updated_at: 2026-08-01T16:00:00Z
sensitivity: INTERNAL
---
```

El cuerpo Markdown puede explicar el estado. El contrato semántico completo se define en `TRACK_AND_WORKFLOW_MODEL.md`.

## 5. Formato mínimo de `SOURCE_MANIFEST.json`

```json
{
  "schema_version": "1.0",
  "track_id": "GM-IA-COLLABORATION-WORKSPACE-01",
  "revision": 1,
  "files": [
    {
      "path": "TRACK_STATE.md",
      "sha256": "<64 lowercase hex>",
      "media_type": "text/markdown",
      "sensitivity": "INTERNAL",
      "source_ref": "owner-created"
    }
  ]
}
```

Un hash ausente se reporta como `INTEGRITY_NOT_DECLARED`. Un hash presente e incorrecto es `INTEGRITY_MISMATCH` y el contenido afectado no se presenta como confiable.

## 6. Eventos de diálogo

Cada línea de `dialog/events.jsonl` es un objeto JSON independiente:

```json
{"event_id":"evt-0001","track_id":"GM-IA-COLLABORATION-WORKSPACE-01","occurred_at":"2026-08-01T16:00:00Z","actor_id":"eduardo","actor_type":"HUMAN","event_type":"OWNER_INSTRUCTION","content_ref":"interventions/owner/00-init/OWNER_INSTRUCTION.md","sensitivity":"INTERNAL"}
```

Una línea inválida se reporta con archivo y número de línea. El lector continúa solo cuando hacerlo no mezcla ni expone contenido sensible; de lo contrario falla cerradamente para el recurso.

## 7. Referencias internas

Una referencia debe incluir:

```text
ref_id
ref_type
relative_path
sha256 cuando exista
```

El lector distingue:

- `MISSING_REFERENCE`;
- `BROKEN_REFERENCE`;
- `HASH_MISMATCH`;
- `REFERENCE_OUTSIDE_ROOT`;
- `UNSUPPORTED_MEDIA_TYPE`.

Las aprobaciones siguen `APPROVAL_MODEL.md`; la sensibilidad sigue `SENSITIVITY_AND_SECRET_HANDLING_POLICY.md`.

## 8. Tres fixtures sintéticos obligatorios

### Fixture A — válido mínimo

```text
valid-minimal\tracks\TEST-MINIMAL-01\
├── TRACK_STATE.md
├── CONTEXT_PACK.md
├── SCOPE.md
└── SOURCE_MANIFEST.json
```

Resultado esperado: track descubierto, estado visible y cero errores.

### Fixture B — válido completo

Incluye los cuatro archivos mínimos, `dialog/events.jsonl`, una decisión, una aprobación válida, una evidencia y hashes correctos.

Resultado esperado: detalle, timeline, decisión, aprobación y evidencia visibles; cero mutaciones.

### Fixture C — inválido fail-closed

Incluye, de forma sintética y sin credenciales reales: referencia `../../outside`, hash incorrecto, estado imposible y cadena con forma de secreto ficticio.

Resultado esperado: no se lee fuera de la raíz, el supuesto valor se enmascara, se generan hallazgos y ningún archivo cambia.

## 9. Bootstrap de pruebas

```text
Tool_location=tests/fixtures/bootstrap-boxghost.sh
Tool_kind=NON_PRODUCTIVE_TEST_UTILITY
Ownership_implementation=Codex
Ownership_audit=Claude Code
Execution=ON_DEMAND_TEST_OR_DEVELOPMENT_ONLY
Production_root_allowed=NO
```

El script deberá:

1. exigir una ruta de destino explícita y confirmación explícita;
2. aceptar solo un destino inexistente o vacío;
3. rechazar raíces de unidad, `GYPPORT`, `Fabric`, la raíz productiva configurada y cualquier ruta amplia;
4. crear únicamente los tres fixtures sintéticos;
5. no contener datos privados ni secretos;
6. terminar sin cambios si cualquier guardrail falla.

## 10. Límites de lectura

Los límites exactos serán configurables y probados. Valores iniciales de seguridad:

- archivo individual: 10 MiB;
- línea JSONL: 1 MiB;
- eventos por respuesta: paginados, máximo 200;
- profundidad de referencia: 8;
- archivos por track en un escaneo: 10 000.

Superar un límite produce un hallazgo explícito; no se trunca silenciosamente contenido que pudiera cambiar su significado.

## 11. Referencias normativas

- Estados y versiones: `TRACK_AND_WORKFLOW_MODEL.md`.
- Aprobaciones: `APPROVAL_MODEL.md`.
- Datos sensibles: `SENSITIVITY_AND_SECRET_HANDLING_POLICY.md`.
- Backup y restauración: `BOXGHOST_OPERATIONS.md`.
- Alcance ejecutable: `GM_AI_WORKSPACE_IMPLEMENTATION_SCOPE_v0.1.md`.
