# GM_FLEETS_MINIMUM_VEHICLE_MASTER_01

PEGAR EN: CHATGPT / CLAUDE - evidencia de implementación para revisión independiente.

```text
TRACK=GYPPORT-MVP-GENERAL-01
STEP=GM_FLEETS_MINIMUM_VEHICLE_MASTER_01
MODE=CONTROLLED_IMPLEMENTATION_WITH_LOCAL_COMMITS
AGENT=CODEX
IMPLEMENTATION_AND_ACCEPTANCE=PASS
INDEPENDENT_AUDIT=NOT_PERFORMED
OWNER_SCOPE_APPROVAL=YES (solicitud explícita de este STEP)
PUSH_AUTHORIZED=NO
REMOTE_CHANGES_AUTHORIZED=NO
DESTRUCTIVE_RESET_PERFORMED=NO
```

## Continuidad y alcance

Repositorios comprobados bajo `D:/NZXTG7/GYPPORT/GYPPORT ERP/GYPPORT`:

- `Modules/gm-fleets`: bootstrap inicial, HEAD inicial `8fccd393ed35e58a0571c6b367287b47905d21f3`.
- `Gystigo`: HEAD inicial `afcba71ec75070992677e41197c2b48bbca01cde`.
- Rama local de ambos: `feature/gm-fleets-minimum-vehicle-master-01`.

Este informe se prepara para los commits locales autorizados. Los hashes finales
se informan tras el commit en la respuesta del STEP; no se declara auditoría
independiente ni publicación. La decisión vigente es implementar únicamente
Vehicle mínimo; la integración con gastos queda expresamente excluida.

## Cambios y límites

`gm-fleets` es un JAR Java 25. Vehicle contiene VehicleId, TenantId, Plate y Brand.
Los únicos datos funcionales son placa y marca. La placa es obligatoria,
`strip()` + mayúsculas con `Locale.ROOT`, máximo 40 caracteres y sin patrón
nacional restrictivo. Marca es texto obligatorio, `strip()`, máximo 120.
La validación ocurre antes de invocar el puerto de persistencia.

Domain/Application no importan Spring/JDBC. El adaptador JDBC recibe la operación
del Host, vincula tenant en toda consulta y traduce DataAccessException a errores
del módulo. No contiene DataSource, driver, gestor transaccional, JPA ni runtime
Flyway propio. Un INSERT es la unidad atómica de creación. No depende de
gm-expenses ni crea FK desde gastos.

Se descubrió V21 como última versión existente antes de crear
`database/modules/gm-fleets/migration/V22__gm_fleets_minimum_vehicle_master.sql`.
V22 crea `fleet_vehicle(vehicle_id, tenant_id, plate, brand, created_at)`, FK a
tenants y unicidad `(tenant_id, plate)`. No se editaron migraciones históricas.
Agrega exclusivamente `fleets.vehicle.read` y `fleets.vehicle.create` y los
concede a roles OWNER canónicos activos existentes. OnboardingConfig los incluye
en el bootstrap explícito de nuevos OWNER.

El Host incorpora configuración de beans, dependencia JAR y recurso Flyway.
Dockerfile, contexto Compose y .dockerignore incluyen el módulo y su migración.
`GET /api/fleets/vehicles` lista y `POST /api/fleets/vehicles` crea. El tenant
procede de AuthenticatedRequestContextFactory; POST rechaza propiedades adicionales
(incluyendo tenantId/organizationId) y responde 400 para entradas inválidas,
409 para placa duplicada y 403 sin permiso. La respuesta solo expone id/plate/brand.
GET materializa la cookie CSRF diferida para el primer POST del navegador, sin
desactivar ni alterar SecurityConfig.

Studio incorpora `/fleets/vehicles` en la composición de navegación existente,
filtrada por permiso, con listado, estado vacío, formulario de dos campos,
guardar/cancelar, error y confirmación. Se habilita navegación de Inicio y el
cierre del drawer móvil al navegar. No se agrega acceso al header superior.
No hay edición, eliminación ni integración con gm-expenses.

## Pruebas automatizadas y runtime

| Verificación final | Resultado |
|---|---|
| gm-fleets Maven test/install | 15 ejecutadas, 0 fallos/errores |
| Host Maven reactor server + dependencias | 222 contabilizadas, 165 ejecutadas, 57 omitidas, 0 fallos/errores |
| GmFleetsHttpApiTest incluido en Host | 5 ejecutadas contra MySQL real aislado, todas PASS |
| Studio contracts | 215 pruebas, 24 archivos, PASS |
| Studio lint y build | PASS |
| Docker build backend y arranque DEV | PASS |
| FRESH_DB_BOOTSTRAP | PASS: B17, V18, V19, V20, V21, V22 aplicadas por Flyway |
| EXISTING_DEV_DB_VALIDATE | PASS: 23 migraciones validadas, versión 22, sin pendientes |

Comandos base: Maven 3.9.16/JDK 25 `-f Modules/gm-fleets/pom.xml test install`;
`-f Gystigo/platform_os/pom.xml -pl server -am test`; desde Gystigo,
`npm run contracts`, `npm run lint` y `npm run build`, cada uno con
`--workspace=@gypport/platform-os-browser-shell`; desde Gystigo/docker,
`docker compose build backend` y `docker compose up -d --no-deps backend`.

La suite SQL está opt-in con `GYPPORT_FLEETS_REAL_DB_TESTS=true` y una URL fija
de pruebas `jdbc:mysql://127.0.0.1:3310/core_business_fleets_test`; credenciales
se suministran por entorno y no están versionadas. Se registran, verifican e
inician sesión cuentas sintéticas por los endpoints normales. Los casos prueban
PERSONAL sin organización, creación/listado/normalización, unicidad, tenant
aislado con placa reutilizable, entradas inválidas, autenticación, permisos y
CSRF. Cada transacción revierte sus datos. Consulta posterior: 0 cuentas y
0 vehículos en la base de pruebas; contenedor temporal detenido, sin borrar
contenedor ni volumen.

## Aceptación visual y datos DEV

Cuenta PERSONAL nueva creada mediante registro normal, verificación Mailpit y
login, sin SQL manual de provisión. Se creó `ABC-1234 / Chevrolet` desde desktop
y `PBC-5678 / Toyota` desde móvil. Se comprobó el rechazo visible del duplicado
`abc-1234`, cancelación y recuperación del listado persistido al volver a entrar.

- PERSONAL_CREATE_VEHICLE=PASS; PERSONAL_LIST_VEHICLES=PASS.
- DUPLICATE_PLATE=PASS; CROSS_TENANT=PASS (suite Host/MySQL real).
- DESKTOP_WEB=PASS (1440 x 900); MOBILE_WEB=PASS (390 x 844).
- Formulario/listado móvil: scrollWidth=390, viewport=390; drawer abre y cierra al navegar.
- RUC_REQUIRED=NO; ORGANIZATION_REQUIRED=NO; MANUAL_SQL_REQUIRED=NO.
- Consola tras recarga final: sin nuevos errores/advertencias.

Capturas inspeccionadas visualmente en la carpeta local de evidencia
`C:/Users/elbur/.codex/visualizations/2026/08/30/01a05471-5d5b-7400-98b0-77b7b0304670/`:
`fleets-desktop-final.png`, `fleets-desktop-duplicate.png`,
`fleets-mobile-form.png`, `fleets-mobile-list.png`, `fleets-mobile-navigation.png`.
Estas capturas locales no se incorporan al repositorio.

DEV conserva su cuenta previa y agrega una cuenta sintética de QA con dos
vehículos en su tenant. Consulta final: 2 cuentas totales, 2 vehículos únicamente
en tenant 2, 0 organizaciones. No se eliminan datos de QA mediante reset o SQL
manual. No se imprimen credenciales, códigos de verificación ni datos del usuario
preexistente en este informe.

## Incidencias resueltas y límites de evidencia

El primer build Docker falló porque .dockerignore excluía la nueva migración;
se añadió la excepción acotada y el build posterior pasó. La primera creación
visual encontró la cookie CSRF diferida; se corrigió el GET y se agregó una
regresión con cookie/header reales, sin `csrf()` simulado en ese POST. La primera
ejecución de esa regresión falló por contaminación del repositorio CSRF de
MockMvc entre pruebas; un contexto fresco para ese caso resolvió el aislamiento.
La ejecución final completa pasó. Hubo advertencias HMR durante la reconstrucción
de design_system/dist; después del build y recarga no aparecieron errores nuevos.
Las denegaciones de acceso del sandbox a Docker/Maven/Git se gestionaron mediante
las autorizaciones correspondientes; no constituyen evidencia de prueba exitosa.

El Dashboard general muestra un aviso de contexto seguro al entrar con esta
cuenta y la recarga completa devuelve al login del shell existente. Vehículos
funciona desde la navegación tras login. No se alteraron estos comportamientos
del shell/Dashboard ni se declara su aceptación fuera del alcance de este STEP.

Las capturas y el build se realizaron sobre el checkout que ya contenía siete
archivos de presentación modificados por el usuario. Permanecen fuera de estos
commits: Button.tsx, tokens.css, AuthPage.css, DashboardHost.css, DashboardHost.jsx,
ShortRegisterPage.jsx y StudioLayout.css. Sus bytes, y 23 archivos SQL previos,
se verificaron contra los hashes de entrada (30/30 idénticos). La aceptación
visual describe ese checkout; no una revisión independiente del estilo en HEAD.

## Cierre y próximo alcance

Staging por lista literal: solo el módulo mínimo y su integración Host/Studio,
pruebas y este informe. Sin staging de archivos protegidos. Dos commits locales
previstos, uno por repositorio; sin push, remotos ni cambios destructivos.

NEXT_EXACT_ACTION=INTEGRATE_GM_FLEETS_VEHICLE_AS_EXPENSE_CASE_ASSOCIATED_RESOURCE

Este es el siguiente alcance indicado por el Owner, no autorización para
ejecutarlo en el STEP actual. STOP: integración con gastos no implementada.
