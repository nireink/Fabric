# GM AI Workspace — Ajuste posterior a revisión crítica v0.2

```text
PEGAR EN: CLAUDE CHAT — CONSOLIDACIÓN DEL AJUSTE

Track: GM-IA-COLLABORATION-WORKSPACE-01
Step: ADJUSTMENT
Mode: ANALYSIS / CROSS-VALIDATION / SCOPE CORRECTION
Agent: ChatGPT Work
Status: READY_FOR_CLAUDE_CHAT_CONSOLIDATION
Intervention: 03
```

## 1. Propósito

Este documento cruza la propuesta inicial de `GM AI Workspace` con la revisión crítica de Claude Chat y corrige el alcance antes de cualquier implementación.

No autoriza:

- creación del frontend o backend;
- creación de la base de datos;
- escritura, movimiento o eliminación en `gm-ai-boxghost`;
- migración del ZIP histórico;
- staging, commit o push.

La siguiente intervención corresponde a Claude Chat para consolidar estas correcciones. Después, ChatGPT Work deberá preparar el handoff verificable y los documentos técnicos necesarios para la auditoría read-only de Claude Code.

## 2. Evidencia revisada

```text
SOURCE_DOCUMENT=Pasted markdown(3).md
SOURCE_ROLE=CLAUDE_CHAT_CRITICAL_REVIEW
SOURCE_SHA256=f877f9299d1355d9b106448c1ebe87036f03516816fd088f3cb95e53f0cfce15
SOURCE_VERDICT=ACCEPT_WITH_CHANGES
CRITICAL_FINDINGS=3
MAJOR_FINDINGS=5
MINOR_FINDINGS=4
```

La revisión es sustancialmente válida: identifica ambigüedades que impedirían una implementación verificable. Sin embargo, una recomendación central se modifica: MySQL no será la fuente primaria de verdad del primer incremento.

## 3. Decisión arquitectónica corregida

### 3.1 Autoridad de datos

Para el primer incremento:

```text
BOXGHOST_CANONICAL_SOURCE=YES
MYSQL_IN_FIRST_SLICE=NO
DERIVED_INDEX_IN_FIRST_SLICE=NO
APPLICATION_MODE=READ_ONLY
```

`Fabric\gm-ai-boxghost` será la fuente canónica de:

- archivos de tracks;
- estado declarativo del track;
- paquetes de contexto;
- intervenciones;
- aprobaciones y decisiones registradas;
- evidencias y auditorías;
- manifiestos e integridad de contenido.

El primer slice leerá y validará directamente Markdown, JSON y JSONL. No dependerá de MySQL para descubrir, interpretar ni presentar un track.

Si posteriormente se incorpora MySQL, SQLite, Lucene u otro índice:

1. será una proyección derivada y reconstruible;
2. no almacenará como autoridad ningún estado que no exista en BoxGhost;
3. tendrá registrado el hash y la versión de la fuente indexada;
4. una divergencia invalidará el índice, nunca el archivo canónico;
5. la recuperación consistirá en reconstruir el índice desde BoxGhost;
6. no se permitirá resolución automática de conflictos que modifique archivos canónicos.

### 3.2 Mutabilidad e historial

No todo archivo de BoxGhost será físicamente inmutable, porque `TRACK_STATE.md`, `CONTEXT_PACK.md` y los índices vigentes deben evolucionar. La regla correcta es:

```text
RAW_CAPTURES=APPEND_ONLY_OR_CONTENT_ADDRESSED
PROMOTED_EVIDENCE=IMMUTABLE
CURRENT_STATE=VERSIONED_UPDATE
DELETION=OWNER_GATED
AUDIT_TRAIL=MANDATORY
```

Los originales capturados y la evidencia promovida se preservan. Los archivos de estado actual pueden actualizarse únicamente mediante nuevas versiones auditadas. El primer slice no realizará ninguna de estas escrituras.

## 4. Cruce de hallazgos

| ID | Hallazgo de Claude Chat | Decisión de ChatGPT Work | Estado |
|---|---|---|---|
| C-01 | Autoridad híbrida MySQL + BoxGhost indefinida | Aceptado con corrección: BoxGhost será canónico; MySQL queda fuera del primer slice y solo podrá ser índice reconstruible | RESOLVED_IN_ADJUSTMENT |
| C-02 | Captura por proveedor no especificada | Aceptado: se definirá el contrato de importación por proveedor, pero la captura queda fuera del primer slice read-only | SPEC_REQUIRED_BEFORE_HANDOFF |
| C-03 | Sensibilidad y secretos sin operación definida | Aceptado: política obligatoria y protección de visualización; captura/redacción automática queda fuera del primer slice | SPEC_REQUIRED_BEFORE_HANDOFF |
| M-04 | Dependencia de un BoxGhost pre-poblado | Aceptado: plantilla, ejemplos y fixtures controlados; bootstrap solo sobre destino vacío de prueba | SPEC_REQUIRED_BEFORE_HANDOFF |
| M-05 | `STEP` subespecificado | Aceptado: separar ciclo de vida, workflow e intervención actual; transiciones auditables | RESOLVED_CONCEPTUALLY |
| M-06 | Aprobaciones incompletas | Aceptado: ampliar identidad, alcance, condición, revocación, vencimiento y evidencia | SPEC_REQUIRED_BEFORE_HANDOFF |
| M-07 | Migración del ZIP ambigua | Aceptado: ninguna migración en el primer slice; se exigirá inventario y matriz de disposición en track posterior | REMOVED_FROM_FIRST_SLICE |
| M-08 | Operación de BoxGhost indefinida | Aceptado: backup, retención, restauración y crecimiento deberán quedar especificados antes de implementación | SPEC_REQUIRED_BEFORE_HANDOFF |
| M-09 | Coordinación entre agentes indefinida | Aceptado y subordinado al orden canónico de colaboración ya aprobado | SPEC_REQUIRED_BEFORE_HANDOFF |
| m-10 | Niveles de sensibilidad no enumerados | Aceptado | MERGED_IN_C-03 |
| m-11 | Integridad sin momentos de verificación | Aceptado: arranque, lectura bajo demanda y auditoría programada futura | RESOLVED_CONCEPTUALLY |
| m-12 | Faltan ejemplos de contexto y estado | Aceptado: tres fixtures mínimos | MERGED_IN_M-04 |
| m-13 | Saltos de `STEP` ambiguos | Aceptado: solo según workflow y con excepción auditada | MERGED_IN_M-05 |

## 5. Modelo corregido de Track

`STEP` no se tratará como un estado genérico aislado. El modelo distinguirá:

```text
LIFECYCLE_STATUS = DRAFT | ACTIVE | PAUSED | CLOSED | ARCHIVED
WORKFLOW_ID       = identificador del flujo aplicable
CURRENT_STEP      = paso definido por el workflow
CURRENT_OWNER     = actor responsable del siguiente resultado
REVISION          = entero monotónico
```

Para este track, el workflow aplicable será el orden canónico ya aprobado:

```text
01 CHATGPT_WORK_INITIAL_PROPOSAL
02 CLAUDE_CHAT_CRITICAL_REVIEW
03 CHATGPT_WORK_ADJUSTMENT
04 CLAUDE_CHAT_CONSOLIDATION
05 CHATGPT_WORK_HANDOFF_VERIFIABLE
06 CLAUDE_CODE_READ_ONLY_AUDIT
07 CODEX_IMPLEMENTATION
08 CLAUDE_CODE_FINAL_AUDIT
09 CLAUDE_CHAT_FINAL_CONSOLIDATION
OWNER_GATE_EDUARDO
```

Reglas:

1. Cada agente puede registrar la terminación de su propia intervención.
2. ChatGPT Work puede preparar el siguiente handoff conforme al workflow aprobado.
3. Ningún agente puede inferir una aprobación de Eduardo.
4. Solo Eduardo aprueba el alcance de modificación y autoriza staging, commit o push.
5. Un retorno a un paso anterior exige `RETURNED_FOR_CHANGES`, motivo, actor y timestamp.
6. Un salto de paso solo será válido cuando el workflow lo permita o Eduardo lo autorice explícitamente.
7. La aplicación del primer slice solo mostrará y validará estas transiciones; no las ejecutará.

## 6. Modelo corregido de Approval

La especificación deberá contemplar, como mínimo:

```text
Approval
  id: UUID
  track_id: string
  scope_type: TRACK | SCOPE_VERSION | DECISION | ARTIFACT | CHANGESET | RELEASE_ACTION
  scope_ref: string
  decision: APPROVED | REJECTED | APPROVED_WITH_CONDITIONS
  conditions: string[]
  granted_by: actor_id
  granted_at: timestamp
  effective_from: timestamp
  expires_at: timestamp | null
  revocable: boolean
  revoked_by: actor_id | null
  revoked_at: timestamp | null
  revocation_reason: string | null
  evidence_refs: string[]
  source_capture_ref: string
  content_sha256: string
```

Reglas adicionales:

- No existe aprobación implícita.
- Una aprobación aplica únicamente al `scope_ref` identificado.
- Una modificación material genera una nueva versión de alcance y requiere nueva aprobación.
- Una corrección dentro del mismo alcance ya aprobado no debe provocar solicitudes repetitivas.
- La revocación no borra la aprobación previa; agrega un evento auditable.
- El primer slice solo visualizará aprobaciones ya registradas.

## 7. Política mínima de sensibilidad

Niveles propuestos:

```text
PUBLIC
INTERNAL
CONFIDENTIAL
RESTRICTED
REDACTED
```

`SECRET` no será un nivel de almacenamiento permitido: si se detecta un secreto operativo, el contenido deberá rechazarse o redactarse antes de ingresar a BoxGhost.

Reglas para el primer slice:

1. No mostrar valores que coincidan con patrones de credenciales reconocibles.
2. Registrar únicamente el tipo de hallazgo, la ruta y el hash; nunca el valor secreto.
3. Fallar de forma cerrada ante clasificación ausente en material marcado como restringido.
4. No modificar automáticamente el archivo durante la lectura.
5. Informar que el archivo requiere saneamiento mediante un proceso separado y aprobado.

La política detallada definirá patrones, falsos positivos, excepciones autorizadas y responsabilidades de clasificación.

## 8. Captura de sesiones por proveedor

La primera implementación no capturará sesiones. Solo leerá capturas ya incorporadas y validadas.

El contrato previo al handoff deberá cubrir:

| Origen | Modalidad inicial | Iniciador | Actualización | Identidad externa |
|---|---|---|---|---|
| ChatGPT / ChatGPT Work | Exportación o archivo expuesto por la plataforma | Eduardo | Nueva revisión de importación; nunca sobrescritura silenciosa | ID nativo cuando exista; de lo contrario, ID derivado documentado |
| Claude Chat | Exportación o captura autorizada | Eduardo | Nueva revisión de importación | ID nativo cuando exista; de lo contrario, ID derivado documentado |
| Codex | Entregables, transcript y resultados expuestos | Eduardo o integración autorizada futura | Eventos anexados con procedencia | ID de sesión expuesto |
| Claude Code | Transcript, comandos, resultados y archivos expuestos | Eduardo o integración autorizada futura | Eventos anexados con procedencia | ID de sesión expuesto |
| Humano | Ingreso manual o archivo firmado/fechado | Actor humano | Nueva intervención | UUID generado por Workspace |

No se promete captura de archivos privados internos que el proveedor no exponga. Integraciones en tiempo real quedan fuera de esta fase.

## 9. Estructura, bootstrap y fixtures

Antes de implementar, `BOXGHOST_STRUCTURE.md` deberá incluir al menos tres casos:

1. track válido mínimo;
2. track válido con decisiones, aprobación y evidencia;
3. track inválido para demostrar fallos cerrados.

La utilidad `bootstrap-boxghost`, si se acepta en el handoff, tendrá estas restricciones:

- solo opera sobre una ruta explícita;
- exige que el destino no exista o esté vacío;
- rechaza rutas raíz, `Fabric`, `GYPPORT` o cualquier destino amplio;
- crea fixtures, nunca datos productivos;
- no modifica `Fabric\gm-ai-boxghost` durante el primer slice;
- puede ejecutarse únicamente en un directorio temporal o de pruebas.

## 10. ZIP histórico y unificación

`GYPPORT_AI_Workspace.zip` permanece como evidencia histórica. El primer slice no copiará esquemas ni código desde el ZIP.

La migración selectiva y la limpieza de duplicados pertenecerán a un track separado. Ese track deberá producir una matriz por archivo:

```text
PATH
SHA256
PURPOSE
CURRENT_AUTHORITY
TARGET_OWNER
DISPOSITION=REUSE | ADAPT | ARCHIVE | DELETE_CANDIDATE
RATIONALE
DEPENDENCIES
OWNER_APPROVAL_REQUIRED
```

Ningún elemento se eliminará solamente por ser antiguo o duplicado. Primero se verificará identidad, autoridad, referencias y posibilidad de recuperación. Toda eliminación material requerirá una única aprobación de Eduardo para el alcance exacto.

## 11. Operación de BoxGhost

La especificación operativa previa a implementación deberá fijar:

- almacenamiento primario local en la ruta confirmada;
- copia secundaria y copia externa cifrada;
- RPO y RTO iniciales;
- frecuencia de backup;
- manifiestos SHA-256;
- pruebas periódicas de restauración;
- retención permanente de conversaciones, decisiones, aprobaciones y evidencia;
- archivo de tracks cerrados sin pérdida de trazabilidad;
- umbrales de crecimiento y procedimiento de expansión;
- recuperación ante eliminación accidental;
- exclusión absoluta de secretos, tokens y credenciales.

La ubicación primaria confirmada es:

```text
D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT\Fabric\gm-ai-boxghost
```

## 12. Protocolo de coordinación

El protocolo deberá implementar documentalmente el orden canónico aprobado:

1. El agente entrante lee `TRACK_STATE.md`, `CONTEXT_PACK.md`, alcance, decisiones, aprobaciones y handoff vigente.
2. Confirma la identidad del track, paso, revisión y hashes de las fuentes relevantes.
3. Produce su intervención en la carpeta que le corresponde.
4. No reescribe intervenciones de otros agentes.
5. Declara hallazgos, evidencia, veredicto y siguiente agente.
6. Cualquier cambio de alcance crea una nueva versión explícita.
7. `CURRENT_OWNER` identifica al actor responsable del siguiente resultado.
8. Solo un actor puede modificar el estado declarativo a la vez; el primer slice únicamente detectará incoherencias.
9. La aplicación no reemplaza la autoridad de Eduardo ni infiere autorizaciones.

## 13. Decisiones que Claude Chat marcó como no resueltas

### D-01 — ¿Quién cambia el paso?

```text
DECISION=RESOLVED_BY_EXISTING_GOVERNANCE
```

Los agentes pueden registrar la terminación y el handoff de sus intervenciones conforme al workflow. Las compuertas de aprobación de alcance y operaciones Git permanecen exclusivamente en Eduardo.

### D-02 — Ubicación de BoxGhost

```text
DECISION=LOCAL_PRIMARY_CONFIRMED
PRIMARY_ROOT=D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT\Fabric\gm-ai-boxghost
SHARED_OR_CLOUD_PRIMARY=DEFERRED
EXTERNAL_ENCRYPTED_BACKUP=REQUIRED_BY_OPERATIONS_SPEC
```

### D-03 — Captura en tiempo real o manual

```text
DECISION=MANUAL_OR_EXPORTED_INPUTS_FOR_INITIAL_VERSION
REAL_TIME_INTEGRATIONS=DEFERRED
```

Esta decisión no afecta el primer slice porque la captura está excluida.

### D-04 — Usuarios iniciales

```text
DECISION=EDUARDO_ONLY_FOR_INITIAL_VERSION
MULTI_USER_ACCESS=DEFERRED
AUTHORIZATION_MODEL=DESIGN_FOR_EXTENSION_WITHOUT_IMPLEMENTING_IT_NOW
```

## 14. Primer slice ajustado

### Incluido

- Resolver la raíz configurada de BoxGhost de forma segura.
- Validar que la ruta esté dentro de la raíz permitida.
- Descubrir tracks mediante estructura y manifiestos válidos.
- Listar y filtrar tracks.
- Mostrar detalle, timeline, `CONTEXT_PACK`, decisiones y aprobaciones existentes.
- Verificar hashes declarados cuando estén disponibles.
- Detectar archivos ausentes, JSON/JSONL inválido, referencias rotas y transiciones imposibles.
- Ocultar la presentación de posibles secretos y emitir un hallazgo sin exponer el valor.
- Operar sin escritura en BoxGhost.
- Usar fixtures sintéticos, nunca conversaciones privadas reales, en pruebas automatizadas.

### Excluido

- Captura o importación de sesiones.
- Escritura, edición, movimiento o eliminación en BoxGhost.
- Creación o revocación de aprobaciones.
- Cambio de `STEP`, lifecycle u ownership.
- MySQL u otro índice persistente.
- Autenticación multiusuario.
- Integraciones en tiempo real.
- Migración del ZIP histórico.
- Limpieza o eliminación de carpetas duplicadas.
- Backup automatizado productivo.
- staging, commit o push.

## 15. Documentos requeridos para la intervención 05

Después de la consolidación de Claude Chat, ChatGPT Work deberá producir un paquete coherente, evitando documentos repetidos:

1. `BOXGHOST_STRUCTURE.md`
2. `TRACK_AND_WORKFLOW_MODEL.md`
3. `APPROVAL_MODEL.md`
4. `SENSITIVITY_AND_SECRET_HANDLING_POLICY.md`
5. `SESSION_CAPTURE_BY_PROVIDER.md`
6. `BOXGHOST_OPERATIONS.md`
7. `AGENT_COORDINATION_PROTOCOL.md`
8. `GM_AI_WORKSPACE_IMPLEMENTATION_SCOPE_v0.1.md`

El octavo documento será el alcance único de implementación y referenciará los otros siete; no duplicará su contenido.

La evaluación del ZIP no generará todavía otro documento activo. Se tratará en el futuro track de unificación mediante una única matriz de disposición.

## 16. Criterios para que Claude Chat consolide

Claude Chat deberá determinar si:

- la autoridad canónica de BoxGhost queda inequívoca;
- excluir MySQL del primer slice elimina el conflicto de autoridad;
- las reglas de transición respetan el orden canónico entre IAs;
- las cuatro decisiones señaladas quedaron resueltas o correctamente diferidas;
- el primer slice sigue siendo verdaderamente read-only;
- los documentos previstos son suficientes sin crear responsabilidades duplicadas;
- el ZIP histórico y la limpieza permanecen fuera del alcance de implementación inicial.

El resultado esperado es uno de:

```text
CONSOLIDATED_READY_FOR_HANDOFF
CONSOLIDATED_WITH_EXACT_CORRECTIONS
RETURNED_FOR_ADJUSTMENT
```

## 17. Estado y siguiente paso

```text
TRACK=GM-IA-COLLABORATION-WORKSPACE-01
COMPLETED_INTERVENTION=03_CHATGPT_WORK_ADJUSTMENT
CURRENT_STATUS=READY_FOR_CLAUDE_CHAT_CONSOLIDATION
NEXT_INTERVENTION=04_CLAUDE_CHAT_CONSOLIDATION
IMPLEMENTATION_AUTHORIZED=NO
CODEX_ALLOWED=NO
CLAUDE_CODE_AUDIT_ALLOWED=NO
FILES_DELETED_OR_MOVED=NO
```

Siguiente paso único: Claude Chat debe revisar y consolidar este ajuste. No debe crear código ni pasar todavía a Codex.
