# BATCH-001 - Baselines y gobernanza de ingeniería

```text
Track: GYPPORT-KNOWLEDGE-CORPUS-DERIVED-STANDARDS-01
Step: BATCH-001-BASELINE-GOVERNANCE
Mode: KNOWLEDGE FIRST / BATCH PROCESSING
Agent: ChatGPT Work
Status: PROCESSED_WITH_UNRESOLVED_CONTRADICTIONS
DOCUMENT_STATUS=PROPOSED_PROCESSING_RECORD
REPOSITORY_PERSISTENCE=LOCAL_FABRIC_CHATGPT_CONFIRMED_ONLY
GYSTIGO_MODIFIED=false
FABRIC_KNOWLEDGE_MODIFIED=false
STAGING=false
COMMIT=false
PUSH=false
```

## 1. Estado de fuentes del lote

| Source ID | Fuente | Estado | Evidencia de identidad |
|---|---|---|---|
| SRC-PROMPT-2026-08-01-001 | Orden adjunta | PROCESSED | SHA-256 `7713F142...8E8A56` |
| SRC-ENG-STD-001 | Estándar maestro v1.1 | PROCESSED | SHA-256 `6F4A4EDC...178F8B`; Git target limpio |
| SRC-BACKEND-PB-001 | Playbook Crear producto v1.0 | PROCESSED | SHA-256 `6F91C060...B43CA`; Git target limpio |
| SRC-AI-GOV-001 | Orden de colaboración v1.0 | PROCESSED_WITH_WORKTREE_FINDING | SHA-256 `49EB24C0...61B5`; archivo modificado en worktree |

`PROCESSED` significa que el documento fue leído para el alcance doctrinal de
este lote. No significa que todas sus fuentes bibliográficas ya hayan sido
procesadas independientemente.

## 2. Síntesis y clasificación doctrinal

| Tesis | Clasificación | Razón |
|---|---|---|
| Arquitectura que busca hacerse prescindible | APPLY_WITH_CONTEXT | La meta válida es reducir carga y costo de cambio; no eliminar límites necesarios |
| Irreversibilidad como fuente de complejidad | ADAPT | Es factor principal, no explicación única; debe combinarse con datos, contratos, seguridad y operación |
| Contratos antes que implementaciones | APPLY_WITH_CONTEXT | Solo en fronteras reales, no una interfaz por clase |
| Adaptadores para dependencias reemplazables | APPLY_WITH_CONTEXT | Requiere proveedor/frontera/costo de sustitución demostrable |
| LEAN no significa improvisación | APPLY | Coincide con solución mínima completa, seguridad y evidencia |
| Preservar opciones reduce costo de cambio | ADAPT | Mantener opciones también cuesta; se justifica por probabilidad y costo real de cambio |

Resultado: la doctrina propuesta converge ampliamente con el estándar maestro
actual. La principal tarea no es añadir más reglas generales, sino redistribuir
propiedad especializada y alinear referencias de gobernanza.

## 3. Catálogo de Unidades de Conocimiento

### KN-000028 - Autoridad y propiedad normativa única

```text
DOMAIN=Governance
SOURCE_DOC_IDS=SRC-ENG-STD-001,SRC-BACKEND-PB-001,SRC-PROMPT-2026-08-01-001
SOURCE_LOCATION=standard 1:107-129; playbook 1:18-34; prompt 90-107
EVIDENCE_TYPE=SOURCE_EVIDENCE
KNOWLEDGE_STATEMENT=Una regla debe tener un propietario documental único y los documentos subordinados deben referenciarla sin duplicarla.
CONTEXT=Jerarquía entre gobernanza, estándar maestro, estándar especializado y playbooks.
LIMITATIONS=La autoridad superior sigue perteneciendo a la gobernanza arquitectónica aprobada.
CONTRADICTIONS=Ninguna material entre las tres fuentes.
GYPPORT_APPLICABILITY=APPLY
CLASSIFICATION=APPLY
TARGET_DOCUMENT=Todos los seis documentos
TARGET_SECTION=Relación con otros documentos
NORMATIVE_STRENGTH=MUST
CONFIDENCE=VERY_HIGH
STATUS=PROPOSED_KNOWLEDGE
```

### KN-000029 - Solución mínima completa

```text
DOMAIN=Engineering
SOURCE_DOC_IDS=SRC-ENG-STD-001,SRC-PROMPT-2026-08-01-001
SOURCE_LOCATION=standard 1:259-308; prompt 38-59,193-212
EVIDENCE_TYPE=SOURCE_EVIDENCE
KNOWLEDGE_STATEMENT=Cada incremento debe ser el menor cambio que resuelva el caso aprobado de extremo a extremo sin omitir seguridad, datos, contrato, prueba o rollback aplicables.
CONTEXT=LEAN y presupuesto de complejidad.
LIMITATIONS=Mínimo no equivale a menor número de archivos o líneas.
CONTRADICTIONS=Ninguna.
GYPPORT_APPLICABILITY=APPLY
CLASSIFICATION=APPLY
TARGET_DOCUMENT=GYPPORT_AI_DEVELOPER_ENGINEERING_STANDARD_v1.1.md
TARGET_SECTION=Solución mínima y complejidad
NORMATIVE_STRENGTH=MUST
CONFIDENCE=VERY_HIGH
STATUS=PROPOSED_KNOWLEDGE
```

### KN-000030 - Abstracción justificada por evidencia

```text
DOMAIN=Engineering
SOURCE_DOC_IDS=SRC-ENG-STD-001,SRC-PROMPT-2026-08-01-001
SOURCE_LOCATION=standard 1:310-320,1317-1356; prompt 157-192,263-323
EVIDENCE_TYPE=SOURCE_EVIDENCE
KNOWLEDGE_STATEMENT=Una abstracción o patrón solo se justifica por una frontera, variación, sustitución, repetición semántica o riesgo real; no por plantilla ni prestigio.
CONTEXT=KISS, YAGNI, contratos y patrones.
LIMITATIONS=Una implementación única puede requerir contrato si protege una frontera costosa.
CONTRADICTIONS=Ninguna.
GYPPORT_APPLICABILITY=APPLY_WITH_CONTEXT
CLASSIFICATION=APPLY_WITH_CONTEXT
TARGET_DOCUMENT=GYPPORT_AI_DEVELOPER_ENGINEERING_STANDARD_v1.1.md
TARGET_SECTION=Abstracción, contratos y patrones
NORMATIVE_STRENGTH=MUST_NOT
CONFIDENCE=VERY_HIGH
STATUS=PROPOSED_KNOWLEDGE
```

### KN-000031 - Contratos en fronteras reales

```text
DOMAIN=Architecture
SOURCE_DOC_IDS=SRC-ENG-STD-001,SRC-PROMPT-2026-08-01-001
SOURCE_LOCATION=standard 1:342-346,438-457; prompt 157-192
EVIDENCE_TYPE=SOURCE_EVIDENCE
KNOWLEDGE_STATEMENT=GYPPORT debe usar contratos públicos pequeños en límites reales y mantener reemplazables las implementaciones, sin crear una interfaz por clase.
CONTEXT=Módulos, red, proveedores e infraestructura.
LIMITATIONS=No aplica automáticamente a dependencias triviales, locales y estables.
CONTRADICTIONS=Ninguna.
GYPPORT_APPLICABILITY=APPLY_WITH_CONTEXT
CLASSIFICATION=APPLY_WITH_CONTEXT
TARGET_DOCUMENT=GYPPORT_AI_DEVELOPER_ENGINEERING_STANDARD_v1.1.md
TARGET_SECTION=Contratos, límites y adaptadores
NORMATIVE_STRENGTH=MUST
CONFIDENCE=HIGH
STATUS=PROPOSED_KNOWLEDGE
```

### KN-000032 - Decisiones según costo de reversión

```text
DOMAIN=Architecture
SOURCE_DOC_IDS=SRC-PROMPT-2026-08-01-001,SRC-ENG-STD-001
SOURCE_LOCATION=prompt 133-156,213-229; standard 1:479-508,965-984
EVIDENCE_TYPE=INTERPRETATION
KNOWLEDGE_STATEMENT=Las decisiones deben clasificarse como reversibles, costosas de revertir o estructurales y exigir evidencia proporcional sobre contratos, datos, seguridad, migración y rollback.
CONTEXT=Gestión de opciones y evolución.
LIMITATIONS=La clasificación exacta requiere contexto de cada decisión.
CONTRADICTIONS=El estándar actual trata reversibilidad, pero no usa de forma uniforme las tres categorías del prompt.
GYPPORT_APPLICABILITY=ADAPT
CLASSIFICATION=ADAPT
TARGET_DOCUMENT=GYPPORT_AI_DEVELOPER_ENGINEERING_STANDARD_v1.1.md
TARGET_SECTION=Decisiones arquitectónicas y reversibilidad
NORMATIVE_STRENGTH=SHOULD
CONFIDENCE=HIGH
STATUS=PROPOSED_KNOWLEDGE
```

### KN-000033 - Trazabilidad de requisito a evidencia

```text
DOMAIN=Engineering
SOURCE_DOC_IDS=SRC-ENG-STD-001,SRC-PROMPT-2026-08-01-001
SOURCE_LOCATION=standard 1:174-236; prompt 393-399,449-474
EVIDENCE_TYPE=SOURCE_EVIDENCE
KNOWLEDGE_STATEMENT=Cada incremento debe enlazar decisión, requisito, regla o contrato, implementación, prueba y evidencia de aceptación.
CONTEXT=Claridad de producto y verificación.
LIMITATIONS=La trazabilidad puede residir en artefactos existentes; no exige un documento por enlace.
CONTRADICTIONS=Ninguna.
GYPPORT_APPLICABILITY=APPLY
CLASSIFICATION=APPLY
TARGET_DOCUMENT=GYPPORT_AI_DEVELOPER_ENGINEERING_STANDARD_v1.1.md
TARGET_SECTION=Requisitos y trazabilidad
NORMATIVE_STRENGTH=MUST
CONFIDENCE=VERY_HIGH
STATUS=PROPOSED_KNOWLEDGE
```

### KN-000034 - Preflight antes de crear

```text
DOMAIN=Engineering Process
SOURCE_DOC_IDS=SRC-ENG-STD-001,SRC-BACKEND-PB-001,SRC-PROMPT-2026-08-01-001
SOURCE_LOCATION=standard 1:238-257; playbook 1:106-130; prompt 400-430,521-537
EVIDENCE_TYPE=SOURCE_EVIDENCE
KNOWLEDGE_STATEMENT=Antes de diseñar o crear, se debe verificar propietario, ubicación, contratos, stack, datos, seguridad, pruebas, Toolchain y alcance cerrado.
CONTEXT=Prevención de duplicación y de ownership paralelo.
LIMITATIONS=Los detalles varían por tipo de componente.
CONTRADICTIONS=Ninguna.
GYPPORT_APPLICABILITY=APPLY
CLASSIFICATION=APPLY
TARGET_DOCUMENT=GYPPORT_PLAYBOOK_IMPLEMENT_SOFTWARE_COMPONENT_v1.0.md
TARGET_SECTION=Comprensión, propiedad y reutilización
NORMATIVE_STRENGTH=MUST
CONFIDENCE=VERY_HIGH
STATUS=PROPOSED_KNOWLEDGE
```

### KN-000035 - Reutilización con clasificación explícita

```text
DOMAIN=Engineering Process
SOURCE_DOC_IDS=SRC-ENG-STD-001,SRC-PROMPT-2026-08-01-001
SOURCE_LOCATION=standard 1:889-909; prompt 407-420
EVIDENCE_TYPE=RECOMMENDATION
KNOWLEDGE_STATEMENT=La evaluación previa debe clasificar una capacidad existente como REUSE, EXTEND, ADAPT, REFACTOR, CREATE o DO_NOT_REUSE según semántica y acoplamiento.
CONTEXT=Implementación general.
LIMITATIONS=La etiqueta no sustituye la justificación.
CONTRADICTIONS=Ninguna.
GYPPORT_APPLICABILITY=APPLY
CLASSIFICATION=APPLY
TARGET_DOCUMENT=GYPPORT_PLAYBOOK_IMPLEMENT_SOFTWARE_COMPONENT_v1.0.md
TARGET_SECTION=Fase de reutilización
NORMATIVE_STRENGTH=MUST
CONFIDENCE=HIGH
STATUS=PROPOSED_KNOWLEDGE
```

### KN-000036 - Datos desde invariantes y ownership

```text
DOMAIN=Database
SOURCE_DOC_IDS=SRC-ENG-STD-001,SRC-BACKEND-PB-001,SRC-PROMPT-2026-08-01-001
SOURCE_LOCATION=standard 1:621-637; playbook 1:150-164; prompt 561-624
EVIDENCE_TYPE=SOURCE_EVIDENCE
KNOWLEDGE_STATEMENT=El diseño de datos parte de procesos, invariantes, cardinalidad, ciclo de vida, tenant y propietario canónico, no de campos de una pantalla.
CONTEXT=Persistencia modular.
LIMITATIONS=El modelo físico requiere evidencia del motor y carga reales.
CONTRADICTIONS=Ninguna.
GYPPORT_APPLICABILITY=APPLY
CLASSIFICATION=APPLY
TARGET_DOCUMENT=GYPPORT_DATABASE_ENGINEERING_STANDARD_v1.0.md
TARGET_SECTION=Propiedad, modelos y relaciones
NORMATIVE_STRENGTH=MUST
CONFIDENCE=VERY_HIGH
STATUS=PROPOSED_KNOWLEDGE
```

### KN-000037 - Normalización predeterminada

```text
DOMAIN=Database
SOURCE_DOC_IDS=SRC-ENG-STD-001,SRC-PROMPT-2026-08-01-001
SOURCE_LOCATION=standard 1:638-660; prompt 625-646
EVIDENCE_TYPE=SOURCE_EVIDENCE
KNOWLEDGE_STATEMENT=La persistencia relacional debe justificar dependencias funcionales y orientarse normalmente a 3FN o BCNF, con unión sin pérdida y preservación suficiente de dependencias.
CONTEXT=Prevención de redundancia y anomalías.
LIMITATIONS=BCNF no es una regla automática para toda tabla.
CONTRADICTIONS=Ninguna.
GYPPORT_APPLICABILITY=APPLY_WITH_CONTEXT
CLASSIFICATION=APPLY_WITH_CONTEXT
TARGET_DOCUMENT=GYPPORT_DATABASE_ENGINEERING_STANDARD_v1.0.md
TARGET_SECTION=Normalización
NORMATIVE_STRENGTH=SHOULD
CONFIDENCE=VERY_HIGH
STATUS=PROPOSED_KNOWLEDGE
```

### KN-000038 - Desnormalización con evidencia y propietario

```text
DOMAIN=Database
SOURCE_DOC_IDS=SRC-ENG-STD-001,SRC-PROMPT-2026-08-01-001
SOURCE_LOCATION=standard 1:651-659; prompt 638-646
EVIDENCE_TYPE=SOURCE_EVIDENCE
KNOWLEDGE_STATEMENT=Desnormalizar exige problema medido, alternativa evaluada, propietario de consistencia, pruebas, observabilidad y reconciliación o reconstrucción.
CONTEXT=Optimización física.
LIMITATIONS=El requisito de ADR del estándar actual debe conservarse o decidirse expresamente.
CONTRADICTIONS=El prompt no menciona ADR en su lista, el estándar sí lo exige.
GYPPORT_APPLICABILITY=APPLY_WITH_CONTEXT
CLASSIFICATION=APPLY_WITH_CONTEXT
TARGET_DOCUMENT=GYPPORT_DATABASE_ENGINEERING_STANDARD_v1.0.md
TARGET_SECTION=Desnormalización y excepciones
NORMATIVE_STRENGTH=MUST
CONFIDENCE=HIGH
STATUS=PROPOSED_KNOWLEDGE
```

### KN-000039 - Unidad transaccional y concurrencia

```text
DOMAIN=Database
SOURCE_DOC_IDS=SRC-ENG-STD-001,SRC-BACKEND-PB-001,SRC-PROMPT-2026-08-01-001
SOURCE_LOCATION=standard 1:671-697; playbook 1:166-198; prompt 657-671,733-751
EVIDENCE_TYPE=SOURCE_EVIDENCE
KNOWLEDGE_STATEMENT=Las invariantes deben protegerse mediante unidad transaccional breve, constraints, aislamiento, concurrencia explícita, idempotencia aplicable y pruebas de rollback/carrera.
CONTEXT=Consistencia multitenant.
LIMITATIONS=El mecanismo concreto depende de motor, contención y riesgo.
CONTRADICTIONS=Ninguna.
GYPPORT_APPLICABILITY=APPLY
CLASSIFICATION=APPLY
TARGET_DOCUMENT=GYPPORT_DATABASE_ENGINEERING_STANDARD_v1.0.md
TARGET_SECTION=Transacciones y concurrencia
NORMATIVE_STRENGTH=MUST
CONFIDENCE=VERY_HIGH
STATUS=PROPOSED_KNOWLEDGE
```

### KN-000040 - Aislamiento multitenant verificable

```text
DOMAIN=Security/Database
SOURCE_DOC_IDS=SRC-ENG-STD-001,SRC-BACKEND-PB-001,SRC-PROMPT-2026-08-01-001
SOURCE_LOCATION=standard 1:718-728; playbook 1:222-242; prompt 600-624,743-751
EVIDENCE_TYPE=SOURCE_EVIDENCE
KNOWLEDGE_STATEMENT=El tenant se resuelve desde identidad autenticada y debe aplicarse a lectura, escritura, autorización, relaciones, unicidad, índices y pruebas negativas.
CONTEXT=ERP SaaS de esquema compartido.
LIMITATIONS=La estrategia física exacta debe verificarse contra el sistema real.
CONTRADICTIONS=Ninguna.
GYPPORT_APPLICABILITY=APPLY
CLASSIFICATION=APPLY
TARGET_DOCUMENT=GYPPORT_DATABASE_ENGINEERING_STANDARD_v1.0.md
TARGET_SECTION=Multitenancy
NORMATIVE_STRENGTH=MUST
CONFIDENCE=VERY_HIGH
STATUS=PROPOSED_KNOWLEDGE
```

### KN-000041 - Contrato HTTP antes de detalles internos

```text
DOMAIN=Backend/API
SOURCE_DOC_IDS=SRC-ENG-STD-001,SRC-BACKEND-PB-001,SRC-PROMPT-2026-08-01-001
SOURCE_LOCATION=standard 1:730-772; playbook 1:200-220; prompt 497-537
EVIDENCE_TYPE=SOURCE_EVIDENCE
KNOWLEDGE_STATEMENT=Una API debe definir entrada, salida, errores, autorización, tenant, compatibilidad e idempotencia aplicable, usando semántica HTTP, OpenAPI y Problem Details sin exponer modelos internos.
CONTEXT=Backend/API REST actual.
LIMITATIONS=OpenAPI aplica cuando existe contrato HTTP y según gobernanza vigente.
CONTRADICTIONS=Ninguna material.
GYPPORT_APPLICABILITY=APPLY
CLASSIFICATION=APPLY
TARGET_DOCUMENT=GYPPORT_PLAYBOOK_CREATE_PRODUCT_BACKEND_API_v1.0.md
TARGET_SECTION=Contrato API
NORMATIVE_STRENGTH=MUST
CONFIDENCE=VERY_HIGH
STATUS=PROPOSED_KNOWLEDGE
```

### KN-000042 - Seguridad por función, objeto, propiedad y tenant

```text
DOMAIN=Security
SOURCE_DOC_IDS=SRC-ENG-STD-001,SRC-BACKEND-PB-001,SRC-PROMPT-2026-08-01-001
SOURCE_LOCATION=standard 1:774-836; playbook 1:222-242; prompt 348-363,497-520
EVIDENCE_TYPE=SOURCE_EVIDENCE
KNOWLEDGE_STATEMENT=La autorización del endpoint no sustituye la autorización de función, objeto, propiedad y tenant; deben existir defaults seguros, entradas limitadas, SQL parametrizado, logs seguros y pruebas negativas.
CONTEXT=Seguridad transversal y Backend/API.
LIMITATIONS=Los controles específicos dependen de amenazas y superficie.
CONTRADICTIONS=Ninguna.
GYPPORT_APPLICABILITY=APPLY
CLASSIFICATION=APPLY
TARGET_DOCUMENT=GYPPORT_AI_DEVELOPER_ENGINEERING_STANDARD_v1.1.md
TARGET_SECTION=Seguridad transversal
NORMATIVE_STRENGTH=MUST
CONFIDENCE=VERY_HIGH
STATUS=PROPOSED_KNOWLEDGE
```

### KN-000043 - Dependencias externas reemplazables

```text
DOMAIN=Architecture/Integration
SOURCE_DOC_IDS=SRC-ENG-STD-001,SRC-PROMPT-2026-08-01-001
SOURCE_LOCATION=standard 1:438-457,758-772,812-826; prompt 183-192
EVIDENCE_TYPE=INTERPRETATION
KNOWLEDGE_STATEMENT=Una dependencia externa significativa debe quedar detrás de un contrato de necesidad GYPPORT y un adaptador que normalice datos, errores y configuración, con estrategia de sustitución.
CONTEXT=Proveedores, SDK e infraestructura.
LIMITATIONS=No se crea adaptador cuando la dependencia es trivial y el aislamiento no aporta valor.
CONTRADICTIONS=Ninguna.
GYPPORT_APPLICABILITY=APPLY_WITH_CONTEXT
CLASSIFICATION=APPLY_WITH_CONTEXT
TARGET_DOCUMENT=GYPPORT_AI_DEVELOPER_ENGINEERING_STANDARD_v1.1.md
TARGET_SECTION=Límites y cadena de suministro
NORMATIVE_STRENGTH=SHOULD
CONFIDENCE=HIGH
STATUS=PROPOSED_KNOWLEDGE
```

### KN-000044 - Pruebas por comportamiento y riesgo

```text
DOMAIN=Quality
SOURCE_DOC_IDS=SRC-ENG-STD-001,SRC-BACKEND-PB-001,SRC-PROMPT-2026-08-01-001
SOURCE_LOCATION=standard 1:911-948; playbook 1:261-289; prompt 440-474,743-751
EVIDENCE_TYPE=SOURCE_EVIDENCE
KNOWLEDGE_STATEMENT=Las pruebas deben demostrar comportamientos, contratos, invariantes, seguridad, tenant, migración, concurrencia y rendimiento aplicables; un porcentaje aislado no sustituye evidencia.
CONTEXT=Verificación proporcional al riesgo.
LIMITATIONS=No todas las categorías aplican a cada incremento.
CONTRADICTIONS=Ninguna.
GYPPORT_APPLICABILITY=APPLY
CLASSIFICATION=APPLY
TARGET_DOCUMENT=GYPPORT_AI_DEVELOPER_ENGINEERING_STANDARD_v1.1.md
TARGET_SECTION=Pruebas y evidencia
NORMATIVE_STRENGTH=MUST
CONFIDENCE=VERY_HIGH
STATUS=PROPOSED_KNOWLEDGE
```

### KN-000045 - Revisión independiente y separación de funciones

```text
DOMAIN=Governance/Quality
SOURCE_DOC_IDS=SRC-ENG-STD-001,SRC-AI-GOV-001
SOURCE_LOCATION=standard 1:950-963,1025-1037; collaboration sections 2-5
EVIDENCE_TYPE=SOURCE_EVIDENCE
KNOWLEDGE_STATEMENT=La validación propia no sustituye auditoría independiente; propuesta, verificación, aprobación, implementación y auditoría son estados separados.
CONTEXT=Flujo multiagente.
LIMITATIONS=El flujo detallado pertenece a la norma de colaboración, no al estándar maestro.
CONTRADICTIONS=La sección 21 del estándar resume un flujo anterior/incompleto frente a la norma aprobada.
GYPPORT_APPLICABILITY=APPLY
CLASSIFICATION=MODIFY_AND_CROSS_REFERENCE
TARGET_DOCUMENT=GYPPORT_AI_DEVELOPER_ENGINEERING_STANDARD_v1.1.md
TARGET_SECTION=Colaboración y revisión
NORMATIVE_STRENGTH=MUST
CONFIDENCE=VERY_HIGH
STATUS=PROPOSED_KNOWLEDGE
```

### KN-000046 - Detención al cumplir o al encontrar bloqueo

```text
DOMAIN=Engineering Process
SOURCE_DOC_IDS=SRC-ENG-STD-001,SRC-BACKEND-PB-001,SRC-PROMPT-2026-08-01-001
SOURCE_LOCATION=standard 1:1117-1135; playbook 1:291-307; prompt 467-486
EVIDENCE_TYPE=SOURCE_EVIDENCE
KNOWLEDGE_STATEMENT=El trabajo se detiene al cumplir el alcance y evidencia aprobados, o antes si falta ownership, hay contradicción material, riesgo tenant, migración no segura o ampliación no autorizada.
CONTEXT=Control de alcance y anti-sobreingeniería.
LIMITATIONS=Un hallazgo no bloqueante se registra para otro paso.
CONTRADICTIONS=Ninguna.
GYPPORT_APPLICABILITY=APPLY
CLASSIFICATION=APPLY
TARGET_DOCUMENT=GYPPORT_PLAYBOOK_IMPLEMENT_SOFTWARE_COMPONENT_v1.0.md
TARGET_SECTION=Condiciones de detención
NORMATIVE_STRENGTH=MUST
CONFIDENCE=VERY_HIGH
STATUS=PROPOSED_KNOWLEDGE
```

### KN-000047 - Unicidad concurrente en la base

```text
DOMAIN=Backend/Database
SOURCE_DOC_IDS=SRC-BACKEND-PB-001,SRC-ENG-STD-001
SOURCE_LOCATION=playbook 1:166-184; standard 1:661-697
EVIDENCE_TYPE=SOURCE_EVIDENCE
KNOWLEDGE_STATEMENT=Una invariante de unicidad concurrente debe residir en un constraint con alcance correcto; la comprobación previa solo mejora experiencia y no sustituye la garantía.
CONTEXT=SKU como caso especializado.
LIMITATIONS=No se prescribe (tenant_id,sku) sin validar modelo y alcance.
CONTRADICTIONS=Ninguna.
GYPPORT_APPLICABILITY=APPLY_WITH_CONTEXT
CLASSIFICATION=APPLY_WITH_CONTEXT
TARGET_DOCUMENT=GYPPORT_PLAYBOOK_CREATE_PRODUCT_BACKEND_API_v1.0.md
TARGET_SECTION=Persistencia y concurrencia
NORMATIVE_STRENGTH=MUST
CONFIDENCE=VERY_HIGH
STATUS=PROPOSED_KNOWLEDGE
```

### KN-000048 - Backend actual no equivale a cierre tecnológico

```text
DOMAIN=Technology Governance
SOURCE_DOC_IDS=SRC-PROMPT-2026-08-01-001,SRC-ENG-STD-001
SOURCE_LOCATION=prompt 538-547; standard 1:164-172,238-255
EVIDENCE_TYPE=INTERPRETATION
KNOWLEDGE_STATEMENT=Java, Spring Boot, JdbcTemplate, REST, MySQL y Flyway son decisiones actuales sujetas a verificación; no constituyen prohibición permanente de otras tecnologías.
CONTEXT=Apertura tecnológica sin neutralidad ficticia.
LIMITATIONS=La versión real del stack no fue validada contra código en esta fase.
CONTRADICTIONS=El prompt informa Spring Boot 3.x; la versión física real queda UNRESOLVED.
GYPPORT_APPLICABILITY=APPLY_WITH_CONTEXT
CLASSIFICATION=UNRESOLVED
TARGET_DOCUMENT=GYPPORT_PLAYBOOK_CREATE_PRODUCT_BACKEND_API_v1.0.md
TARGET_SECTION=Contexto tecnológico actual
NORMATIVE_STRENGTH=SHOULD
CONFIDENCE=MEDIUM
STATUS=PENDING_VALIDATION
```

### KN-000049 - Migraciones inmutables y evolución compatible

```text
DOMAIN=Database
SOURCE_DOC_IDS=SRC-ENG-STD-001,SRC-PROMPT-2026-08-01-001
SOURCE_LOCATION=standard 1:705-716; prompt 657-671
EVIDENCE_TYPE=SOURCE_EVIDENCE
KNOWLEDGE_STATEMENT=Las migraciones aplicadas no se editan; la evolución usa cambios incrementales, precondiciones, validación, compatibilidad y rollback o roll-forward seguro.
CONTEXT=Evolución de esquema y datos.
LIMITATIONS=El procedimiento detallado pertenece al playbook de base modular.
CONTRADICTIONS=Ninguna.
GYPPORT_APPLICABILITY=APPLY
CLASSIFICATION=APPLY
TARGET_DOCUMENT=GYPPORT_DATABASE_ENGINEERING_STANDARD_v1.0.md
TARGET_SECTION=Migraciones
NORMATIVE_STRENGTH=MUST
CONFIDENCE=VERY_HIGH
STATUS=PROPOSED_KNOWLEDGE
```

### KN-000050 - Propiedad especializada de datos

```text
DOMAIN=Document Architecture
SOURCE_DOC_IDS=SRC-ENG-STD-001,SRC-PROMPT-2026-08-01-001
SOURCE_LOCATION=standard 1:621-728; prompt 90-107,561-678
EVIDENCE_TYPE=RECOMMENDATION
KNOWLEDGE_STATEMENT=El estándar maestro debe conservar principios generales de datos y referenciar al estándar especializado, que poseerá modelado, normalización, índices, migraciones y operación detallada.
CONTEXT=Extracción sin duplicación normativa.
LIMITATIONS=Requiere decisión conceptual antes de modificar el estándar aprobado.
CONTRADICTIONS=El estándar maestro actual posee detalles que el nuevo mapa asigna al estándar de base de datos.
GYPPORT_APPLICABILITY=ADAPT
CLASSIFICATION=MOVE_AND_CROSS_REFERENCE
TARGET_DOCUMENT=GYPPORT_DATABASE_ENGINEERING_STANDARD_v1.0.md
TARGET_SECTION=Todo el estándar especializado
NORMATIVE_STRENGTH=MUST
CONFIDENCE=HIGH
STATUS=PROPOSED_KNOWLEDGE
```

### KN-000051 - Identidad del playbook Backend/API no resuelta

```text
DOMAIN=Document Governance
SOURCE_DOC_IDS=SRC-BACKEND-PB-001,SRC-PROMPT-2026-08-01-001
SOURCE_LOCATION=playbook 1:18-34,64-104; prompt 69-89,487-560
EVIDENCE_TYPE=CONTRADICTION
KNOWLEDGE_STATEMENT=El archivo v1.0 existente es la fuente exclusiva de Crear producto, mientras el prompt asigna al mismo nombre un procedimiento Backend/API general.
CONTEXT=Versionado, alcance y ownership documental.
LIMITATIONS=No puede resolverse sin decisión de Eduardo y estrategia de compatibilidad/supersesión.
CONTRADICTIONS=Especializado en Crear producto versus general para producto, servicio o endpoint.
GYPPORT_APPLICABILITY=UNRESOLVED
CLASSIFICATION=UNRESOLVED
TARGET_DOCUMENT=GYPPORT_PLAYBOOK_CREATE_PRODUCT_BACKEND_API_v1.0.md
TARGET_SECTION=Identidad, alcance y compatibilidad
NORMATIVE_STRENGTH=MUST
CONFIDENCE=VERY_HIGH
STATUS=OPEN_DECISION
```

### KN-000052 - Versiones aprobadas no se sobrescriben como propuestas

```text
DOMAIN=Document Governance
SOURCE_DOC_IDS=SRC-ENG-STD-001,SRC-BACKEND-PB-001,SRC-PROMPT-2026-08-01-001
SOURCE_LOCATION=standard 1:1-15,1402-1414; playbook 1:1-16; prompt 20-37,1048-1070
EVIDENCE_TYPE=CONTRADICTION
KNOWLEDGE_STATEMENT=Un borrador PROPOSED no debe reemplazar silenciosamente un documento APPROVED con el mismo nombre y versión.
CONTEXT=Integridad normativa y evolución documental.
LIMITATIONS=El nombre o versión de los futuros borradores requiere decisión.
CONTRADICTIONS=El estado de partida del prompt no coincide con los archivos físicos aprobados.
GYPPORT_APPLICABILITY=APPLY
CLASSIFICATION=UNRESOLVED
TARGET_DOCUMENT=Todos los documentos existentes afectados
TARGET_SECTION=Identificación e historial
NORMATIVE_STRENGTH=MUST_NOT
CONFIDENCE=VERY_HIGH
STATUS=OPEN_DECISION
```

## 4. Matriz fuente -> KN

| Fuente | KN |
|---|---|
| SRC-PROMPT-2026-08-01-001 | 028-052 excepto 047 |
| SRC-ENG-STD-001 | 028-050, 052 |
| SRC-BACKEND-PB-001 | 028, 034, 036, 039-042, 044, 046-047, 051-052 |
| SRC-AI-GOV-001 | 045 |

## 5. Matriz KN -> documento

| Documento | KN principales |
|---|---|
| Estándar maestro | 028-033, 042-045, 052 |
| Playbook de componente | 034-035, 044-046 |
| Playbook Backend/API | 034, 039-042, 046-048, 051-052 |
| Estándar de base de datos | 036-040, 049-050 |
| Playbook de base modular | 034, 036-040, 046, 049 |
| Estándar UI/UX | 028-035, 042-046 como referencias transversales; contenido propio pendiente |

## 6. Matriz regla -> propietario

| Regla | Propietario | No duplicar en |
|---|---|---|
| Solución mínima, abstracción, contratos, seguridad general | Estándar maestro | Cinco documentos subordinados |
| Flujo general de implementación | Playbook de componente | Playbooks especializados completos |
| Contrato y procedimiento Backend/API | Playbook Backend/API | Estándar maestro y DB |
| Modelado, integridad, normalización, multitenancy físico | Estándar DB | Backend y estándar maestro |
| Pasos de diseño/migración/prueba de DB | Playbook DB modular | Estándar DB |
| UX, UI, accesibilidad, tokens | Estándar UI/UX | Estándar maestro |
| Colaboración multiagente | Norma de colaboración existente | Los seis documentos |

## 7. Matriz de duplicados y variantes

| Elemento | Tipo | Tratamiento |
|---|---|---|
| Anexo A del estándar vs playbook Crear producto | Duplicado histórico controlado | Conservar `SUPERSEDED`; no copiar en nuevas propuestas |
| Sección 11 DB del estándar vs futuro estándar DB | Solapamiento normativo | Mover detalle; conservar principios y referencia |
| Sección 12 API vs playbook Backend/API | Solapamiento parcial | Maestro conserva reglas transversales; playbook posee procedimiento |
| Sección 21 IA vs norma de colaboración | Variante conflictiva | Reemplazar contenido futuro por referencia canónica |
| Checklist general vs checklists especializados | Repetición necesaria limitada | Referenciar general y añadir solo riesgos del dominio |

## 8. Matriz de contradicciones

| ID | Contradicción | Severidad | Estado |
|---|---|---|---|
| CON-001 | Baselines `UNRESOLVED` en prompt vs `APPROVED` físicamente | Alta | OPEN |
| CON-002 | CP-0002 integral declarado vs no localizado | Alta | OPEN |
| CON-003 | Playbook Crear producto específico vs playbook Backend/API general con mismo ID | Crítica | OPEN_OWNER_DECISION |
| CON-004 | Flujo IA del estándar vs orden de colaboración aprobado | Alta | OPEN_RECONCILIATION |
| CON-005 | Spring Boot 3.x informado vs stack real no validado | Media | PENDING_CODE_VALIDATION |
| CON-006 | Detalle DB en maestro vs propiedad exclusiva especializada propuesta | Alta | OPEN_CONCEPTUAL_REVIEW |

## 9. Matriz de decisiones y reversibilidad

| Decisión | Clase | Razón |
|---|---|---|
| Redacción de un borrador aislado en `.chatgpt` | Reversible | No altera autoridad ni consumidores |
| Cambiar referencias cruzadas | Costosa de revertir | Afecta navegación normativa y agentes |
| Repurpose del playbook Backend/API v1.0 | Estructural | Cambia alcance de una norma aprobada |
| Extraer reglas DB del maestro | Estructural | Cambia ownership normativo y precedencia |
| Añadir clasificación de reversibilidad al maestro | Reversible/costosa según fuerza | Puede agregarse sin eliminar doctrina, pero exige revisión |
| Modificar versión o estado aprobado | Estructural | Requiere decisión y trazabilidad formal |

## 10. Matriz de cobertura por dominio

| Dominio | Cobertura del lote | Confianza | Pendiente principal |
|---|---:|---|---|
| Ingeniería general | Alta | Muy alta | Contraste independiente con libros |
| Implementación general | Media | Alta | El playbook objetivo aún no existe |
| Backend/API | Alta para Crear producto; media general | Muy alta | Resolver identidad y generalización |
| Base de datos | Media-alta normativa | Alta | Procesar fuentes DB y corpus histórico |
| Playbook DB modular | Baja | Media | Procesamiento de fuentes y procedimiento completo |
| UI/UX/Design System | Baja | Media | Lote UI/UX completo pendiente |
| Gobernanza multiagente | Alta | Alta | Archivo fuente tiene worktree modificado |

Los porcentajes no se inventan porque el denominador doctrinal completo aún no
está establecido.

## 11. Matriz editorial KEEP/MODIFY/ADD/MOVE/REMOVE

### Estándar maestro v1.1 existente

| Sección | Clasificación | Tratamiento propuesto |
|---|---|---|
| 0-10 | KEEP/MODIFY | Conservar; añadir doctrina explícita de reversibilidad/contratos sin duplicar |
| 11 Base de datos | MOVE/CROSS_REFERENCE | Mantener principios mínimos; trasladar detalle al estándar DB |
| 12 API | KEEP/CROSS_REFERENCE | Mantener reglas generales de contrato; procedimiento en playbook |
| 13-20 | KEEP | Propiedad transversal correcta |
| 21 Flujo IA | MODIFY/CROSS_REFERENCE | Referenciar orden canónico aprobado, no mantener flujo paralelo |
| 22-26 | KEEP | Límites, DoD y detención permanecen generales |
| Anexo A | REMOVE_FROM_FUTURE_DRAFT | Conservar solo como historia en el aprobado actual |
| Anexo B | KEEP | Patrones son materia transversal |
| 27-29 | MODIFY | Actualizar referencias/ownership tras decisión conceptual |

### Playbook Backend/API existente

| Sección | Clasificación | Tratamiento propuesto |
|---|---|---|
| Identidad/compatibilidad | UNRESOLVED | No cambiar hasta decidir alcance y versión |
| CP-01 a CP-11 | KEEP_AS_SPECIALIZED_PROFILE | Buen perfil de Crear producto, no procedimiento universal completo |
| Bibliografía por referencia | KEEP | Evita duplicación |
| Precondiciones/participantes/salidas | ADD si se generaliza | Exigidos por nueva estructura mínima |
| Despliegue/deprecación/observabilidad | ADD si se generaliza | Faltan como flujo general explícito |

## 12. Fuentes inaccesibles

| Fuente | Estado | Impacto |
|---|---|---|
| Checkpoint integral CP-0002 | INACCESSIBLE | No se puede demostrar la aceptación lógica completa |
| KN-000001..015 declarados históricamente | INACCESSIBLE | IDs reservados; trazabilidad previa incompleta |
| Documentos maestros históricos declarados | INACCESSIBLE | No pueden usarse como baseline |
| Código/stack real | EXCLUDED_WITH_REASON | Versiones y capacidades quedan por validar después |

## 13. Asuntos no resueltos

1. ¿Debe preservarse el playbook aprobado de Crear producto y crearse otro
   playbook Backend/API general con nombre/versión distintos?
2. ¿Debe el estándar maestro evolucionar a v1.2 en lugar de producir otra
   propuesta llamada v1.1?
3. ¿Qué contenido exacto permanece en la sección DB del maestro tras crear el
   estándar especializado?
4. ¿Cuál es el checkpoint CP-0002 integral y dónde está?
5. ¿Cuál es el estado limpio/canónico de la norma de colaboración actualmente
   modificada en el worktree?
6. ¿Qué stack Backend/API está realmente vigente? Se requiere fase posterior de
   validación contra código.

## 14. Resultado del lote

- 4 fuentes lógicas procesadas dentro de su alcance.
- 25 KN nuevos: `KN-000028` a `KN-000052`.
- 10 matrices iniciadas y actualizadas.
- 6 contradicciones explícitas; ninguna resuelta silenciosamente.
- Propiedad documental preliminar establecida.
- Los seis documentos finales no fueron redactados.
- No se modificó Gystigo ni `Fabric/Knowledge`.

## 15. Único siguiente paso

Ejecutar el Lote 002 de ingeniería general con las fuentes bibliográficas
declaradas por el estándar (Sommerville, Clean Code, Design Patterns y
algoritmos), verificando de forma independiente sus afirmaciones y actualizando
KN/matrices sin redactar todavía los seis documentos finales.
