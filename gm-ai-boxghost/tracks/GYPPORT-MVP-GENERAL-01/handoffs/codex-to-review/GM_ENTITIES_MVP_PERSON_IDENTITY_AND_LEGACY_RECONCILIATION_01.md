# GM_ENTITIES_MVP_PERSON_IDENTITY_AND_LEGACY_RECONCILIATION_01

Fecha: 2026-08-31. Ejecución local controlada; sin publicación remota.

```text
TRACK=GYPPORT-MVP-GENERAL-01
STEP=GM_ENTITIES_MVP_PERSON_IDENTITY_AND_LEGACY_RECONCILIATION_01
STATUS=COMPLETED
CANONICAL_PERSON_OWNER=gm-entities
PERSON_EMAIL_REQUIRED=NO
PERSON_IDENTIFIER_REQUIRED=NO
CEDULA_REQUIRED_FOR_ACCOUNT_REGISTRATION=NO
REGISTRATION_IDENTITY_PRECHECK=OPTIONAL; neutral pending claim; skip preserves normal registration
PUBLIC_IDENTIFIER_ENUMERATION=NO
IDENTIFIER_LOOKUP_MODEL=global CEDULA + normalized value + EC; NOT_FOUND / SAME_MDM_PARTY / OTHER_MDM_PARTY
IDENTIFIER_NOT_FOUND_BEHAVIOR=authenticated profile attaches unverified; public registration awaits trusted approval
SAME_IDENTITY_BEHAVIOR=ALREADY_REGISTERED; no duplicate
OTHER_IDENTITY_BEHAVIOR=IDENTITY_CLAIM_REQUIRED; no automatic linkage
IDENTITY_CLAIM_MODEL=existing identity_claims extended; PENDING / APPROVED / REJECTED; immutable subject binding; 24-hour expiry
IDENTITY_VERIFICATION_IMPLEMENTED=FOUNDATION_ONLY
IDENTITY_VERIFICATION_LIMITATION=runtime trusted verifier returns no decision; no approval endpoint or official integration
AUTOMATIC_MERGE_ON_IDENTIFIER_MATCH=NO
LEGACY_RECONCILIATION_MODEL=approved claim; transactional Party MDM repoint + Host redundant account link + existing merge log
SOURCE_MDM_DELETE=NO
CANONICAL_MDM_RESOLUTION=terminal target with visited set and maximum 32 iterations
USER_ACCOUNT_ID_PRESERVED=YES
TENANT_PARTY_ID_PRESERVED=YES
TRANSACTION_IDS_PRESERVED=YES
HISTORICAL_SNAPSHOTS_REWRITTEN=NO
MULTI_TENANT_PARTY_CONTEXT_PRESERVED=YES
IDENTITY_LINK_GRANTS_TENANT_ACCESS=NO
SHOW_SOURCE_TENANT=NO
SHOW_SOURCE_ORGANIZATION=NO
SHOW_EMPLOYMENT_HISTORY=NO
SHOW_RELATIONSHIP_HISTORY=NO
PROFILE_IDENTITY_COMPLETION=reminder without global lock; registered/unregistered; own claim status only
REGISTRATION_PRECHECK_UI=implemented; original skip flow reused; neutral pending response
EXPENSES_PERSON_COMPATIBILITY=PASS
MERGE_AUDIT_MODEL=mdm_party_merge_logs source/target/reason/claim/process/time + identity_claims subject/proof/status
MIGRATION_CREATED=V26__canonical_person_identity_claims.sql + V27__reuse_canonical_identity_claims.sql
FRESH_DB_BOOTSTRAP=PASS; empty schema core_business_identity_fresh_27; B17..V27, 11 migrations
EXISTING_DEV_DB_VALIDATE=PASS; 28 migrations validated; V26 and V27 applied successfully
GM_ENTITIES_TESTS=139 passed; 0 failures/errors/skips
GYSTIGO_TESTS=257 total; 200 passed; 57 conditionally skipped; 0 failures/errors
STUDIO_TESTS=260 passed; 29 test files
LINT=PASS
BUILD=PASS; Studio production build and final Host Docker image
TESTS_FAILED=0 final full suites
PREEXISTING_DIRTY_FILES_PRESERVED=YES; 33 SHA-256 hashes unchanged
LOCAL_COMMITS_CREATED=gm-entities 8a1ffbd2f52bf2977679f8cd6297f930e36d1fb4; Gystigo commit containing this report
PUSH_PERFORMED=NO
REMOTE_CHANGES_PERFORMED=NO
BLOCKERS=no trusted runtime verification/approval mechanism; intentionally fail closed
NEXT_EXACT_ACTION=GM_ENTITIES_MVP_PERSON_DIRECTORY_ADMIN_02
STOP
```

## Alcance y decisiones

Persona sigue siendo MdmParty(PERSON) + Party del tenant, propiedad de gm-entities. UserAccount, contraseña, correo de acceso, verificación de correo, sesión y autorización permanecen en el Host. No se agregaron dependencias Maven, columnas de cédula paralelas, administración de Personas, empleados, invitaciones, RUC/SRI ni permisos nuevos.

El correo primario de Persona puede ser nulo; el registro de UserAccount conserva los requisitos existentes. Crear una Persona desde el selector de Gastos exige solamente nombre, admite correo y cédula opcionales, y no crea una cuenta. Se reutilizan los catálogos IDENTIFIER_TYPE/CEDULA y EC y la unicidad existente. Un checksum correcto nunca cambia is_verified a true.

La cédula ilustrativa del Owner, 1712344860, falla el checksum preexistente. Se mantuvo el validador y se agregó cobertura de rechazo. Los escenarios positivos usan la fixture sintética 1712345659, ya válida para ese validador; no acreditan identidad real.

El artefacto GM_ENTITIES_MVP_CURRENT_STATE_AUDIT_00 no fue localizado en los repositorios/tareas consultados. La línea base se comprobó directamente en código, esquema y runtime. Se leyeron AGENTS, START_HERE, estándar de integración, gobierno de arquitectura y ADR de acceso a datos. Este informe es evidencia de implementación y autorrevisión, no un dictamen independiente de Claude Code.

## Política pública y límite operativo

El precheck público valida formato y crea una solicitud opaca sin consultar existencia global. Números existentes e inexistentes reciben el mismo estado, mensaje y estructura. Después del formulario ambos permanecen pendientes, sin crear UserAccount, Party ni MDM mientras no haya prueba confiable. Esta restricción evita que la diferencia entre registro exitoso y pendiente revele existencia. Por ello, la rama pública de identificador inexistente NO completa inmediatamente el registro con cédula en el runtime actual: es una limitación deliberada respecto al flujo conceptual del Owner. La alternativa visible “Crear cuenta normalmente” omite el precheck y usa el registro previo sin cédula.

El token UUID se vincula una vez al correo normalizado de la cuenta solicitante. Esto es una vinculación de la solicitud, no una identidad inmutable basada en correo. La solicitud expira a las 24 horas; las filas se retienen como auditoría. No se añadió limpieza periódica ni limitación específica de frecuencia del precheck. No se realizó una prueba estadística de timing ni de carga concurrente.

El puerto confiable solo se sustituye por dobles de prueba en MySQL aislado. No existen aprobación HTTP, opción de aprobar todo, proveedor gubernamental ni fusiones DEV ejecutadas manualmente. No se certifica verificación oficial ni una operación productiva de aprobación.

En perfil autenticado: identificador inexistente se adjunta sin verificar; el mismo devuelve ALREADY_REGISTERED; uno de otra identidad inicia claim. Solo se muestran identificadores propios enmascarados y estado/UUID de solicitud propia. Campos de autoridad enviados por navegador se rechazan. La identidad no concede acceso al tenant de origen.

## Esquema auditado y reconciliación

La inspección de metadatos en DEV identificó nueve FK preexistentes hacia mdm_parties. El análisis también incluye las referencias históricas sin FK de identity_claims. Acciones:

| Referencia | Tratamiento |
| --- | --- |
| parties.mdm_party_id | Reasignar todos los vínculos del source al target dentro de la transacción; conservar Party IDs y tenant IDs. |
| user_accounts.mdm_party_id | El adaptador del Host actualiza solamente el vínculo redundante no nulo; valida consistencia con Party. No modifica contraseña, correo, sesión, roles ni accesos. |
| mdm_party_identifiers | Mantener identificador global en target. Si source tiene identificadores, denegar la fusión y exigir revisión separada. |
| mdm_party_tax_profiles | Denegar si source tiene datos fiscales; no inventar reconciliación fiscal. |
| mdm_party_contacts / mdm_party_addresses | Conservar en source como procedencia histórica; no sobrescribir datos del target. |
| organizations.mdm_party_id | Guard del Host deniega la operación si source tiene esta dependencia; rollback integral. |
| mdm_party_merge_logs source/target | Conservar referencias existentes y agregar evento; source único, sin autofusión. |
| identity_claims.existing_mdm_party_id y referencias del solicitante | Conservar evidencia heredada; las solicitudes nuevas guardan target, source, sujeto y prueba. |
| mdm_identity_claims de V26 | Copia histórica conservada por V27; ningún lector/escritor de aplicación permanece en ella. |

No se fusionan Party del mismo tenant: la colisión tenant+MDM requiere revisión separada. Se bloquean ambos MDM en orden estable y se rechazan inserciones nuevas de Party/identificadores sobre un source ya sustituido. La resolución tiene protección de ciclos y profundidad. No se reescriben transacciones, documentos ni snapshots, ni se trasladan permisos entre tenants.

La auditoría usa el merge log existente: source, target, timestamp y reason con claim UUID y referencia del proceso confiable. El usuario solicitante no se presenta como aprobador. La prueba y el sujeto están en identity_claims; merged_by_user_id permanece nulo cuando aprueba un proceso, no un usuario identificado.

V26 se aplicó antes de detectar la tabla identity_claims heredada durante la revisión final. No se reescribió ninguna migración aplicada. V27 amplía esa tabla, copia las solicitudes V26 conservando UUID/estado/prueba/vencimiento y deja la tabla transitoria intacta pero sin uso por la aplicación. Filas heredadas sin expiry quedan fuera del nuevo procesador; no se aprueban ni reinterpretan automáticamente. No hubo DROP, DELETE de datos DEV, repair ni reset. B17 y V1..V25 permanecen intactas.

## Evidencia de pruebas

La suite nueva PersonIdentityReconciliationHttpTest contiene nueve escenarios con HTTP real sobre MockMvc + Host + MySQL aislado. Cubre Persona sin correo antes de cuenta, selector de Gastos, respuestas públicas existentes/inexistentes equivalentes, reutilización aprobada de MDM, alta aprobada con identificador ausente, idempotencia, perfil y campos forjados, estado ajeno 404, rechazo/prueba de sujeto incorrecto, reconciliación tardía con gasto/anticipo entregado/documento real, aislamiento entre tenants, colisión de Party y rollback por fallo del adaptador Host. Las aprobaciones son exclusivamente dobles confiables de prueba.

La última suite completa del Host terminó con exit 0 después de V27: 257 tests, 200 ejecutados aprobados y 57 omitidos. A las 15:47 se comprobó V26→V27 en core_business_fleets_test y bootstrap desde esquema vacío de core_business_identity_fresh_27 (11 migraciones B17..V27). En DEV, Flyway validó 28 migraciones y aplicó V27 a las 20:49 UTC; V26/V27 constan success=1. La comparación binaria de la solicitud V26 copiada reportó missing_or_changed_copies=0 (1 fila conservada). Se usó comparación binaria porque las tablas heredada/transitoria tienen collations distintas.

Imagen final activa: sha256:10e653f5819874788f22c2e6657fa0c225beaaacfeb1708da709b7a176362d46; contenedor gypport-backend-dev healthy. Mi perfil se leyó nuevamente después de V27. El contenedor aislado gypport-person-identity-test-20260831 quedó detenido, con ambos esquemas conservados. Los logs locales filtrados de ejecución están en TEMP/identity-host-isolated-v27.log y TEMP/identity-entities.log; los XML Surefire quedan en target/surefire-reports de cada proyecto.

El escenario tardío compara snapshots de tablas de Gastos y la respuesta HTTP antes/después, conserva IDs de cuenta/Party/transacciones/documento y bytes normalizados del documento. La prueba de rollback abarca una transacción con fixtures, claim y fallo inyectado después del repoint; no se presenta como una prueba separada de recuperación ante caída de proceso. Pruebas de módulo cubren ciclos/profundidad, claim y clasificación SAME/OTHER.

Comandos ejecutados desde los repositorios reales:
- Maven gm-entities: install -q (suite completa y JAR local).
- Maven Gystigo/platform_os: -pl server -am test -q; variables GYPPORT_IDENTITY_REAL_DB_TESTS=true y GYPPORT_FLEETS_REAL_DB_TESTS=true; datasource aislado.
- Studio: npm run build, npm run contracts y npm run lint en el workspace browser shell.
- Docker Compose: build backend, up -d --no-deps backend; salud y logs Flyway filtrados.

Los 57 tests optativos restantes de Host se omiten por sus condiciones de entorno; no se activaron suites destructivas dirigidas a DEV. La nueva suite aislada sí verifica perfil, seguridad, registro y compatibilidad con Gastos. Se corrigieron durante desarrollo fixtures (categoryScope y comparación de byte[]), el mock JDBC afectado por resolución canónica y la selección del bean CreatePersonPartyUseCase en tests. El resultado final informado corresponde a la última ejecución completa, no a esos intentos intermedios.

Prueba visual manual a 1280x720: precheck, omisión al registro original, mensaje pendiente sin contraseña retenida, login PERSONAL, Mi perfil con recordatorio no bloqueante, navegación a Gastos y formulario de Persona con correo/cédula opcionales. Capturas inspeccionadas:
- C:/Users/elbur/.codex/visualizations/2026/08/30/01a05471-5d5b-7400-98b0-77b7b0304670/identity-precheck.png
- C:/Users/elbur/.codex/visualizations/2026/08/30/01a05471-5d5b-7400-98b0-77b7b0304670/identity-claim-pending.png
- C:/Users/elbur/.codex/visualizations/2026/08/30/01a05471-5d5b-7400-98b0-77b7b0304670/identity-profile-reminder.png

No se afirma aceptación visual del Owner ni cobertura móvil nueva en este STEP. Se reutiliza íntegramente el borrador visual existente; no se modificaron ShortRegisterPage, authService, shell, tokens ni los demás 33 archivos protegidos.

## Git y archivos

Baseline gm-entities: feat/entities-initial-development, 169d0f2acf2ef7899ff61f85e8b08c3ad8190a0f.
Baseline Gystigo: feature/gm-fleets-minimum-vehicle-master-01, bde68a76b9888ec22a57f935eb953fe58a6f4501.
gm-expenses y gm-fleets permanecen sin cambios; no se tocaron los dos responsables locales heredados ni se crearon FK/dependencias entre sus dominios.

Archivos gm-entities (25):
- src/main/java/com/gypport/business/entities/application/AddPartyIdentifierUseCase.java
- src/main/java/com/gypport/business/entities/application/CreatePersonPartyCommand.java
- src/main/java/com/gypport/business/entities/application/CreatePersonPartyUseCase.java
- src/main/java/com/gypport/business/entities/application/GetPartyProfileUseCase.java
- src/main/java/com/gypport/business/entities/identity/domain/MdmParty.java
- src/main/java/com/gypport/business/entities/identity/domain/PartyIdentifierRepository.java
- src/main/java/com/gypport/business/entities/identity/infrastructure/persistence/jdbc/JdbcMdmPartyRepository.java
- src/main/java/com/gypport/business/entities/identity/infrastructure/persistence/jdbc/JdbcPartyIdentifierRepository.java
- src/main/java/com/gypport/business/entities/party/infrastructure/persistence/jdbc/JdbcTenantPartyRepository.java
- src/test/java/com/gypport/business/entities/application/AddPartyIdentifierUseCaseTest.java
- src/test/java/com/gypport/business/entities/application/GetPartyProfileUseCaseTest.java
- src/test/java/com/gypport/business/entities/identity/domain/MdmPartyTest.java
- src/test/java/com/gypport/business/entities/identity/infrastructure/persistence/jdbc/JdbcMdmPartyRepositoryTest.java
- src/main/java/com/gypport/business/entities/application/CreateIdentifiedPersonUseCase.java
- src/main/java/com/gypport/business/entities/application/IdentifierResolution.java
- src/main/java/com/gypport/business/entities/identity/application/CanonicalIdentityPort.java
- src/main/java/com/gypport/business/entities/identity/application/IdentityAccountLinkPort.java
- src/main/java/com/gypport/business/entities/identity/application/IdentityClaim.java
- src/main/java/com/gypport/business/entities/identity/application/IdentityClaimRepository.java
- src/main/java/com/gypport/business/entities/identity/application/IdentityClaimService.java
- src/main/java/com/gypport/business/entities/identity/application/TrustedIdentityVerificationPort.java
- src/main/java/com/gypport/business/entities/identity/infrastructure/persistence/jdbc/JdbcCanonicalIdentityPort.java
- src/main/java/com/gypport/business/entities/identity/infrastructure/persistence/jdbc/JdbcIdentityClaimRepository.java
- src/test/java/com/gypport/business/entities/identity/application/IdentityClaimTest.java
- src/test/java/com/gypport/business/entities/identity/infrastructure/persistence/jdbc/CanonicalIdentityResolutionTest.java

Archivos Gystigo (23, incluido este informe):
- platform_os/server/src/main/java/com/gypport/server/module/expenses/ExpensePersonController.java
- platform_os/server/src/main/java/com/gypport/server/module/expenses/ExpensePersonDirectory.java
- platform_os/server/src/main/java/com/gypport/server/module/onboarding/application/RegisterPersonAccountUseCase.java
- platform_os/server/src/main/java/com/gypport/server/module/profile/controller/MeProfileController.java
- platform_os/server/src/main/java/com/gypport/server/module/tenant/controller/AuthController.java
- platform_os/server/src/main/java/com/gypport/server/shared/config/OnboardingConfig.java
- platform_os/server/src/main/java/com/gypport/server/shared/config/SecurityConfig.java
- platform_os/server/src/test/java/com/gypport/server/module/profile/MyProfileHostIntegrationTest.java
- platform_os/studio/channel/browser/shell/src/App.jsx
- platform_os/studio/channel/browser/shell/src/application/expenses/components/PersonSelector.jsx
- platform_os/studio/channel/browser/shell/src/application/profile/ProfilePage.jsx
- database/core/migration/V26__canonical_person_identity_claims.sql
- platform_os/server/src/main/java/com/gypport/server/module/identity/repository/IdentityAccountLinkAdapter.java
- platform_os/server/src/main/java/com/gypport/server/module/onboarding/application/IdentityValidationRequiredException.java
- platform_os/server/src/main/java/com/gypport/server/module/profile/application/ProfileIdentityService.java
- platform_os/server/src/main/java/com/gypport/server/module/profile/controller/IdentityPrecheckController.java
- platform_os/server/src/main/java/com/gypport/server/shared/config/IdentityClaimConfig.java
- platform_os/server/src/test/java/com/gypport/server/module/profile/PersonIdentityReconciliationHttpTest.java
- platform_os/studio/channel/browser/shell/src/application/onboarding/RegistrationIdentityPrecheck.jsx
- platform_os/studio/channel/browser/shell/src/application/profile/IdentityCompletion.css
- platform_os/studio/channel/browser/shell/src/application/profile/identityService.js
- database/core/migration/V27__reuse_canonical_identity_claims.sql
- docs/ai/handoffs/codex-to-review/GM_ENTITIES_MVP_PERSON_IDENTITY_AND_LEGACY_RECONCILIATION_01.md

El staging usa listas literales, nunca git add .; se comprueban nombres, diff --cached --check y equivalencia del blob indexado con el archivo revisado. Los 33 archivos visuales se mantienen fuera del índice, con los mismos hashes previos. Build/pruebas frontend corresponden al workspace combinado con esos borradores preservados, no a un checkout limpio sin ellos.

La siguiente acción queda indicada solamente: GM_ENTITIES_MVP_PERSON_DIRECTORY_ADMIN_02. No se inicia administración de Personas, relaciones laborales ni invitaciones/RBAC.
