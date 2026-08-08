PEGAR EN: CHATGPT CODEX — REANUDACIÓN CONTROLADA DE LA FASE 1

Track: GM-AI-LOCAL-CONTEXT-CLASSIFICATION-01
Step: PHASE 1 / ROOT-01..ROOT-04 / CLASSIFICATION BATCH 001
Mode: BOUNDED SOURCE CLASSIFICATION / SOURCE READ-ONLY / NO GIT
Agent: ChatGPT Codex
Status: OWNER_AUTHORIZED_TO_EXECUTE

# 1. AUTORIZACIÓN VIGENTE

```text
OWNER_APPROVAL_ID=OA-GM-AI-LOCAL-CONTEXT-CLASSIFICATION-01-PHASE-1
OWNER_APPROVAL_STATUS=GRANTED
OWNER_APPROVAL_REVOKED=NO
OWNER_APPROVAL_MUST_BE_REPEATED=NO

TEMPORARY_CLASSIFICATION_SUSPENSION=LIFTED
SUSPENSION_LIFT_REFERENCE=OWNER_EXPLICIT_DIRECTIVE_20260802
PHASE_1_STATUS=AUTHORIZED_TO_RESUME
```

Eduardo aprueba reanudar exclusivamente la Fase 1 del track:

```text
GM-AI-LOCAL-CONTEXT-CLASSIFICATION-01
```

La autorización comprende únicamente la clasificación de:

```text
ROOT-01
ROOT-02
ROOT-03
ROOT-04
```

dentro del alcance exacto previamente aprobado para la Fase 1.

No solicites nuevamente esta aprobación.

# 2. CONDICIÓN OPERATIVA ACEPTADA

La identidad actual de BoxGhost queda reconciliada:

```text
BOXGHOST_PATH=D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT\Fabric\gm-ai-boxghost

BOXGHOST_HAS_OWN_GIT_METADATA=NO
BOXGHOST_IS_INDEPENDENT_GIT_REPOSITORY=NO
BOXGHOST_INHERITS_GIT_RESOLUTION_FROM=Fabric
BOXGHOST_TRACKING_RELATION_TO_FABRIC=UNTRACKED

REPOSITORY_IDENTITY_DISCREPANCY=RESOLVED
REPOSITORY_IDENTITY_AUDIT_STATUS=CLOSED
GIT_REMEDIATION_REQUIRED=NO
GIT_REMEDIATION_AUTHORIZED=NO
```

Esta condición no bloquea la clasificación autorizada.

La creación de archivos dentro de `gm-ai-boxghost` no significa que se incorporen al repositorio Git `Fabric`. No ejecutes ninguna acción que cambie esa relación.

# 3. FUENTE CANÓNICA DEL ALCANCE

Antes de acceder a los orígenes, recupera del contexto anterior de este mismo track la definición congelada y aprobada de:

```text
ROOT-01
ROOT-02
ROOT-03
ROOT-04
FROZEN_SOURCE_ENUMERATION
FROZEN_CLASSIFICATION_TAXONOMY
FROZEN_BATCH_RULES
FROZEN_SECRET_HANDLING_RULES
FROZEN_DESTINATION_RULES
```

Usa las rutas exactas previamente aprobadas. No deduzcas rutas por similitud, nombres de usuario, estructura probable o búsqueda general del disco.

No uses el bootstrap cronológico ni la reauditoría Git como sustitutos de la definición original de la Fase 1.

Si no puedes recuperar inequívocamente las cuatro rutas aprobadas:

```text
BLOCKER=FROZEN_ROOT_DEFINITION_NOT_RECOVERABLE
CLASSIFICATION_STATUS=NOT_EXECUTED
```

En ese caso, persiste únicamente `request.md` y `report.md`, informa el bloqueo y detente. No solicites nuevamente la aprobación del propietario.

# 4. ALCANCE DEL LOTE

La referencia histórica revisada para esta fase es:

```text
FROZEN_EXPECTED_SOURCE_FILES=354
BATCH_SIZE_MAXIMUM=50
CURRENT_BATCH=BATCH-001
```

Ejecuta únicamente el primer lote determinista de hasta 50 archivos pertenecientes a la enumeración congelada de 354 archivos.

No amplíes el universo porque aparezcan archivos nuevos.

Si el universo exacto de 354 archivos no puede reproducirse:

```text
BLOCKER=FROZEN_SOURCE_ENUMERATION_NOT_REPRODUCIBLE
CLASSIFICATION_STATUS=NOT_EXECUTED
```

No clasifiques una selección aproximada.

Ordena la enumeración congelada mediante la ruta relativa canónica ya aprobada y selecciona exclusivamente las primeras 50 entradas pendientes.

No ejecutes `BATCH-002` ni otro lote durante esta intervención.

# 5. OPERACIONES AUTORIZADAS

Sobre los archivos exactos de `BATCH-001`, puedes ejecutar únicamente:

```text
CONFIRM_SOURCE_PATH
READ_SOURCE_METADATA
READ_SOURCE_CONTENT_WHEN_REQUIRED_FOR_CLASSIFICATION
CALCULATE_SHA256
DETECT_DUPLICATES_BY_HASH
DETECT_SECRET_OR_AUTHENTICATION_INDICATORS
CLASSIFY_WITH_FROZEN_TAXONOMY
ASSIGN_CLASSIFICATION_CONFIDENCE
RECORD_SAFE_CLASSIFICATION_EVIDENCE
```

La lectura de contenido debe limitarse a lo necesario para decidir la clasificación.

No muestres ni persistas:

```text
SECRET_VALUES
TOKENS
PASSWORDS
COOKIES
SESSION_VALUES
PRIVATE_KEYS
AUTHORIZATION_HEADERS
CONNECTION_STRINGS_WITH_CREDENTIALS
PERSONAL_DATA_NOT_REQUIRED_FOR_CLASSIFICATION
```

Cuando detectes un indicador sensible, registra solamente:

```text
SENSITIVE_INDICATOR_DETECTED=YES
SENSITIVE_INDICATOR_TYPE=<categoría segura>
VALUE_REDACTED=YES
```

# 6. TAXONOMÍA

Usa exclusivamente la taxonomía congelada y aprobada de la Fase 1.

La taxonomía histórica incluye, como referencia de validación:

```text
PERSIST_TRACK_SPECIFIC
PERSIST_SHARED_CONTEXT
KEEP_UNCLASSIFIED
DUPLICATE_REFERENCE_ONLY
EXCLUDE_SECRET
EXCLUDE_AUTHENTICATION
EXCLUDE_REGENERABLE_CACHE
EXCLUDE_BUILD_OR_DEPENDENCY
EXCLUDE_TELEMETRY
EXCLUDE_IRRELEVANT
MANUAL_OWNER_REVIEW_REQUIRED
```

No agregues, elimines ni renombres categorías durante esta ejecución.

Si el alcance aprobado posterior contiene una taxonomía congelada más precisa, esa definición posterior prevalece.

Cuando una clasificación no alcance el umbral de confianza aprobado:

```text
CLASSIFICATION=MANUAL_OWNER_REVIEW_REQUIRED
```

No conviertas una inferencia débil en una clasificación definitiva.

# 7. PROTECCIÓN DE LOS ARCHIVOS FUENTE

Todos los archivos fuente originales permanecen protegidos.

Está prohibido:

```text
MODIFY_SOURCE_FILE
OVERWRITE_SOURCE_FILE
APPEND_TO_SOURCE_FILE
RENAME_SOURCE_FILE
MOVE_SOURCE_FILE
DELETE_SOURCE_FILE
CREATE_FILE_INSIDE_SOURCE_ROOT
CHANGE_SOURCE_TIMESTAMPS_INTENTIONALLY
CHANGE_SOURCE_PERMISSIONS
```

En esta intervención no copies archivos fuente originales.

La clasificación será de metadatos y contenido analítico únicamente. Una categoría `PERSIST_*` representa una recomendación de destino; no autoriza todavía copiar el archivo original.

Reporta:

```text
SOURCE_FILES_CREATED=0
SOURCE_FILES_MODIFIED=0
SOURCE_FILES_DELETED=0
SOURCE_FILES_MOVED=0
SOURCE_FILES_COPIED=0
```

# 8. LÍMITES DE ACCESO

Puedes acceder únicamente a:

```text
ROOT-01
ROOT-02
ROOT-03
ROOT-04
BOXGHOST_PATH
CURRENT_TRACK_PATH
CHATGPT_CODEX_INTERVENTIONS_PATH
```

donde:

```text
CURRENT_TRACK_PATH=D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT\Fabric\gm-ai-boxghost\tracks\GM-AI-LOCAL-CONTEXT-CLASSIFICATION-01

CHATGPT_CODEX_INTERVENTIONS_PATH=D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT\Fabric\gm-ai-boxghost\tracks\GM-AI-LOCAL-CONTEXT-CLASSIFICATION-01\interventions\chatgpt-codex
```

No inspecciones:

```text
OTHER_TRACKS
OTHER_REPOSITORIES
MODULES_GM_AI_WORKSPACE
QNAP
REMOTE_STORAGE
GITHUB
UNRELATED_USER_DIRECTORIES
UNAPPROVED_DISK_ROOTS
```

No sigas enlaces simbólicos, junctions o reparse points que salgan de las rutas autorizadas.

# 9. PROHIBICIONES GIT

No ejecutes comandos Git durante esta intervención.

En particular, está prohibido:

```text
GIT_INIT
GIT_STATUS
GIT_REV_PARSE
GIT_STASH
GIT_ADD
GIT_COMMIT
GIT_PUSH
GIT_FETCH
GIT_PULL
GIT_CLONE
GIT_CHECKOUT
GIT_SWITCH
GIT_RESTORE
GIT_RESET
GIT_CLEAN
MODIFY_GIT_CONFIG
MODIFY_GIT_INDEX
MODIFY_GIT_REFERENCES
MODIFY_BRANCH
MODIFY_STASH
CREATE_DOT_GIT
```

No declares el estado actual del worktree porque no debes comprobarlo mediante Git.

Reporta:

```text
GIT_COMMANDS_EXECUTED=0
GIT_MUTATION_OCCURRED=NO
FILES_STAGED_BY_THIS_EXECUTION=0
COMMITS_CREATED_BY_THIS_EXECUTION=0
PUSHES_EXECUTED_BY_THIS_EXECUTION=0
GITHUB_AUTHENTICATION_USED=NO
BOXGHOST_INCORPORATED_INTO_FABRIC=NO
```

# 10. IDENTIFICADOR CRONOLÓGICO

Persiste esta ejecución en una nueva intervención:

```text
interventions\chatgpt-codex\CHATGPT-CODEX-20260802-NNN
```

Calcula `NNN` examinando únicamente los nombres de las carpetas directas de:

```text
interventions\chatgpt-codex
```

que coincidan exactamente con:

```text
CHATGPT-CODEX-20260802-[0-9][0-9][0-9]
```

Reglas:

1. Toma la secuencia válida más alta y suma uno.
2. No rellenes huecos.
3. No reutilices identificadores.
4. No renombres intervenciones existentes.
5. No modifiques entradas mal formadas.
6. Reporta entradas mal formadas solo como cantidad agregada.
7. Comprueba la ausencia de colisión inmediatamente antes de crear la carpeta.
8. No asumas `002`; calcúlalo físicamente.

Si existe colisión:

```text
BLOCKER=INTERVENTION_IDENTIFIER_COLLISION
PERSISTENCE_STATUS=NOT_EXECUTED
```

No elijas otra secuencia automáticamente.

# 11. PERSISTENCIA AUTORIZADA

Dentro de la nueva intervención crea exclusivamente:

```text
request.md
report.md
```

Contenido:

* `request.md`: copia íntegra y fiel de esta instrucción.
* `report.md`: informe completo de la clasificación de `BATCH-001`.
* Incluye en `report.md` el registro individual de hasta 50 archivos.
* No crees copias de los archivos fuente.
* No crees índices, manifests, checkpoints, logs o archivos adicionales.
* No modifiques intervenciones anteriores.
* No modifiques archivos de otros agentes.
* No actualices todavía estados acumulativos del track.

Por cada archivo registra de forma segura:

```text
BATCH_POSITION
SOURCE_ROOT_ID
SAFE_RELATIVE_PATH
FILE_TYPE
SIZE_BYTES
SHA256
DUPLICATE_STATUS
SENSITIVE_INDICATOR_DETECTED
SENSITIVE_INDICATOR_TYPE
VALUE_REDACTED
CLASSIFICATION
CLASSIFICATION_CONFIDENCE
SAFE_RATIONALE
SOURCE_MUTATION=NO
SOURCE_COPY=NO
```

No imprimas rutas absolutas privadas en el registro individual. Usa el identificador `ROOT-01..ROOT-04` y una ruta relativa segura.

# 12. ORDEN DE EJECUCIÓN

Ejecuta exactamente:

1. Confirma la autorización y el levantamiento de la suspensión.
2. Recupera las definiciones congeladas de `ROOT-01..ROOT-04`.
3. Confirma la existencia y tipo de las cuatro rutas sin enumerar contenido ajeno.
4. Recupera la enumeración congelada de 354 archivos.
5. Verifica que el universo no se haya ampliado.
6. Selecciona determinísticamente `BATCH-001`, con máximo 50 archivos.
7. Ejecuta el análisis de indicadores sensibles sin exponer valores.
8. Calcula SHA-256.
9. Detecta duplicados por hash dentro del universo autorizado.
10. Clasifica cada archivo con la taxonomía congelada.
11. Formula el informe final completo.
12. Calcula el identificador cronológico de ChatGPT Codex.
13. Comprueba inmediatamente la ausencia de colisión.
14. Crea una sola carpeta de intervención.
15. Crea `request.md`.
16. Crea `report.md`.
17. Verifica mediante lectura ambos archivos.
18. Devuelve exactamente el contenido persistido en `report.md`.
19. Detente sin iniciar `BATCH-002`.

La persistencia debe realizarse al final.

# 13. SALIDA OBLIGATORIA

El informe debe comenzar con:

```text
TRACK=GM-AI-LOCAL-CONTEXT-CLASSIFICATION-01
STEP=PHASE_1_ROOT_01_TO_ROOT_04_CLASSIFICATION_BATCH_001
AGENT=CHATGPT_CODEX
AGENT_DIRECTORY=chatgpt-codex
MODE=BOUNDED_SOURCE_CLASSIFICATION_SOURCE_READ_ONLY_NO_GIT
TIMEZONE=America/Guayaquil

OWNER_APPROVAL_ID=OA-GM-AI-LOCAL-CONTEXT-CLASSIFICATION-01-PHASE-1
OWNER_APPROVAL_STATUS=GRANTED
TEMPORARY_CLASSIFICATION_SUSPENSION=LIFTED
SUSPENSION_LIFT_REFERENCE=OWNER_EXPLICIT_DIRECTIVE_20260802
PHASE_1_STATUS=RESUMED

BOXGHOST_IS_INDEPENDENT_GIT_REPOSITORY=NO
BOXGHOST_INHERITS_GIT_RESOLUTION_FROM=Fabric
BOXGHOST_TRACKING_RELATION_TO_FABRIC=UNTRACKED
REPOSITORY_IDENTITY_AUDIT_STATUS=CLOSED

INTERVENTION_LOCAL_DATE=20260802
INTERVENTION_SEQUENCE=<NNN|NOT_ALLOCATED>
INTERVENTION_ID=<CHATGPT-CODEX-20260802-NNN|NOT_ALLOCATED>
INTERVENTION_PATH=<ruta relativa segura|NOT_CREATED>

VALID_SAME_DAY_CHATGPT_CODEX_INTERVENTIONS_COUNT=<cantidad>
HIGHEST_EXISTING_SEQUENCE=<NNN|NONE>
NEXT_SEQUENCE=<NNN|NOT_ALLOCATED>
MALFORMED_ENTRIES_COUNT=<cantidad>
IDENTIFIER_COLLISION=<YES|NO|NOT_CHECKED>

ROOT_01_DEFINITION_RECOVERED=<YES|NO>
ROOT_02_DEFINITION_RECOVERED=<YES|NO>
ROOT_03_DEFINITION_RECOVERED=<YES|NO>
ROOT_04_DEFINITION_RECOVERED=<YES|NO>

ROOT_01_EXISTS=<YES|NO|NOT_CHECKED>
ROOT_02_EXISTS=<YES|NO|NOT_CHECKED>
ROOT_03_EXISTS=<YES|NO|NOT_CHECKED>
ROOT_04_EXISTS=<YES|NO|NOT_CHECKED>

FROZEN_EXPECTED_SOURCE_FILES=354
FROZEN_ENUMERATION_REPRODUCED=<YES|NO>
CURRENT_BATCH=BATCH-001
BATCH_SIZE_LIMIT=50
BATCH_FILES_SELECTED=<cantidad>
BATCH_FILES_READ=<cantidad>
BATCH_FILES_CLASSIFIED=<cantidad>
BATCH_FILES_EXCLUDED=<cantidad>
BATCH_DUPLICATES_FOUND=<cantidad>
BATCH_SECRETS_BLOCKED=<cantidad>
BATCH_AUTHENTICATION_FILES_BLOCKED=<cantidad>
BATCH_MANUAL_REVIEW_PENDING=<cantidad>
BATCH_PERSIST_RECOMMENDATIONS=<cantidad>

SOURCE_FILES_CREATED=0
SOURCE_FILES_MODIFIED=0
SOURCE_FILES_DELETED=0
SOURCE_FILES_MOVED=0
SOURCE_FILES_COPIED=0

PERSISTENCE_DIRECTORIES_CREATED=<0|1>
PERSISTENCE_FILES_CREATED=<0|2>
PERSISTENCE_FILES_MODIFIED=0
PREVIOUS_INTERVENTIONS_MODIFIED=0
PREVIOUS_INTERVENTIONS_RENAMED=0

REQUEST_MD_CREATED=<YES|NO>
REPORT_MD_CREATED=<YES|NO>
REQUEST_MD_VERIFIED=<YES|NO>
REPORT_MD_VERIFIED=<YES|NO>

GIT_COMMANDS_EXECUTED=0
GIT_MUTATION_OCCURRED=NO
FILES_STAGED_BY_THIS_EXECUTION=0
COMMITS_CREATED_BY_THIS_EXECUTION=0
PUSHES_EXECUTED_BY_THIS_EXECUTION=0
GITHUB_AUTHENTICATION_USED=NO
BOXGHOST_INCORPORATED_INTO_FABRIC=NO

CLASSIFICATION_STATUS=<COMPLETED|BLOCKED|NOT_EXECUTED>
PERSISTENCE_STATUS=<COMPLETED|BLOCKED|NOT_EXECUTED>
BLOCKERS=<lista|NONE>
VERDICT=<BATCH_001_READY_FOR_CLAUDE_CODE_AUDIT|PHASE_1_EXECUTION_BLOCKED>
NEXT_STEP=CHATGPT_WORK_VALIDATES_CODEX_REPORT_AND_PREPARES_CLAUDE_CODE_PHASE_1_AUDIT
```

Incluye después:

## A. Autorización aplicada

Confirma que:

```text
OWNER_APPROVAL_WAS_NOT_REQUESTED_AGAIN
TEMPORARY_SUSPENSION_WAS_LIFTED
PHASE_1_SCOPE_WAS_NOT_EXPANDED
```

## B. Preflight

Informa únicamente:

* Recuperación de las cuatro definiciones congeladas.
* Existencia y tipo de las cuatro raíces.
* Reproducción o bloqueo de la enumeración de 354 archivos.
* Identificación del lote de hasta 50 archivos.
* Ausencia de colisión cronológica.

## C. Resultado agregado del lote

Presenta los conteos por categoría sin revelar información sensible.

## D. Clasificación individual segura

Incluye el registro de cada archivo de `BATCH-001` con los campos definidos, valores sensibles redactados y rutas relativas seguras.

## E. Persistencia

```text
NEW_CHATGPT_CODEX_INTERVENTION_CREATED=<YES|NO>
INTERVENTION_ID=<CHATGPT-CODEX-20260802-NNN|NOT_ALLOCATED>
REQUEST_MD_CREATED=<YES|NO>
REPORT_MD_CREATED=<YES|NO>
REQUEST_MD_VERIFIED=<YES|NO>
REPORT_MD_VERIFIED=<YES|NO>
PERSISTENCE_STATUS=<COMPLETED|BLOCKED|NOT_EXECUTED>
```

## F. Confirmación de límites

Si el lote y la persistencia terminan correctamente, declara exactamente:

```text
ONLY_BATCH_001_OF_THE_FROZEN_PHASE_1_SCOPE_WAS_CLASSIFIED
NO_SCOPE_BEYOND_ROOT_01_TO_ROOT_04_WAS_ACCESSED
NO_SOURCE_FILE_WAS_CREATED_MODIFIED_RENAMED_MOVED_COPIED_OR_DELETED
NO_SECRET_AUTHENTICATION_VALUE_OR_PRIVATE_CREDENTIAL_WAS_PERSISTED
NO_SOURCE_FILE_WAS_COPIED_INTO_BOXGHOST
NO_BATCH_AFTER_BATCH_001_WAS_STARTED
NO_EXISTING_INTERVENTION_WAS_MODIFIED_RENAMED_OR_OVERWRITTEN
NO_EXISTING_IDENTIFIER_WAS_REUSED
ONLY_ONE_NEW_CHATGPT_CODEX_INTERVENTION_WAS_CREATED
NO_INTERVENTION_WAS_CREATED_FOR_ANOTHER_AGENT
NO_GIT_COMMAND_WAS_EXECUTED
NO_GIT_REPOSITORY_WAS_INITIALIZED_OR_REPAIRED
NO_BOXGHOST_CONTENT_WAS_INCORPORATED_INTO_FABRIC
NO_FILE_WAS_STAGED_COMMITTED_OR_PUSHED
NO_GITHUB_AUTHENTICATION_WAS_USED
OWNER_APPROVAL_SCOPE_WAS_NOT_EXPANDED
```

# 14. CIERRE

No inicies `BATCH-002`.

No copies todavía archivos clasificados como `PERSIST_*`.

No modifiques el repositorio `Fabric`.

No incorpores `gm-ai-boxghost` a Git.

No autorices staging, commit ni push.

No solicites nuevamente la aprobación concedida.

Devuelve el contenido completo de `report.md` a ChatGPT Work.

Siguiente paso único:

```text
NEXT_STEP=CHATGPT_WORK_VALIDATES_CODEX_REPORT_AND_PREPARES_CLAUDE_CODE_PHASE_1_AUDIT
```
