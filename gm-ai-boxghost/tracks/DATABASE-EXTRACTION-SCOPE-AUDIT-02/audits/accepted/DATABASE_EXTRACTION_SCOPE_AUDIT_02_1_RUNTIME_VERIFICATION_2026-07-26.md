# DATABASE_EXTRACTION_SCOPE_AUDIT_02_1_RUNTIME_VERIFICATION_2026-07-26

**Track:** DATABASE-EXTRACTION-SCOPE-AUDIT-02 · **Step:** 02.1 — Verificación runtime post-implementación
**Rol:** Auditor independiente (Claude) · **Modo:** Verificación ejecutable, cambios mínimos y reversibles
**Documento antecesor:** `DATABASE_EXTRACTION_SCOPE_AUDIT_2026-07-26.md`
**Commit auditado:** `595f0d4` (`refactor(database): extract canonical database assets`)

---

## Contexto

El informe original `DATABASE_EXTRACTION_SCOPE_AUDIT_2026-07-26.md` fue un análisis estático read-only que concluyó `READY FOR CODEX IMPLEMENTATION`. Una verificación documental posterior confirmó que la extracción descrita ya había sido ejecutada directamente por el Architecture Owner en el commit `595f0d4`, con integridad de contenido confirmada (SHA-256 idénticos) y sin referencias operativas obsoletas remanentes.

Este STEP (`02.1`) ejecuta las validaciones de la Tarea 5 del informe original que requerían comandos reales — no verificables por lectura de repositorio — y documenta un hallazgo que solo apareció al inspeccionar el estado runtime.

---

## Resultados por tarea

### Tarea 0 — Puerta de entorno
`PASS`. Sin cambios staged/unstaged inesperados.

### Tarea 1 — Historial preservado
`CONFIRMADO 4/4`. Los 4 archivos movidos (`V1__core_business_baseline.sql`, `V2__core_reference_seed_data.sql`, `core_business_dev_20260709_schema_only.sql`, `MASTER_DATABASE_ORIGIN_ANALYSIS.md`) muestran la misma cadena de historial a través del `git mv`:

```text
595f0d4 (extracción) → 5b07dca (flatten) → dbc374e (creación original)
```

### Tarea 2 — Backend compila y testea
`PASS`. `./mvnw -B -ntp clean verify` → `BUILD SUCCESS`, 1 test ejecutado sin fallos. Confirmado además que `db/migration` está ausente del JAR empaquetado (`jar tf ... | Select-String "db/migration"` sin resultados) — comportamiento esperado, no regresión.

### Tarea 3/4 — Docker inicializa base nueva / volumen existente no afectado

**Hallazgo real, no anticipado por el análisis estático:** existía un contenedor `gypport-mysql-dev` ya materializado *antes* del commit `595f0d4`, cuyo bind mount seguía apuntando a la ruta antigua (`platform_os/server/src/main/resources/db/migration`) a pesar de que `docker/compose.yaml` ya reflejaba correctamente la ruta nueva (`database/core/migration`). Docker no actualiza automáticamente los mounts de un contenedor existente al cambiar el archivo compose — solo se aplica al recrearlo.

- **Riesgo en el momento de la detección:** ninguno inmediato — el volumen de datos (`gypport_mysql_dev_data`) ya estaba poblado, por lo que MySQL nunca reejecuta `docker-entrypoint-initdb.d` mientras ese volumen exista.
- **Riesgo latente identificado:** si en el futuro se recreara el volumen de datos desde cero usando ese mismo contenedor sin recrearlo, la inicialización habría leído la ruta antigua (vacía tras la extracción), resultando en una base de datos sin V1/V2 sin ningún error visible.
- **Corrección aplicada:** `docker compose -f docker/compose.yaml up -d --force-recreate mysql`, que recrea únicamente el contenedor (no el volumen nombrado de datos).
- **Verificación posterior:** `docker inspect gypport-mysql-dev --format "{{json .Mounts}}"` confirmó el mount corregido apuntando a `database/core/migration`, con `gypport_mysql_dev_data` intacto como volumen independiente.

### Tarea 5 — `UI_Experiments` intacto
`CONFIRMADO`. `UI_Experiments` está fuera del árbol Git de `Gystigo` (`fatal: ... is outside repository`), por lo que ningún `git mv` ejecutado dentro de este repositorio pudo haberlo afectado — confirmado por imposibilidad estructural, no solo por inspección de contenido.

---

## Cierre de cobertura

```text
GIT_GATE=PASS
HISTORY_PRESERVED=4/4 CONFIRMED
BACKEND_BUILD_RESULT=PASS
JAR_MIGRATION_FILES_ABSENT=CONFIRMED
DOCKER_COMPOSE_CONFIG_PATH=CORRECT
DOCKER_RUNNING_CONTAINER_MOUNT=CORRECTED (era stale, ahora coincide)
EXISTING_VOLUME_PRESERVED=YES (no se tocó gypport_mysql_dev_data)
UI_EXPERIMENTS_UNTOUCHED=YES
DOCUMENT_STATUS_NOTE_ADDED=PENDING (Tarea 6, aún no ejecutada)
DOCUMENT_MOVED_TO_ACCEPTED=PENDING
RESULT=TASK_5_VALIDATION_COMPLETE_WITH_ONE_GAP_FOUND_AND_CORRECTED
```

---

## Conclusión

El informe original (`DATABASE_EXTRACTION_SCOPE_AUDIT_2026-07-26.md`) fue correcto en la totalidad de su análisis estático: los 8 archivos identificados, el riesgo Flyway/classpath, y el boundary de implementación. Sin embargo, por ser estrictamente read-only, no pudo detectar que un contenedor Docker ya en ejecución conservaría un mount obsoleto tras el cambio de código — un estado que solo la inspección runtime podía revelar. Esto confirma el valor de exigir las validaciones ejecutables de la Tarea 5 en vez de aceptar el veredicto documental como suficiente por sí solo.

El hallazgo fue corregido de forma segura (recreación de contenedor, sin tocar el volumen de datos) y verificado. No se modificó ningún archivo de código de producción como parte de esta verificación — el único cambio fue operativo (recreación de contenedor Docker) y documental (pendiente: nota de estado + `git mv` del informe original a `accepted/`).

```text
OWNERSHIP_DECISIONS_APPROVED=NONE
IMPLEMENTATION_AUTHORIZED=NO (más allá de la recreación de contenedor ya ejecutada)
READY_FOR_TASK_6=YES
```
