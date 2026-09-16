# PEGAR EN: CLAUDE CHAT — REVISIÓN CRÍTICA DE LA PROPUESTA INICIAL

```text
TRACK=GM-AI-WORKSPACE-FOUNDATION-01
STEP=INITIAL_PROPOSAL
MODE=ANALYSIS_AND_SCOPE_DEFINITION
AGENT=CHATGPT_WORK
STATUS=READY_FOR_CLAUDE_CRITICAL_REVIEW
IMPLEMENTATION_AUTHORIZED=NO
DELETION_AUTHORIZED=NO
STAGING_COMMIT_PUSH_AUTHORIZED=NO
```

## 1. Objetivo

Construir `GM AI Workspace` como una aplicación privada para Eduardo y desarrolladores autorizados que permita coordinar el trabajo entre ChatGPT, ChatGPT Work, Codex, Claude Chat, Claude Code y participantes humanos sin perder el hilo de los tracks.

La aplicación debe presentar, capturar, indexar y reconstruir contexto. La memoria operativa no vivirá dentro del repositorio de código.

## 2. Decisiones de ubicación vigentes

```text
APPLICATION_NAME=GM AI Workspace
TECHNICAL_NAME=gm-ai-workspace
APPLICATION_LOCATION=D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT\Modules\gm-ai-workspace

PERSISTENT_MEMORY_NAME=GM AI BoxGhost
PERSISTENT_MEMORY_LOCATION=D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT\Fabric\GM_AI_BoxGhost

KNOWLEDGE_LOCATION=D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT\Fabric\Knowledge
PRODUCT_LOCATION=D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT\Gystigo

PLATFORM_OS_COUPLING=PROHIBITED
CUSTOMER_AVAILABILITY=DISABLED
RAW_CONVERSATIONS_IN_MODULE_GIT=PROHIBITED
RAW_CONVERSATIONS_IN_GYSTIGO=PROHIBITED
```

Responsabilidades exclusivas:

| Componente | Propietario de |
|---|---|
| `Modules\gm-ai-workspace` | Interfaz, API, lógica de aplicación, contratos y pruebas |
| `Fabric\GM_AI_BoxGhost` | Tracks, conversaciones, sesiones, contexto, aprobaciones, decisiones, evidencias, auditorías y archivos útiles de trabajo |
| `Fabric\Knowledge` | Libros, fuentes, corpus y conocimiento derivado |
| `Gystigo` | Producto ERP y documentación canónica aprobada |

## 3. Evidencia examinada del ZIP histórico

```text
SOURCE_FILE=GYPPORT_AI_Workspace.zip
SHA256=ac24436adcb26033eea4b9beea4c7d599d68d003b227ba20609f02b850d4a924
ZIP_ENTRIES=131
UNCOMPRESSED_BYTES=243014
SOURCE_STATUS=ARCHIVED_SUPERSEDED_NON_CANONICAL
```

El ZIP incluye:

- Un repositorio `.git` histórico que no debe copiarse al módulo nuevo.
- Cuatro esquemas JSON y cuatro pruebas contractuales.
- Validadores fail-closed de configuración y autorización.
- Un CLI CommonJS para límites, drift y findings.
- Un servidor HTTP local CommonJS.
- Un panel HTML para findings, reviews y decisiones humanas.
- Configuraciones y documentos con rutas antiguas a `docs\ai`, GDA y otras clasificaciones ya superadas.

Tratamiento propuesto:

| Contenido | Decisión propuesta |
|---|---|
| `.git/` del ZIP | Archivar únicamente; nunca fusionar con el repositorio nuevo |
| `schemas/*.json` | Adaptar a `contracts/schemas/legacy-candidates/` y evaluar uno por uno |
| `tests/contracts/` | Portar la intención de las pruebas, no copiar automáticamente |
| Validación fail-closed | Conservar como requisito obligatorio |
| Protección contra path traversal | Conservar como requisito y prueba de seguridad |
| `cli.cjs` | Extraer requisitos; decidir después si sobrevive como herramienta de migración |
| `server.cjs` | No usar como backend definitivo; sustituir por Spring Boot |
| `public/index.html` | Usar como referencia funcional, no como frontend definitivo |
| Rutas `docs\ai` | Sustituir por `GM_AI_BOXGHOST_ROOT` |
| Documentos `ARCHIVED / SUPERSEDED` | Evidencia histórica, nunca autoridad vigente |

## 4. Resultado funcional esperado

La primera versión útil debe permitir:

1. Ver todos los tracks activos y cerrados.
2. Abrir un track y comprender su estado actual sin releer toda la conversación.
3. Ver una línea de tiempo unificada de intervenciones humanas y de IAs.
4. Consultar el último `CONTEXT_PACK`, checkpoint, alcance, decisiones y aprobaciones.
5. Consultar sesiones capturadas, adjuntos, archivos generados, parches, resultados de comandos y evidencias.
6. Identificar qué agente produjo cada elemento, cuándo, en qué superficie y con qué hash.
7. Importar posteriormente exportaciones autorizadas de cada proveedor sin mezclar secretos ni cachés internos.
8. Registrar aprobaciones humanas explícitas sin inferirlas automáticamente.

## 5. Propuesta de interfaz

### Navegación principal

```text
Inicio
Tracks
Conversaciones
Capturas
Archivos
Aprobaciones
Decisiones
Evidencias
Auditorías
Configuración
```

### Pantalla inicial

La pantalla `Inicio` mostrará:

- Track activo y próximo paso.
- Aprobaciones pendientes.
- Últimas sesiones importadas.
- Alertas de contexto incompleto.
- Integridad de BoxGhost.
- Estado de proveedores y repositorios configurados.

### Pantalla de tracks

Cada fila mostrará:

```text
TRACK_ID
TITLE
STATUS
CURRENT_STEP
OWNER
LAST_AGENT
LAST_ACTIVITY_AT
CONTEXT_HEALTH
OPEN_FINDINGS
PENDING_APPROVALS
```

### Detalle de un track

Cabecera:

```text
Track | estado | alcance | propietario | paso actual | siguiente acción
```

Pestañas:

```text
Resumen
Diálogo
Sesiones
Intervenciones
Archivos
Aprobaciones
Decisiones
Evidencias
Auditorías
```

Un panel lateral mostrará siempre:

- `CONTEXT_PACK.md` vigente.
- Último checkpoint.
- Límites activos.
- Decisiones aplicables.
- Archivos fuente enlazados.

### Lenguaje visual

Se propone usar el Design System de GYPPORT y sus tokens, con la identidad base ya validada:

```text
PRIMARY=#29A9E0
PRIMARY_DARK=#06204D
TENANT_THEME_OVERRIDE=NOT_APPLICABLE_IN_INITIAL_PRIVATE_VERSION
```

La interfaz debe priorizar densidad informativa legible, trazabilidad y estados explícitos. No debe parecer un chat genérico.

## 6. Arquitectura técnica propuesta

```text
Frontend: React + TypeScript + Vite + Tailwind CSS
Backend: Java 25 + Spring Boot
Data access: JdbcTemplate
Metadata database: MySQL 8.4
Content storage: Fabric\GM_AI_BoxGhost
Contracts: JSON Schema + OpenAPI
Initial execution: local/private
```

Se propone un monolito modular, no microservicios. La aplicación se dividirá por capacidades y podrá separar componentes únicamente cuando exista evidencia real de necesidad.

```text
frontend/
backend/
contracts/
config/
docs/
tools/
tests/
```

Capacidades backend iniciales:

```text
workspace
track
timeline
sessioncapture
intervention
context
artifact
approval
decision
evidence
audit
source
integrity
```

## 7. Modelo mínimo de dominio

| Entidad | Responsabilidad |
|---|---|
| `Workspace` | Configuración y límites del entorno |
| `Project` | Agrupación de tracks y repositorios |
| `Track` | Unidad de trabajo con estado, alcance y próximo paso |
| `SessionCapture` | Captura recuperable de una sesión de un agente o humano |
| `TimelineEvent` | Evento normalizado para reconstruir el diálogo |
| `Intervention` | Entrega formal dentro del orden multi-IA |
| `ContextPacket` | Contexto seleccionado para continuar el trabajo |
| `Artifact` | Archivo producido o recibido |
| `Approval` | Autorización humana explícita y delimitada |
| `Decision` | Decisión registrada y relacionada con evidencia |
| `Evidence` | Prueba técnica o documental verificable |
| `Audit` | Verificación independiente y su veredicto |
| `SourceReference` | Procedencia, ubicación, hash y sensibilidad |

No se propone modelar todavía GYPPORT Brain ni GYPPORT Genome como servicios independientes.

## 8. Regla de persistencia híbrida

MySQL conservará metadatos consultables:

- Identificadores y relaciones.
- Estados y transiciones.
- Índices de búsqueda.
- Ubicaciones lógicas.
- Hashes y tamaños.
- Clasificación de sensibilidad.
- Auditoría de acciones de la aplicación.

BoxGhost conservará el contenido recuperable:

- Transcripciones y exportaciones.
- Prompts y respuestas expuestos.
- Adjuntos y archivos generados.
- Parches, logs y resultados de herramientas.
- Context packs y checkpoints.
- Evidencias y auditorías.
- Objetos únicos por SHA-256.

```text
SECRETS_IN_BOXGHOST=PROHIBITED
PROVIDER_PRIVATE_INTERNAL_FILES=NOT_ASSUMED_ACCESSIBLE
REGENERABLE_DEPENDENCIES=node_modules,dist,build
REGENERABLE_DEPENDENCIES_RETENTION=EXCLUDED
```

## 9. Contrato de captura de sesiones

Cada captura promovida debe producir:

```text
SESSION_MANIFEST.json
TRANSCRIPT.jsonl
SUMMARY.md
FILES_MANIFEST.json
attachments/
generated-files/
terminal-logs/
patches/
tool-results/
```

Campos mínimos del manifiesto:

```text
capture_id
track_id
agent
provider
surface
external_session_id
started_at
finished_at
captured_at
source_type
content_sha256
sensitivity
retention=PERMANENT
```

Flujo de importación:

```text
receive -> quarantine -> scan -> hash -> classify -> associate -> store -> index -> verify
```

No debe existir captura automática ciega de cookies, tokens, credenciales, cachés o archivos internos no expuestos por los proveedores.

## 10. API candidata del primer producto

Solo se congela el prefijo; los contratos se revisarán antes de implementar.

```text
GET  /api/v1/workspace
GET  /api/v1/tracks
GET  /api/v1/tracks/{trackId}
GET  /api/v1/tracks/{trackId}/timeline
GET  /api/v1/tracks/{trackId}/context
GET  /api/v1/tracks/{trackId}/captures
GET  /api/v1/tracks/{trackId}/artifacts
GET  /api/v1/tracks/{trackId}/decisions
GET  /api/v1/tracks/{trackId}/audits
GET  /api/v1/integrity
POST /api/v1/imports/sessions
POST /api/v1/approvals
```

Los endpoints de escritura deben usar validación fail-closed, rutas permitidas, control de concurrencia, idempotencia y auditoría.

## 11. Primer incremento implementable recomendado

Se recomienda un vertical slice de solo lectura antes de habilitar importaciones o aprobaciones:

### Incluido

1. Inicializar el repositorio nuevo sin reutilizar `.git` del ZIP.
2. Crear frontend, backend, contratos y pruebas mínimas.
3. Configurar `GM_AI_BOXGHOST_ROOT` por variable de entorno.
4. Fallar al arrancar si la ruta no existe, no es absoluta o no cumple la estructura mínima.
5. Leer `projects/gypport/ACTIVE_TRACKS.json`.
6. Leer `TRACK_STATE.md`, `CONTEXT_PACK.md` y la línea de tiempo de un track.
7. Exponer los endpoints GET necesarios.
8. Renderizar `Inicio`, `Tracks` y `Detalle del track`.
9. Probar path traversal, raíces fuera de límites y datos inválidos.
10. Abrir código y BoxGhost desde un único archivo de Visual Studio Code.

### Excluido

- Escritura o eliminación dentro de BoxGhost.
- Conectores automáticos con ChatGPT, Claude o Codex.
- Captura en tiempo real.
- Aprobaciones mutables desde la interfaz.
- RAG, embeddings, GYPPORT Brain o agentes autónomos.
- Despliegue externo o disponibilidad para clientes.
- Cambios en Gystigo, Platform OS o Fabric Knowledge.
- Staging, commit o push.

Esta rebanada permite validar primero la frontera más importante: el módulo puede reconstruir contexto desde BoxGhost sin mezclar código y memoria.

## 12. Estructura propuesta del repositorio

```text
Modules\gm-ai-workspace\
├── README.md
├── AGENTS.md
├── .gitignore
├── .env.example
├── GM_AI_Workspace.code-workspace
├── frontend\
│   ├── src\
│   │   ├── app\
│   │   ├── components\
│   │   ├── features\tracks\
│   │   ├── services\
│   │   └── types\
│   ├── tests\
│   └── package.json
├── backend\
│   ├── src\main\java\com\gypport\aiworkspace\
│   │   ├── workspace\
│   │   ├── track\
│   │   ├── timeline\
│   │   ├── context\
│   │   ├── integrity\
│   │   └── shared\
│   ├── src\main\resources\
│   ├── src\test\
│   └── pom.xml
├── contracts\
│   ├── openapi\
│   └── schemas\
├── config\
├── docs\
│   ├── architecture\
│   ├── decisions\
│   └── migration\
├── tools\
└── tests\
```

`GM_AI_Workspace.code-workspace` deberá abrir dos raíces:

```text
Modules\gm-ai-workspace
Fabric\GM_AI_BoxGhost
```

BoxGhost debe permanecer fuera del repositorio Git y configurarse como lectura en el primer incremento.

## 13. Seguridad inicial

- Escuchar únicamente en `127.0.0.1` durante la etapa local.
- Spring Security activo desde el comienzo.
- Sin credenciales predeterminadas ni secretos versionados.
- CORS limitado al frontend local configurado.
- Validar y normalizar todas las rutas antes de acceder al sistema de archivos.
- Prohibir symlinks o junctions que escapen de `GM_AI_BOXGHOST_ROOT`.
- Límites de tamaño y tipo de archivo para futuras importaciones.
- Registro append-only de acciones sensibles.
- Aprobaciones explícitas: nunca inferidas de una conversación.

## 14. Criterios de aceptación del primer incremento

```text
BACKEND_TESTS=PASS
FRONTEND_TESTS=PASS
FRONTEND_TYPECHECK=PASS
FRONTEND_LINT=PASS
FRONTEND_BUILD=PASS
CONTRACT_TESTS=PASS
PATH_TRAVERSAL_TESTS=PASS
BOXGHOST_OUTSIDE_GIT=VERIFIED
RAW_CONVERSATIONS_IN_MODULE=0
LEGACY_GIT_IMPORTED=NO
GYSTIGO_MODIFIED=NO
PLATFORM_OS_COUPLING=0
```

Pruebas funcionales mínimas:

1. La aplicación falla de forma comprensible sin `GM_AI_BOXGHOST_ROOT`.
2. Rechaza una ruta relativa o fuera de la raíz autorizada.
3. Lista tracks válidos desde BoxGhost.
4. Muestra estado, contexto y diálogo de un track.
5. Tolera archivos opcionales ausentes sin inventar contenido.
6. Señala un manifiesto inválido como error de integridad.
7. No escribe ni modifica ningún archivo de BoxGhost.

## 15. Plan posterior de unificación y limpieza

Después de validar la aplicación y antes de eliminar carpetas antiguas se abrirá un track independiente:

```text
TRACK=GM-AI-WORKSPACE-LEGACY-UNIFICATION-01
MODE=INVENTORY_MIGRATION_AND_DEDUPLICATION
DEFAULT_ACTION=NO_DELETE
```

Ese track inventariará como mínimo:

```text
GYPPORT_AI_Workspace.zip
Fabric\AI_Workspace
Fabric\.chatgpt
Fabric\Private_State
Fabric\GM_AI_BoxGhost
Gystigo\docs\ai
cualquier GM_AI_Workspace o gm-ai-workspace anterior
```

Cada archivo recibirá:

```text
SOURCE_PATH
SHA256
SIZE
LAST_MODIFIED
CONTENT_CLASS
AUTHORITY_STATUS
SENSITIVITY
TARGET_OWNER
TARGET_PATH
ACTION=REUSE|ADAPT|MOVE|ARCHIVE|DELETE_CANDIDATE|KEEP
RATIONALE
```

Reglas de unificación:

1. Comparar por contenido y SHA-256, no solo por nombre.
2. No elegir como autoridad un archivo marcado `ARCHIVED` o `SUPERSEDED`.
3. No mezclar memoria operativa con código ni documentación canónica.
4. Un contenido funcional debe tener un único propietario y una única ruta activa.
5. `.chatgpt` y otras carpetas de compatibilidad solo podrán contener punteros o configuración, no otra copia canónica de la memoria.
6. Los archivos históricos conservados irán al archivo de procedencia de BoxGhost.
7. Los secretos se excluyen y se reportan sin mostrar su valor.
8. Ningún archivo se eliminará antes de presentar un `DELETION_PLAN.md` exacto y recibir una sola aprobación explícita de Eduardo.
9. Antes de eliminar se generarán hashes, mapa de migración, respaldo verificable y prueba de restauración.
10. No se hará staging, commit o push sin una autorización aparte de Eduardo.

Entregables del track de unificación:

```text
INVENTORY.csv
DUPLICATE_GROUPS.json
AUTHORITY_MAP.md
MIGRATION_MAP.md
CONFLICTS.md
DELETION_PLAN.md
BACKUP_MANIFEST.json
RESTORE_TEST.md
FINAL_STRUCTURE.md
```

## 16. Orden obligatorio de ejecución

Esta propuesta no se entrega directamente a Codex. Debe recorrer:

```text
1. ChatGPT Work: INITIAL_PROPOSAL                         <- documento actual
2. Claude Chat: CRITICAL_REVIEW
3. ChatGPT Work: ADJUSTMENT_AND_CROSS_VALIDATION
4. Claude Chat: PROVISIONAL_CONSOLIDATION
5. ChatGPT Work: TECHNICAL_VERIFICATION_HANDOFF
6. Claude Code: READ_ONLY_VERIFICATION
7. Eduardo: SINGLE_SCOPE_APPROVAL_GATE
8. Codex: IMPLEMENTATION_AND_TESTS
9. Claude Code: FINAL_AUDIT
10. Claude Chat: FINAL_CONSOLIDATION
11. ChatGPT Work: FINAL_CROSS_VALIDATION_AND_CLOSURE
```

Solo Eduardo autoriza staging, commit o push.

## 17. Solicitud exacta para Claude Chat

Realice una revisión crítica conceptual de esta propuesta. No escriba código ni declare el alcance aprobado.

Evalúe especialmente:

1. Si el vertical slice de solo lectura es la primera implementación correcta.
2. Si la frontera `gm-ai-workspace` / `GM_AI_BoxGhost` está suficientemente protegida.
3. Si el modelo híbrido MySQL + archivos crea duplicación o ambigüedad de autoridad.
4. Si faltan entidades esenciales o existen entidades prematuras.
5. Si la persistencia permanente de sesiones puede realizarse sin capturar secretos ni datos internos no expuestos.
6. Si la interfaz permite reconstruir contexto y no se limita a parecer un chat.
7. Si el plan de migración selectiva del ZIP evita revivir decisiones superadas.
8. Si el futuro track de unificación elimina duplicidad sin riesgo de pérdida.
9. Qué debe corregirse antes de preparar el handoff verificable para Claude Code.

Devuelva:

```text
VERDICT=ACCEPT|ACCEPT_WITH_CHANGES|REJECT
CRITICAL_FINDINGS=<number>
MAJOR_FINDINGS=<number>
MINOR_FINDINGS=<number>
REQUIRED_CHANGES=<ordered list>
RECOMMENDED_FIRST_SLICE=<exact scope>
UNRESOLVED_DECISIONS=<ordered list>
```
