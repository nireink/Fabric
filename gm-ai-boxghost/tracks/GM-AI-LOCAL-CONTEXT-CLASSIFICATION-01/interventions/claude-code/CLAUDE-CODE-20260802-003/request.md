PEGAR EN: CLAUDE CODE — AUDITORÍA DEL REBASELINE DE LA FASE 1

```text
TRACK=GM-AI-LOCAL-CONTEXT-CLASSIFICATION-01
STEP=PHASE_1_REBASELINE_CONTRACT_AND_ENUMERATION_AUDIT
MODE=INDEPENDENT_READ_ONLY_AUDIT
AGENT=CLAUDE_CODE
TIMEZONE=America/Guayaquil

AUDIT_TARGET_INTERVENTION=CHATGPT-CODEX-20260802-003
OWNER_APPROVAL_ID=OA-GM-AI-LOCAL-CONTEXT-CLASSIFICATION-01-REBASELINE-01
OWNER_APPROVAL_STATUS=GRANTED
```

1. Objetivo
Audita independientemente la intervención:

```text
tracks\GM-AI-LOCAL-CONTEXT-CLASSIFICATION-01\interventions\chatgpt-codex\CHATGPT-CODEX-20260802-003
```

La intervención contiene exactamente:

```text
request.md
report.md
01_PHASE_1_ROOT_REGISTRY_v1.0.md
02_PHASE_1_SOURCE_ENUMERATION_v1.0.csv
03_PHASE_1_SOURCE_ENUMERATION_MANIFEST_v1.0.md
04_PHASE_1_CLASSIFICATION_CONTRACT_v1.0.md
```

No modifiques esos archivos.
2. Alcance autorizado
Puedes:

```text
READ_THE_SIX_INTERVENTION_ARTIFACTS
CALCULATE_SHA256_OF_THE_SIX_INTERVENTION_ARTIFACTS
VALIDATE_UTF8_NO_BOM_AND_LF
VALIDATE_CSV_SCHEMA_ORDER_AND_BATCH_ASSIGNMENTS
VALIDATE_ROOT_REGISTRY
VALIDATE_ENUMERATION_MANIFEST
VALIDATE_CLASSIFICATION_CONTRACT
USE_METADATA_ONLY_FOR_APPROVED_ROOT_VERIFICATION
COMPARE_CURRENT_METADATA_WITH_THE_FROZEN_ENUMERATION
```

No puedes:

```text
READ_SOURCE_FILE_CONTENT
CALCULATE_SOURCE_CONTENT_HASH
CLASSIFY_SOURCE_FILES
EXECUTE_BATCH_001
COPY_MOVE_MODIFY_OR_DELETE_SOURCE_FILES
FOLLOW_SYMBOLIC_LINKS_JUNCTIONS_OR_REPARSE_POINTS
ACCESS_OUTSIDE_THE_FOUR_APPROVED_ROOTS
MODIFY_PREVIOUS_INTERVENTIONS
RUN_GIT
STAGE_COMMIT_OR_PUSH
REQUEST_OWNER_APPROVAL_AGAIN
```

3. Raíces autoritativas

```text
ROOT-01=C:\Users\elbur\.codex\attachments
ROOT-02=C:\Users\elbur\.claude
ROOT-03=C:\Users\elbur\AppData\Local\Claude-3p
ROOT-04=C:\Users\elbur\AppData\Local\claude-cli-nodejs
```

No sustituyas ni amplíes estas rutas.
4. Verificaciones obligatorias
Verifica:

1. Que existan exactamente los seis archivos autorizados.
2. Que no se haya modificado ninguna intervención anterior.
3. Que el registro contenga exactamente las cuatro raíces aprobadas.
4. Que el CSV tenga exactamente estas columnas y orden:

```text
BASELINE_ORDINAL
SOURCE_ROOT_ID
SAFE_RELATIVE_PATH
FILE_TYPE
SIZE_BYTES
ENUMERATION_STATUS
BATCH_ASSIGNMENT
```

5. Que el CSV contenga 364 entradas de datos, ordinales consecutivos y ocho lotes de hasta 50 archivos.
6. Que no contenga rutas absolutas.
7. Que las rutas relativas sean seguras y estén asociadas exclusivamente con `ROOT-01..ROOT-04`.
8. Que el CSV use UTF-8 sin BOM y terminaciones LF.
9. Que su SHA-256 sea:

```text
1e6c89ea4f7959dc37738901fa0fc713d460f9cd51845dd6c236631e14016b96
```

10. Que el manifiesto declare correctamente:

```text
HISTORICAL_EXPECTED_SOURCE_FILES=354
NEW_BASELINE_SOURCE_FILES=364
COUNT_DIFFERENCE=10
COUNT_MATCHES_HISTORICAL_REFERENCE=NO
```

11. Que el contrato defina exactamente 12 categorías, incluya `EXCLUDE_PERSONAL_DATA` y aplique confianza mínima `0.90`.
12. Que ninguna categoría autorice copiar, mover o eliminar archivos.
13. Que `BATCH-001` no haya sido ejecutado.
14. Que no se hayan leído ni calculado hashes del contenido fuente.

5. Verificación independiente de hashes
Recalcula los SHA-256 de los seis artefactos.
Contrasta estos cinco valores registrados:

```text
REQUEST_MD_SHA256=a8dcdb963606f73372a32cf71a55feceb544482d9cce8f7610fbcd66cde57acf
ROOT_REGISTRY_SHA256=de5941d0204f289904b0cf0a352204b0b74d4477bb22a796d8923706e1d79b51
SOURCE_ENUMERATION_CSV_SHA256=1e6c89ea4f7959dc37738901fa0fc713d460f9cd51845dd6c236631e14016b96
ENUMERATION_MANIFEST_SHA256=bff87b6693449769077ad81681d7d9cacfc60da0be11ea22e3a732bacbc531f6
CLASSIFICATION_CONTRACT_SHA256=5c062430b9a91756f041258f315216d4a836c9d9157ff31ac7dc844d06343cc5
```

Calcula además el hash final de `report.md` y regístralo únicamente en tu propio informe de auditoría:

```text
AUDITED_REPORT_MD_SHA256=<valor calculado externamente>
REPORT_SELF_HASH_REQUIRED=NO
REPORT_HASH_EXTERNALLY_RECORDED=YES
```

No exijas que `report.md` contenga su propio hash. Esa condición es autorreferencial: agregar el hash al archivo cambiaría sus bytes y lo invalidaría.
Evalúa expresamente:

```text
SELF_HASH_REQUIREMENT_TECHNICALLY_SATISFIABLE=NO
SELF_HASH_LIMITATION_AFFECTS_ENUMERATION_INTEGRITY=<YES|NO>
SELF_HASH_LIMITATION_AFFECTS_CONTRACT_VALIDITY=<YES|NO>
EXTERNAL_AUDIT_HASH_PROVIDES_INTEGRITY_EVIDENCE=<YES|NO>
```

No rechaces automáticamente los cuatro contratos por esta única limitación. Determina si existe alguna inconformidad material independiente del auto-hash.
6. Resultado requerido
Tu informe debe separar:

```text
IMPLEMENTATION_FINDINGS
ENUMERATION_FINDINGS
CONTRACT_FINDINGS
HASH_FINDINGS
SECURITY_BOUNDARY_FINDINGS
SELF_HASH_SPECIFICATION_FINDING
```

Usa uno de estos veredictos:

```text
VERDICT=REBASELINE_ACCEPTED_WITH_EXTERNAL_REPORT_HASH
VERDICT=REBASELINE_REQUIRES_CORRECTION
VERDICT=REBASELINE_REJECTED
```

Solo usa `REBASELINE_REQUIRES_CORRECTION` o `REBASELINE_REJECTED` si detectas una inconformidad material distinta de que `report.md` no contenga el hash de sus propios bytes finales.
Si todo lo demás es conforme:

```text
VERDICT=REBASELINE_ACCEPTED_WITH_EXTERNAL_REPORT_HASH
PHASE_1_CONTRACTS_ACCEPTED=YES
BATCH_001_EXECUTED=NO
CLASSIFICATION_AUTHORIZATION_CONSUMED=NO
NEXT_STEP=CHATGPT_WORK_CONSOLIDATES_AUDIT_BEFORE_BATCH_001
```

Persiste únicamente tu intervención de auditoría conforme a la secuencia cronológica del directorio `claude-code`. No ejecutes Git y detente después de devolver el informe persistido.
