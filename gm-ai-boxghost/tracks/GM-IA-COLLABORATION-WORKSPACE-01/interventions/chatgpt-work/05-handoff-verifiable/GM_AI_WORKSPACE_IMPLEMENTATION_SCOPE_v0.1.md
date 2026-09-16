# GM AI Workspace — Implementation Scope v0.1

```text
Track: GM-IA-COLLABORATION-WORKSPACE-01
Intervention: 05_CHATGPT_WORK_HANDOFF_VERIFIABLE
Scope_version: v0.1
Status: PROPOSED_FOR_READ_ONLY_AUDIT
Implementation_authorized: NO
```

## 1. Objetivo

Implementar, después de la auditoría y aprobación correspondientes, un primer slice vertical de solo lectura que descubra, valide y presente tracks ya existentes en `Fabric\gm-ai-boxghost`.

Este documento es el único alcance de implementación. Las siete especificaciones adjuntas son contratos normativos y no amplían por sí solas las capacidades incluidas.

## 2. Ubicaciones

```text
APPLICATION_ROOT=D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT\Modules\gm-ai-workspace
BOXGHOST_ROOT=D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT\Fabric\gm-ai-boxghost
BOXGHOST_ROOT_CONFIG=GM_AI_BOXGHOST_ROOT
```

El módulo contiene código y pruebas. BoxGhost contiene datos privados. Ninguna conversación real se copia al repositorio del módulo.

## 3. Autoridad

```text
BOXGHOST_CANONICAL=YES
DATABASE_IN_FIRST_SLICE=NO
DERIVED_PERSISTENT_INDEX=NO
BOXGHOST_WRITES=NO
```

El lector nunca resuelve una divergencia modificando la fuente. MySQL queda fuera del slice.

## 4. Capacidades incluidas

### Backend

- resolver la raíz configurada de forma segura;
- descubrir tracks válidos;
- leer Markdown, JSON y JSONL admitidos;
- validar esquema, rutas, referencias, hashes y límites;
- construir vistas de listado, detalle y timeline en memoria;
- detectar estados/transiciones incoherentes;
- detectar patrones de secretos sin exponer valores;
- devolver hallazgos estructurados y seguros;
- responder solo mediante operaciones de lectura.

### Frontend

- listar y filtrar tracks;
- mostrar lifecycle, step, owner, revision y scope version;
- mostrar detalle, timeline, `CONTEXT_PACK`, decisiones y aprobaciones existentes;
- mostrar integridad, referencias rotas y otros hallazgos;
- enmascarar posibles secretos;
- comunicar estados vacío, ausente, inválido y no autorizado sin ambigüedad.

```text
FRONTEND_CAPABILITIES=DISPLAY_ONLY
BACKEND_CAPABILITIES=READ_VALIDATE_REPORT
```

## 5. Superficie HTTP propuesta

Solo métodos `GET`:

```text
GET /api/workspace/health
GET /api/tracks
GET /api/tracks/{trackId}
GET /api/tracks/{trackId}/timeline
GET /api/tracks/{trackId}/context
GET /api/tracks/{trackId}/decisions
GET /api/tracks/{trackId}/approvals
GET /api/tracks/{trackId}/findings
```

No habrá `POST`, `PUT`, `PATCH` ni `DELETE`. Los errores no devolverán rutas absolutas, contenido sensible ni trazas internas.

## 6. Capacidades excluidas

- captura o importación de sesiones;
- creación, edición, movimiento o eliminación en BoxGhost;
- cambios de workflow, lifecycle, owner o scope;
- creación, revocación o aprobación;
- base de datos o índice persistente;
- autenticación multiusuario;
- integraciones de proveedor en tiempo real;
- backup productivo o restauración;
- migración del ZIP histórico;
- limpieza de carpetas duplicadas;
- staging, commit, push o despliegue.

## 7. Contratos aplicables

| Tema | Documento normativo |
|---|---|
| Estructura, archivos, rutas y fixtures | `BOXGHOST_STRUCTURE.md` |
| Estado, workflow, retornos y versiones | `TRACK_AND_WORKFLOW_MODEL.md` |
| Aprobaciones existentes | `APPROVAL_MODEL.md` |
| Sensibilidad y secretos | `SENSITIVITY_AND_SECRET_HANDLING_POLICY.md` |
| Captura futura, expresamente excluida | `SESSION_CAPTURE_BY_PROVIDER.md` |
| Backup y ZIP futuro | `BOXGHOST_OPERATIONS.md` |
| Handoffs y autoridad | `AGENT_COORDINATION_PROTOCOL.md` |

En caso de contradicción, este alcance decide inclusión/exclusión y el documento temático decide el contrato de su materia.

## 8. Bootstrap y fixtures

```text
BOOTSTRAP_DECISION:
  Tool_location: tests/fixtures/bootstrap-boxghost.sh
  Packaging: inside gm-ai-workspace; non-productive
  Ownership: Codex implements; Claude Code audits
  Execution: on demand in tests or development only
  Production_execution: prohibited
  Production_root: Fabric\gm-ai-boxghost must never be a target
  Safety: reject non-empty or broad directories; require explicit confirmation
```

El script crea exclusivamente los tres fixtures sintéticos definidos en `BOXGHOST_STRUCTURE.md`. Su escritura controlada en un destino de pruebas no habilita escritura productiva en BoxGhost.

## 9. Seguridad

- normalización y verificación de rutas reales antes de leer;
- rechazo de traversal, symlinks/junctions fuera de raíz y tipos no permitidos;
- límites de tamaño, líneas, profundidad y paginación;
- parsing sin evaluación de código;
- ningún secreto en UI, logs, excepciones o fixtures;
- CORS limitado a orígenes locales configurados durante desarrollo;
- errores fail-closed cuando la confianza del recurso no puede establecerse.

## 10. Pruebas mínimas

### Contrato

- fixture válido mínimo;
- fixture válido completo;
- fixture inválido fail-closed;
- hashes correctos, ausentes e incorrectos;
- JSON/JSONL inválido;
- referencia ausente y traversal;
- workflow válido, salto inválido y retorno sin evaluación de versión;
- aprobación válida, vencida, revocada y con scope hash incorrecto;
- patrón secreto sintético enmascarado en API, UI y logs.

### No mutación

Antes y después de cada suite se calcula un manifiesto de los fixtures y de una copia read-only de prueba. Los hashes, nombres, mtimes relevantes y número de archivos deben permanecer iguales, salvo el directorio nuevo que el bootstrap crea explícitamente en una prueba aislada.

### API/UI

- todos los endpoints admitidos son GET;
- métodos de escritura devuelven 405 o no existen;
- listado, detalle, timeline y hallazgos son accesibles;
- estados de error no filtran rutas absolutas ni valores sensibles;
- paginación y límites funcionan.

## 11. Criterios de aceptación

```text
AC-01 BoxGhost es la única fuente leída y no se crea BD.
AC-02 Ninguna operación del producto modifica BoxGhost.
AC-03 Los tres fixtures producen los resultados esperados.
AC-04 Traversal y enlaces fuera de raíz fallan cerradamente.
AC-05 Los hashes y referencias se validan y reportan.
AC-06 El modelo de track distingue lifecycle, workflow, step, owner y revision.
AC-07 Los retornos muestran la evaluación de versión de alcance.
AC-08 Las aprobaciones se presentan con alcance, condiciones, vigencia y revocación.
AC-09 Los secretos sintéticos nunca aparecen en respuestas, UI o logs.
AC-10 No existen endpoints ni controles de mutación.
AC-11 Las pruebas usan solo datos sintéticos.
AC-12 El ZIP histórico, la captura y la unificación no aparecen como código activo.
```

## 12. Cambios previstos, no autorizados todavía

Claude Code deberá verificar la existencia y estado real de:

- `Modules\gm-ai-workspace`;
- reglas `AGENTS.md` aplicables;
- repositorio y working tree;
- stack realmente disponible;
- conflictos con estructuras preexistentes;
- ruta de BoxGhost y capacidad de auditarla sin escribir;
- ZIP histórico y duplicados solo para confirmar que permanecen fuera del changeset.

El changeset exacto se cerrará después de esa auditoría. No se presupone que las carpetas planeadas ya existan.

## 13. Compuertas

```text
NEXT=CLAUDE_CODE_READ_ONLY_AUDIT
OWNER_APPROVAL_REQUIRED_BEFORE_CODEX=YES
OWNER_APPROVAL_ALREADY_INFERRED=NO
CODEX_ALLOWED_NOW=NO
FABRIC_WRITE_ALLOWED=NO
GIT_WRITE_ALLOWED=NO
```

La aprobación deberá identificar `SCOPE_VERSION`, hashes del paquete y conjunto exacto de rutas autorizadas.
