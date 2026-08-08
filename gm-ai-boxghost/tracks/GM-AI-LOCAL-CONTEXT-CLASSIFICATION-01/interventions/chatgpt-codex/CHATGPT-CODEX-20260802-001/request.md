PEGAR EN: CHATGPT CODEX — BOOTSTRAP EXCLUSIVO DE LA ESTRUCTURA CRONOLÓGICA DEL TRACK

Track: GM-AI-LOCAL-CONTEXT-CLASSIFICATION-01
Step: CHRONOLOGICAL TRACK PERSISTENCE BOOTSTRAP
Mode: BOUNDED FILESYSTEM BOOTSTRAP / NO SOURCE CLASSIFICATION / NO GIT
Agent: ChatGPT Codex
Status: OWNER_APPROVED_FOR_BOOTSTRAP_ONLY

# 1. AUTORIZACIÓN DEL PROPIETARIO

Eduardo aprobó expresamente:

```text
APRUEBO EXCLUSIVAMENTE EL BOOTSTRAP DE LA ESTRUCTURA CRONOLÓGICA DEL TRACK
GM-AI-LOCAL-CONTEXT-CLASSIFICATION-01.

No autorizo todavía la clasificación de ROOT-01..ROOT-04.
No autorizo git init, staging, commit ni push.
No autorizo incorporar gm-ai-boxghost al repositorio Fabric.
```

Registra esta autorización como:

```text
OWNER_APPROVAL_REFERENCE=OWNER_EXPLICIT_APPROVAL_20260802
OWNER_APPROVAL_SCOPE=CHRONOLOGICAL_TRACK_PERSISTENCE_BOOTSTRAP_ONLY
OWNER_APPROVAL_STATUS=GRANTED
OWNER_APPROVAL_EXPANSION=PROHIBITED
```

Esta aprobación no autoriza:

* Reanudar la Fase 1.
* Clasificar, leer, copiar, mover, renombrar o modificar `ROOT-01..ROOT-04`.
* Auditar nuevamente la identidad Git de BoxGhost.
* Inicializar o reparar repositorios.
* Incorporar BoxGhost al repositorio padre `Fabric`.
* Ejecutar staging, commit o push.
* Modificar intervenciones anteriores.
* Crear documentos de gobernanza, índices, manifiestos o checkpoints adicionales.
* Ejecutar trabajo correspondiente a otro agente.

# 2. OBJETIVO ÚNICO

Crear exclusivamente la estructura cronológica de persistencia del track:

```text
GM-AI-LOCAL-CONTEXT-CLASSIFICATION-01
```

y registrar esta ejecución como una nueva intervención de ChatGPT Codex.

La estructura canónica resultante debe ser:

```text
gm-ai-boxghost\
└── tracks\
    └── GM-AI-LOCAL-CONTEXT-CLASSIFICATION-01\
        └── interventions\
            ├── chatgpt-chat\
            ├── chatgpt-work\
            ├── claude-chat\
            ├── claude-code\
            └── chatgpt-codex\
                └── CHATGPT-CODEX-20260802-NNN\
                    ├── request.md
                    └── report.md
```

No crees intervenciones para los otros cuatro agentes.

Los directorios:

```text
chatgpt-chat
chatgpt-work
claude-chat
claude-code
```

deben quedar vacíos si no contenían intervenciones previamente.

# 3. RUTA CANÓNICA

Ruta base:

```text
D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT\Fabric\gm-ai-boxghost
```

Ruta del track:

```text
D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT\Fabric\gm-ai-boxghost\tracks\GM-AI-LOCAL-CONTEXT-CLASSIFICATION-01
```

Ruta de intervenciones:

```text
D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT\Fabric\gm-ai-boxghost\tracks\GM-AI-LOCAL-CONTEXT-CLASSIFICATION-01\interventions
```

Condición previa:

```text
BOXGHOST_BASE_PATH_MUST_ALREADY_EXIST=YES
```

Si la ruta base exacta de `gm-ai-boxghost` no existe:

```text
BLOCKER=BOXGHOST_CANONICAL_BASE_PATH_NOT_FOUND
BOOTSTRAP_STATUS=NOT_EXECUTED
```

No selecciones otra ubicación.

No crees otra carpeta `gm-ai-boxghost`.

No busques copias alternativas en otros discos, perfiles, repositorios, unidades externas, QNAP, servicios remotos o GitHub.

# 4. CONVENCIÓN CANÓNICA DE AGENTES

Aplica exclusivamente esta correspondencia:

| Agente o rol  | Directorio      | Identificador                |
| ------------- | --------------- | ---------------------------- |
| ChatGPT Chat  | `chatgpt-chat`  | `CHATGPT-CHAT-YYYYMMDD-NNN`  |
| ChatGPT Work  | `chatgpt-work`  | `CHATGPT-WORK-YYYYMMDD-NNN`  |
| Claude Chat   | `claude-chat`   | `CLAUDE-CHAT-YYYYMMDD-NNN`   |
| Claude Code   | `claude-code`   | `CLAUDE-CODE-YYYYMMDD-NNN`   |
| ChatGPT Codex | `chatgpt-codex` | `CHATGPT-CODEX-YYYYMMDD-NNN` |

Reglas:

```text
CHATGPT_CHAT_AND_CHATGPT_WORK_ARE_SEPARATE_ROLES=YES
DIRECTORY_NAMES_USE_LOWERCASE=YES
INTERVENTION_IDENTIFIERS_USE_UPPERCASE=YES
SEQUENCE_SCOPE=PER_AGENT_PER_LOCAL_DATE
TIMEZONE=America/Guayaquil
LEGACY_INTERVENTIONS_REMAIN_IMMUTABLE=YES
```

Esta ejecución corresponde únicamente a:

```text
AGENT=CHATGPT_CODEX
AGENT_DISPLAY_NAME=ChatGPT Codex
AGENT_DIRECTORY=chatgpt-codex
AGENT_ID=CHATGPT-CODEX
INTERVENTION_ID_FORMAT=CHATGPT-CODEX-YYYYMMDD-NNN
```

# 5. PREFLIGHT OBLIGATORIO

Antes de escribir:

1. Confirma que la ruta base exacta de `gm-ai-boxghost` existe y es un directorio.
2. Comprueba cada ruta requerida sin recorrer su contenido fuente.
3. Determina si alguna ruta estructural requerida existe como archivo en vez de directorio.
4. Comprueba que no se accederá a `ROOT-01..ROOT-04`.
5. Comprueba que no se ejecutará ningún comando Git.
6. Calcula el identificador de esta intervención usando solamente entradas directas de `interventions\chatgpt-codex`, si ese directorio ya existe.

Si una ruta estructural requerida existe como archivo:

```text
BLOCKER=REQUIRED_DIRECTORY_PATH_OCCUPIED_BY_FILE
BOOTSTRAP_STATUS=NOT_EXECUTED
```

No renombres, muevas, elimines ni sobrescribas ese archivo.

La comprobación de preflight debe limitarse a nombres y tipos de las rutas estructurales necesarias. No inspecciones contenido de documentos privados.

# 6. CÁLCULO DE LA INTERVENCIÓN

Para esta ejecución:

```text
TIMEZONE=America/Guayaquil
INTERVENTION_LOCAL_DATE=20260802
EXPECTED_PREFIX=CHATGPT-CODEX-20260802-
SEQUENCE_SCOPE=PER_AGENT_PER_LOCAL_DATE
```

Si `interventions\chatgpt-codex` todavía no existe, utiliza:

```text
INTERVENTION_SEQUENCE=001
INTERVENTION_ID=CHATGPT-CODEX-20260802-001
```

Si ya existe, examina únicamente sus carpetas directas que coincidan exactamente con:

```text
CHATGPT-CODEX-20260802-[0-9][0-9][0-9]
```

Reglas:

1. Si no hay coincidencias válidas, utiliza `001`.
2. Si hay coincidencias, toma el número mayor y suma uno.
3. No rellenes huecos.
4. No reutilices identificadores.
5. No uses secuencias de otros agentes.
6. No renombres intervenciones anteriores.
7. No modifiques entradas mal formadas.
8. Conserva siempre tres dígitos.
9. Reporta entradas mal formadas únicamente mediante una cantidad agregada.
10. No muestres sus nombres.

Antes de crear la intervención, comprueba nuevamente que el identificador calculado no exista.

Si existe una colisión:

```text
BLOCKER=INTERVENTION_IDENTIFIER_COLLISION
INTERVENTION_PERSISTENCE_STATUS=NOT_EXECUTED
```

No sobrescribas ni recalcules automáticamente otro número.

# 7. ESCRITURA AUTORIZADA

La única escritura autorizada es:

```text
CREATE_MISSING_TRACK_CHRONOLOGICAL_STRUCTURE_DIRECTORIES
CREATE_ONE_NEW_CHATGPT_CODEX_INTERVENTION_DIRECTORY
CREATE_REQUEST_MD
CREATE_REPORT_MD
```

Puedes crear únicamente los directorios faltantes dentro de esta cadena:

```text
tracks\
tracks\GM-AI-LOCAL-CONTEXT-CLASSIFICATION-01\
tracks\GM-AI-LOCAL-CONTEXT-CLASSIFICATION-01\interventions\
tracks\GM-AI-LOCAL-CONTEXT-CLASSIFICATION-01\interventions\chatgpt-chat\
tracks\GM-AI-LOCAL-CONTEXT-CLASSIFICATION-01\interventions\chatgpt-work\
tracks\GM-AI-LOCAL-CONTEXT-CLASSIFICATION-01\interventions\claude-chat\
tracks\GM-AI-LOCAL-CONTEXT-CLASSIFICATION-01\interventions\claude-code\
tracks\GM-AI-LOCAL-CONTEXT-CLASSIFICATION-01\interventions\chatgpt-codex\
tracks\GM-AI-LOCAL-CONTEXT-CLASSIFICATION-01\interventions\chatgpt-codex\CHATGPT-CODEX-20260802-NNN\
```

No recrees ni modifiques directorios que ya existan.

Dentro de la nueva intervención crea exclusivamente:

```text
request.md
report.md
```

Contenido:

* `request.md`: copia íntegra y fiel de esta instrucción.
* `report.md`: informe final completo de esta ejecución.
* No crees `README.md`.
* No crees `TRACK.md`.
* No crees índices, manifests, estados, checkpoints, logs ni archivos de evidencia adicionales.
* No agregues archivos en los directorios de otros agentes.
* No modifiques archivos existentes.

# 8. ACCIONES PROHIBIDAS

```text
ACCESS_ROOT_01_TO_ROOT_04
SCAN_ROOT_01_TO_ROOT_04
READ_SOURCE_CONTEXT
CLASSIFY_SOURCE_CONTEXT
COPY_SOURCE_CONTEXT
MOVE_SOURCE_CONTEXT
RENAME_SOURCE_CONTEXT
DELETE_SOURCE_CONTEXT
RESUME_PHASE_1

CREATE_INTERVENTION_FOR_ANOTHER_AGENT
MODIFY_EXISTING_INTERVENTION
APPEND_TO_EXISTING_REPORT
OVERWRITE_EXISTING_FILE
RENAME_EXISTING_INTERVENTION
REUSE_EXISTING_IDENTIFIER
CREATE_ADDITIONAL_PERSISTENCE_FILE

RUN_ANY_GIT_COMMAND
CREATE_DOT_GIT
GIT_INIT
GIT_CLONE
GIT_FETCH
GIT_PULL
GIT_CHECKOUT
GIT_SWITCH
GIT_RESTORE
GIT_RESET
GIT_CLEAN
GIT_ADD
GIT_COMMIT
GIT_PUSH
MODIFY_GIT_CONFIG
MODIFY_GIT_REFERENCE
MODIFY_BRANCH
MODIFY_STASH
DELETE_OR_MOVE_GIT_METADATA

INCORPORATE_BOXGHOST_INTO_FABRIC
MODIFY_FABRIC_REPOSITORY
CLEAN_FABRIC_WORKTREE
USE_GITHUB_AUTHENTICATION
ACCESS_REMOTE_STORAGE
REQUEST_OWNER_APPROVAL_AGAIN
```

No ejecutes siquiera consultas Git read-only. La identidad del repositorio ya fue reconciliada y no forma parte de este paso.

No declares que el worktree está limpio o sucio porque no debes comprobarlo mediante Git.

# 9. ORDEN DE EJECUCIÓN

Ejecuta exactamente:

1. Confirma la ruta base exacta de BoxGhost.
2. Ejecuta el preflight únicamente sobre las rutas estructurales.
3. Determina qué directorios estructurales ya existen.
4. Calcula `CHATGPT-CODEX-20260802-NNN`.
5. Comprueba que no exista colisión.
6. Crea únicamente los directorios estructurales faltantes.
7. Crea una sola carpeta de intervención de ChatGPT Codex.
8. Crea `request.md`.
9. Formula y crea `report.md`.
10. Verifica mediante lectura que los dos archivos existen.
11. Verifica mediante nombres y tipos que los cinco directorios canónicos de agentes existen.
12. Devuelve a ChatGPT Work el mismo contenido persistido en `report.md`.

No inspecciones otros tracks.

No enumeres contenido ajeno a la estructura creada.

# 10. MÉTRICAS SEPARADAS

Reporta:

```text
SOURCE_CONTEXT_DIRECTORIES_ACCESSED=0
SOURCE_CONTEXT_FILES_READ=0
SOURCE_CONTEXT_FILES_CREATED=0
SOURCE_CONTEXT_FILES_MODIFIED=0
SOURCE_CONTEXT_FILES_DELETED=0
SOURCE_CONTEXT_FILES_MOVED=0
SOURCE_CONTEXT_FILES_COPIED=0

BOOTSTRAP_STRUCTURE_DIRECTORIES_ALREADY_EXISTED=<cantidad>
BOOTSTRAP_STRUCTURE_DIRECTORIES_CREATED=<cantidad>
CHATGPT_CODEX_INTERVENTION_DIRECTORIES_CREATED=<0|1>
PERSISTENCE_FILES_CREATED=<0|2>
PERSISTENCE_FILES_MODIFIED=0
EXISTING_INTERVENTIONS_MODIFIED=0
EXISTING_INTERVENTIONS_RENAMED=0

GIT_COMMANDS_EXECUTED=0
GIT_MUTATION_OCCURRED=NO
FILES_STAGED_BY_THIS_EXECUTION=0
COMMITS_CREATED_BY_THIS_EXECUTION=0
PUSHES_EXECUTED_BY_THIS_EXECUTION=0
GITHUB_AUTHENTICATION_USED=NO
```

No confundas los directorios estructurales con la carpeta de intervención.

# 11. SALIDA OBLIGATORIA

El `report.md` y la respuesta devuelta deben comenzar con:

```text
TRACK=GM-AI-LOCAL-CONTEXT-CLASSIFICATION-01
STEP=CHRONOLOGICAL_TRACK_PERSISTENCE_BOOTSTRAP
AGENT=CHATGPT_CODEX
AGENT_DIRECTORY=chatgpt-codex
MODE=BOUNDED_FILESYSTEM_BOOTSTRAP_NO_GIT
TIMEZONE=America/Guayaquil

OWNER_APPROVAL_REFERENCE=OWNER_EXPLICIT_APPROVAL_20260802
OWNER_APPROVAL_SCOPE=CHRONOLOGICAL_TRACK_PERSISTENCE_BOOTSTRAP_ONLY
OWNER_APPROVAL_STATUS=GRANTED

BOXGHOST_BASE_PATH_EXISTS=<YES|NO>
TRACK_DIRECTORY_EXISTS_AFTER_EXECUTION=<YES|NO>
INTERVENTIONS_DIRECTORY_EXISTS_AFTER_EXECUTION=<YES|NO>

CHATGPT_CHAT_DIRECTORY_EXISTS=<YES|NO>
CHATGPT_WORK_DIRECTORY_EXISTS=<YES|NO>
CLAUDE_CHAT_DIRECTORY_EXISTS=<YES|NO>
CLAUDE_CODE_DIRECTORY_EXISTS=<YES|NO>
CHATGPT_CODEX_DIRECTORY_EXISTS=<YES|NO>

INTERVENTION_LOCAL_DATE=20260802
INTERVENTION_SEQUENCE=<NNN|NOT_ALLOCATED>
INTERVENTION_ID=<CHATGPT-CODEX-20260802-NNN|NOT_ALLOCATED>
INTERVENTION_PATH=<ruta relativa segura|NOT_CREATED>
SEQUENCE_SCOPE=PER_AGENT_PER_LOCAL_DATE

VALID_SAME_DAY_CHATGPT_CODEX_INTERVENTIONS_COUNT=<cantidad>
HIGHEST_EXISTING_SEQUENCE=<NNN|NONE>
NEXT_SEQUENCE=<NNN|NOT_ALLOCATED>
MALFORMED_ENTRIES_COUNT=<cantidad>
IDENTIFIER_COLLISION=<YES|NO|NOT_CHECKED>

SOURCE_CONTEXT_DIRECTORIES_ACCESSED=0
SOURCE_CONTEXT_FILES_READ=0
SOURCE_CONTEXT_FILES_CREATED=0
SOURCE_CONTEXT_FILES_MODIFIED=0
SOURCE_CONTEXT_FILES_DELETED=0
SOURCE_CONTEXT_FILES_MOVED=0
SOURCE_CONTEXT_FILES_COPIED=0

BOOTSTRAP_STRUCTURE_DIRECTORIES_ALREADY_EXISTED=<cantidad>
BOOTSTRAP_STRUCTURE_DIRECTORIES_CREATED=<cantidad>
CHATGPT_CODEX_INTERVENTION_DIRECTORIES_CREATED=<0|1>
PERSISTENCE_FILES_CREATED=<0|2>
PERSISTENCE_FILES_MODIFIED=0
EXISTING_INTERVENTIONS_MODIFIED=0
EXISTING_INTERVENTIONS_RENAMED=0

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

BOOTSTRAP_STATUS=<COMPLETED|BLOCKED|NOT_EXECUTED>
BLOCKERS=<lista|NONE>
VERDICT=<CHRONOLOGICAL_STRUCTURE_READY|BOOTSTRAP_BLOCKED>
NEXT_STEP=CHATGPT_WORK_VALIDATES_BOOTSTRAP_AND_PREPARES_CLAUDE_CODE_REAUDIT
```

Después incluye:

## A. Autorización aplicada

Confirma que se aplicó exclusivamente la autorización del bootstrap y que no se amplió a la Fase 1.

## B. Preflight

Describe únicamente:

* Existencia de la ruta base.
* Ausencia o presencia de colisiones estructurales.
* Cálculo seguro del identificador.
* Cantidades agregadas de entradas válidas y mal formadas.

No muestres nombres de otras intervenciones.

## C. Estructura creada

Presenta el árbol cronológico resultante sin enumerar contenido privado:

```text
interventions\
├── chatgpt-chat\
├── chatgpt-work\
├── claude-chat\
├── claude-code\
└── chatgpt-codex\
    └── CHATGPT-CODEX-20260802-NNN\
        ├── request.md
        └── report.md
```

## D. Persistencia de esta intervención

```text
NEW_CHATGPT_CODEX_INTERVENTION_CREATED=<YES|NO>
INTERVENTION_ID=<CHATGPT-CODEX-20260802-NNN|NOT_ALLOCATED>
REQUEST_MD_CREATED=<YES|NO>
REPORT_MD_CREATED=<YES|NO>
REQUEST_MD_VERIFIED=<YES|NO>
REPORT_MD_VERIFIED=<YES|NO>
PERSISTENCE_STATUS=<COMPLETED|BLOCKED|NOT_EXECUTED>
```

## E. Confirmación de límites

Si el bootstrap finaliza correctamente, declara exactamente:

```text
ONLY_THE_APPROVED_CHRONOLOGICAL_TRACK_STRUCTURE_WAS_BOOTSTRAPPED
ONLY_ONE_CHATGPT_CODEX_INTERVENTION_WAS_CREATED
NO_INTERVENTION_WAS_CREATED_FOR_ANOTHER_AGENT
NO_EXISTING_INTERVENTION_WAS_MODIFIED_RENAMED_OR_OVERWRITTEN
NO_EXISTING_IDENTIFIER_WAS_REUSED
NO_ROOT_01_TO_ROOT_04_DIRECTORY_WAS_ACCESSED_OR_SCANNED
NO_SOURCE_CONTEXT_FILE_WAS_READ_CLASSIFIED_CREATED_MODIFIED_MOVED_COPIED_OR_DELETED
NO_PHASE_1_CLASSIFICATION_ACTION_WAS_EXECUTED
NO_GIT_COMMAND_WAS_EXECUTED
NO_GIT_REPOSITORY_WAS_INITIALIZED_OR_REPAIRED
NO_BOXGHOST_CONTENT_WAS_ADDED_TO_FABRIC
NO_FILE_WAS_STAGED_COMMITTED_OR_PUSHED
NO_GITHUB_AUTHENTICATION_WAS_USED
OWNER_APPROVAL_SCOPE_WAS_NOT_EXPANDED
```

Si el bootstrap queda bloqueado, no declares que se crearon elementos inexistentes. Informa exactamente el estado parcial comprobado.

# 12. CIERRE

No autorices todavía la clasificación de `ROOT-01..ROOT-04`.

No reanudes la Fase 1.

No autorices todavía una implementación de clasificación por ChatGPT Codex.

No ejecutes la repetición de la auditoría de Claude Code.

No solicites nuevamente la aprobación ya concedida para el bootstrap.

Devuelve el informe a ChatGPT Work.

Siguiente paso único:

```text
NEXT_STEP=CHATGPT_WORK_VALIDATES_BOOTSTRAP_AND_PREPARES_CLAUDE_CODE_REAUDIT
```
