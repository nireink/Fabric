# DATABASE_EXTRACTION_SCOPE_AUDIT_2026-07-26


> **NOTA DE ESTADO (agregada en verificación posterior, 2026-07-26):** La extracción de 8 archivos recomendada en este informe fue ejecutada directamente por el Architecture Owner en el commit `595f0d4` (`refactor(database): extract canonical database assets`), verificada bit a bit contra los SHA-256 de la Tarea 5, y confirmada en runtime en el Step `02.1` (ver `DATABASE_EXTRACTION_SCOPE_AUDIT_02_1_RUNTIME_VERIFICATION_2026-07-26.md`). Este documento ya no describe trabajo pendiente de implementación por Codex; queda como registro histórico de la auditoría que precedió y coincide con el cambio ya aplicado.

Track: DATABASE-EXTRACTION-SCOPE-AUDIT-02
Mode: READ-ONLY ESTRICTO (ningún archivo fue creado, movido, eliminado, compilado, commiteado ni publicado — con la única excepción de este informe)
Repositorio auditado: `D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT\Gystigo`
Excluido: `D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT\UI_Experiments` (no inspeccionado)

---

## TAREA 0 — PUERTA DE ENTORNO

| Verificación | Esperado | Observado | Resultado |
|---|---|---|---|
| Raíz Git | `.../GYPPORT/Gystigo` | `D:/NZXTG7/GYPPORT/GYPPORT ERP/GYPPORT/Gystigo` | ✅ COINCIDE |
| HEAD | `67cfdd1` | `67cfdd129db36de32484dcfe9508e9bf29bbe612` (short: `67cfdd1`) | ✅ COINCIDE |
| Working tree | limpio | `git status --porcelain=v1` sin salida | ✅ COINCIDE |
| Divergencia `origin/master...HEAD` | `0/0` | `0 0` | ✅ COINCIDE |

**Resultado de la puerta:** los cuatro checks de Tarea 0 coinciden con el contexto confirmado. No se detiene con `ENVIRONMENT BLOCKED`.

**Hallazgo adicional no cubierto por Tarea 0 (documentado, no bloqueante para el resto del análisis, pero sí relevante para el veredicto):** el "FOUNDATION DOCUMENT" indicado —`GYPPORT_Governance_Architecture/standards/DATABASE_MIGRATION_STANDARD.md`— **no existe dentro del repositorio `Gystigo`**. Existe en una ruta hermana fuera del repositorio auditado:

```
D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT\Governance\GYPPORT_Governance_Architecture\standards\DATABASE_MIGRATION_STANDARD.md
```

Fue leído íntegramente desde esa ubicación externa. Su contenido es plenamente consistente con el mapeo de extracción y con el contexto confirmado de esta auditoría (mismo mapeo Origen→Destino, mismo punto único de re-cableo en `docker/compose.yaml`). Se reporta como discrepancia de ruta, no como bloqueo de contenido.

---

## TAREA 1 — AUDITORÍA SEMÁNTICA DE LAS 21 REFERENCIAS

Búsqueda ejecutada sobre patrones `platform_os/server/database`, `src/main/resources/db/migration`, `db/migration` en los cuatro archivos indicados. Conteo verificado: `AGENTS.md`=8, `docker/README.md`=1, `docs/project/GYPPORT_MASTER_PROJECT_CONTEXT.md`=11, `docker/compose.yaml`=1 → **21 coincidencias totales**, consistente con "20 referencias adicionales" (fuera de compose.yaml) + 1 en compose.yaml.

### `docker/compose.yaml`

| # | Línea | Clasificación | Texto actual | Reemplazo exacto |
|---|---|---|---|---|
| 1 | 15 | **A — operativa vigente** | `- ../platform_os/server/src/main/resources/db/migration:/docker-entrypoint-initdb.d:ro` | `- ../database/core/migration:/docker-entrypoint-initdb.d:ro` |

Razón: es el único punto real de re-cableo funcional. El propio `DATABASE_MIGRATION_STANDARD.md` §1 lo identifica como "único punto de re-cableo necesario". Sin este cambio, Docker montaría un directorio que ya no contiene los `.sql`.

### `docker/README.md`

| # | Línea | Clasificación | Texto actual | Reemplazo exacto |
|---|---|---|---|---|
| 2 | 13 | **A — operativa vigente** | `platform_os/server/src/main/resources/db/migration/` | `database/core/migration/` |

Contexto (líneas 9-14): "Docker no es propietario de las migraciones de GYPPORT®. Las fuentes SQL canónicas permanecen en: `platform_os/server/src/main/resources/db/migration/`". Es una declaración de la ubicación *actual* de la fuente canónica, no un registro histórico — debe actualizarse junto con el compose.

Nota adicional (línea 31, sin cambio de ruta, clasificación **C**): "La inspección actual no encontró Flyway ni otro motor de migraciones activo en el backend." Esta frase sigue siendo verificable como cierta hoy (ver Tarea 2) y no requiere modificación.

### `AGENTS.md` (8 coincidencias)

| # | Línea | Clasificación | Texto actual | Reemplazo exacto |
|---|---|---|---|---|
| 3 | 157 | **A** | `platform_os/server/database/` (listado de áreas) | `database/core/` |
| 4 | 158 | **A** | `platform_os/server/src/main/resources/db/migration/` (listado de áreas) | `database/core/migration/` |
| 5 | 163 | **A** | `` `platform_os/server/database/` is for database evidence and analysis. `` | `` `database/core/` is for database evidence and analysis. `` |
| 6 | 165 | **A** | `` `platform_os/server/src/main/resources/db/migration/` is for executable Business SQL migrations, such as Flyway migrations. `` | `` `database/core/migration/` is for executable Business SQL migrations, such as Flyway migrations. `` |
| 7 | 243 | **A** | `platform_os/server/database/baseline/core_business_dev_20260709_schema_only.sql` (bloque "Current expected DB-01 files") | `database/core/baseline/core_business_dev_20260709_schema_only.sql` |
| 8 | 244 | **A** | `platform_os/server/database/analysis/MASTER_DATABASE_ORIGIN_ANALYSIS.md` | `database/core/analysis/MASTER_DATABASE_ORIGIN_ANALYSIS.md` |
| 9 | 245 | **A** | `platform_os/server/src/main/resources/db/migration/V1__core_business_baseline.sql` | `database/core/migration/V1__core_business_baseline.sql` |
| 10 | 246 | **A** | `platform_os/server/src/main/resources/db/migration/V2__core_reference_seed_data.sql` | `database/core/migration/V2__core_reference_seed_data.sql` |

Razón común (#3-10): `AGENTS.md` describe áreas de implementación vigentes y el STEP DB-01 (líneas 120-259) en presente/futuro operativo, no como bitácora histórica. Son referencias operativas que un agente (Codex u otro) usaría literalmente para saber dónde escribir o verificar archivos — deben reflejar la ubicación real tras el movimiento.

**No propongo reemplazo global ciego**: el bloque de líneas 129-138 (`platform_os/server/` como directorio protegido para "external Studio capability work") **no coincidió** con los patrones buscados como ruta de migración/database, pero contiene `platform_os/server/` como boundary de protección general del backend — ese `platform_os/server/` genérico se conserva sin cambio (clasificación **C**), porque sigue siendo cierto: el backend Java/Spring Boot permanece en `platform_os/server/`; solo su carpeta `database/` y `src/main/resources/db/migration/` se extraen.

### `docs/project/GYPPORT_MASTER_PROJECT_CONTEXT.md` (11 coincidencias)

| # | Línea | Clasificación | Texto actual | Reemplazo exacto |
|---|---|---|---|---|
| 11 | 93 | **A** | `platform_os/server/database/` (listado "Áreas de implementación") | `database/core/` |
| 12 | 94 | **A** | `platform_os/server/src/main/resources/db/migration/` | `database/core/migration/` |
| 13 | 100 | **A** | `` `platform_os/server/database` contiene evidencia histórica/análisis de base de datos. `` | `` `database/core` contiene evidencia histórica/análisis de base de datos. `` |
| 14 | 101 | **A** | `` `platform_os/server/src/main/resources/db/migration` contiene migraciones SQL ejecutables por Flyway. `` | `` `database/core/migration` contiene migraciones SQL ejecutables por Flyway (activación de Flyway aún pendiente — ver DB-02). `` |
| 15 | 480 | **A** | `` `platform_os/server/database/baseline/` contiene evidencia histórica estructural auditada... `` | `` `database/core/baseline/` contiene evidencia histórica estructural auditada... `` |
| 16 | 483 | **A** | `` `platform_os/server/database/analysis/` contiene análisis persistente del modelo real... `` | `` `database/core/analysis/` contiene análisis persistente del modelo real... `` |
| 17 | 487 | **A** | `` `platform_os/server/src/main/resources/db/migration/` contiene migraciones SQL ejecutables del backend. Esta ruta pertenece al runtime Spring Boot/Flyway... `` | `` `database/core/migration/` contiene migraciones SQL ejecutables del backend. Esta ruta es la fuente canónica montada por Docker; no pertenece al classpath del runtime Spring Boot (ver Tarea 2). `` |
| 18 | 504 | **A** | `platform_os/server/database/baseline/core_business_dev_20260709_schema_only.sql` | `database/core/baseline/core_business_dev_20260709_schema_only.sql` |
| 19 | 505 | **A** | `platform_os/server/database/analysis/MASTER_DATABASE_ORIGIN_ANALYSIS.md` | `database/core/analysis/MASTER_DATABASE_ORIGIN_ANALYSIS.md` |
| 20 | 506 | **A** | `platform_os/server/src/main/resources/db/migration/V1__core_business_baseline.sql` | `database/core/migration/V1__core_business_baseline.sql` |
| 21 | 507 | **A** | `platform_os/server/src/main/resources/db/migration/V2__core_reference_seed_data.sql` | `database/core/migration/V2__core_reference_seed_data.sql` |

Razón común (#11-21): mismo patrón que `AGENTS.md` — es la versión en inglés/español del mismo documento de contexto de proyecto, con el mismo bloque "Áreas de implementación" y el mismo STEP DB-01. Todas son referencias operativas vigentes.

**Matiz importante en #14 y #17**: el texto actual afirma que la ruta "contiene migraciones SQL ejecutables **por Flyway**" / "pertenece al runtime Spring Boot/Flyway". La Tarea 2 confirma que **Flyway no está configurado hoy** (ni en el pom.xml ni en application.yaml, tras el merge appmod a Spring Boot 4.1.0). Esta frase describe el **destino previsto** (DB-02, "Flyway activation pending", confirmado en `docs/project/CODEX_PROJECT_CONTEXT_GYPPORT.md` línea 36), no el estado actual de ejecución. No es una contradicción que requiera corrección urgente, pero el reemplazo propuesto para la línea 487 aclara explícitamente que hoy no hay classpath/Flyway real, para que no se lea como afirmación de hecho presente. Se deja como ajuste editorial sugerido, no obligatorio.

**Coincidencia sin patrón de ruta que igual merece mención (clasificación C, no requiere modificación):** `docs/project/CODEX_PROJECT_CONTEXT_GYPPORT.md` líneas 35-36 mencionan "DB-01" y "DB-02 — Flyway activation pending" en prosa, sin ruta de archivo. No coincidió con los patrones de búsqueda de rutas y no requiere cambio como parte de este movimiento.

**No se encontraron referencias tipo B** (histórica que deba conservar la ruta anterior aclarando que era ubicación previa) en estos cuatro archivos: ninguna de las 21 coincidencias está en una sección redactada en pasado/bitácora cerrada; todas describen estado operativo vigente o instrucciones activas para agentes.

---

## TAREA 2 — RIESGO SPRING BOOT / FLYWAY / CLASSPATH

Verificación ejecutada contra el estado **actual** del repositorio (post-merge appmod), no contra el hallazgo de la auditoría previa a ese merge.

**Evidencia inspeccionada:**
- `platform_os/server/pom.xml` — parent `spring-boot-starter-parent` versión **4.1.0** (confirma que el merge appmod ya aplicó). Dependencias: `spring-boot-starter-jdbc`, `-security`, `-validation`, `-web`, `mysql-connector-j` (runtime), `-test`, `spring-security-test`. **Cero** referencias a `flyway-core`, `flyway-mysql` o cualquier artefacto Flyway. Sin sección `<resources>`/`<testResources>` — se aplica el manejo de recursos por defecto de Maven.
- `platform_os/server/src/main/resources/application.yaml` (único archivo `application*` existente en el módulo, no hay variantes por perfil): solo contiene `spring.application.name` y `spring.datasource.{url,username,password}`. **Cero** claves `spring.flyway.*`, `spring.sql.init.*`, `schema.sql`/`data.sql`.
- Código Java (`grep` recursivo en `platform_os/server/src`): **cero** ocurrencias de `Flyway`, `classpath:db/migration`, `db.migration`, `DataSourceInitializer`, `ScriptUtils`, `sql.init`.
- Tests del backend (`platform_os/server/src/test`): **cero** referencias a `db/migration`, `database/baseline`, `database/analysis` o `Flyway`.
- `platform_os/server/Dockerfile`: build multi-stage que hace `COPY src src` y `./mvnw ... package`; solo copia `src/`, `pom.xml`, `mvnw`, `.mvn` — nunca copia `database/`. El contexto de build en `docker/compose.yaml` (`context: ../platform_os/server`) confirma que el build del backend está delimitado a ese subárbol.
- `docker/compose.yaml`: dos servicios — `mysql` (monta `.../db/migration` en `/docker-entrypoint-initdb.d:ro`) y `backend` (build desde `platform_os/server/Dockerfile`, sin volumen de migraciones).
- Workflows (`.github/modernize/java-upgrade/hooks/scripts/*.ps1`, `*.sh`): son hooks de la herramienta de modernización de Java del propio appmod, no referencian rutas de migración/base de datos.
- Documentación operativa: `docker/README.md` línea 31 y `docs/project/CODEX_PROJECT_CONTEXT_GYPPORT.md` línea 36 confirman explícitamente, en prosa, que Flyway está pendiente de activación (DB-02), no activo.

**Respuestas explícitas:**

1. **¿El backend usa Flyway realmente o únicamente la inicialización de MySQL Docker?**
   Únicamente la inicialización de MySQL Docker (`docker-entrypoint-initdb.d`, ejecución de una sola vez al crear un volumen vacío). No hay Flyway ni ningún motor de migración activo en el backend, hoy, con Spring Boot 4.1.0.

2. **¿Existe una dependencia implícita de `classpath:db/migration`?**
   No en el sentido de configuración Flyway (no hay Flyway). Existe únicamente una inclusión implícita por convención de Maven: al no haber `<resources>` con exclusiones, todo `src/main/resources/**` —incluyendo `db/migration/`— se copia a `target/classes` y de ahí al JAR. Ningún código lee esos archivos desde el classpath en tiempo de ejecución.

3. **¿V1 y V2 se incluyen actualmente dentro del JAR?**
   Sí, como recurso de classpath sin uso (`db/migration/V1__core_business_baseline.sql`, `V2__core_reference_seed_data.sql` terminan en `BOOT-INF/classes/db/migration/` dentro del jar ejecutable), por el comportamiento por defecto de Maven, no por configuración explícita.

4. **¿Dejarían de incluirse después del movimiento?**
   Sí. Al mover los `.sql` fuera de `platform_os/server/src/main/resources/`, dejan de estar bajo el árbol de recursos de Maven de ese módulo y ya no se empaquetarían en el JAR.

5. **¿El backend seguiría compilando, testeando, empaquetando y arrancando?**
   Sí. Ningún código, test, o configuración del backend referencia esos archivos por ruta o por classpath. Su ausencia del JAR no afecta compilación, tests, empaquetado ni arranque.

6. **¿Docker seguiría inicializando correctamente una base nueva?**
   Sí, **condicionado exclusivamente** a actualizar la línea de volumen en `docker/compose.yaml` (Tarea 1, hallazgo #1) para apuntar a `../database/core/migration`. El mecanismo de MySQL (`docker-entrypoint-initdb.d`) lee directamente del filesystem del host vía bind mount, no del JAR ni del classpath — por eso el movimiento es transparente para Docker una vez re-cableado el volumen.

7. **¿Hace falta modificar `pom.xml` o alguna configuración adicional?**
   No. No existe hoy ninguna configuración Flyway o de recursos que referencie esa ruta desde Maven/Spring. El único archivo que requiere modificación técnica real es `docker/compose.yaml`.

8. **¿Cuál es el mecanismo mínimo y portable para conservar una única fuente canónica, sin duplicar V1 y V2?**
   Mover físicamente los dos archivos una sola vez a `database/core/migration/` (fuera de `platform_os/server/`) y re-apuntar únicamente el volumen de `docker/compose.yaml` a esa ruta. **No** introducir un paso de Maven (`maven-resources-plugin`, `build-helper-maven-plugin`, etc.) que copie o vuelva a incluir esos archivos en `src/main/resources/db/migration`, porque eso recrearía exactamente la duplicación que se busca evitar y un riesgo de drift entre dos copias. Cuando se active Flyway real (DB-02), la ubicación fuera del classpath del módulo es compatible: Flyway se puede configurar con `spring.flyway.locations=filesystem:<ruta-absoluta-o-resuelta-en-runtime>` apuntando a `database/core/migration` (o a una copia entregada por el propio proceso de despliegue/imagen), sin volver a depender de `classpath:db/migration`. Ese diseño queda fuera del alcance de este movimiento y debe tratarse como parte de la implementación de DB-02, no de esta extracción de carpetas.

**Conclusión de Tarea 2:** el movimiento de V1/V2 a `database/core/migration/` es seguro para el backend Spring Boot actual. El único cambio técnico obligatorio fuera de los `git mv` es la línea 15 de `docker/compose.yaml`. No se requiere ningún cambio en `pom.xml`, `application.yaml`, código Java, ni tests.

---

## TAREA 3 — BÚSQUEDA AMPLIADA DE DEPENDENCIAS

Búsqueda read-only ejecutada sobre todo el repositorio, excluyendo `.git`, `node_modules`, `target`, `UI_Experiments`, para los términos solicitados. Resultado consolidado:

| Término | Archivos con coincidencia (fuera de los 4 ya auditados) |
|---|---|
| `platform_os/server/database` | (cubierto en Tarea 1) |
| `src/main/resources/db/migration` / `db/migration` | (cubierto en Tarea 1) + `platform_os/server/src/main/java/.../UserAccountJdbcRepository.java:18` (ver abajo) |
| `V1__core_business_baseline.sql` | Igual que arriba (Javadoc) |
| `V2__core_reference_seed_data.sql` | Ninguna adicional |
| `core_business_dev_20260709_schema_only.sql` | Ninguna adicional dentro del árbol principal |
| `MASTER_DATABASE_ORIGIN_ANALYSIS.md` | Ninguna adicional dentro del árbol principal |

**Hallazgo de código (referencia implícita, no de ruta):** `platform_os/server/src/main/java/com/gypport/server/module/identity/repository/UserAccountJdbcRepository.java`, línea 18, Javadoc:
> "...Trabaja contra el esquema canónico de `user_accounts` definido en la migración `V1__core_business_baseline.sql` (columnas...)"

Clasificación: **C — no requiere modificación**. Es una referencia por *nombre de archivo* dentro de un comentario Javadoc, para documentar el contrato de columnas, no una ruta de filesystem ni una dependencia de classpath. El archivo `V1__core_business_baseline.sql` conserva su nombre y contenido tras el movimiento; el comentario sigue siendo exacto.

**Hallazgo fuera del árbol principal (informativo, fuera de alcance de la extracción):** existen copias de `MASTER_DATABASE_ORIGIN_ANALYSIS.md` y `core_business_dev_20260709_schema_only.sql` dentro de:
```
.claude/worktrees/aiws-004-p1-2-review-725e05/gypport/platform_os/server/database/...
.claude/worktrees/dashboard-engine-gypport-eee073/gypport/platform_os/server/database/...
.claude/worktrees/gypport-aiws-003-review-d1ce8e/gypport/platform_os/server/database/...
.claude/worktrees/gypport-master-database-4e6dfa/gypport/platform_os/server/database/...
.claude/worktrees/login-files-repair-01367d/gypport/platform_os/server/database/...
```
Estos son **git worktrees independientes** (checkouts de otras ramas/sesiones previas de agentes), cada uno con su propio árbol de trabajo. No son parte del HEAD `67cfdd1` que se está auditando y **no deben tocarse** como parte de esta extracción — un `git mv` en el worktree principal no los afecta ni ellos afectan la validez de este movimiento. Se reportan únicamente porque el patrón de búsqueda los alcanzó; no se abrieron ni inspeccionaron más allá de confirmar su existencia y ruta.

**No se encontraron** referencias en: `.github/` workflows reales (solo hooks del appmod de Java, sin relación), Dockerfiles (`platform_os/server/Dockerfile` no referencia estas rutas), scripts PowerShell/Bash/CMD/Node del repositorio, ni configuración de recursos Maven adicional (no existe `<resources>` en el único `pom.xml` del repo).

**Distinción explícita/implícita:**
- **Explícitas** (deben editarse): las 21 rutas de Tarea 1.
- **Implícita por convención Maven** (no requiere edición, pero cambia de comportamiento): inclusión de `db/migration/*.sql` en el JAR vía default resource handling (ver Tarea 2, preguntas 2-4).
- **Implícita por convención Docker Compose** (requiere edición): el bind mount de la línea 15, ya cubierto como referencia A en Tarea 1.

---

## TAREA 4 — BOUNDARY FINAL DE IMPLEMENTACIÓN

Boundary exacto autorizable para una futura implementación (Codex), basado en la evidencia de Tareas 1-3:

**Archivos a mover vía `git mv` (4):**
1. `platform_os/server/src/main/resources/db/migration/V1__core_business_baseline.sql` → `database/core/migration/V1__core_business_baseline.sql`
2. `platform_os/server/src/main/resources/db/migration/V2__core_reference_seed_data.sql` → `database/core/migration/V2__core_reference_seed_data.sql`
3. `platform_os/server/database/baseline/core_business_dev_20260709_schema_only.sql` → `database/core/baseline/core_business_dev_20260709_schema_only.sql`
4. `platform_os/server/database/analysis/MASTER_DATABASE_ORIGIN_ANALYSIS.md` → `database/core/analysis/MASTER_DATABASE_ORIGIN_ANALYSIS.md`

**Archivos a editar (3, contenido — no ruta):**
5. `docker/compose.yaml` — línea 15, único re-cableo técnico obligatorio.
6. `AGENTS.md` — 8 líneas (157, 158, 163, 165, 243-246).
7. `docs/project/GYPPORT_MASTER_PROJECT_CONTEXT.md` — 11 líneas (93, 94, 100, 101, 480, 483, 487, 504-507).

**Archivo a editar (1, opcional/menor):**
8. `docker/README.md` — línea 13.

**No se amplía el boundary a:**
- `platform_os/server/pom.xml` — Tarea 2 confirmó que no requiere cambio (no hay Flyway, no hay `<resources>` que excluir/incluir).
- `platform_os/server/src/main/resources/application.yaml` — sin referencias.
- Código Java / tests — sin referencias de ruta (solo el comentario Javadoc por nombre de archivo, que no requiere cambio).
- `platform_os/server/Dockerfile` — sin referencias.
- `docs/project/CODEX_PROJECT_CONTEXT_GYPPORT.md` — coincidencia solo en prosa sobre Flyway/DB-02, sin ruta; no requiere cambio como parte de este movimiento.

**Total boundary mínimo: 8 archivos** (4 movidos + 4 editados). Esto coincide con el boundary mínimo candidato original ampliado únicamente con `docker/README.md`, que sí contiene una referencia operativa de ruta (Tarea 1, hallazgo #2) y por tanto es indispensable, no opcional.

---

## TAREA 5 — VALIDACIONES POSTERIORES PROPUESTAS

Codex debe ejecutar, en este orden, tras la implementación:

1. **Historial preservado:** `git log --follow --oneline -- database/core/migration/V1__core_business_baseline.sql` (y análogos para los otros 3 archivos) debe mostrar el historial previo a través del `git mv`.
2. **Rutas antiguas ausentes:** confirmar que las 4 rutas de origen ya no existen (`test -e <ruta_antigua>` debe fallar para cada una).
3. **Rutas nuevas presentes con SHA-256 idéntico:**
   - `V1__core_business_baseline.sql` = `7c48fad3b5a702a97ab90e9cd9150642074a5eaf22d9605562d01639e0366ba1`
   - `V2__core_reference_seed_data.sql` = `ae5f5a454b789afadeb436ede0adf70fc0522df73ed6cbcf313b1b7cc96b9abd`
   - `core_business_dev_20260709_schema_only.sql` = `112110d13fb563bb959459d61f5d2bafb236b8b59136a038c9472dd7b1a7b3cf`
   - `MASTER_DATABASE_ORIGIN_ANALYSIS.md` = `05f580bcb503f64153a26fee0f54e05a6dfbad0734d5b6fc9ee2459bdb5b5a31`
   (SHA-256 calculados en esta auditoría contra el estado actual en HEAD `67cfdd1`; deben coincidir bit a bit tras el `git mv`.)
4. **Sin referencias operativas obsoletas:** re-ejecutar la búsqueda de Tarea 1/3 sobre el árbol completo (excluyendo `.git`, `node_modules`, `target`, `UI_Experiments`, `.claude/worktrees`) y confirmar cero coincidencias de rutas antiguas fuera de comentarios tipo B (no aplica aquí, no hay tipo B) o del propio Javadoc por nombre de archivo (Tarea 3, que no cambia).
5. **`docker/compose.yaml` apunta a `database/core/migration`:** `grep -n "database/core/migration" docker/compose.yaml` debe encontrar la línea 15 actualizada.
6. **Docker inicializa base nueva:** `docker compose -f docker/compose.yaml up` sobre un volumen `gypport_mysql_dev_data` recién creado (no el existente) debe crear las 57 tablas (V1) y cargar los datos de referencia (V2), verificable con `SHOW TABLES` y conteo de filas en catálogos.
7. **Volumen existente no destruido:** confirmar que el volumen Docker nombrado `gypport_mysql_dev_data` (si ya existe con datos de desarrollo) no se elimina ni se recrea como efecto colateral del cambio de ruta del bind mount — el bind mount solo afecta el origen de los scripts de inicialización, nunca el volumen de datos ya poblado.
8. **Backend compila y testea:** `./mvnw -B -ntp clean verify` (o el goal equivalente) desde `platform_os/server` debe completar sin fallos nuevos atribuibles al movimiento.
9. **JAR conserva o pierde acceso a migraciones según lo esperado:** confirmar (documentar, no bloquear) que `db/migration/*.sql` **ya no** aparece dentro de `target/server-0.0.1-SNAPSHOT.jar` tras el build — es el cambio esperado y aceptado (Tarea 2, pregunta 4), no una regresión.
10. **`UI_Experiments` intacto:** `git status` y `git diff --stat` no deben mostrar ninguna ruta bajo `UI_Experiments/`.

---

## TAREA 6 — ROLLBACK (diseño únicamente, no ejecutar)

1. **Reversión de los 4 `git mv`:** `git mv database/core/migration/V1__core_business_baseline.sql platform_os/server/src/main/resources/db/migration/V1__core_business_baseline.sql` (y análogos para los otros 3), en un único commit de reversión o vía `git revert <commit-de-la-extracción>` si la extracción fue un commit atómico.
2. **Restauración de `docker/compose.yaml`:** revertir la línea 15 a `../platform_os/server/src/main/resources/db/migration:/docker-entrypoint-initdb.d:ro`.
3. **Restauración de documentación y gobernanza:** revertir `AGENTS.md`, `docs/project/GYPPORT_MASTER_PROJECT_CONTEXT.md` y `docker/README.md` a su contenido previo (las 20 líneas + 1 de Tarea 1).
4. **Configuración Maven/Spring:** no aplica — no se modifica ninguna en la implementación propuesta (Tarea 2, pregunta 7), por lo que el rollback en este punto es un no-op verificado, no una acción pendiente.
5. **Protección de volúmenes y datos Docker:** el rollback de código/rutas **no** debe ir acompañado de `docker volume rm gypport_mysql_dev_data` ni de recreación del volumen. Si el volumen ya fue recreado con la nueva ruta antes del rollback, el rollback de código no reconstruye datos perdidos — esto debe quedar explícito como limitación conocida, no resuelto automáticamente.
6. **Prohibición explícita:** el rollback no debe, bajo ninguna circunstancia, eliminar bases de datos, volúmenes Docker con datos reales, ni el contenido de `database/core/` si contiene datos que ya no existen en `platform_os/server/` (es decir, rollback de rutas, no de datos).
7. **Verificación post-rollback:** repetir Tarea 0 (root, HEAD, working tree, divergencia) y confirmar que las 4 rutas originales existen de nuevo con los mismos SHA-256 reportados en Tarea 5.

---

## RESUMEN DE HALLAZGOS CLAVE

- Entorno técnico (Tarea 0, los 4 checks): **coincide** con el contexto confirmado.
- Documento fundacional: existe, pero **fuera** del repositorio auditado (en `GYPPORT/Governance/`, no en `GYPPORT/Gystigo/`). Leído y consistente con el resto de la auditoría.
- Flyway: **confirmado que NO está configurado** hoy, verificado contra el `pom.xml` (Spring Boot **4.1.0**, post-merge appmod) y `application.yaml` actuales — no se asumió el hallazgo de la auditoría previa al merge, se reprodujo desde cero con el mismo resultado.
- 21 referencias clasificadas: **20 tipo A** (operativas, requieren actualización), **0 tipo B**, **1 tipo C** explícita adicional fuera del conteo de rutas (comentario Javadoc) más menciones de prosa sin ruta (docker/README.md línea 31, CODEX_PROJECT_CONTEXT_GYPPORT.md líneas 35-36) que no requieren cambio.
- Riesgo Spring Boot/Flyway/classpath: **bajo**. El movimiento no rompe compilación, tests, empaquetado ni arranque del backend. Único cambio técnico obligatorio: `docker/compose.yaml` línea 15.
- Boundary final: **8 archivos** (4 `git mv` + 4 ediciones: `docker/compose.yaml`, `AGENTS.md`, `docs/project/GYPPORT_MASTER_PROJECT_CONTEXT.md`, `docker/README.md`).
- Hallazgo colateral fuera de alcance: copias de 2 de los 4 archivos existen en 5 git worktrees bajo `.claude/worktrees/`, no forman parte de HEAD y no deben tocarse.

---

## VEREDICTO FINAL

**READY FOR CODEX IMPLEMENTATION**

Condiciones que sustentan el veredicto:
- Los 4 checks técnicos de entorno coinciden exactamente con el contexto confirmado.
- El contenido del documento fundacional (leído desde su ubicación real fuera del repo) es consistente con el mapeo de extracción propuesto — no hay contradicción que bloquee.
- El riesgo Flyway/classpath fue reverificado desde cero contra el estado post-appmod (Spring Boot 4.1.0) y es bajo: un único archivo requiere cambio técnico real (`docker/compose.yaml`).
- El boundary de 8 archivos es exhaustivo contra la búsqueda ampliada de Tarea 3; no quedan dependencias implícitas sin identificar.

Advertencia no bloqueante para quien ejecute la implementación: la ruta del documento fundacional en las instrucciones de esta auditoría (`GYPPORT_Governance_Architecture/standards/DATABASE_MIGRATION_STANDARD.md`, relativa al repo `Gystigo`) no es correcta — la ruta real es `D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT\Governance\GYPPORT_Governance_Architecture\standards\DATABASE_MIGRATION_STANDARD.md`, fuera del repositorio `Gystigo`. Si algún paso de gobernanza futuro depende de citar esa ruta como relativa al repo, debe corregirse la referencia.
