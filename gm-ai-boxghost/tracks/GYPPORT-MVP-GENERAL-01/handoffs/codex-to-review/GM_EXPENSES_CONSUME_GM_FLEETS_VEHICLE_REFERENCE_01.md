# gm-expenses consume vehículos canónicos de gm-fleets

PEGAR EN: CHATGPT / CLAUDE — evidencia de implementación y commits locales autorizados.

```text
TRACK=GYPPORT-MVP-GENERAL-01
STEP=GM_EXPENSES_CONSUME_GM_FLEETS_VEHICLE_REFERENCE_01
MODE=CONTROLLED_IMPLEMENTATION_WITH_LOCAL_COMMITS
AGENT=CODEX
DATE=2026-08-31
STATUS=COMPLETED
IMPLEMENTATION_AND_REQUESTED_ACCEPTANCE=PASS
INDEPENDENT_AUDIT=NOT_PERFORMED
PUSH_AUTHORIZED=NO
REMOTE_CHANGES_AUTHORIZED=NO
```

COMPLETED se refiere a implementación, pruebas y commits locales de este STEP, no a auditoría independiente o publicación.

## Continuidad y repositorios

Raíz comprobada: `D:/NZXTG7/GYPPORT/GYPPORT ERP/GYPPORT`.

| Repositorio | Rama | HEAD inicial |
|---|---|---|
| Gystigo | feature/gm-fleets-minimum-vehicle-master-01 | beb88046837a1afce8b1d25b722ed80b0adb959c |
| Modules/gm-expenses | master | 0b1d71ed3dbf72ee81f301f9d8cd99eb7b4970a6 |
| Modules/gm-fleets | feature/gm-fleets-minimum-vehicle-master-01 | 6f0647aad439a9afa7aaabc57f519d0b129f3309 |

El pedido actual autoriza expresamente implementación y commits locales; no exige cambiar de rama. Se conserva cada rama existente. Los módulos estaban limpios. Gystigo tenía 33 archivos dirty/untracked e índice vacío. Los 33 hashes SHA-256 originales permanecen iguales; no se incluyen en staging ni en el commit. No se cambió branding, shell, navegación ni permisos.

## Auditoría del modelo anterior

CURRENT_EXPENSE_VEHICLE_MODEL=C: modelo mixto de referencia e información editable similar a un maestro temporal.
CURRENT_VEHICLE_REFERENCE_TABLE=vehicle_reference.
CURRENT_CREATE_FLOW=POST /api/vehicle-references permitía placa/description y referencia canónica opcional; RegisterExpense resolvía el UUID local y copiaba solo placa.
CURRENT_QUERY_FLOW=GET /api/vehicle-references leía referencias locales; detalle de gasto leía el snapshot de placa persistido, no Fleet.

VehicleReference ya contenía UUID local, ownership tenant/organización, Plate, description, CanonicalFleetVehicleReference opcional, active y version. ExpenseDetails requería conjuntamente vehículo/snapshot cuando la categoría lo exige. La tabla expense tiene FK interna a vehicle_reference, nunca a Fleet.

La unicidad por placa en vehicle_reference, su alta HTTP y el quick-add de placa hacían que también actuara como maestro. Se retira esa alta HTTP y se interpreta la referencia de nuevos gastos como una captura histórica, manteniendo el modelo y los datos previos.

No se ejecutó SQL manual para contar o clasificar filas antiguas. No se afirma que el reset anterior hubiese vaciado todas las referencias ni se atribuye automáticamente carácter descartable a datos históricos. Se preservan todas las filas existentes; la nueva cuenta PERSONAL comenzó sin vehículos ni gastos mediante APIs reales.

## Integración y seguridad

CANONICAL_VEHICLE_OWNER=gm-fleets.

Fleet mantiene VehicleId numérico positivo, tenant, plate (máximo 40), brand (máximo 120). No se modifica gm-fleets ni se añaden campos, endpoints o dependencias.

Se reutiliza CanonicalFleetVehicleReference como texto opaco dentro de gm-expenses. La UI consume:

```json
{"items":[{"reference":"17","plate":"PCH5159","brand":"KIA"}]}
```

Ese ejemplo ilustra el contrato; no atribuye el ID 17 al vehículo de aceptación.

- GET /api/vehicle-references: proyección del Host a través de ListVehiclesUseCase de gm-fleets, con tenant derivado de la sesión. Exige expenses.expense.read y fleets.vehicle.read. No expone tenantId.
- POST /api/expenses: recibe fleetVehicleReference como texto, nunca placa/marca como fuentes del snapshot. Exige permiso de creación y fleets.vehicle.read si se selecciona vehículo.
- El antiguo vehicleId en alta se rechaza con 400 para evitar confundir UUID local y referencia Fleet. En el detalle, vehicleId conserva su significado histórico de UUID local.
- POST /api/vehicle-references devuelve 410 y dirige al maestro Fleet. No crea referencias manipuladas por el cliente.
- ExpenseVehicleResolver pertenece a Application de gm-expenses. FleetExpenseVehicleResolver, implementado en el Host, consulta el caso de uso Fleet del tenant y comprueba ID y tenant antes de persistir nada.
- Una referencia inexistente o de otro tenant produce 404 genérico. No se confía en filtrado del navegador.
- La captura, el gasto y su recibo de idempotencia se ejecutan dentro de la transacción de RegisterExpenseUseCase. Cada gasto nuevo captura una referencia local nueva; no actualiza referencias de gastos anteriores.
- La referencia local guarda canonical_fleet_vehicle_reference, placa y marca en description. El gasto persiste vehículo local, vehicle_snapshot_plate y vehicle_snapshot_description. El detalle usa exclusivamente los snapshots del gasto.
- No hay importaciones Fleet ni dependencia Maven en gm-expenses; no hay consulta directa de tablas Fleet desde Expenses ni FK entre los dos módulos.

El Host usa la consulta existente de listado para resolver una referencia dentro del tenant. Es deliberadamente el mecanismo mínimo disponible; un caso de uso Fleet de búsqueda puntual podrá sustituirlo cuando sea necesario por volumen, sin cambiar el puerto consumidor.

## Migración V23

`database/modules/gm-expenses/migration/V23__gm_expenses_fleet_vehicle_snapshots.sql`:

- Añade expense.vehicle_snapshot_description nullable para conservar la marca; históricos quedan null sin inventar marcas.
- Amplía las columnas de placa de referencia/gasto/anticipo a 40 para aceptar exactamente las placas del maestro Fleet.
- Sustituye unicidad de placa en la tabla local de referencias por índice no único: varios gastos pueden capturar la misma placa sin ser vehículos canónicos duplicados.
- Sustituye la restricción antigua de formato por no vacío. El valor de referencia sigue el formato canónico actual de Fleet, incluido espacio interior; la unicidad canónica continúa exclusivamente en fleet_vehicle.
- No borra ni actualiza filas, no edita migraciones históricas, no toca restricciones de categorías ni FKs.

Bootstrap aislado confirmado: B17 y V18–V23 aplicadas por Flyway, 24 migraciones validadas. DEV existente: 24 validadas, únicamente V23 aplicada al reiniciar el backend. Sin reset, clean, repair o SQL manual.

## UI

El selector aparece automáticamente y es required para Combustible, Peaje, Parqueadero y Mantenimiento. Para categorías sin obligación sigue disponible como opción en detalles adicionales. Cada opción muestra placa — marca. No hay entrada manual de placa ni formulario Fleet duplicado.

Sin vehículos: “No tienes vehículos registrados.” y “+ Registrar vehículo” abren /fleets/vehicles. Al volver a abrir Nuevo gasto se consulta nuevamente la lista del Host. Se conservan responsable, anticipo, fecha, descripción y el flujo de evidencia existente en detalle.

## Pruebas y evidencia

| Verificación | Resultado |
|---|---|
| gm-expenses Maven test/install | 606 ejecutadas, 0 fallos, 0 errores |
| gm-fleets Maven test | 15 ejecutadas, 0 fallos, 0 errores; código intacto |
| Host reactor test | 233 contabilizadas, 176 ejecutadas, 57 opt-in omitidas; 0 fallos/errores finales |
| ExpenseFleetHttpApiTest | 8 casos reales MySQL/HTTP, PASS |
| FleetExpenseVehicleResolverTest | 3 pruebas de límites, aislamiento y captura histórica, PASS |
| GmFleetsHttpApiTest | 5 casos reales, PASS |
| Studio | 250 pruebas en 28 archivos, PASS |
| Studio lint/build | PASS / PASS |
| Docker build y arranque DEV | PASS |
| git diff --check | PASS con core.longpaths=true en Gystigo |

Las suites nuevas registran, verifican e inician sesión por HTTP con cuentas sintéticas y rollback transaccional, sin SQL manual. Prueban cada categoría obligatoria sin vehículo y con vehículo, categorías opcionales, dos gastos para el mismo vehículo, replay de operación, aislamiento entre tenants, lista vacía, retiro de alta local, autenticación y CSRF.

Los 57 casos omitidos tienen sus propios opt-in y algunos escriben fixtures SQL/cleanup sobre una base DEV específica; no se habilitaron indiscriminadamente. No se presentan como ejecutados. La nueva suite ejecuta la integración Fleet/Expense solicitada en MySQL aislado.

Prueba web real con cuenta PERSONAL nueva registrada/verificada por el flujo normal de DEV (Mailpit local):
1. Gastos vacío → Combustible → mensaje sin vehículos → Registrar vehículo.
2. En Fleet: PCH5159 / KIA guardado.
3. Gastos → Nuevo gasto → Combustible → PCH5159 — KIA → 30.00 → “Combustible viaje Yantzaza” → Guardar.
4. Detalle: COMBUSTIBLE, USD 30.00, PCH5159 — KIA. Refresco directo conserva datos.
5. En móvil: Alimentación 20.00 sin vehículo guardada correctamente.
6. Selector móvil requerido, visible y sin desbordamiento; sesión cerrada al terminar.

Capturas inspeccionadas en desktop 1440×900 y móvil 390×844. Ancho del documento igual al viewport en ambos. Evidencia fuera de Git bajo:
`C:/Users/elbur/.codex/visualizations/2026/08/30/01a05471-5d5b-7400-98b0-77b7b0304670/`

- expense-fleet-empty-desktop.png
- expense-fleet-selector-desktop.png
- expense-fleet-detail-desktop.png
- expense-fleet-selector-mobile.png
- expense-fleet-detail-mobile.png
- expense-fleet-food-mobile.png

## Incidencias resueltas y límites

La primera compilación del Host señaló el supuesto incorrecto de UUID para VehicleId; se corrigió al tipo real, proyectado como texto opaco. No se cambió Fleet.

Cuatro pruebas de replay fallaron inicialmente porque el mecanismo previo calculaba el hash incluyendo occurredAt del servidor. RegisterExpense ahora calcula un payload estable que incluye ownership, actor y datos de negocio, pero excluye la hora de transporte. El guard compartido no cambia; las pruebas de replay HTTP y de conflicto por payload distinto pasan. Los recibos antiguos no se reescriben; no se garantiza replay de requests anteriores al cambio de contrato.

Hubo lecturas iniciales con rutas/nombres incorrectos y dos intentos fallidos de construir el inventario PowerShell; se corrigieron antes de editar. Git requiere core.longpaths para un documento previo y emite advertencias de ignore global/CRLF. No se modificó configuración global ni se ocultaron fallos de pruebas.

No se probó dispositivo móvil físico, ni edición de Vehicle por HTTP (no existe todavía). La preservación al variar datos del maestro se prueba con el adaptador del Host y snapshots del módulo; la persistencia del snapshot se prueba además contra MySQL y refresco web.

Los artefactos locales deben mantenerse coordinados: gm-expenses, Host y V23. Una reversión futura debe ser explícita y forward-only para datos; no se propone reducir columnas ni reintroducir unicidad sobre capturas existentes.

## Archivos y commits

gm-expenses: 9 archivos de Application, snapshots, JDBC, Plate y contratos; commit local
`855cacb022e433526f8e88d76e0631380d751b8a`.

Gystigo: commit local preparado exclusivamente con estos 14 archivos; su SHA se informa al cerrar el STEP:

```text
database/modules/gm-expenses/migration/V23__gm_expenses_fleet_vehicle_snapshots.sql
platform_os/server/src/main/java/com/gypport/server/module/expenses/ExpenseController.java
platform_os/server/src/main/java/com/gypport/server/module/expenses/ExpensesResponseFormatting.java
platform_os/server/src/main/java/com/gypport/server/module/expenses/FleetExpenseVehicleResolver.java
platform_os/server/src/main/java/com/gypport/server/module/expenses/VehicleReferenceController.java
platform_os/server/src/main/java/com/gypport/server/shared/config/GmExpensesConfig.java
platform_os/server/src/test/java/com/gypport/server/module/expenses/ExpenseFleetHttpApiTest.java
platform_os/server/src/test/java/com/gypport/server/module/expenses/FleetExpenseVehicleResolverTest.java
platform_os/server/src/test/java/com/gypport/server/module/expenses/GmExpensesHttpApiTest.java
platform_os/studio/channel/browser/shell/src/application/expenses/ExpenseDetailPage.jsx
platform_os/studio/channel/browser/shell/src/application/expenses/NewExpensePage.jsx
platform_os/studio/channel/browser/shell/src/application/expenses/expenseService.js
platform_os/studio/verification/contracts/fleets/ExpenseVehicleReference.contract.mjs
docs/ai/handoffs/codex-to-review/GM_EXPENSES_CONSUME_GM_FLEETS_VEHICLE_REFERENCE_01.md
```

Los 33 archivos preexistentes de Gystigo quedan idénticos y sin staging. gm-fleets permanece en su HEAD inicial, sin cambios. No se hace push, fetch ni otra escritura remota.

Estado residual esperado de Gystigo tras el commit, verificado contra los hashes iniciales:

```text
 M design_system/src/components/Button/Button.tsx
 M design_system/src/tokens/tokens.css
 M package-lock.json
 M platform_os/studio/channel/browser/shell/package.json
 M platform_os/studio/channel/browser/shell/src/application/AuthPage.css
 M platform_os/studio/channel/browser/shell/src/application/authentication/authService.js
 M platform_os/studio/channel/browser/shell/src/application/dashboard/DashboardHost.css
 M platform_os/studio/channel/browser/shell/src/application/dashboard/DashboardHost.jsx
 M platform_os/studio/channel/browser/shell/src/application/dashboard/resolveDashboard.js
 M platform_os/studio/channel/browser/shell/src/application/onboarding/ShortRegisterPage.jsx
 M platform_os/studio/channel/browser/shell/src/layout/StudioHeader.jsx
 M platform_os/studio/channel/browser/shell/src/layout/StudioLayout.css
 M platform_os/studio/channel/browser/shell/src/layout/StudioLayout.jsx
 M platform_os/studio/channel/browser/shell/src/layout/StudioNavigation.jsx
 M platform_os/studio/channel/browser/shell/src/layout/StudioSidebar.jsx
 M platform_os/studio/channel/browser/shell/src/main.jsx
 M platform_os/studio/composition/business-platform/BusinessPlatformComposition.js
 M platform_os/studio/verification/integration/FrontendCanonicalIntegration.contract.mjs
?? docs/ai/handoffs/codex-to-review/STUDIO_LEFT_NAVIGATION_MODULE_INTEGRATION_01.md
?? docs/ai/handoffs/codex-to-review/STUDIO_PERSONAL_DASHBOARD_USER_MENU_AND_ICON_REFINEMENT_01.md
?? docs/ai/handoffs/codex-to-review/STUDIO_PRESTASHOP_INSPIRED_PRIMARY_UI_REBASELINE_01.md
?? docs/ai/handoffs/codex-to-review/STUDIO_TOP_HEADER_BRANDING_AND_ACCOUNT_REBASELINE_02.md
?? docs/ai/handoffs/codex-to-review/STUDIO_TOP_RIGHT_ACCOUNT_ICON_REFINEMENT_03.md
?? platform_os/studio/channel/browser/shell/fixtures/HeaderBrandingFixture.jsx
?? platform_os/studio/channel/browser/shell/fixtures/header-branding.html
?? platform_os/studio/channel/browser/shell/src/application/authentication/browserSessionSource.js
?? platform_os/studio/channel/browser/shell/src/layout/StudioIcon.jsx
?? platform_os/studio/channel/browser/shell/src/layout/StudioPrimaryShell.css
?? platform_os/studio/channel/browser/shell/src/layout/StudioUserMenu.jsx
?? platform_os/studio/channel/browser/shell/src/layout/UserAvatar.jsx
?? platform_os/studio/verification/contracts/browser/PersonalDashboard.contract.mjs
?? platform_os/studio/verification/contracts/browser/StudioPrimaryShell.contract.mjs
?? platform_os/studio/verification/contracts/browser/StudioSessionNavigation.contract.mjs
```

## Reporte solicitado

```text
TRACK=GYPPORT-MVP-GENERAL-01
STEP=GM_EXPENSES_CONSUME_GM_FLEETS_VEHICLE_REFERENCE_01
STATUS=COMPLETED
CURRENT_EXPENSE_VEHICLE_MODEL=Referencia local histórica con vínculo canónico Fleet y snapshot por gasto
CANONICAL_VEHICLE_OWNER=gm-fleets
INTEGRATION_MECHANISM=ExpenseVehicleResolver; implementación Host sobre ListVehiclesUseCase
GM_EXPENSES_COMPILE_DEPENDS_ON_GM_FLEETS=NO
DIRECT_CROSS_MODULE_DB_FK=NO
VEHICLE_SELECTOR_SOURCE=GET /api/vehicle-references -> Host -> gm-fleets
VEHICLE_SELECTOR_FIELDS=reference,plate,brand
PLATE_MANUAL_ENTRY_REMOVED=YES
NO_VEHICLE_EMPTY_STATE=PASS
REGISTER_VEHICLE_NAVIGATION=/fleets/vehicles; PASS
COMBUSTIBLE_REQUIRES_VEHICLE=PASS
PEAJE_REQUIRES_VEHICLE=PASS
PARQUEADERO_REQUIRES_VEHICLE=PASS
MANTENIMIENTO_REQUIRES_VEHICLE=PASS
ALIMENTACION_WITHOUT_VEHICLE=PASS
PERSONAL_FLEET_TO_EXPENSE_FLOW=PASS
CROSS_TENANT_VEHICLE_REFERENCE=PASS; 404 sin crear gasto
EXPENSE_VEHICLE_SNAPSHOT=plate + description(marca); referencia Fleet en captura local
MIGRATION_CREATED=V23__gm_expenses_fleet_vehicle_snapshots.sql
DESKTOP_WEB=PASS
MOBILE_WEB=PASS
GM_FLEETS_TESTS=15_PASS
GM_EXPENSES_TESTS=606_PASS
GYSTIGO_TESTS=176_PASS;57_SKIPPED
STUDIO_TESTS=250_PASS
TESTS_FAILED=0_FINAL;4_REPLAY_FAILURES_CORRECTED
BACKEND_CHANGED=YES
DATABASE_CHANGED=YES;V23 y datos sintéticos de aceptación mediante UI
FLYWAY_CHANGED=YES;solo migración nueva V23
LOCAL_COMMITS_CREATED=2;gm-expenses y Gystigo
PUSH_PERFORMED=NO
REMOTE_CHANGES_PERFORMED=NO
NEXT_EXACT_ACTION=DESIGN_GM_EXPENSES_EXPENSE_CASE_FOUNDATION
STOP
```

No se inició Expense Case ni el perfil técnico de Fleet.
