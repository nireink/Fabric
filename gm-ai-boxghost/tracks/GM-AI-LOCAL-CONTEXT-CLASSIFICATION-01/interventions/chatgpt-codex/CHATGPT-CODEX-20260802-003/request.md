PEGAR EN: CHATGPT CODEX — CONSTRUCCIÓN DE LA NUEVA LÍNEA BASE DE LA FASE 1

Track: GM-AI-LOCAL-CONTEXT-CLASSIFICATION-01
Step: PHASE 1 / CONTRACT REBASELINE IMPLEMENTATION
Mode: APPROVED BASELINE CONSTRUCTION / METADATA-ONLY SOURCE ENUMERATION / NO CLASSIFICATION / NO GIT
Agent: ChatGPT Codex
Status: OWNER_APPROVED_FOR_EXECUTION

# 1. OBJETIVO

Construye la nueva línea base contractual de la Fase 1.

Esta intervención reemplaza únicamente los dos contratos históricos que Claude Code confirmó como no recuperables:

```text
FROZEN_SOURCE_ENUMERATION_NOT_REPRODUCIBLE
FROZEN_CLASSIFICATION_TAXONOMY_NOT_RECOVERABLE
```

No presentes la nueva enumeración como recuperación del universo histórico.

```text
PROCESS_TYPE=PHASE_1_CONTRACT_REBASELINE
HISTORICAL_CONTRACT_RECOVERY=NO
HISTORICAL_EXPECTED_SOURCE_FILES=354
HISTORICAL_354_STATUS=REFERENCE_ONLY
```

El conteo actual debe obtenerse físicamente. No lo ajustes para que coincida con `354`.

# 2. EVIDENCIA PREVIA ACEPTADA

```text
CODEX_BLOCKING_INTERVENTION=CHATGPT-CODEX-20260802-002
CLAUDE_CODE_AUDIT=CLAUDE-CODE-20260802-002
CLAUDE_CODE_VERDICT=CODEX_BLOCK_CONFIRMED

OLD_BATCH_001_EXECUTED=NO
OLD_SOURCE_FILES_CLASSIFIED=0
REBASELINE_REQUIRED=YES
```

La revisión crítica de Claude Chat fue consolidada por ChatGPT Work con correcciones obligatorias:

```text
CLASSIFICATION_CATEGORIES=12
EXCLUDE_PERSONAL_DATA=REQUIRED
MINIMUM_FINAL_CLASSIFICATION_CONFIDENCE=0.90
CSV_HASH_FREEZES_MEMBERSHIP_AND_ORDER=YES
CSV_HASH_FREEZES_SOURCE_CONTENT=NO
SOURCE_CONTENT_HASHING_DEFERRED_TO_EACH_BATCH=YES
```

# 3. APROBACIÓN DEL PROPIETARIO

```text
OWNER_APPROVAL_ID=OA-GM-AI-LOCAL-CONTEXT-CLASSIFICATION-01-REBASELINE-01
OWNER_APPROVAL_STATUS=GRANTED
OWNER_APPROVAL_SCOPE=PHASE_1_CONTRACT_REBASELINE_ONLY
OWNER_APPROVAL_REVOKED=NO
```

La aprobación contenía inicialmente dos separadores omitidos. Eduardo confirmó posteriormente esta corrección autoritativa:

```text
CONFIRMO_CORRECCIÓN_DE_RUTAS

ROOT-01=C:\Users\elbur\.codex\attachments
ROOT-02=C:\Users\elbur\.claude
```

La corrección no modifica el alcance y no requiere una nueva aprobación.

Las cuatro rutas definitivas son:

```text
ROOT-01=C:\Users\elbur\.codex\attachments
ROOT-02=C:\Users\elbur\.claude
ROOT-03=C:\Users\elbur\AppData\Local\Claude-3p
ROOT-04=C:\Users\elbur\AppData\Local\claude-cli-nodejs
```

Usa exclusivamente estas rutas. No las inventes, completes, reemplaces ni deduzcas.

# 4. UBICACIÓN DEL TRACK

```text
WORKSPACE_ROOT=D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT
TRACK_RELATIVE_PATH=Fabric\gm-ai-boxghost\tracks\GM-AI-LOCAL-CONTEXT-CLASSIFICATION-01
TRACK_ROOT=D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT\Fabric\gm-ai-boxghost\tracks\GM-AI-LOCAL-CONTEXT-CLASSIFICATION-01
```

Antes de ejecutar, confirma físicamente:

```text
WORKSPACE_ROOT_EXISTS
TRACK_ROOT_EXISTS
INTERVENTIONS_DIRECTORY_EXISTS
CHATGPT_CODEX_DIRECTORY_EXISTS
```

No busques otro track alternativo. Si la ruta exacta no existe:

```text
BLOCKER=TRACK_ROOT_NOT_FOUND
EXECUTION_STATUS=BLOCKED
```

# 5. ACCESO AUTORIZADO A LAS FUENTES

Para construir la enumeración puedes realizar únicamente operaciones de metadatos:

```text
CONFIRM_ROOT_EXISTENCE
CONFIRM_ROOT_DIRECTORY_TYPE
DETECT_ROOT_REPARSE_POINT_STATUS
ENUMERATE_DIRECTORY_ENTRIES
DETECT_ENTRY_TYPE
DETECT_REPARSE_POINTS
OBTAIN_FILE_SIZE
OBTAIN_FILE_EXTENSION
OBTAIN_RELATIVE_PATH
COMPARE_TWO_METADATA_ENUMERATION_PASSES
```

Está prohibido durante esta intervención:

```text
READ_SOURCE_FILE_CONTENT
CALCULATE_SOURCE_CONTENT_HASH
CLASSIFY_SOURCE_FILE
COPY_SOURCE_FILE
MOVE_SOURCE_FILE
RENAME_SOURCE_FILE
MODIFY_SOURCE_FILE
DELETE_SOURCE_FILE
FOLLOW_SYMBOLIC_LINK
FOLLOW_JUNCTION
FOLLOW_REPARSE_POINT
START_BATCH_001
START_ANY_LATER_BATCH
```

No abras archivos fuente aunque su extensión parezca segura.

La lectura autorizada se limita a metadatos del sistema de archivos necesarios para construir la enumeración.

# 6. VERIFICACIÓN DE RAÍCES

Para cada raíz registra:

```text
ROOT_ID
OWNER_APPROVED_ABSOLUTE_PATH
ROOT_TYPE=AI_LOCAL_CONTEXT_SOURCE
ROOT_ORDER
EXISTS_AT_BASELINE_TIME
DIRECTORY_TYPE_CONFIRMED
REPARSE_POINT_STATUS
ACCESS_BOUNDARY=ROOT_ONLY_NO_ESCAPE
INCLUSION_RULE=REGULAR_FILES_ONLY
EXCLUSION_RULE=SYMLINK_JUNCTION_REPARSE_POINT
OWNER_APPROVAL_REFERENCE
```

Reglas:

1. El orden canónico es `ROOT-01`, `ROOT-02`, `ROOT-03`, `ROOT-04`.
2. Cada raíz debe existir y ser un directorio real.
3. Si una raíz es un enlace, junction o reparse point, detente.
4. No sigas enlaces o reparse points encontrados dentro de una raíz.
5. No permitas que una ruta relativa resuelta salga de su raíz autorizada.
6. No enumeres ninguna ubicación exterior.
7. Registra únicamente cantidades agregadas de entradas excluidas por tipo.

Si una raíz falta o no puede verificarse:

```text
BLOCKER=APPROVED_ROOT_NOT_VERIFIABLE
BASELINE_STATUS=BLOCKED
```

# 7. ENUMERACIÓN DETERMINISTA

Incluye todos los archivos regulares físicamente contenidos en las cuatro raíces.

No excluyas un archivo por parecer caché, telemetría, dependencia, secreto, autenticación, dato personal o contenido irrelevante. Esas decisiones pertenecen a la futura clasificación, no a la construcción del universo.

Excluye únicamente:

```text
DIRECTORIES
SYMBOLIC_LINKS
JUNCTIONS
REPARSE_POINTS
NON_REGULAR_FILES
ENTRIES_RESOLVING_OUTSIDE_APPROVED_ROOT
```

Realiza dos pasadas de enumeración basadas solamente en metadatos y compara:

```text
SOURCE_ROOT_ID
NORMALIZED_RELATIVE_PATH
FILE_SIZE
ENTRY_TYPE
```

Si las dos pasadas no producen el mismo conjunto:

```text
BLOCKER=SOURCE_ENUMERATION_NOT_STABLE
BASELINE_STATUS=BLOCKED
```

No persistas un CSV incompleto como línea base aceptada.

# 8. REPRESENTACIÓN CANÓNICA DEL CSV

Crea:

```text
02_PHASE_1_SOURCE_ENUMERATION_v1.0.csv
```

Columnas exactas y en este orden:

```text
BASELINE_ORDINAL
SOURCE_ROOT_ID
SAFE_RELATIVE_PATH
FILE_TYPE
SIZE_BYTES
ENUMERATION_STATUS
BATCH_ASSIGNMENT
```

Reglas:

1. Codificación `UTF-8` sin BOM.
2. Terminación de línea `LF`.
3. Separador `,`.
4. Aplica comillas dobles cuando lo requiera el valor.
5. Escapa una comilla interna duplicándola.
6. No agregues líneas vacías al inicio o al final.
7. Usa separadores `/` dentro de `SAFE_RELATIVE_PATH`.
8. No uses una ruta absoluta en el CSV.
9. Conserva la capitalización real del nombre.
10. `FILE_TYPE` se deriva únicamente de la extensión, sin leer contenido.
11. Usa `NO_EXTENSION` cuando corresponda.
12. `SIZE_BYTES` se obtiene de metadatos.
13. `ENUMERATION_STATUS=ENUMERATED`.
14. Ordena primero por `ROOT_ORDER`.
15. Dentro de cada raíz, ordena por ruta normalizada mediante comparación insensible a mayúsculas.
16. Usa la ruta original como desempate determinista.
17. Asigna `BASELINE_ORDINAL` consecutivamente desde `1`.
18. Asigna lotes de hasta 50 entradas:

    * ordinales `1..50`: `BATCH-001`;
    * ordinales `51..100`: `BATCH-002`;
    * continúa consecutivamente;
    * el último lote puede contener menos de 50 archivos.
19. La asignación de lote no autoriza su ejecución.
20. No persistas valores de contenido encontrados dentro de archivos.

Si un nombre de archivo o segmento de ruta parece contener directamente una credencial, token, secreto o valor de autenticación, no lo publiques sin protección. Detén la creación de la enumeración y reporta únicamente:

```text
BLOCKER=SENSITIVE_VALUE_DETECTED_IN_PATH_METADATA
SENSITIVE_VALUE_PERSISTED=NO
```

No incluyas el valor detectado en el informe.

# 9. CUATRO ARTEFACTOS CANÓNICOS

Crea exclusivamente estos cuatro artefactos de línea base:

```text
01_PHASE_1_ROOT_REGISTRY_v1.0.md
02_PHASE_1_SOURCE_ENUMERATION_v1.0.csv
03_PHASE_1_SOURCE_ENUMERATION_MANIFEST_v1.0.md
04_PHASE_1_CLASSIFICATION_CONTRACT_v1.0.md
```

Deben quedar dentro de la nueva intervención de Codex, junto con los dos archivos obligatorios de trazabilidad:

```text
request.md
report.md
```

`request.md` y `report.md` no constituyen contratos adicionales; son evidencia de la intervención.

No crees scripts, archivos temporales persistentes, respaldos, índices, manifiestos adicionales ni checkpoints.

# 10. MANIFIESTO DE ENUMERACIÓN

`03_PHASE_1_SOURCE_ENUMERATION_MANIFEST_v1.0.md` debe contener como mínimo:

```text
BASELINE_ID=PHASE-1-REBASELINE-v1.0
BASELINE_CREATION_DATE=20260802
TIMEZONE=America/Guayaquil
PROCESS_TYPE=PHASE_1_CONTRACT_REBASELINE
HISTORICAL_CONTRACT_RECOVERY=NO

ROOT_REGISTRY_REFERENCE=01_PHASE_1_ROOT_REGISTRY_v1.0.md
ENUMERATION_FILE_REFERENCE=02_PHASE_1_SOURCE_ENUMERATION_v1.0.csv
CLASSIFICATION_CONTRACT_REFERENCE=04_PHASE_1_CLASSIFICATION_CONTRACT_v1.0.md

ENUMERATION_ALGORITHM=<descripción exacta>
NORMALIZATION_RULES=<reglas exactas>
SORTING_RULES=<reglas exactas>
INCLUSION_RULES=REGULAR_FILES_ONLY
EXCLUSION_RULES=SYMLINK_JUNCTION_REPARSE_POINT_NON_REGULAR_OUTSIDE_ROOT

HISTORICAL_EXPECTED_SOURCE_FILES=354
NEW_BASELINE_SOURCE_FILES=<conteo físico>
COUNT_DIFFERENCE=<NEW_BASELINE_SOURCE_FILES-354>
COUNT_MATCHES_HISTORICAL_REFERENCE=<YES|NO>

ENUMERATION_CSV_ENCODING=UTF-8_NO_BOM
ENUMERATION_CSV_LINE_ENDING=LF
ENUMERATION_CSV_SHA256=<SHA-256 de los bytes exactos del CSV>
ENUMERATION_CSV_HASH_SCOPE=MEMBERSHIP_ORDER_AND_RECORDED_METADATA_ONLY
ENUMERATION_CSV_HASH_FREEZES_SOURCE_CONTENT=NO
SOURCE_CONTENT_HASHING_STAGE=EACH_CLASSIFICATION_BATCH

OWNER_APPROVAL_ID=OA-GM-AI-LOCAL-CONTEXT-CLASSIFICATION-01-REBASELINE-01
OWNER_APPROVAL_STATUS=GRANTED
```

El hash del CSV protege la representación congelada de pertenencia, orden y metadatos registrados. No demuestra que el contenido de los archivos permanezca sin cambios.

Durante cada lote futuro se deberá calcular el SHA-256 de contenido de cada archivo. Si un archivo cambia respecto del estado observado durante el procesamiento de su lote, ese archivo deberá bloquearse.

# 11. CONTRATO DE CLASIFICACIÓN

`04_PHASE_1_CLASSIFICATION_CONTRACT_v1.0.md` debe definir estas doce categorías:

```text
1. EXCLUDE_SECRET
2. EXCLUDE_AUTHENTICATION
3. EXCLUDE_PERSONAL_DATA
4. EXCLUDE_REGENERABLE_CACHE
5. EXCLUDE_BUILD_OR_DEPENDENCY
6. EXCLUDE_TELEMETRY
7. EXCLUDE_IRRELEVANT
8. DUPLICATE_REFERENCE_ONLY
9. PERSIST_TRACK_SPECIFIC
10. PERSIST_SHARED_CONTEXT
11. KEEP_UNCLASSIFIED
12. MANUAL_OWNER_REVIEW_REQUIRED
```

Para cada categoría define expresamente:

```text
DEFINITION
POSITIVE_CRITERIA
NEGATIVE_CRITERIA
PRECEDENCE
CONFIDENCE_REQUIREMENT
SENSITIVITY_BEHAVIOR
DUPLICATE_BEHAVIOR
DESTINATION_KEY
COPY_AUTHORIZATION
AMBIGUITY_BEHAVIOR
SAFE_EVIDENCE_REQUIREMENTS
```

Aplica estas reglas mínimas:

## 11.1 EXCLUDE_SECRET

Incluye archivos cuyo contenido contenga secretos operativos, claves privadas, API keys, tokens, contraseñas, cadenas de conexión con credenciales o material equivalente.

```text
DESTINATION_KEY=NO_DESTINATION
COPY_AUTHORIZATION=NO
SECRET_VALUE_PERSISTENCE=PROHIBITED
```

## 11.2 EXCLUDE_AUTHENTICATION

Incluye cookies, sesiones, credenciales, almacenes de autenticación, tokens OAuth y estados de acceso.

```text
DESTINATION_KEY=NO_DESTINATION
COPY_AUTHORIZATION=NO
AUTHENTICATION_VALUE_PERSISTENCE=PROHIBITED
```

## 11.3 EXCLUDE_PERSONAL_DATA

Incluye archivos cuyo contenido exponga datos personales que no sean necesarios para preservar conocimiento técnico legítimo.

No persistas nombres, correos, direcciones, teléfonos, identificadores personales ni otros valores detectados.

```text
DESTINATION_KEY=NO_DESTINATION
COPY_AUTHORIZATION=NO
PERSONAL_VALUE_PERSISTENCE=PROHIBITED
MINIMUM_CONFIDENCE=0.90
```

Si existe duda o la confianza es inferior a `0.90`:

```text
CLASSIFICATION=MANUAL_OWNER_REVIEW_REQUIRED
```

## 11.4 EXCLUDE_REGENERABLE_CACHE

Incluye artefactos temporales o cachés regenerables que no aportan contexto durable.

```text
DESTINATION_KEY=NO_DESTINATION
COPY_AUTHORIZATION=NO
```

## 11.5 EXCLUDE_BUILD_OR_DEPENDENCY

Incluye dependencias descargables, salidas de compilación y artefactos generados reproducibles.

```text
DESTINATION_KEY=NO_DESTINATION
COPY_AUTHORIZATION=NO
```

## 11.6 EXCLUDE_TELEMETRY

Incluye telemetría, métricas, diagnósticos automáticos y registros operativos sin valor contextual durable.

```text
DESTINATION_KEY=NO_DESTINATION
COPY_AUTHORIZATION=NO
```

## 11.7 EXCLUDE_IRRELEVANT

Incluye contenido que no guarda relación material con GYPPORT®, sus tracks, decisiones, arquitectura o colaboración entre agentes.

```text
DESTINATION_KEY=NO_DESTINATION
COPY_AUTHORIZATION=NO
```

## 11.8 DUPLICATE_REFERENCE_ONLY

Aplica a archivos no sensibles cuyo SHA-256 de contenido sea idéntico a una entrada canónica anterior del universo congelado.

```text
DESTINATION_KEY=REFERENCE_ONLY
COPY_AUTHORIZATION=NO
```

La seguridad se evalúa antes que la duplicidad.

## 11.9 PERSIST_TRACK_SPECIFIC

Incluye conocimiento durable aplicable exclusivamente al track actual.

```text
DESTINATION_KEY=TRACK_CONTEXT_CANDIDATE
COPY_AUTHORIZATION=NO
```

## 11.10 PERSIST_SHARED_CONTEXT

Incluye conocimiento durable y reutilizable por más de un track, agente o componente de GYPPORT®.

```text
DESTINATION_KEY=SHARED_CONTEXT_CANDIDATE
COPY_AUTHORIZATION=NO
```

## 11.11 KEEP_UNCLASSIFIED

Incluye archivos cuyo formato o evidencia disponible impide una evaluación técnica, pero sin indicios que exijan exclusión sensible inmediata.

```text
DESTINATION_KEY=UNCLASSIFIED_HOLD
COPY_AUTHORIZATION=NO
```

No debe usarse para evitar una revisión manual cuando existan ambigüedad, riesgo o baja confianza.

## 11.12 MANUAL_OWNER_REVIEW_REQUIRED

Incluye conflictos taxonómicos no resueltos, riesgo sensible, ambigüedad material o confianza inferior a `0.90`.

```text
DESTINATION_KEY=OWNER_REVIEW_QUEUE
COPY_AUTHORIZATION=NO
```

No persistas el valor sensible que originó la revisión.

# 12. PRECEDENCIA Y CONFIANZA

Precedencia:

```text
1. EXCLUDE_SECRET
2. EXCLUDE_AUTHENTICATION
3. EXCLUDE_PERSONAL_DATA
4. EXCLUDE_REGENERABLE_CACHE
5. EXCLUDE_BUILD_OR_DEPENDENCY
6. EXCLUDE_TELEMETRY
7. EXCLUDE_IRRELEVANT
8. DUPLICATE_REFERENCE_ONLY
9. PERSIST_TRACK_SPECIFIC
10. PERSIST_SHARED_CONTEXT
11. KEEP_UNCLASSIFIED
```

`MANUAL_OWNER_REVIEW_REQUIRED` funciona como compuerta fail-closed y prevalece cuando:

```text
CONFIDENCE_LT_0.90
AMBIGUITY_NOT_RESOLVED
SENSITIVE_RISK_NOT_RESOLVED
PRECEDENCE_DOES_NOT_PRODUCE_UNIQUE_RESULT
```

Reglas:

```text
MINIMUM_FINAL_CLASSIFICATION_CONFIDENCE=0.90
SAFETY_EXCLUSION_OVERRIDES_DUPLICATE_STATUS=YES
SAFETY_EXCLUSION_OVERRIDES_PERSISTENCE=YES
LOW_CONFIDENCE_OVERRIDES_FINAL_CLASSIFICATION=YES
ARTIFICIAL_CONFIDENCE_INCREASE=PROHIBITED
```

# 13. DUPLICADOS Y DESTINOS

Los duplicados se determinarán en los lotes futuros mediante SHA-256 de contenido.

1. Evalúa seguridad antes que duplicidad.
2. Un archivo sensible conserva su categoría de exclusión.
3. Entre duplicados no sensibles, la primera entrada según el orden congelado será canónica.
4. Las entradas posteriores serán `DUPLICATE_REFERENCE_ONLY`.
5. No elimines, muevas ni copies duplicados.
6. Registra únicamente identificadores seguros.

Destinos lógicos:

```text
PERSIST_TRACK_SPECIFIC=TRACK_CONTEXT_CANDIDATE
PERSIST_SHARED_CONTEXT=SHARED_CONTEXT_CANDIDATE
MANUAL_OWNER_REVIEW_REQUIRED=OWNER_REVIEW_QUEUE
KEEP_UNCLASSIFIED=UNCLASSIFIED_HOLD
DUPLICATE_REFERENCE_ONLY=REFERENCE_ONLY
ALL_EXCLUDE_CATEGORIES=NO_DESTINATION
```

Para las doce categorías:

```text
COPY_AUTHORIZATION=NO
MOVE_AUTHORIZATION=NO
DELETE_AUTHORIZATION=NO
```

# 14. PROTECCIÓN DE INFORMACIÓN

El contrato debe declarar:

```text
SECRET_VALUE_PERSISTENCE=PROHIBITED
AUTHENTICATION_VALUE_PERSISTENCE=PROHIBITED
PERSONAL_VALUE_PERSISTENCE=PROHIBITED
PRIVATE_KEY_CONTENT_PERSISTENCE=PROHIBITED
COOKIE_OR_SESSION_VALUE_PERSISTENCE=PROHIBITED
CONNECTION_STRING_CREDENTIAL_PERSISTENCE=PROHIBITED
```

Cuando un lote futuro detecte un indicador sensible, solo podrá registrar:

```text
SENSITIVE_INDICATOR_DETECTED=YES
SENSITIVE_INDICATOR_TYPE=<categoría segura>
VALUE_REDACTED=YES
```

Esta intervención no debe detectar indicadores mediante lectura de contenido porque no está autorizada a abrir los archivos.

# 15. IDENTIFICADOR CRONOLÓGICO

Persiste la intervención exclusivamente en:

```text
interventions\chatgpt-codex\CHATGPT-CODEX-20260802-NNN
```

Calcula `NNN` usando únicamente carpetas directas que coincidan exactamente con:

```text
CHATGPT-CODEX-20260802-[0-9][0-9][0-9]
```

Reglas:

1. Obtén la secuencia válida más alta y suma uno.
2. No rellenes huecos.
3. No reutilices identificadores.
4. No renombres intervenciones existentes.
5. No modifiques entradas mal formadas.
6. Reporta entradas mal formadas solo como cantidad agregada.
7. Comprueba la ausencia de colisión inmediatamente antes de crear la carpeta.
8. No asumas que corresponde `003`; calcúlalo físicamente.

Si existe colisión:

```text
BLOCKER=INTERVENTION_IDENTIFIER_COLLISION
PERSISTENCE_STATUS=NOT_EXECUTED
```

No selecciones automáticamente otro identificador.

# 16. PERSISTENCIA AUTORIZADA

Dentro de la nueva intervención crea exactamente:

```text
CHATGPT-CODEX-20260802-NNN\
├── request.md
├── report.md
├── 01_PHASE_1_ROOT_REGISTRY_v1.0.md
├── 02_PHASE_1_SOURCE_ENUMERATION_v1.0.csv
├── 03_PHASE_1_SOURCE_ENUMERATION_MANIFEST_v1.0.md
└── 04_PHASE_1_CLASSIFICATION_CONTRACT_v1.0.md
```

Reglas:

* `request.md`: copia íntegra y fiel de esta instrucción.
* `report.md`: informe final completo.
* Los otros cuatro archivos son la línea base aprobada.
* No modifiques intervenciones anteriores.
* No actualices `TRACK_STATE.md`, índices, manifiestos globales, checkpoints o estados acumulativos.
* No crees archivos adicionales.
* No hagas staging, commit ni push.
* Realiza la persistencia solamente después de completar las verificaciones en memoria.
* Después de persistir, relee y verifica los seis archivos.
* Calcula y registra el SHA-256 de los seis archivos persistidos.
* El SHA-256 de estos artefactos sí está autorizado; no calcules SHA-256 de archivos fuente.

# 17. SALIDA OBLIGATORIA

`report.md` debe comenzar con:

```text
TRACK=GM-AI-LOCAL-CONTEXT-CLASSIFICATION-01
STEP=PHASE_1_CONTRACT_REBASELINE_IMPLEMENTATION
AGENT=CHATGPT_CODEX
AGENT_DIRECTORY=chatgpt-codex
EXECUTION_MODE=APPROVED_METADATA_ONLY_BASELINE_CONSTRUCTION
TIMEZONE=America/Guayaquil

OWNER_APPROVAL_ID=OA-GM-AI-LOCAL-CONTEXT-CLASSIFICATION-01-REBASELINE-01
OWNER_APPROVAL_STATUS=GRANTED
OWNER_ROUTE_CORRECTION_CONFIRMED=YES
OWNER_APPROVAL_SCOPE=PHASE_1_CONTRACT_REBASELINE_ONLY

INTERVENTION_LOCAL_DATE=20260802
INTERVENTION_SEQUENCE=<NNN|NOT_ALLOCATED>
INTERVENTION_ID=<CHATGPT-CODEX-20260802-NNN|NOT_ALLOCATED>
INTERVENTION_PATH=<ruta relativa segura|NOT_CREATED>

VALID_SAME_DAY_CHATGPT_CODEX_INTERVENTIONS_COUNT=<cantidad>
HIGHEST_EXISTING_SEQUENCE=<NNN|NONE>
NEXT_SEQUENCE=<NNN|NOT_ALLOCATED>
MALFORMED_ENTRIES_COUNT=<cantidad>
IDENTIFIER_COLLISION=<YES|NO|NOT_CHECKED>

APPROVED_ROOTS=4
ROOTS_VERIFIED=<0..4>
ROOT_REPARSE_POINTS_FOLLOWED=0
INTERNAL_REPARSE_POINTS_FOLLOWED=0
OUTSIDE_ROOT_ACCESS_OCCURRED=NO

ENUMERATION_PASS_1_COUNT=<cantidad>
ENUMERATION_PASS_2_COUNT=<cantidad>
ENUMERATION_PASSES_MATCH=<YES|NO>
HISTORICAL_EXPECTED_SOURCE_FILES=354
NEW_BASELINE_SOURCE_FILES=<cantidad|NOT_COMPLETED>
COUNT_DIFFERENCE=<entero|NOT_COMPLETED>
COUNT_MATCHES_HISTORICAL_REFERENCE=<YES|NO|NOT_COMPLETED>
BATCHES_ASSIGNED=<cantidad|0>
SOURCE_CONTENT_FILES_READ=0
SOURCE_CONTENT_HASHES_CALCULATED=0
SOURCE_FILES_CLASSIFIED=0
SOURCE_FILES_COPIED=0
SOURCE_FILES_MOVED=0
SOURCE_FILES_MODIFIED=0
SOURCE_FILES_DELETED=0

ROOT_REGISTRY_CREATED=<YES|NO>
SOURCE_ENUMERATION_CREATED=<YES|NO>
ENUMERATION_MANIFEST_CREATED=<YES|NO>
CLASSIFICATION_CONTRACT_CREATED=<YES|NO>
CLASSIFICATION_CATEGORIES_DEFINED=<0|12>
EXCLUDE_PERSONAL_DATA_INCLUDED=<YES|NO>
MINIMUM_FINAL_CLASSIFICATION_CONFIDENCE=<0.90|NOT_CREATED>

REQUEST_MD_CREATED=<YES|NO>
REPORT_MD_CREATED=<YES|NO>
ALL_SIX_FILES_VERIFIED=<YES|NO>
ARTIFACT_HASHES_RECORDED=<YES|NO>

BATCH_001_EXECUTED=NO
LATER_BATCH_EXECUTED=NO
CLASSIFICATION_AUTHORIZATION_CONSUMED=NO

PREVIOUS_INTERVENTIONS_MODIFIED=0
PREVIOUS_INTERVENTIONS_RENAMED=0
GIT_COMMANDS_EXECUTED=0
FILES_STAGED_BY_THIS_EXECUTION=0
COMMITS_CREATED_BY_THIS_EXECUTION=0
PUSHES_EXECUTED_BY_THIS_EXECUTION=0
GITHUB_AUTHENTICATION_USED=NO
BOXGHOST_INCORPORATED_INTO_FABRIC=NO

BLOCKERS=<lista|NONE>
VERDICT=<REBASELINE_IMPLEMENTED_READY_FOR_CLAUDE_CODE_AUDIT|REBASELINE_IMPLEMENTATION_BLOCKED>
PERSISTENCE_STATUS=<COMPLETED|BLOCKED|NOT_EXECUTED>
NEXT_STEP=CLAUDE_CODE_AUDITS_PHASE_1_REBASELINE_CONTRACTS_AND_ENUMERATION
```

Incluye después:

```text
## A. Identificación y aprobación
## B. Verificación de raíces
## C. Algoritmo y estabilidad de la enumeración
## D. Conteo nuevo frente a referencia histórica
## E. Artefactos creados
## F. Integridad SHA-256
## G. Límites respetados
## H. Veredicto
## I. Persistencia
```

No publiques en `report.md` nombres individuales de archivos fuente ni valores sensibles.

# 18. CONFIRMACIÓN FINAL DE LÍMITES

Si la ejecución concluye correctamente, declara exactamente:

```text
THE_FOUR_OWNER_APPROVED_ROOTS_WERE_USED_WITHOUT_SUBSTITUTION
THE_HISTORICAL_COUNT_354_WAS_RETAINED_AS_REFERENCE_ONLY
THE_NEW_BASELINE_COUNT_WAS_NOT_ARTIFICIALLY_ADJUSTED
ONLY_REGULAR_FILE_METADATA_WAS_ENUMERATED
NO_SOURCE_FILE_CONTENT_WAS_READ
NO_SOURCE_CONTENT_HASH_WAS_CALCULATED
NO_SOURCE_FILE_WAS_CLASSIFIED
NO_SOURCE_FILE_WAS_COPIED_MOVED_MODIFIED_OR_DELETED
NO_SYMBOLIC_LINK_JUNCTION_OR_REPARSE_POINT_WAS_FOLLOWED
NO_PATH_OUTSIDE_THE_APPROVED_ROOTS_WAS_ACCESSED
NO_BATCH_001_CLASSIFICATION_WAS_EXECUTED
NO_LATER_BATCH_WAS_STARTED
NO_EXISTING_INTERVENTION_WAS_MODIFIED_OR_RENAMED
NO_INTERVENTION_IDENTIFIER_WAS_REUSED
ONLY_THE_NEW_CHATGPT_CODEX_INTERVENTION_AND_ITS_SIX_APPROVED_FILES_WERE_CREATED
NO_GIT_COMMAND_WAS_EXECUTED
NO_FILE_WAS_STAGED_COMMITTED_OR_PUSHED
NO_GITHUB_AUTHENTICATION_WAS_USED
NO_BOXGHOST_CONTENT_WAS_INCORPORATED_INTO_FABRIC
OWNER_APPROVAL_WAS_NOT_REQUESTED_AGAIN
```

# 19. ORDEN DE EJECUCIÓN

Ejecuta exactamente:

1. Confirma `WORKSPACE_ROOT` y `TRACK_ROOT`.
2. Verifica la aprobación y su corrección de rutas.
3. Valida existencia y tipo de las cuatro raíces.
4. Confirma que las raíces no sean reparse points.
5. Realiza la primera enumeración exclusivamente de metadatos.
6. Realiza la segunda enumeración exclusivamente de metadatos.
7. Compara ambas enumeraciones.
8. Si existe inestabilidad o riesgo sensible en metadatos de ruta, detente fail-closed.
9. Construye en memoria los cuatro artefactos.
10. Calcula el conteo real sin forzarlo a `354`.
11. Construye el CSV canónico.
12. Calcula el SHA-256 del CSV.
13. Construye el manifiesto.
14. Construye el contrato de doce categorías.
15. Calcula físicamente el siguiente identificador de Codex.
16. Comprueba ausencia de colisión.
17. Crea una sola carpeta de intervención.
18. Crea exactamente los seis archivos autorizados.
19. Relee los seis archivos.
20. Verifica fidelidad, estructura y hashes.
21. Devuelve exactamente el contenido persistido en `report.md`.
22. Detente.

# 20. PROHIBICIONES FINALES

```text
DO_NOT_START_BATCH_001
DO_NOT_CLASSIFY_ANY_SOURCE
DO_NOT_READ_SOURCE_CONTENT
DO_NOT_HASH_SOURCE_CONTENT
DO_NOT_COPY_MOVE_MODIFY_OR_DELETE_SOURCE
DO_NOT_FOLLOW_REPARSE_POINTS
DO_NOT_EXPAND_BEYOND_ROOT_01_TO_ROOT_04
DO_NOT_MODIFY_PREVIOUS_INTERVENTIONS
DO_NOT_UPDATE_TRACK_STATE
DO_NOT_RUN_GIT
DO_NOT_STAGE_COMMIT_OR_PUSH
DO_NOT_REQUEST_OWNER_APPROVAL_AGAIN
```

Siguiente paso único:

```text
NEXT_STEP=CLAUDE_CODE_AUDITS_PHASE_1_REBASELINE_CONTRACTS_AND_ENUMERATION
```