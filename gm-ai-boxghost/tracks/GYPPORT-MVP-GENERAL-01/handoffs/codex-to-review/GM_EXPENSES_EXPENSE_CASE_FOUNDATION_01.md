# GM_EXPENSES_EXPENSE_CASE_FOUNDATION_01

Fecha: 2026-08-31. Track: GYPPORT-MVP-GENERAL-01.

Implementación local completada; pendiente aceptación del Owner. Sin push, cambios remotos, reset, stash ni edición de migraciones históricas. No se inició el motor de recomendaciones.

## Auditoría y decisión

- CURRENT_GROUPING_MODEL: no existía un contenedor independiente. ActivityContext describe ExpenseAdvance; AdvanceSettlement concilia ese anticipo. Ninguno representa actividades sin anticipo. Las allocations son imputaciones verificadas de cada gasto, no expedientes.
- CURRENT_RESPONSIBLE_MODEL: ResponsibleReference de gm-expenses, con vínculo canónico opcional a gm-entities y aislamiento tenant/organización. Se reutiliza, sin nuevo maestro Person.
- CURRENT_REVIEWER_MODEL: acciones de revisión de Expense autorizadas por permisos y actor autenticado; no había selector canónico de supervisor del expediente.
- CURRENT_ADVANCE_RELATION: Expense referencia opcionalmente ExpenseAdvance; se preservan congelamiento, revisión y conciliación existentes.
- CURRENT_EXPENSE_RELATION: Expense era el registro financiero independiente. Se agrega una relación nullable a ExpenseCase; no se reescriben históricos.
- El shell existente cumple header fixed y sidebar fixed/collapsible: 216 px expandido, 60 px compacto, etiquetas ocultas. No se modificó branding, navegación, menú de cuenta ni CSS del shell.

## Implementación

gm-expenses incorpora el paquete `casefile` con ExpenseCase, ExpenseCasePublicId, ExpenseCaseResource, repositorio, adaptador JDBC, puerto de verificación de recursos y servicio de aplicación transaccional. El nombre se recorta y valida a 1..150 caracteres. Responsable obligatorio, supervisor null, anticipo opcional y estado organizativo ABIERTO. CreatedAt, createdBy y version siguen convenciones del módulo.

Los recursos usan código abierto y referencia opaca; únicamente VEHICLE está habilitado por el adaptador del Host. ListVehiclesUseCase de gm-fleets verifica la referencia dentro del tenant autenticado y proporciona la captura placa/marca. No existe dependencia compilada gm-expenses -> gm-fleets ni FK entre módulos.

Crear expediente valida responsable activo, anticipo accesible/del mismo responsable y todos los recursos. Revisor no nulo falla cerrado mientras no exista selector canónico. La creación, asociación, desasociación y registro dentro del expediente usan recibos idempotentes. El registro financiero tiene una clave de operación interna distinta y el recibo externo vincula el resultado al expediente, evitando reutilizar la misma operación en otro expediente. Las mutaciones de recursos y gastos bloquean la fila del expediente dentro de la transacción.

Los recursos se desactivan con actor/fecha, conservando filas y capturas. El alta de gasto exige que cualquier vehículo recibido pertenezca al conjunto activo del expediente y delega en RegisterExpenseUseCase: catálogo, política requires_vehicle, snapshot, revisión, documentos y anticipo siguen siendo los existentes. Los snapshots de gastos anteriores permanecen intactos al desasociar un recurso.

V24 crea expense_case y expense_case_resource, agrega expense.expense_case_id nullable y sus FKs locales, incorpora la clave única de ámbito del anticipo requerida por la nueva FK y extiende los tipos de recibo idempotente. Se verificó que V23 era la última versión antes de crear V24. Ningún archivo SQL aplicado anteriormente fue editado.

## API y Studio

| Operación | Endpoint |
| --- | --- |
| Crear / listar | POST / GET /api/expense-cases |
| Detalle | GET /api/expense-cases/{reference} |
| Asociar recurso | POST /api/expense-cases/{reference}/resources |
| Desasociar conservando historial | POST /api/expense-cases/{reference}/resources/{resourceId}/deactivate |
| Registrar gasto contextual | POST /api/expense-cases/{reference}/expenses |

El Host reutiliza EXPENSE_READ / EXPENSE_CREATE y exige Fleet read al seleccionar vehículos y Advance read al asociar anticipos. Los payloads de comandos tienen allowlists: no aceptan tenant, organización, responsable/anticipo por gasto ni IDs de gastos existentes. El contexto procede únicamente de la sesión autenticada. Los tests de permisos demuestran cero invocaciones al servicio ante denegación.

`/expenses` ahora muestra Expedientes de gasto. Crear expediente, detalle e ingreso contextual viven bajo `/expenses/cases/...`; `/expenses/items` mantiene la consulta secundaria de todos los gastos e históricos, y las rutas anteriores de detalle y alta siguen compatibles. Categoría pertenece al gasto. La selección respeta scope + code del catálogo. Alimentación no fuerza recurso; un vehículo se preselecciona para categorías que lo requieren; con varios se exige elección explícita.

El formulario reutiliza QuickAddReference y el transporte expenseService. EvidenceSection y su lectura de archivos se comparten; la subida usa el endpoint de documentos existente. Si el gasto se registra pero falla el adjunto, la UI conserva su ID y permite reintentar sin duplicar el registro financiero. Se restablece el desplazamiento al entrar en las nuevas páginas para mostrar su título bajo la cabecera fija.

## Límites explícitos

- Responsable: selección/referencia existente, creada una sola vez para cada actividad si hace falta. No hay autoasignación silenciosa de persona ni directorio organizativo nuevo. En DEV se creó mediante UI una referencia válida llamada Expense Fleet QA para la cuenta PERSONAL sintética existente.
- Revisor: null; selector y asignación diferidos. No se modifican permisos ni autoaprobación.
- Anticipo: asociación a uno existente del mismo responsable; se puede crear previamente en el flujo actual. Se muestran su estado real e importes informativos, sin nueva contabilidad. El ejemplo USD 500 permanece BORRADOR, no se simula desembolso.
- Estado del expediente: ABIERTO; los estados de revisión pertenecen a cada Expense. No se inventa otro workflow.
- Gastado registrado excluye rechazados/excluidos y se agrupa por moneda. El saldo es informativo y se identifica como tal; no sustituye AdvanceSettlement ni incorpora sus ajustes contables.
- Tipos COMPUTER, EQUIPMENT, FIXED_ASSET y OTHER diferidos. Sin maestros adicionales, perfil técnico Fleet, RUC/SRI ni recomendaciones.
- La automatización del navegador disponible no expone carga de archivos. Se validó carga real por HTTP en tests y se adjuntó un PNG sintético por el API autenticado de DEV; luego se comprobó en Studio el documento persistido. No se declara automatizada la selección del archivo mediante diálogo del sistema.
- Auditoría independiente externa: no realizada en este STEP; este documento entrega la evidencia para revisión, sin atribuir aceptación a otro agente.

## Evidencia ejecutada

### Automatizada

- gm-expenses: 617 tests, 0 fallos/errores, 0 omitidos; incluye 11 nuevos casos de dominio/comandos.
- gm-fleets: 15 tests, 0 fallos/errores.
- Host: 243 descubiertos, 186 ejecutados, 57 optativos omitidos; 0 fallos/errores. Los omitidos no se cuentan como PASS. Se habilitó GYPPORT_FLEETS_REAL_DB_TESTS contra el contenedor aislado, no los antiguos opt-in dependientes de DEV.
- ExpenseCaseHttpApiTest: 6 escenarios reales HTTP/MySQL; fixtures por register/verify/login y endpoints de negocio, rollback por prueba. Evidencia real, revisión existente, replay, referencia cruzada entre expedientes, históricos, recursos desactivados y cross-tenant.
- ExpenseCasePermissionTest: 4 tests; permisos de expediente/Fleet/anticipo y rechazo de autoridad enviada por cliente antes de llamar a aplicación.
- Studio: 258 tests en 29 archivos; 8 reglas nuevas de selección contextual. Lint y build PASS.
- Arranque vacío: contenedor gypport-expense-case-test-20260831, puerto 3310, schema core_business_fleets_test. Flyway validó 25 migraciones y aplicó B17 + V18..V24 (8), terminando en V24. Reejecución validó V24 sin migraciones pendientes.
- DEV: backend reconstruido y reiniciado, core_business_dev pasó V23 -> V24 mediante Flyway. Validación de 25 migraciones y aplicación de una migración exitosa. No hubo SQL manual de aceptación ni cambios destructivos.

### Navegador y DEV

Cuenta sintética PERSONAL previamente existente, tenant 4. Ningún RUC ni organización requerido.

- Evento `08d65010-1ff1-4f70-b3a6-e8d73041d8e2`: Cena Navidad 2026, responsable válido, revisor null, ningún vehículo, anticipo existente USD 500. Alimentación USD 150, gasto `992816a9-b0ce-465b-8bb9-44ec0cc1f848`; documento `e89a6b0a-8c87-4db5-95e6-5251a8618423`, recibo-prueba-expediente.png visible tras recarga.
- Viaje `32a0daf5-3b98-4046-aaf2-32f4a8ca233d`: PCH5159 — KIA, Alimentación USD 20 sin selector de vehículo y Combustible USD 80 con vehículo preseleccionado. Captura de placa/marca visible en detalle. Total inicial USD 100.
- Segundo vehículo creado por UI Fleet: ABC1234 — TOYOTA. Asociado al mismo viaje. Combustible queda sin selección y bloquea el formulario hasta elegir. Registro desde móvil de USD 10 con selección explícita de ABC1234; snapshot correcto, total final del viaje USD 110.
- Cross-tenant de expediente, responsable, anticipo, vehículo y recurso denegado por pruebas HTTP reales. Vehículo no asociado y desactivado denegados; snapshots anteriores conservados.
- 1440x900, 1366x768 y 390x844: sin desbordamiento horizontal. Header top=0 al desplazar contenido (scrollY 374 escritorio / 269 móvil); sidebar independiente. Compactación 216 -> 60 px y etiquetas display:none comprobadas.
- Navegación Gastos <-> Vehículos, detalle/alta contextual, recarga directa de expedientes y Vehículos, menú de cuenta móvil y evidencia visible verificados.

Capturas fuera del repositorio, bajo `C:/Users/elbur/.codex/visualizations/2026/08/30/01a05471-5d5b-7400-98b0-77b7b0304670/`:

- expense-case-detail-1440.png
- expense-case-detail-1366.png
- expense-case-event-evidence-1366.png
- expense-case-multi-1440.png
- expense-cases-list-390.png
- expense-cases-drawer-390.png
- expense-case-new-390.png
- expense-case-detail-390.png
- expense-case-multi-form-390.png
- expense-case-mobile-created-390.png

## Preservación y Git

Baseline Gystigo: bf145f7501da7602844c21199aeb7307a9921f4b. Baseline gm-expenses: 855cacb022e433526f8e88d76e0631380d751b8a. gm-fleets queda en 6f0647aad439a9afa7aaabc57f519d0b129f3309, sin cambios.

Los 33 archivos visuales preexistentes de Gystigo conservan exactamente sus hashes SHA-256 iniciales. Ninguno se incluye en staging. Se reutiliza el shell funcionando en ese working tree; la publicación futura de sus borradores es un alcance separado. No se editó UI_Experiments.

Commit gm-expenses: 860e007, 8 archivos nuevos. Gystigo: commit que contiene este reporte, 21 archivos del STEP (20 de implementación/pruebas y este reporte). Staging por allowlist literal, índice inspeccionado y diff --check correcto. No se tocaron permisos, autenticación, Fleet Domain ni migraciones históricas.

## Reporte solicitado

```text
TRACK=GYPPORT-MVP-GENERAL-01
STEP=GM_EXPENSES_EXPENSE_CASE_FOUNDATION_01
STATUS=COMPLETED
CURRENT_GROUPING_MODEL=ActivityContext del anticipo; sin contenedor independiente previo
EXPENSE_CASE_MODEL=ExpenseCase; nombre, responsable, revisor nullable, anticipo nullable, ABIERTO, auditoría y version
RESPONSIBLE_MODEL=ResponsibleReference existente; selección/creación única por expediente
REVIEWER_MODEL=null; selector canónico diferido
RESOURCE_MODEL=Código abierto + referencia opaca + snapshot + historial de desactivación
ENABLED_RESOURCE_TYPES=VEHICLE
DEFERRED_RESOURCE_TYPES=COMPUTER,EQUIPMENT,FIXED_ASSET,OTHER
CANONICAL_VEHICLE_OWNER=gm-fleets
GM_EXPENSES_COMPILE_DEPENDS_ON_GM_FLEETS=NO
DIRECT_CROSS_MODULE_DB_FK=NO
CASE_CREATE_ENDPOINT=POST /api/expense-cases
CASE_LIST_ENDPOINT=GET /api/expense-cases
CASE_DETAIL_ENDPOINT=GET /api/expense-cases/{reference}
CASE_RESOURCE_ENDPOINT=POST /api/expense-cases/{reference}/resources; POST .../{resourceId}/deactivate
CASE_EXPENSE_ENDPOINT=POST /api/expense-cases/{reference}/expenses
MIGRATION_CREATED=V24__gm_expenses_case_foundation.sql
HISTORICAL_EXPENSE_COMPATIBILITY=PASS; relación nullable, sin reescritura
PRIMARY_EXPENSES_UI=/expenses -> Expedientes de gasto
CASE_CREATE_UI=PASS
CASE_DETAIL_UI=PASS
ADD_EXPENSE_UI=PASS
ADVANCE_INTEGRATION=Referencia al anticipo existente; conciliación intacta
REVIEW_LIFECYCLE_REUSED=YES
EVIDENCE_MECHANISM_REUSED=YES
PERSONAL_EVENT_CASE=PASS
PERSONAL_VEHICLE_CASE=PASS
MULTI_VEHICLE_SELECTION=PASS
COMBUSTIBLE_VEHICLE_RULE=PASS
ALIMENTACION_WITHOUT_VEHICLE=PASS
CROSS_TENANT_CASE=PASS
CROSS_TENANT_RESOURCE=PASS
FIXED_TOP_HEADER=PASS
COLLAPSIBLE_LEFT_NAV=PASS
DESKTOP_WEB=PASS
MOBILE_WEB=PASS
FRESH_DB_BOOTSTRAP=PASS
EXISTING_DEV_DB_VALIDATE=PASS
GM_EXPENSES_TESTS=617_PASS
GM_FLEETS_TESTS=15_PASS
GYSTIGO_TESTS=186_PASS;57_SKIPPED
STUDIO_TESTS=258_PASS
LINT=PASS
BUILD=PASS
TESTS_FAILED=0_FINAL
LOCAL_COMMITS_CREATED=2; gm-expenses y Gystigo
PUSH_PERFORMED=NO
REMOTE_CHANGES_PERFORMED=NO
BLOCKERS=NONE; límites diferidos documentados
NEXT_EXACT_ACTION=OWNER_ACCEPTANCE_EXPENSE_CASE_MVP
STOP
```
