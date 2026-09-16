# Approval Model

## 1. Principio

Una aprobación es un registro explícito, delimitado, verificable y no destructivo. No existe aprobación implícita. El primer slice solo muestra y valida aprobaciones ya presentes en BoxGhost.

## 2. Esquema lógico

```yaml
schema_version: "1.0"
id: "apr-<uuid>"
track_id: "GM-IA-COLLABORATION-WORKSPACE-01"
scope_type: "TRACK | SCOPE_VERSION | DECISION | ARTIFACT | CHANGESET | RELEASE_ACTION"
scope_ref: "scope-versions/v0.1/SCOPE.md"
scope_sha256: "<64 lowercase hex>"
decision: "APPROVED | REJECTED | APPROVED_WITH_CONDITIONS"
conditions: []
granted_by: "eduardo"
granted_at: "2026-08-01T18:00:00Z"
effective_from: "2026-08-01T18:00:00Z"
expires_at: null
revocable: true
revoked_by: null
revoked_at: null
revocation_reason: null
evidence_refs: []
source_capture_ref: "captures/human/<session>/TRANSCRIPT.jsonl"
content_sha256: "<hash of canonical approval record>"
sensitivity: "INTERNAL"
```

## 3. Alcance

| `scope_type` | Aplicación |
|---|---|
| `TRACK` | Decisión general del track, sin autorizar automáticamente cada cambio material |
| `SCOPE_VERSION` | Versión exacta del alcance |
| `DECISION` | Decisión individual |
| `ARTIFACT` | Archivo o paquete identificado por hash |
| `CHANGESET` | Conjunto exacto de rutas y cambios |
| `RELEASE_ACTION` | staging, commit, push, despliegue u otra acción expresamente nombrada |

La autorización para implementar no autoriza staging, commit o push. Cada acción Git se registra como `RELEASE_ACTION` o conforme a la compuerta explícita del propietario.

## 4. Condiciones y vigencia

- `APPROVED_WITH_CONDITIONS` exige al menos una condición verificable.
- Una condición no puede ampliar el alcance; solo restringirlo o exigir evidencia.
- `effective_from` no puede ser anterior a `granted_at`.
- Una aprobación vencida no es válida para acciones posteriores.
- La aprobación continúa siendo evidencia histórica tras vencer o revocarse.

## 5. Revocación

La revocación se registra como evento adicional; nunca reescribe ni elimina el registro original.

```yaml
event_type: APPROVAL_REVOKED
approval_ref: approvals/apr-123.json
revoked_by: eduardo
revoked_at: 2026-08-02T10:00:00Z
reason: "El alcance cambió materialmente"
```

Solo un actor con autoridad equivalente o superior puede revocar. Para este track, las aprobaciones de alcance y Git pertenecen a Eduardo.

## 6. Cambios y no repetición

- Un cambio material produce una nueva versión de alcance y requiere una aprobación nueva.
- Una corrección no material dentro del mismo alcance aprobado no provoca una solicitud repetitiva.
- El consumidor verifica `scope_ref` y `scope_sha256`; una coincidencia solo por nombre no basta.
- Una aprobación de otro track no cruza automáticamente a este.
- Una aprobación con múltiples efectos debe enumerar cada referencia o usar un changeset cerrado y hasheado.

## 7. Visibilidad

El primer usuario es Eduardo. La UI puede mostrar:

- decisión y estado de vigencia;
- actor y timestamps;
- alcance y hash;
- condiciones;
- evidencia;
- historial de revocación.

Los campos o evidencias restringidos se presentan según `SENSITIVITY_AND_SECRET_HANDLING_POLICY.md`. Nunca se muestra un secreto para probar una aprobación.

## 8. Validaciones

- campos obligatorios presentes;
- UUID o identificador conforme al esquema;
- `track_id` coincide con el track contenedor;
- `scope_ref` existe, permanece en la raíz y coincide con su hash;
- condiciones consistentes con `decision`;
- timestamps ordenados;
- revocación permitida y completa;
- `content_sha256` verificable;
- `source_capture_ref` existente y seguro.

Hallazgos:

```text
APPROVAL_SCOPE_MISSING
APPROVAL_SCOPE_HASH_MISMATCH
APPROVAL_EXPIRED
APPROVAL_REVOKED
APPROVAL_CONDITION_MISSING
APPROVAL_SOURCE_MISSING
APPROVAL_AUTHORITY_INVALID
```

## 9. Referencias

- Versionado material: `TRACK_AND_WORKFLOW_MODEL.md`.
- Coordinación y autoridad: `AGENT_COORDINATION_PROTOCOL.md`.
- Estructura de archivos: `BOXGHOST_STRUCTURE.md`.
