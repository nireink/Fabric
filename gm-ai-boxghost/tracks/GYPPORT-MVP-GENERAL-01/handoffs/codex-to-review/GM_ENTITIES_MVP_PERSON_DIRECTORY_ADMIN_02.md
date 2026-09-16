# GM_ENTITIES_MVP_PERSON_DIRECTORY_ADMIN_02

Fecha: 2026-08-31. Implementación local controlada; sin publicación remota.

```text
TRACK=GYPPORT-MVP-GENERAL-01
STEP=GM_ENTITIES_MVP_PERSON_DIRECTORY_ADMIN_02
STATUS=OWNER_DECISION_REQUIRED
CANONICAL_PERSON_OWNER=gm-entities
PERSON_EMAIL_REQUIRED=NO
PERSON_IDENTIFIER_REQUIRED=NO
PERSON_DIRECTORY_PROJECTION=opaque Party UUID reference, displayName, optional primary email, optional masked CEDULA; Host composes account access
PERSON_SEARCH_FIELDS=displayName substring, email substring, exact ten-digit CEDULA; authenticated and tenant scoped
PERSON_READ_PERMISSION=entities.person.read
PERSON_MANAGE_PERMISSION=entities.person.manage
EXISTING_OWNER_PERMISSION_BACKFILL=V28 grants both permissions to active system OWNER roles
NEW_OWNER_PERMISSION_BOOTSTRAP=OnboardingConfig includes both permissions
PERSON_LIST_ENDPOINT=GET /api/entities/persons
PERSON_CREATE_ENDPOINT=POST /api/entities/persons
PERSON_DETAIL_ENDPOINT=GET /api/entities/persons/{reference}
PERSON_UPDATE_ENDPOINT=NOT_IMPLEMENTED
PERSON_LIST_UI=/entities/persons responsive table/cards, server pagination and search
PERSON_CREATE_UI=inline form; name required; EC/CEDULA and email optional
PERSON_DETAIL_UI=/entities/persons/{reference}; identity/contact/account-access display only
ACCOUNT_STATUS_DISPLAY=WITH_ACCESS/WITHOUT_ACCESS composed in Host; no credentials or actions
IDENTIFIER_MASKING=****** plus final four digits; status REGISTERED, never VERIFIED
PERSON_WITH_ID_NO_EMAIL=PASS
PERSON_WITH_EMAIL_NO_ID=PASS
PERSON_WITH_ID_AND_EMAIL=PASS
DUPLICATE_IDENTIFIER=PASS; canonical MDM reused, tenant Party ensured, no merge or duplicate
CROSS_TENANT_LIST=PASS
CROSS_TENANT_SEARCH=PASS
CROSS_TENANT_DETAIL=PASS
CROSS_TENANT_PROVENANCE_EXPOSED=NO
EXPENSES_PERSON_COMPATIBILITY=PASS
IDENTITY_RECONCILIATION_REGRESSION=PASS
MIGRATION_CREATED=V28__person_directory_permissions.sql
FRESH_DB_BOOTSTRAP=PASS; empty core_person_admin_fresh_28 to V28
EXISTING_DEV_DB_VALIDATE=PASS
GM_ENTITIES_TESTS=139 passed; 0 failures/errors/skips
GYSTIGO_TESTS=258 total; 201 passed; 57 conditional skips; 0 failures/errors
STUDIO_TESTS=260 passed in 29 files
LINT=PASS
BUILD=PASS
TESTS_FAILED=0 final
PREEXISTING_DIRTY_FILES_PRESERVED=NO; 28/33 hashes unchanged; 5 concurrent visual changes retained unstaged
LOCAL_COMMITS_CREATED=gm-entities commit containing directory use cases; Gystigo commit containing integration and this report
PUSH_PERFORMED=NO
REMOTE_CHANGES_PERFORMED=NO
BLOCKERS=Owner must reconcile five protected visual files whose hashes changed outside this STEP allowlist
NEXT_EXACT_ACTION=OWNER_ACCEPTANCE_GM_ENTITIES_PERSON_DIRECTORY_ADMIN
STOP
```

## Implementación y límites

El directorio canónico sigue en gm-entities. La proyección JDBC aplica tenant_id en listado, búsqueda, detalle y creación de contexto; solo devuelve la referencia UUID de Party. El correo se deriva del contacto primario EMAIL existente y la cédula del PartyIdentifier CEDULA/EC. No se exponen IDs numéricos, MDM, tenant de origen, organización, historial laboral, Gastos ni procedencia cross-tenant.

La creación valida nombre/correo/cédula antes de mutar. Sin cédula crea MdmParty + Party. Con cédula nueva usa CreateIdentifiedPersonUseCase y queda no verificada. Si la cédula global ya existe, resuelve el MDM terminal y asegura únicamente un Party en el tenant actual; conserva nombre/contacto canónicos, no fusiona, no concede acceso al tenant de origen y responde reusedCanonicalIdentity=true. El caso ilustrativo 1712344860 continúa inválido según el checksum aceptado; las pruebas positivas usan fixtures sintéticas válidas.

El acceso a GYPPORT se compone en el Host consultando UserAccount del mismo Party y tenant. gm-entities no depende de Gystigo. No se implementaron invitación, contraseña, roles, edición, borrado, empleados, party_roles ni party_relationships.

V28 crea solamente entities.person.read/manage y hace backfill de OWNER siguiendo V22. El provisioning futuro exige que ambos códigos activos existan. No duplica permisos previos porque se confirmó que no existían antes de V28.

## Verificación

La prueba MySQL personAdminListSearchCreateDetailAndTenantIsolation cubre las tres combinaciones de datos, paginación, búsqueda, detalle, aparición inmediata en /api/expense-persons, ausencia de UserAccount, ocultamiento entre tenants y reutilización global sin duplicar identificador. Toda Person creada desde Gastos comparte la misma tabla/proyección y aparece en Personas.

El Host completo pasó después de corregir la consulta de email para usar mdm_party_contacts. El intento intermedio que buscó una columna inexistente m.primary_email falló y no se presenta como resultado final. La ejecución final dejó 258 tests, 201 aprobados y 57 omitidos por condiciones de entorno. La suite previa de claims/merge permanece aprobada.

Flyway validó 29 migraciones. core_business_fleets_test migró V27→V28 y la suite completa pasó. core_person_admin_fresh_28 partió de esquema vacío, ejecutó B17..V28 y ServerApplicationTests terminó con exit 0. DEV se validó y migró mediante la imagen final local.

Studio: contratos 260/260, lint y build productivo aprobados. La navegación se añadió desde StudioBootstrap como definición registrada adicional; BusinessPlatformComposition.js, que pertenece a los 33 borradores visuales protegidos, no fue modificado.

Se inspeccionaron 1440x900, 1366x768 y 390x844 en navegador local autenticado: navegación, lista, formulario, detalle y ausencia de overflow horizontal. Esto es prueba visual técnica, no aceptación estética del Owner.

## Archivos y Git

gm-entities:
- src/main/java/com/gypport/business/entities/application/AdminCreatePersonUseCase.java
- src/main/java/com/gypport/business/entities/application/PersonDirectoryPort.java
- src/main/java/com/gypport/business/entities/application/PersonDirectoryService.java
- src/main/java/com/gypport/business/entities/party/infrastructure/persistence/jdbc/JdbcPersonDirectory.java
- src/test/java/com/gypport/business/entities/application/PersonDirectoryServiceTest.java

Gystigo:
- database/core/migration/V28__person_directory_permissions.sql
- platform_os/server/src/main/java/com/gypport/server/module/entities/EntitiesPermissions.java
- platform_os/server/src/main/java/com/gypport/server/module/entities/PersonAdminController.java
- platform_os/server/src/main/java/com/gypport/server/shared/config/IdentityClaimConfig.java
- platform_os/server/src/main/java/com/gypport/server/shared/config/OnboardingConfig.java
- platform_os/server/src/test/java/com/gypport/server/module/profile/PersonIdentityReconciliationHttpTest.java
- platform_os/studio/channel/browser/shell/src/App.jsx
- platform_os/studio/channel/browser/shell/src/bootstrap/StudioBootstrap.js
- platform_os/studio/channel/browser/shell/src/application/entities/PersonDirectoryPage.jsx
- platform_os/studio/channel/browser/shell/src/application/entities/PersonDirectoryPage.css
- platform_os/studio/channel/browser/shell/src/application/entities/personNavigation.js
- platform_os/studio/channel/browser/shell/src/application/entities/personService.js
- docs/ai/handoffs/codex-to-review/GM_ENTITIES_MVP_PERSON_DIRECTORY_ADMIN_02.md

Staging mediante listas literales; los 33 borradores preexistentes permanecen fuera del índice. La comprobación final detectó que StudioHeader.jsx, StudioLayout.jsx, StudioNavigation.jsx, StudioSidebar.jsx y StudioPrimaryShell.css cambiaron durante la ejecución sin pertenecer a la lista de edición de este STEP; 28 hashes siguen iguales. Esos cinco cambios se conservaron íntegros, no se restauraron y no se incluyeron. Por ello el resultado funcional está completo pero el estado formal queda OWNER_DECISION_REQUIRED. No se modificaron gm-expenses ni gm-fleets, ni se creó dependencia entre módulos. Siguiente acción: revisión del Owner y OWNER_ACCEPTANCE_GM_ENTITIES_PERSON_DIRECTORY_ADMIN.
