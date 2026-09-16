# BoxGhost Operations

## 1. Propósito y autoridad

La raíz primaria es:

```text
D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT\Fabric\gm-ai-boxghost
```

Es almacenamiento canónico local. Una copia o backup no se convierte en autoridad mientras no exista un procedimiento de restauración aprobado.

## 2. Objetivos operativos iniciales

```text
RPO_TARGET=24_HOURS
RTO_TARGET=8_HOURS
PRIMARY=LOCAL
SECONDARY_COPY=REQUIRED
EXTERNAL_ENCRYPTED_COPY=REQUIRED
RESTORE_TEST=QUARTERLY
```

Son objetivos para la operación inicial de un solo usuario, no capacidades del primer slice. Si el volumen o criticidad aumenta, se abre una revisión de RPO/RTO.

## 3. Política de backup

- Copia incremental local diaria.
- Copia completa semanal a almacenamiento secundario distinto.
- Copia externa cifrada al menos semanal.
- Manifiesto SHA-256 por conjunto de backup.
- Cifrado en tránsito y reposo para la copia externa.
- Credenciales fuera de BoxGhost y fuera de los manifiestos.
- Registro de inicio, fin, resultado, volumen y errores sin valores sensibles.

Retención técnica sugerida de backups:

```text
DAILY=30
WEEKLY=12
MONTHLY=24
YEARLY=7
```

Esta rotación no reduce la retención canónica permanente de conversaciones, decisiones, aprobaciones y evidencia.

## 4. Retención canónica

| Clase | Retención |
|---|---|
| Capturas expuestas y saneadas | Permanente |
| Intervenciones y prompts/respuestas | Permanente |
| Decisiones y aprobaciones | Permanente |
| Evidencias y auditorías | Permanente |
| Borradores/temporales promovidos | Permanente |
| Manifiestos y hashes | Permanente |
| Cachés y builds regenerables | No ingresan |
| Secretos y credenciales | Prohibidos |

Cerrar o archivar un track cambia su ubicación operativa, no su autoridad, identidad ni trazabilidad.

## 5. Archivo de tracks

Un track puede pasar a `archive/closed-tracks` únicamente cuando:

1. está `CLOSED`;
2. no tiene referencias activas rotas;
3. posee manifiesto final y hashes verificados;
4. existe backup verificado;
5. el movimiento está registrado y autorizado.

El primer slice no mueve tracks.

## 6. Restauración

1. Declarar incidente y congelar escrituras externas al slice.
2. Seleccionar el backup por fecha, manifiesto e identidad.
3. Restaurar en un directorio temporal aislado, nunca encima de la raíz activa.
4. Verificar hashes, estructura, referencias y detección de secretos.
5. Comparar contra el último estado conocido.
6. Obtener autorización de Eduardo para el reemplazo o merge controlado.
7. Registrar evidencia de restauración y resultado.

Las pruebas trimestrales restauran datos sintéticos o una copia protegida en destino aislado. Una prueba exitosa incluye tiempo medido y verificación de hashes.

## 7. Capacidad y crecimiento

- Medición mensual de tamaño, número de objetos, tracks y tasa de crecimiento.
- Aviso a 70 % de capacidad del volumen.
- Plan de expansión obligatorio a 85 %.
- No usar limpieza destructiva como mecanismo de capacidad.
- Los objetos duplicados pueden almacenarse una vez por SHA-256, conservando todas las referencias y procedencias.

## 8. Incidentes

| Incidente | Respuesta mínima |
|---|---|
| Eliminación accidental | Detener cambios, identificar manifiesto, restaurar aislado |
| Hash divergente | Marcar no confiable, conservar evidencia, no autocorregir |
| Secreto detectado | Bloquear exposición, notificar, rotar fuera de BoxGhost, sanear mediante proceso aprobado |
| Backup fallido | Reintento controlado, alerta, no borrar backups previos |
| Ruta fuera de raíz | Rechazo fail-closed y hallazgo de seguridad |

## 9. Primer slice

Incluye lectura y reporte de integridad. Excluye backup automatizado, restauración productiva, archivado y cualquier escritura.

## Apéndice A — Matriz futura de disposición del ZIP

`GYPPORT_AI_Workspace.zip` no se migra en este track. El futuro track de unificación utilizará una tabla por archivo:

| Campo | Significado |
|---|---|
| `PATH` | Ruta dentro del ZIP o carpeta histórica |
| `SHA256` | Identidad de contenido |
| `PURPOSE` | Responsabilidad observada |
| `CURRENT_AUTHORITY` | Fuente vigente que hoy manda |
| `TARGET_OWNER` | Único destino propuesto |
| `DISPOSITION` | `REUSE`, `ADAPT`, `ARCHIVE`, `DELETE_CANDIDATE` |
| `RATIONALE` | Razón verificable |
| `DEPENDENCIES` | Referencias y consumidores |
| `RECOVERY_PATH` | Cómo recuperar antes de eliminar |
| `OWNER_APPROVAL_REQUIRED` | Siempre `YES` para eliminación material |

Reglas:

- El ZIP original se conserva por hash como evidencia.
- No se extrae directamente en el módulo.
- No se elimina por antigüedad o similitud nominal.
- Un `DELETE_CANDIDATE` no es una autorización de eliminación.
- La disposición se decide en un track independiente con una única aprobación de Eduardo para el alcance exacto.

## 10. Referencias

- Estructura canónica: `BOXGHOST_STRUCTURE.md`.
- Secretos e incidentes: `SENSITIVITY_AND_SECRET_HANDLING_POLICY.md`.
- Coordinación de autorizaciones: `APPROVAL_MODEL.md` y `AGENT_COORDINATION_PROTOCOL.md`.

## 11. Captura permanente de contexto local de agentes

Por directiva expresa del propietario, toda intervención debe descubrir y
preservar antes de su cierre los artefactos locales de Codex, Claude Chat y
Claude Code necesarios para reconstruirla o continuarla.

```text
CODEX_ATTACHMENTS_CAPTURE=REQUIRED
CLAUDE_CONTEXT_CAPTURE=REQUIRED
RAW_CONTEXT_RETENTION=PERMANENT
RAW_CAPTURES=IMMUTABLE_OR_CONTENT_ADDRESSED
SOURCE_PROVENANCE=MANDATORY
SHA256_MANIFEST=MANDATORY
UNCLASSIFIED_INBOX=REQUIRED
SECRET_EXCLUSION=MANDATORY
CONVERSATION_ONLY_CONTEXT_ALLOWED=NO
```

Reglas operativas:

1. inventariar antes de copiar y no asumir una estructura local fija;
2. clasificar por track, agente, aplicación, contenido y procedencia;
3. conservar ruta original, nombre, tamaño, timestamp, SHA-256 e identificador;
4. escanear secretos antes de persistir y fallar cerradamente para el archivo
   afectado, sin registrar el valor detectado;
5. excluir autenticación, credenciales, cookies, tokens, cachés, builds,
   telemetría sin valor probatorio y árboles regenerables;
6. mantener una copia legible bajo el track y un objeto inmutable bajo
   `objects/sha256/<prefix>/<sha256>`;
7. no sobrescribir silenciosamente rutas ni objetos; una coincidencia de hash
   agrega procedencia y una colisión bloquea;
8. usar `imports/unclassified/<agent>` solo después de clasificación y escaneo,
   nunca como copia ciega de carpetas completas;
9. registrar evento append-only, manifiesto y resultado de backup/protección;
10. una intervención con contexto relevante no persistido no puede declararse
    canónicamente completada.
