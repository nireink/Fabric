PEGAR EN: CHATGPT CODEX — SEGUNDO INTENTO CORRECTIVO DEL REBASELINE

```text
TRACK=GM-AI-LOCAL-CONTEXT-CLASSIFICATION-01
STEP=PHASE_1_CORRECTED_REBASELINE_AFTER_CONTEXT_DIAGNOSIS
MODE=APPROVED_METADATA_ONLY_CORRECTIVE_IMPLEMENTATION
AGENT=CHATGPT_CODEX
TIMEZONE=America/Guayaquil

OWNER_APPROVAL_ID=OA-GM-AI-LOCAL-CONTEXT-CLASSIFICATION-01-REBASELINE-01
OWNER_APPROVAL_STATUS=GRANTED
OWNER_APPROVAL_REUSE=AUTHORIZED
NEW_OWNER_APPROVAL_REQUIRED=NO

FAILED_BASELINE_REFERENCE=CHATGPT-CODEX-20260802-003
FAILED_CORRECTION_REFERENCE=CHATGPT-CODEX-20260803-001
INITIAL_AUDIT_REFERENCE=CLAUDE-CODE-20260802-003
DIAGNOSTIC_AUDIT_REFERENCE=CLAUDE-CODE-20260803-001

DIAGNOSTIC_AUDIT_VERDICT=ROOT_04_DISCREPANCY_DIAGNOSED_READY_FOR_CODEX_RETRY
DIAGNOSTIC_CATEGORY=ENVIRONMENT_OR_PATH_CONTEXT_MISMATCH
DIAGNOSTIC_CONFIDENCE=0.75
EXACT_CONTEXT_MISMATCH_MECHANISM=UNRESOLVED
```

# 1. Orden

Construye una nueva línea base corregida de la Fase 1, exclusivamente mediante metadatos.

No repitas sin comprobación el mecanismo que produjo únicamente dos archivos en `ROOT-04`. Antes de crear los seis artefactos, debes superar el preflight de completitud definido a continuación.

No modifiques ninguna intervención anterior.

# 2. Evidencia diagnóstica obligatoria

La auditoría `CLAUDE-CODE-20260803-001` comprobó sobre la raíz física:

```text
C:\Users\elbur\AppData\Local\claude-cli-nodejs
```

los siguientes resultados:

```text
POWERSHELL_DEFAULT_REGULAR_FILE_COUNT=1304
POWERSHELL_FORCE_REGULAR_FILE_COUNT=1304
DOTNET_DIRECTORY_ENUMERATE_FILES_COUNT=1304
HIDDEN_OR_SYSTEM_FILES_COUNT=0
HIDDEN_OR_SYSTEM_DIRECTORIES_COUNT=0
REPARSE_POINTS_COUNT=0
ENUMERATION_ERRORS_COUNT=0
SECOND_CONFIRMATION_PASS_COUNT=1304
NORMALIZED_METADATA_DIFFERENCES_BETWEEN_PASSES=0
```

El valor `1304` es una referencia observada, no un conteo que debas forzar. La carpeta puede cambiar legítimamente.

Queda descartado como causa:

```text
ATTRIBUTE_FILTER_DEFECT
HIDDEN_SYSTEM_ATTRIBUTE_OMISSION
REPARSE_POINT_OMISSION
ENUMERATION_INSTABILITY
SOURCE_STATE_DRIFT_OBSERVED_DURING_AUDIT
```

# 3. Raíces autorizadas

Usa exactamente:

```text
ROOT-01=C:\Users\elbur\.codex\attachments
ROOT-02=C:\Users\elbur\.claude
ROOT-03=C:\Users\elbur\AppData\Local\Claude-3p
ROOT-04=C:\Users\elbur\AppData\Local\claude-cli-nodejs
```

No sustituyas estas rutas por ZIP, copias, aliases, directorios sincronizados, rutas equivalentes ni snapshots.

# 4. Límites

Autorizado:

```text
READ_FILESYSTEM_METADATA
VERIFY_ROOT_AND_DIRECTORY_ATTRIBUTES
ENUMERATE_REGULAR_FILES
COMPARE_MULTIPLE_METADATA_ENUMERATION_METHODS
RECORD_SAFE_RELATIVE_PATHS
RECORD_FILE_EXTENSIONS
RECORD_FILE_SIZES
CREATE_ONE_NEW_CHATGPT_CODEX_INTERVENTION
CREATE_THE_SIX_AUTHORIZED_ARTIFACTS_IF_PREFLIGHT_PASSES
CALCULATE_SHA256_OF_NEW_INTERVENTION_ARTIFACTS
```

Prohibido:

```text
READ_SOURCE_FILE_CONTENT
CALCULATE_SOURCE_CONTENT_HASH
CLASSIFY_SOURCE_FILES
EXECUTE_BATCH_001
COPY_MOVE_MODIFY_OR_DELETE_SOURCE_FILES
FOLLOW_SYMBOLIC_LINKS_JUNCTIONS_OR_REPARSE_POINTS
ACCESS_OUTSIDE_THE_FOUR_APPROVED_ROOTS
MODIFY_RENAME_OR_DELETE_PREVIOUS_INTERVENTIONS
RUN_GIT
STAGE_COMMIT_OR_PUSH
USE_GITHUB_AUTHENTICATION
REQUEST_OWNER_APPROVAL_AGAIN
```

# 5. Preflight obligatorio de ROOT-04

Antes de crear el CSV, ejecuta directamente sobre `ROOT-04`:

```text
METHOD_1=PowerShell recursive enumeration without -Force
METHOD_2=PowerShell recursive enumeration with -Force
METHOD_3=.NET Directory.EnumerateFiles recursive enumeration
```

Además:

1. Verifica que la ruta literal exista.
2. Verifica que sea un directorio.
3. Verifica que la raíz no sea reparse point.
4. Verifica que `ROOT-04\Cache` exista.
5. Verifica que `ROOT-04\Cache` no sea reparse point.
6. Detecta reparse points antes de descender y no los sigas.
7. Registra excepciones o directorios inaccesibles.
8. No publiques nombres individuales de archivos.
9. Registra únicamente resultados agregados.

Declara:

```text
ROOT_04_LITERAL_PATH_USED
ROOT_04_EXISTS
ROOT_04_IS_DIRECTORY
ROOT_04_IS_REPARSE_POINT
ROOT_04_CACHE_EXISTS
ROOT_04_CACHE_IS_REPARSE_POINT

ROOT_04_POWERSHELL_DEFAULT_COUNT
ROOT_04_POWERSHELL_FORCE_COUNT
ROOT_04_DOTNET_RECURSIVE_COUNT

ROOT_04_HIDDEN_REGULAR_FILES_COUNT
ROOT_04_SYSTEM_REGULAR_FILES_COUNT
ROOT_04_REPARSE_ENTRIES_EXCLUDED
ROOT_04_INACCESSIBLE_DIRECTORIES_COUNT
ROOT_04_ENUMERATION_ERRORS_COUNT

ROOT_04_METHOD_COUNTS_MATCH
ROOT_04_TWO_FILE_RESULT_REPRODUCED
ROOT_04_INCLUSIVE_UNIVERSE_VISIBLE_TO_CURRENT_EXECUTION
```

## Gate de completitud

Solo continúa si:

```text
ROOT_04_METHOD_COUNTS_MATCH=YES
ROOT_04_TWO_FILE_RESULT_REPRODUCED=NO
ROOT_04_INCLUSIVE_UNIVERSE_VISIBLE_TO_CURRENT_EXECUTION=YES
ROOT_04_ENUMERATION_ERRORS_COUNT=0
ROOT_04_INACCESSIBLE_DIRECTORIES_COUNT=0
```

No es obligatorio que el resultado sea exactamente `1304`, pero debe representar el universo recursivo actual y no puede volver a ser el resultado incompleto de dos archivos.

Si Codex vuelve a observar solamente dos archivos o los métodos discrepan:

```text
BLOCKER=CODEX_EXECUTION_CONTEXT_CANNOT_OBSERVE_AUDITED_ROOT_04_UNIVERSE
VERDICT=REBASELINE_CORRECTION_BLOCKED_BY_EXECUTION_CONTEXT
PERSISTENCE_STATUS=BLOCKED
PHASE_1_BASELINE_ACCEPTED=NO
BATCH_001_EXECUTED=NO
NEXT_STEP=CHATGPT_WORK_DETERMINES_HOST_CONTEXT_EXECUTION_METHOD
```

En ese caso crea únicamente `request.md` y `report.md`. No construyas un CSV incompleto.

# 6. Enumeración completa

Si el preflight supera el gate, realiza dos pasadas completas sobre las cuatro raíces.

Cada pasada debe:

1. Enumerar todos los archivos regulares.
2. Recorrer todos los subdirectorios físicamente contenidos.
3. Incluir archivos de caché, dependencias, telemetría y cualquier otro archivo regular.
4. Excluir directorios, reparse points, enlaces simbólicos, junctions y entradas no regulares.
5. No seguir ninguna entrada excluida.
6. Registrar exclusivamente metadatos.
7. Normalizar las rutas relativas a NFC y separadores `/`.

Compara ambas pasadas por:

```text
SOURCE_ROOT_ID
NORMALIZED_RELATIVE_PATH
FILE_SIZE
ENTRY_TYPE
```

Declara:

```text
ROOT_01_PASS_1_COUNT
ROOT_01_PASS_2_COUNT
ROOT_01_PASSES_MATCH

ROOT_02_PASS_1_COUNT
ROOT_02_PASS_2_COUNT
ROOT_02_PASSES_MATCH

ROOT_03_PASS_1_COUNT
ROOT_03_PASS_2_COUNT
ROOT_03_PASSES_MATCH

ROOT_04_PASS_1_COUNT
ROOT_04_PASS_2_COUNT
ROOT_04_PASSES_MATCH

ENUMERATION_PASS_1_COUNT
ENUMERATION_PASS_2_COUNT
ENUMERATION_PASSES_MATCH
ENUMERATION_METADATA_SETS_MATCH
ROOT_COUNT_SUMS_MATCH_TOTALS
```

No aceptes coincidencia solamente por totales; deben coincidir rutas normalizadas, tamaños y tipos.

# 7. Artefactos

Si las pasadas coinciden, crea una nueva intervención con exactamente:

```text
request.md
report.md
01_PHASE_1_ROOT_REGISTRY_v1.0.md
02_PHASE_1_SOURCE_ENUMERATION_v1.0.csv
03_PHASE_1_SOURCE_ENUMERATION_MANIFEST_v1.0.md
04_PHASE_1_CLASSIFICATION_CONTRACT_v1.0.md
```

El CSV conservará exactamente:

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

```text
UTF8_NO_BOM
LF_LINE_ENDINGS
RELATIVE_PATHS_ONLY
FORWARD_SLASHES
DETERMINISTIC_ROOT_AND_PATH_ORDER
CONSECUTIVE_ORDINALS_FROM_1
CONSECUTIVE_BATCHES_OF_MAXIMUM_50
ENUMERATION_STATUS=ENUMERATED
```

La asignación de lotes no autoriza su clasificación.

# 8. Conteos de control

Registra separadamente:

```text
HISTORICAL_EXPECTED_SOURCE_FILES=354
REJECTED_BASELINE_SOURCE_FILES=364
PREVIOUS_AUDIT_ROOT_04_COUNT=1304
NEW_CORRECTED_BASELINE_SOURCE_FILES=<conteo físico actual>
DIFFERENCE_FROM_HISTORICAL_354=<entero>
DIFFERENCE_FROM_REJECTED_BASELINE_364=<entero>
```

No ajustes el resultado para coincidir con `354`, `364`, `1304` ni `1666`.

# 9. Contrato de clasificación

Reproduce las doce categorías aprobadas sin clasificar archivos:

```text
EXCLUDE_SECRET
EXCLUDE_AUTHENTICATION
EXCLUDE_PERSONAL_DATA
EXCLUDE_REGENERABLE_CACHE
EXCLUDE_BUILD_OR_DEPENDENCY
EXCLUDE_TELEMETRY
EXCLUDE_IRRELEVANT
DUPLICATE_REFERENCE_ONLY
PERSIST_TRACK_SPECIFIC
PERSIST_SHARED_CONTEXT
KEEP_UNCLASSIFIED
MANUAL_OWNER_REVIEW_REQUIRED
```

Conserva:

```text
MINIMUM_FINAL_CLASSIFICATION_CONFIDENCE=0.90
COPY_AUTHORIZATION=NO
MOVE_AUTHORIZATION=NO
DELETE_AUTHORIZATION=NO
```

No clasifiques automáticamente el contenido situado bajo `Cache`.

# 10. Identificador

Calcula la fecha local real de `America/Guayaquil` y el siguiente identificador disponible:

```text
CHATGPT-CODEX-YYYYMMDD-NNN
```

Considera únicamente directorios directos que coincidan exactamente con el patrón de esa fecha.

No asumas la secuencia, no rellenes huecos y no reutilices identificadores.

Si la fecha local continúa siendo `20260803` y no existe otra intervención válida posterior, el identificador esperado sería:

```text
CHATGPT-CODEX-20260803-002
```

Este valor es solo una expectativa de control; debes calcularlo físicamente.

# 11. Integridad

Después de persistir:

1. Comprueba que existan exactamente los archivos autorizados.
2. Relee los artefactos.
3. Calcula su SHA-256.
4. Registra en `report.md` los hashes de los otros cinco archivos.
5. Calcula el hash final de `report.md` después de cerrarlo.
6. Devuelve ese hash externamente.

Declara:

```text
REPORT_SELF_HASH_REQUIRED=NO
REPORT_HASH_TO_BE_EXTERNALLY_RECORDED=YES
SELF_HASH_LIMITATION_IS_NOT_A_BASELINE_BLOCKER=YES
```

# 12. Veredicto

Si el preflight permite ver el universo completo, las pasadas coinciden y se crean los seis artefactos:

```text
VERDICT=REBASELINE_CORRECTED_READY_FOR_CLAUDE_CODE_AUDIT
PERSISTENCE_STATUS=COMPLETED
PHASE_1_BASELINE_ACCEPTED=NO
BATCH_001_EXECUTED=NO
CLASSIFICATION_AUTHORIZATION_CONSUMED=NO
NEXT_STEP=CLAUDE_CODE_AUDITS_NEW_CORRECTED_REBASELINE
```

Si Codex continúa observando únicamente dos archivos:

```text
VERDICT=REBASELINE_CORRECTION_BLOCKED_BY_EXECUTION_CONTEXT
PERSISTENCE_STATUS=BLOCKED
PHASE_1_BASELINE_ACCEPTED=NO
BATCH_001_EXECUTED=NO
NEXT_STEP=CHATGPT_WORK_DETERMINES_HOST_CONTEXT_EXECUTION_METHOD
```

Devuelve el contenido completo de `report.md` y, fuera del archivo:

```text
REPORT_MD_FINAL_SHA256=<hash final>
```

Después detente. No ejecutes `BATCH-001`.
