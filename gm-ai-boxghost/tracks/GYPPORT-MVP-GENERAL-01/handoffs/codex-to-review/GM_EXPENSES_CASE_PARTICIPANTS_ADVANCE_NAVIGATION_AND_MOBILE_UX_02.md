# GYPPORT MVP — Participantes, anticipos y navegación de Gastos

Fecha: 2026-08-31. Implementación local finalizada; aceptación visual/producto del Owner pendiente.

```text
TRACK=GYPPORT-MVP-GENERAL-01
STEP=GM_EXPENSES_CASE_PARTICIPANTS_ADVANCE_NAVIGATION_AND_MOBILE_UX_02
STATUS=COMPLETED
CANONICAL_PERSON_OWNER=gm-entities
PERSON_DIRECTORY_INTEGRATION=ExpenseParticipantDirectoryPort -> composición Gystigo Host -> PersonDirectoryService de gm-entities
GM_EXPENSES_COMPILE_DEPENDS_ON_GM_ENTITIES=NO
DIRECT_CROSS_MODULE_PERSON_FK=NO
PERSON_CREATE_PATH=POST /api/expense-persons -> Host -> CreatePersonPartyUseCase existente de gm-entities
PERSON_SELECTOR_SOURCE=GET /api/expense-persons; Party UUID opaco y nombre; filtrado por tenant autenticado
EXPENSE_CASE_RESPONSIBLE_MODEL=Person canónica obligatoria, seleccionada al crear el expediente
EXPENSE_CASE_REVIEWER_MODEL=Person canónica opcional; no concede acceso ni permisos
ADVANCE_RECEIVER_MODEL=Responsable del expediente, resuelto y validado por el servidor
ADVANCE_DELIVERED_BY_MODEL=Person canónica seleccionable, distinta del actor registrador
ADVANCE_RECORDED_BY_MODEL=Actor derivado exclusivamente del principal autenticado
DUPLICATE_RESPONSIBLE_INPUT_REMOVED=YES
RECEIVER_READ_ONLY=YES
DELIVERED_BY_SELECTABLE=YES
RECORDED_BY_SERVER_DERIVED=YES
VEHICLE_ADVANCE_READ_ONLY=YES
PERSON_SNAPSHOT_MODEL=Referencias Party UUID y nombres históricos mínimos; no copia mutable de identidad/contactos
KATHERINE_CREATED_IN_GM_ENTITIES=PASS
JUAN_CREATED_IN_GM_ENTITIES=PASS
DUPLICATE_PERSON_CREATED=NO
EXPENSES_INTERNAL_TABS=Expedientes | Gastos | Anticipos | Reportes
EXPEDIENTES_TAB=PASS; /expenses por defecto, responsables/revisores y recursos
GASTOS_TAB=PASS; /expenses/items; nueva creación requiere seleccionar expediente abierto
ANTICIPOS_TAB=PASS; /advances; expediente, receptor, entregador, monto, estado y fecha
REPORTES_TAB=PASS; /expenses/reports; totales reales, cantidad, promedio y categoría por moneda
FREE_FLOATING_EXPENSE_CREATE_ALLOWED=NO
REPORTS_USE_REAL_DATA=YES
MOBILE_CASE_DETAIL=PASS
MOBILE_REGISTER_EXPENSE=PASS
MOBILE_EVIDENCE=PASS; controles web y persistencia HTTP; cámara/selector nativo NO automatizados
MOBILE_SUCCESS=PASS
PERSONAL_CONTEXT=PASS
CROSS_TENANT_PERSON=PASS
CROSS_TENANT_VEHICLE=PASS
CROSS_TENANT_CASE=PASS
REVIEWER_REFERENCE_GRANTS_PERMISSION=NO
MIGRATION_CREATED=V25__gm_expenses_canonical_participants.sql
FRESH_DB_BOOTSTRAP=PASS
EXISTING_DEV_DB_VALIDATE=PASS
GM_ENTITIES_TESTS=128 passed; 0 failures/errors/skipped
GM_EXPENSES_TESTS=617 passed; 0 failures/errors/skipped
GM_FLEETS_TESTS=15 passed; 0 failures/errors/skipped
GYSTIGO_TESTS=248 discovered; 191 executed passed; 57 conditionally skipped; 0 failures/errors
STUDIO_TESTS=260 passed in 29 files
LINT=PASS
BUILD=PASS
TESTS_FAILED=0 in final runs
DESKTOP_1440=PASS
DESKTOP_1366=PASS
MOBILE_390=PASS
PREEXISTING_DIRTY_FILES_PRESERVED=YES; 33 archivos con hashes idénticos
GLOBAL_STUDIO_SIDEBAR_CHANGED=NO
HISTORICAL_MIGRATIONS_CHANGED=NO
UI_EXPERIMENTS_CHANGED=NO
LOCAL_COMMITS_CREATED=gm-entities 169d0f2; gm-expenses fb87e34; Gystigo: commit que contiene este informe
PUSH_PERFORMED=NO
REMOTE_CHANGES_PERFORMED=NO
BLOCKERS=NONE for implementation; aceptación Owner y captura física móvil pendientes
NEXT_EXACT_ACTION=OWNER_ACCEPTANCE_EXPENSE_PARTICIPANTS_AND_ADVANCE_FLOW
STOP
```

## Decisiones y límites preservados

- Se reutiliza `CreatePersonPartyUseCase`, sin duplicar reglas de Person. El modelo canónico actual exige nombre y correo principal; no se añadió obligatoriedad de cédula, RUC, Organization ni creación de UserAccount.
- gm-expenses no incorpora dependencia Maven/import de gm-entities, SQL sobre sus tablas ni FK entre módulos. El Host compone los dos módulos. gm-fleets continúa siendo el dueño de Vehicle y no tiene cambios.
- `responsible_reference` preexistente se conserva por compatibilidad con las FK financieras locales: las nuevas referencias usan el Party UUID y un nombre inmutable de primer uso; no guardan cédula, teléfono, correo ni otro maestro mutable. El selector y la resolución vigente proceden siempre de gm-entities. Se bloqueó la actualización de identidad en estas proyecciones canónicas y se retiró su antigua creación HTTP.
- Cada expediente guarda su responsable y revisor con snapshots. La entrega guarda receptor, entregador, actor autenticado, fecha, método y recursos. El campo histórico `delivered_by_user_account_id` conserva su significado de actor del sistema; la Person que entrega usa campos nuevos separados.
- La creación opcional del anticipo ocurre dentro de la misma transacción/idempotencia que el nuevo expediente. No se reasignan anticipos existentes a nuevos expedientes.
- La entrega bloquea el expediente y verifica versión, responsable y personas del tenant. Tras entregar, no permite reemplazar/desactivar sus recursos. Los gastos existentes conservan sus snapshots al desactivar recursos antes de entrega.
- Las rutas de nueva creación independiente de gastos y anticipos devuelven 410 y orientan al expediente; las rutas de lectura, revisión y liquidación existentes se conservan. Los formularios antiguos no alcanzables permanecen en el árbol de fuentes, sin eliminación de trabajo previo.
- Los registros históricos siguen legibles. No se inventaron referencias Person para antiguos responsables locales. Un anticipo antiguo sin expediente/responsable canónico no puede entregarse con el nuevo flujo; necesita una decisión explícita de reconciliación, fuera de este STEP.
- Reportes consulta agregados SQL reales bajo el contexto autorizado, excluye gastos rechazados/excluidos e incluye gastos históricos. Separa monedas y no confunde totales con liquidación contable.
- Se corrigió la identidad idempotente de adjuntos: usa el contenido y los datos de la operación, no el timestamp ni la identidad del arreglo de bytes. Un reintento conserva un solo documento.
- Se materializa el token CSRF diferido en la lectura del directorio, siguiendo el patrón Fleet existente. CSRF permanece activo. Una prueba HTTP con contexto fresco verifica el primer POST tras login.
- Sin cambios a autenticación/RBAC, recomendaciones, OCR, nómina, integración contable, RUC/SRI, cambio de organización, Flutter o APK.

## Evidencia funcional y de seguridad

Prueba con usuario PERSONAL sintético `Expense Fleet QA`, tenant 4; no se usaron credenciales del Owner. Creación normal por UI/API, sin SQL manual.

- Directorio canónico: Juan Alejandro, María Pérez y Katherine creados desde los selectores. La consulta API verificó una sola aparición de Juan y de Katherine; los reintentos idempotentes no crearon duplicados. La reutilización de referencias también está cubierta por pruebas HTTP.
- Expediente `41296b07-08af-40c8-a3d8-eab9e0d37334`: **Viaje los encuentros**, responsable Juan Alejandro, revisora María Pérez, vehículo PCH5159 — KIA.
- Anticipo `c06001ec-930e-4b00-9c16-fbf6a81bdd84`: USD 400, entregado por Katherine, registrado por el actor autenticado de pruebas, transferencia, 7 días. Receptor y recurso visibles de solo lectura.
- Gasto `42e679be-51e5-4d51-80fc-e628cbc61b06`: registrado desde viewport 390×844, MANTENIMIENTO, USD 30, 2026-08-31, “Cambio de neumáticos”. Éxito y detalle consultan los datos persistidos.
- Resumen del expediente: recibido USD 400, gastado USD 30, saldo USD 370. Un anticipo en borrador muestra entrega pendiente, no dinero recibido.
- Evidencia `446d306b-a897-43dd-bdfa-bbe57e937fa5`, `mantenimiento-prueba.png`: adjuntada por el endpoint existente; repetir la operación devolvió el mismo identificador y la lista conservó un documento. Su nombre se verificó en el detalle web.
- Reporte del contexto de prueba: USD 340, 7 gastos, promedio USD 48.57; Alimentación 190, Combustible 120, Mantenimiento 30. Incluye los registros históricos del tenant, no solamente el nuevo expediente.
- Navegación interna y recarga directa comprobadas durante la sesión en las vistas de expediente, anticipo y reportes. El selector previo a un nuevo gasto maneja ninguno/uno/varios expedientes elegibles sin permitir creación independiente.
- Pruebas HTTP reales: personas/revisor/entregador ajenos al tenant, vehículo ajeno, expediente/anticipo ajeno, intento de falsificar tenant/actor, rollback, reutilización de Person, entrega, recursos históricos, reportes y reintento de evidencia. Pruebas de permiso niegan operaciones antes de consultar el puerto.
- La designación como revisor no crea cuenta ni permiso. La aprobación sigue pasando por los permisos del principal.

## Base de datos y ejecución

- Descubrimiento encontró V24 como última migración; se agregó únicamente V25. B17 y V1..V24 permanecen sin cambios.
- MySQL aislado `gypport-expense-participants-test-20260831`, puerto 3310, esquema `core_business_fleets_test`: arranque vacío, 26 migraciones validadas y 9 aplicadas desde baseline B17 hasta V25. Las suites HTTP se ejecutaron contra este datasource.
- DEV `gypport-mysql-dev`, puerto 3308, `core_business_dev`: validación y aplicación incremental V24 → V25 correctas; sin rebaseline destructivo ni reescritura histórica.
- Backend DEV reconstruido y actualizado con la composición; permanece saludable en 8080. El contenedor aislado de pruebas se detuvo al terminar, sin eliminarlo ni borrar datos. MySQL DEV y Mailpit permanecen saludables.
- Maven: módulos y reactor Host ejecutados; resultados finales verificados en Surefire XML. Las 57 pruebas Host omitidas corresponden a sus condiciones opt-in; no se declaran ejecutadas.
- Studio: `npm run contracts --workspace=@gypport/platform-os-browser-shell`, `npm run lint --workspace=@gypport/platform-os-browser-shell`, `npm run build --workspace=@gypport/platform-os-browser-shell`, todos PASS.
- Incidencias intermedias resueltas antes del cierre: selección explícita del bean canónico de creación; aislamiento del contexto de prueba CSRF; ejecución secuencial de build y contratos para no leer `dist` mientras se regenera.
- Build y pruebas UI corresponden al checkout actual con sus 33 borradores visuales preservados. No se certifica que un checkout limpio del nuevo commit, sin esos borradores previos, reproduzca toda la apariencia mostrada.

## Evidencia visual y alcance móvil

Capturas en `C:/Users/elbur/.codex/visualizations/2026/08/30/01a05471-5d5b-7400-98b0-77b7b0304670/`:

- `participants-reports-1440.png`: escritorio 1440×900, datos reales y navegación.
- `participants-advances-1366.png`: escritorio 1366×768, receptor, expediente, entregador y estado.
- `participants-mobile-case-390.png`: 390×844, resumen 400/30/370 y CTA.
- `participants-mobile-register-390.png`: categorías canónicas con iconos Lucide.
- `participants-mobile-evidence-390.png`: controles de evidencia.
- `participants-mobile-success-390.png`: confirmación de gasto persistido.
- `participants-delivery-1440.png`: captura completa de entrega; al capturar con desplazamiento el header fijo aparece dentro de la imagen completa. No se usa como prueba geométrica de viewport.

Se verificaron los controles web `accept`/archivo y `capture=environment`, la persistencia del adjunto por HTTP y su visualización. **No se automatizó el selector nativo, una cámara física ni la selección real desde galería.** El soporte efectivo de captura depende del navegador/dispositivo; debe comprobarlo el Owner en su teléfono. No hay APIs nativas ni OCR.

## Alcance Git

Tres commits locales, sin publicación. gm-entities y gm-expenses partían limpios. Gystigo conserva fuera del staging los 33 archivos visuales preexistentes, verificados por SHA-256. Sin reset, restore, clean, stash ni cambios en UI_Experiments. El identificador del commit Gystigo se obtiene con `git log -1 --format=%H -- docs/ai/handoffs/codex-to-review/GM_EXPENSES_CASE_PARTICIPANTS_ADVANCE_NAVIGATION_AND_MOBILE_UX_02.md`; el informe pertenece a ese mismo commit.

Archivos de este STEP (rutas relativas a cada repositorio):

### Modules/gm-entities

- `src/main/java/com/gypport/business/entities/application/PersonDirectoryPort.java`
- `src/main/java/com/gypport/business/entities/application/PersonDirectoryService.java`
- `src/main/java/com/gypport/business/entities/party/infrastructure/persistence/jdbc/JdbcPersonDirectory.java`
- `src/test/java/com/gypport/business/entities/application/PersonDirectoryServiceTest.java`

### Modules/gm-expenses

- `src/main/java/com/gypport/business/expenses/advance/domain/AdvanceDeliverySnapshot.java`
- `src/main/java/com/gypport/business/expenses/advance/infrastructure/persistence/jdbc/JdbcExpenseAdvanceRepository.java`
- `src/main/java/com/gypport/business/expenses/application/AttachExpenseDocumentCommand.java`
- `src/main/java/com/gypport/business/expenses/application/AttachExpenseDocumentUseCase.java`
- `src/main/java/com/gypport/business/expenses/casefile/application/ExpenseCaseService.java`
- `src/main/java/com/gypport/business/expenses/casefile/domain/ExpenseCase.java`
- `src/main/java/com/gypport/business/expenses/casefile/domain/ExpenseCaseRepository.java`
- `src/main/java/com/gypport/business/expenses/casefile/infrastructure/persistence/jdbc/JdbcExpenseCaseRepository.java`
- `src/main/java/com/gypport/business/expenses/reference/domain/ResponsibleReference.java`
- `src/test/java/com/gypport/business/expenses/casefile/ExpenseCaseTest.java`
- `src/main/java/com/gypport/business/expenses/casefile/application/CaseAdvanceDeliveryService.java`
- `src/main/java/com/gypport/business/expenses/casefile/application/ExpenseParticipantDirectoryPort.java`
- `src/main/java/com/gypport/business/expenses/expense/application/ExpenseReportPort.java`
- `src/main/java/com/gypport/business/expenses/expense/application/ExpenseReportService.java`
- `src/main/java/com/gypport/business/expenses/expense/infrastructure/persistence/jdbc/JdbcExpenseReportPort.java`

### Gystigo

- `platform_os/server/src/main/java/com/gypport/server/module/expenses/ExpenseAdvanceController.java`
- `platform_os/server/src/main/java/com/gypport/server/module/expenses/ExpenseCaseController.java`
- `platform_os/server/src/main/java/com/gypport/server/module/expenses/ExpenseController.java`
- `platform_os/server/src/main/java/com/gypport/server/module/expenses/ExpensesErrorMapper.java`
- `platform_os/server/src/main/java/com/gypport/server/module/expenses/ExpensesResponseFormatting.java`
- `platform_os/server/src/main/java/com/gypport/server/module/expenses/ResponsibleReferenceController.java`
- `platform_os/server/src/main/java/com/gypport/server/shared/config/ExpenseCaseConfig.java`
- `platform_os/server/src/test/java/com/gypport/server/module/expenses/ExpenseCaseHttpApiTest.java`
- `platform_os/server/src/test/java/com/gypport/server/module/expenses/ExpenseFleetHttpApiTest.java`
- `platform_os/studio/channel/browser/shell/src/App.jsx`
- `platform_os/studio/channel/browser/shell/src/application/expenses/AdvanceDetailPage.jsx`
- `platform_os/studio/channel/browser/shell/src/application/expenses/AdvanceListPage.jsx`
- `platform_os/studio/channel/browser/shell/src/application/expenses/ExpenseDetailPage.jsx`
- `platform_os/studio/channel/browser/shell/src/application/expenses/ExpenseListPage.jsx`
- `platform_os/studio/channel/browser/shell/src/application/expenses/cases/ExpenseCaseDetailPage.jsx`
- `platform_os/studio/channel/browser/shell/src/application/expenses/cases/ExpenseCaseListPage.jsx`
- `platform_os/studio/channel/browser/shell/src/application/expenses/cases/ExpenseCases.css`
- `platform_os/studio/channel/browser/shell/src/application/expenses/cases/NewCaseExpensePage.jsx`
- `platform_os/studio/channel/browser/shell/src/application/expenses/cases/NewExpenseCasePage.jsx`
- `platform_os/studio/channel/browser/shell/src/application/expenses/expenseService.js`
- `platform_os/studio/verification/contracts/browser/ExpenseCases.contract.mjs`
- `database/modules/gm-expenses/migration/V25__gm_expenses_canonical_participants.sql`
- `platform_os/server/src/main/java/com/gypport/server/module/expenses/ExpensePersonController.java`
- `platform_os/server/src/main/java/com/gypport/server/module/expenses/ExpensePersonDirectory.java`
- `platform_os/server/src/main/java/com/gypport/server/module/expenses/ExpenseReportController.java`
- `platform_os/server/src/test/java/com/gypport/server/module/expenses/ExpenseParticipantPermissionTest.java`
- `platform_os/studio/channel/browser/shell/src/application/expenses/ExpenseModuleNavigation.jsx`
- `platform_os/studio/channel/browser/shell/src/application/expenses/ExpenseReportsPage.jsx`
- `platform_os/studio/channel/browser/shell/src/application/expenses/cases/ChooseExpenseCasePage.jsx`
- `platform_os/studio/channel/browser/shell/src/application/expenses/cases/ExpenseSuccessPage.jsx`
- `platform_os/studio/channel/browser/shell/src/application/expenses/components/PersonSelector.jsx`
- `platform_os/studio/channel/browser/shell/src/application/expenses/reportRules.js`
- `docs/ai/handoffs/codex-to-review/GM_EXPENSES_CASE_PARTICIPANTS_ADVANCE_NAVIGATION_AND_MOBILE_UX_02.md`

NEXT_EXACT_ACTION=OWNER_ACCEPTANCE_EXPENSE_PARTICIPANTS_AND_ADVANCE_FLOW

STOP. No iniciar recomendaciones contextuales de gastos.
