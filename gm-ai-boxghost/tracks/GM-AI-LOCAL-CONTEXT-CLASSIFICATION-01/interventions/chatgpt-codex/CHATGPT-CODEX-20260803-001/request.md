PEGAR EN: CHATGPT CODEX — CORRECCIÓN DEL REBASELINE DE LA FASE 1

TRACK=GM-AI-LOCAL-CONTEXT-CLASSIFICATION-01
STEP=PHASE_1_CONTRACT_REBASELINE_CORRECTION
MODE=APPROVED_METADATA_ONLY_CORRECTIVE_IMPLEMENTATION
AGENT=CHATGPT_CODEX
TIMEZONE=America/Guayaquil

OWNER_APPROVAL_ID=OA-GM-AI-LOCAL-CONTEXT-CLASSIFICATION-01-REBASELINE-01
OWNER_APPROVAL_STATUS=GRANTED
OWNER_APPROVAL_REUSE=AUTHORIZED
NEW_OWNER_APPROVAL_REQUIRED=NO

FAILED_IMPLEMENTATION_REFERENCE=CHATGPT-CODEX-20260802-003
AUDIT_REFERENCE=CLAUDE-CODE-20260802-003
AUDIT_VERDICT=REBASELINE_REQUIRES_CORRECTION

# 1. ORDEN CORRECTIVA

Corrige exclusivamente la línea base de enumeración de la Fase 1.

La auditoría independiente confirmó una inconformidad material:

ROOT-04 fue registrado en el CSV con únicamente 2 archivos, pero una comprobación física directa encontró 1.304 archivos regulares dentro de:

C:\Users\elbur\AppData\Local\claude-cli-nodejs\Cache

Por tanto, la enumeración de 364 archivos creada en CHATGPT-CODEX-20260802-003 no constituye una línea base completa.

No modifiques, sobrescribas, renombres ni elimines:

CHATGPT-CODEX-20260802-003
CLAUDE-CODE-20260802-003
ninguna otra intervención existente

Esas intervenciones deben conservarse como evidencia histórica.

# 2. RAÍCES AUTORIZADAS

Usa exactamente estas cuatro raíces, sin sustituciones:

ROOT-01=C:\Users\elbur\.codex\attachments
ROOT-02=C:\Users\elbur\.claude
ROOT-03=C:\Users\elbur\AppData\Local\Claude-3p
ROOT-04=C:\Users\elbur\AppData\Local\claude-cli-nodejs

No utilices archivos ZIP como representación de estas carpetas.

La enumeración debe realizarse directamente sobre las cuatro raíces físicas.

# 3. LÍMITES

Está autorizado únicamente:

READ_FILESYSTEM_METADATA
VERIFY_DIRECTORY_AND_REPARSE_ATTRIBUTES
ENUMERATE_REGULAR_FILES
RECORD_SAFE_RELATIVE_PATHS
RECORD_FILE_EXTENSIONS
RECORD_FILE_SIZES
COMPARE_TWO_METADATA_ENUMERATION_PASSES
CREATE_ONE_NEW_CHATGPT_CODEX_INTERVENTION
CREATE_EXACTLY_SIX_AUTHORIZED_FILES
HASH_THE_SIX_NEW_ARTIFACTS

Está prohibido:

READ_SOURCE_FILE_CONTENT
HASH_SOURCE_FILE_CONTENT
CLASSIFY_SOURCE_FILES
EXECUTE_BATCH_001
COPY_MOVE_MODIFY_OR_DELETE_SOURCE_FILES
FOLLOW_SYMBOLIC_LINKS_JUNCTIONS_OR_REPARSE_POINTS
ACCESS_OUTSIDE_THE_FOUR_APPROVED_ROOTS
MODIFY_PREVIOUS_INTERVENTIONS
RUN_GIT
STAGE_COMMIT_OR_PUSH
USE_GITHUB_AUTHENTICATION
REQUEST_OWNER_APPROVAL_AGAIN

# 4. DIAGNÓSTICO OBLIGATORIO DEL DEFECTO

Antes de construir la nueva línea base, determina por metadatos por qué la ejecución anterior omitió los archivos de ROOT-04.

Registra únicamente una causa técnica segura, por ejemplo:

ENUMERATION_IMPLEMENTATION_DEFECT
DIRECTORY_TRAVERSAL_DEFECT
ATTRIBUTE_FILTER_DEFECT
NESTED_DIRECTORY_OMISSION
ACCESS_OR_VISIBILITY_DEFECT
UNDETERMINED

No publiques nombres individuales de archivos fuente ni valores sensibles.

Confirma expresamente:

PREVIOUS_ROOT_04_FROZEN_COUNT=2
AUDIT_OBSERVED_ROOT_04_COUNT=1304
PREVIOUS_ROOT_04_ENUMERATION_COMPLETE=NO

El valor 1.304 es evidencia de auditoría, no un conteo que debas forzar. El conteo nuevo debe calcularse físicamente en el momento de esta corrección.

# 5. ENUMERACIÓN CORRECTA

Realiza dos pasadas independientes sobre las cuatro raíces.

Cada pasada debe:

1. Verificar que la raíz existe y es un directorio real.
2. Verificar que la propia raíz no sea reparse point.
3. Recorrer todos sus subdirectorios físicamente contenidos.
4. Incluir todos los archivos regulares, incluso cachés, dependencias, telemetría y archivos aparentemente irrelevantes.
5. Excluir únicamente:
   - directorios;
   - enlaces simbólicos;
   - junctions;
   - reparse points;
   - archivos no regulares;
   - entradas que resuelvan fuera de su raíz.
6. No seguir ninguna entrada excluida.
7. Registrar solamente metadatos.
8. Producir conteos separados para ROOT-01, ROOT-02, ROOT-03 y ROOT-04.

Compara las dos pasadas mediante:

SOURCE_ROOT_ID
NORMALIZED_RELATIVE_PATH
FILE_SIZE
ENTRY_TYPE

Declara obligatoriamente:

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

La suma de los cuatro conteos por raíz debe coincidir exactamente con el conteo total de cada pasada.

No declares estabilidad únicamente porque coincidan los totales. Deben coincidir también el conjunto de rutas relativas, tamaños y tipos.

Si las pasadas difieren:

BLOCKER=SOURCE_ENUMERATION_NOT_STABLE
PERSISTENCE_STATUS=BLOCKED
VERDICT=REBASELINE_CORRECTION_BLOCKED

No persistas un nuevo CSV presentado como línea base válida.

# 6. CONTROL ESPECÍFICO DE ROOT-04

Comprueba directamente que el recorrido alcance los archivos regulares contenidos bajo:

ROOT-04\Cache

No leas su contenido.

Registra únicamente:

ROOT_04_CACHE_DIRECTORY_EXISTS=<YES|NO>
ROOT_04_CACHE_REGULAR_FILES_PASS_1=<cantidad>
ROOT_04_CACHE_REGULAR_FILES_PASS_2=<cantidad>
ROOT_04_CACHE_PASSES_MATCH=<YES|NO>
ROOT_04_FULL_RECURSIVE_ENUMERATION_CONFIRMED=<YES|NO>

Si ROOT-04 vuelve a producir únicamente 2 archivos o una cifra incompatible con la inspección física actual:

BLOCKER=ROOT_04_ENUMERATION_INCOMPLETE
VERDICT=REBASELINE_CORRECTION_BLOCKED

No fuerces el resultado a 1.304, porque la carpeta puede cambiar legítimamente entre ejecuciones.

# 7. REPRESENTACIÓN CANÓNICA

Crea nuevamente los cuatro artefactos canónicos dentro de una nueva intervención:

01_PHASE_1_ROOT_REGISTRY_v1.0.md
02_PHASE_1_SOURCE_ENUMERATION_v1.0.csv
03_PHASE_1_SOURCE_ENUMERATION_MANIFEST_v1.0.md
04_PHASE_1_CLASSIFICATION_CONTRACT_v1.0.md

La nueva intervención contendrá exactamente:

request.md
report.md
01_PHASE_1_ROOT_REGISTRY_v1.0.md
02_PHASE_1_SOURCE_ENUMERATION_v1.0.csv
03_PHASE_1_SOURCE_ENUMERATION_MANIFEST_v1.0.md
04_PHASE_1_CLASSIFICATION_CONTRACT_v1.0.md

No crees scripts persistentes, respaldos, archivos temporales, índices ni manifiestos adicionales.

El CSV conservará exactamente estas columnas:

BASELINE_ORDINAL
SOURCE_ROOT_ID
SAFE_RELATIVE_PATH
FILE_TYPE
SIZE_BYTES
ENUMERATION_STATUS
BATCH_ASSIGNMENT

Conserva las reglas originales:

UTF-8 sin BOM
terminación LF
rutas relativas con /
sin rutas absolutas
orden ROOT-01, ROOT-02, ROOT-03, ROOT-04
orden determinista dentro de cada raíz
ordinales consecutivos desde 1
lotes consecutivos de hasta 50
ENUMERATION_STATUS=ENUMERATED

La asignación de lotes no autoriza su ejecución.

# 8. CONTEOS DE REFERENCIA

Conserva separadamente:

HISTORICAL_EXPECTED_SOURCE_FILES=354
REJECTED_BASELINE_SOURCE_FILES=364
NEW_CORRECTED_BASELINE_SOURCE_FILES=<conteo físico nuevo>
DIFFERENCE_FROM_HISTORICAL_354=<entero>
DIFFERENCE_FROM_REJECTED_BASELINE_364=<entero>

Los valores 354, 364 y 1.304 son referencias de control. Ninguno debe utilizarse para ajustar artificialmente el resultado.

# 9. CONTRATO DE CLASIFICACIÓN

Reproduce el contrato aprobado de doce categorías sin ejecutar ninguna clasificación:

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

Conserva:

MINIMUM_FINAL_CLASSIFICATION_CONFIDENCE=0.90
COPY_AUTHORIZATION=NO
MOVE_AUTHORIZATION=NO
DELETE_AUTHORIZATION=NO

No clasifiques anticipadamente los archivos de ROOT-04 como caché, aunque estén ubicados bajo Cache. En esta intervención solo se construye el universo físico.

# 10. IDENTIFICADOR DE INTERVENCIÓN

Calcula físicamente el siguiente identificador disponible usando la fecha local real de ejecución:

CHATGPT-CODEX-YYYYMMDD-NNN

Considera únicamente carpetas directas cuyo nombre coincida exactamente con el patrón correspondiente a esa fecha.

No asumas el número de secuencia.
No rellenes huecos.
No reutilices identificadores.
Comprueba la ausencia de colisión inmediatamente antes de crear la carpeta.

# 11. INTEGRIDAD

Después de persistir:

1. Relee los seis archivos.
2. Verifica que existan exactamente seis.
3. Calcula el SHA-256 de cada archivo.
4. Registra en report.md los hashes de los otros cinco archivos.
5. El hash final de report.md debe calcularse después de cerrarlo y devolverse externamente en la respuesta de Codex.

No bloquees la corrección porque report.md no pueda contener de forma estable el hash de sus propios bytes.

Declara:

REPORT_SELF_HASH_REQUIRED=NO
REPORT_HASH_TO_BE_EXTERNALLY_RECORDED=YES
SELF_HASH_LIMITATION_IS_NOT_A_BASELINE_BLOCKER=YES

# 12. RESULTADO

Si las cuatro raíces se enumeran completamente, las dos pasadas coinciden y ROOT-04 queda incluido:

VERDICT=REBASELINE_CORRECTED_READY_FOR_CLAUDE_CODE_AUDIT
PERSISTENCE_STATUS=COMPLETED
PHASE_1_BASELINE_ACCEPTED=NO
BATCH_001_EXECUTED=NO
CLASSIFICATION_AUTHORIZATION_CONSUMED=NO
NEXT_STEP=CLAUDE_CODE_AUDITS_CORRECTED_PHASE_1_REBASELINE

Si existe inestabilidad, acceso incompleto o cualquier otra condición material:

VERDICT=REBASELINE_CORRECTION_BLOCKED
PERSISTENCE_STATUS=<BLOCKED|NOT_EXECUTED>
BATCH_001_EXECUTED=NO

# 13. CONFIRMACIÓN FINAL

Incluye en report.md:

THE_FOUR_OWNER_APPROVED_ROOTS_WERE_USED_WITHOUT_SUBSTITUTION
ROOT_04_WAS_ENUMERATED_RECURSIVELY_FROM_THE_LIVE_DIRECTORY
THE_INCOMPLETE_364_FILE_BASELINE_WAS_NOT_REUSED
THE_NEW_BASELINE_COUNT_WAS_NOT_ARTIFICIALLY_ADJUSTED
ONLY_REGULAR_FILE_METADATA_WAS_ENUMERATED
NO_SOURCE_FILE_CONTENT_WAS_READ
NO_SOURCE_CONTENT_HASH_WAS_CALCULATED
NO_SOURCE_FILE_WAS_CLASSIFIED
NO_SOURCE_FILE_WAS_COPIED_MOVED_MODIFIED_OR_DELETED
NO_SYMBOLIC_LINK_JUNCTION_OR_REPARSE_POINT_WAS_FOLLOWED
NO_PATH_OUTSIDE_THE_APPROVED_ROOTS_WAS_ACCESSED
NO_BATCH_001_CLASSIFICATION_WAS_EXECUTED
NO_EXISTING_INTERVENTION_WAS_MODIFIED_OR_RENAMED
ONLY_ONE_NEW_INTERVENTION_WITH_SIX_FILES_WAS_CREATED
NO_GIT_COMMAND_WAS_EXECUTED
NO_FILE_WAS_STAGED_COMMITTED_OR_PUSHED
NO_GITHUB_AUTHENTICATION_WAS_USED
OWNER_APPROVAL_WAS_NOT_REQUESTED_AGAIN

Devuelve el contenido completo de report.md y, fuera del archivo, el SHA-256 final calculado de report.md. Después detente.
