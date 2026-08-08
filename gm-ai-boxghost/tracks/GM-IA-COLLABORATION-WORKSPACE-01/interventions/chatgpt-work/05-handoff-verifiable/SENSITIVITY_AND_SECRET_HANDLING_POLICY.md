# Sensitivity and Secret Handling Policy

## 1. Objetivo

Evitar que credenciales u otros secretos ingresen a BoxGhost y prevenir su exposición durante la lectura. El primer slice detecta, enmascara la presentación y reporta; no sanea ni modifica automáticamente archivos.

## 2. Niveles permitidos

| Nivel | Uso |
|---|---|
| `PUBLIC` | Información autorizada para divulgación pública |
| `INTERNAL` | Trabajo interno ordinario de GYPPORT |
| `CONFIDENTIAL` | Información empresarial limitada |
| `RESTRICTED` | Acceso excepcional y explícitamente autorizado |
| `REDACTED` | Derivado saneado que conserva marcadores de redacción |

`SECRET` no es un nivel permitido de almacenamiento. Describe una clase de hallazgo que debe impedir la importación.

## 3. Responsabilidad

- El iniciador de una importación declara la sensibilidad.
- El importador aplica validación automática complementaria.
- Eduardo o el propietario autorizado sanea el archivo original.
- El primer slice de lectura no reclasifica ni desclasifica.
- Una futura desclasificación requerirá evento, actor, razón y evidencia.

## 4. Flujo obligatorio de datos sensibles

```text
SENSIBLE_DATA_HANDLING_FLOW:
  1. Captura inicial -> clasificación de sensibilidad
  2. Detección de patrón de secreto -> FALLO CERRADO durante importación
  3. Rechazo con reporte: "Contiene credenciales de tipo X en ruta Y; redactar antes de reintentar"
  4. Eduardo o el propietario autorizado sanea el archivo original
  5. Reintentar importación como una nueva revisión
  6. Solo el archivo saneado ingresa a BoxGhost
  7. Conservar el hash del original únicamente si puede registrarse sin conservar el secreto
```

El primer slice solo detecta y reporta. No redacta automáticamente. El reporte nunca incluye el valor detectado, fragmentos recuperables ni suficiente contexto para reconstruirlo.

## 5. Hash del original rechazado

Cuando sea posible y esté autorizado, se registra:

```text
original_sha256
detection_type
source_path_or_external_ref
detected_at
status=REJECTED_REQUIRES_MANUAL_SANITIZATION
```

El hash no autoriza conservar una copia del archivo rechazado dentro de BoxGhost. Si la política del proveedor o el proceso seguro no permiten calcularlo, se registra `ORIGINAL_HASH_UNAVAILABLE`.

## 6. Categorías de detección

La implementación debe reconocer al menos:

- claves API con prefijos conocidos;
- claves privadas PEM;
- tokens OAuth/JWT con estructura plausible;
- credenciales de nube;
- cadenas de conexión con contraseña;
- variables de entorno de contraseña o token;
- cookies o tokens de sesión;
- archivos de credenciales por nombre y contenido.

Los patrones se mantienen en configuración versionada y las pruebas usan valores sintéticos. No se documentan secretos reales ni se registran coincidencias completas.

## 7. Acciones por momento

| Momento | Acción |
|---|---|
| Importación futura | Rechazo total del archivo o paquete afectado; sin escritura parcial |
| Lectura de archivo ya existente | Enmascarar presentación, marcar recurso no confiable y emitir hallazgo |
| Manifiesto sin sensibilidad | Fallo cerrado para `RESTRICTED`; hallazgo bloqueante en los demás casos |
| Falso positivo | Revisión humana; excepción estrecha, documentada y hasheada |
| Secreto confirmado en BoxGhost | Detener exposición, notificar a Eduardo, rotar/revocar fuera de BoxGhost y sanear mediante proceso aprobado |

## 8. Enmascaramiento de salida

La UI y los logs muestran únicamente:

```text
finding_id
detection_type
relative_path
line_number opcional
file_sha256
status
```

El valor se reemplaza por `[REDACTED_SECRET_PATTERN]`. Logs, excepciones, telemetría y resultados de pruebas obedecen la misma regla.

## 9. Archivos restringidos

- Acceso denegado por defecto cuando falta autorización.
- No se generan previews ni snippets para contenido restringido no autorizado.
- No se cachea contenido sensible en el navegador.
- Los adjuntos heredarán la clasificación más restrictiva de su contenedor salvo declaración más estricta.

La primera versión es para Eduardo, pero esta frontera se mantiene para futura extensibilidad.

## 10. Falsos positivos y excepciones

Una excepción contiene patrón, ruta o hash exacto, razón, actor, vencimiento y evidencia. No se aceptan excepciones globales permanentes. Un ejemplo sintético para pruebas puede marcarse como `TEST_FIXTURE_ONLY`, pero nunca habilita ese patrón en producción.

## 11. Referencias

- Captura e importación: `SESSION_CAPTURE_BY_PROVIDER.md`.
- Estructura y manifiestos: `BOXGHOST_STRUCTURE.md`.
- Backup y respuesta operativa: `BOXGHOST_OPERATIONS.md`.
- Alcance del lector: `GM_AI_WORKSPACE_IMPLEMENTATION_SCOPE_v0.1.md`.
