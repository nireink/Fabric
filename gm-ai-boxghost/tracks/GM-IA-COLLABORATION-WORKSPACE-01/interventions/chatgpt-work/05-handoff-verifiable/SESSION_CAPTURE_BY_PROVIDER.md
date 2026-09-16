# Session Capture by Provider

## 1. Estado

Este documento define el contrato futuro de captura. La captura e importación están fuera del primer slice read-only. Ninguna integración en tiempo real queda autorizada por esta especificación.

## 2. Contrato común de sesión

```text
captures/<provider>/<yyyy-mm-dd>-<session-id>/
├── SESSION_MANIFEST.json
├── PROMPTS.md
├── RESPONSES.md
├── TRANSCRIPT.jsonl
├── SUMMARY.md
├── FILES_MANIFEST.json
├── attachments/
├── generated-files/
├── terminal-logs/
├── patches/
└── tool-results/
```

Campos mínimos del manifiesto:

```yaml
schema_version: "1.0"
provider: CHATGPT | CHATGPT_WORK | CODEX | CLAUDE_CHAT | CLAUDE_CODE | HUMAN
surface: string
external_session_id: string | null
derived_session_id: string
track_id: string
initiated_by: actor_id
captured_at: timestamp
source_mode: EXPORT | EXPOSED_FILE | MANUAL | AUTHORIZED_INTEGRATION
source_revision: string
supersedes_capture_ref: string | null
sensitivity: PUBLIC | INTERNAL | CONFIDENTIAL | RESTRICTED | REDACTED
files_manifest_ref: FILES_MANIFEST.json
content_sha256: string
retention: PERMANENT
```

## 3. Modalidad por proveedor

| Proveedor | Modalidad inicial | Iniciador | Actualización | Identidad externa |
|---|---|---|---|---|
| ChatGPT | Exportación o archivo expuesto | Eduardo | Nueva captura enlazada; sin sobrescritura | ID nativo si está expuesto; si no, derivado |
| ChatGPT Work | Conversación, archivos y entregables expuestos | Eduardo | Nueva revisión de captura | ID expuesto cuando exista |
| Claude Chat | Exportación o captura autorizada | Eduardo | Nueva revisión de captura | ID nativo cuando exista |
| Codex | Transcript, resultados y artefactos expuestos | Eduardo o integración futura autorizada | Eventos anexados o nueva revisión | ID de sesión expuesto |
| Claude Code | Transcript, comandos, resultados y archivos expuestos | Eduardo o integración futura autorizada | Eventos anexados o nueva revisión | ID de sesión expuesto |
| Humano | Archivo o intervención manual fechada | Actor humano | Nueva intervención | UUID generado por Workspace |

La aplicación no promete obtener razonamiento interno, cachés privados ni archivos que un proveedor no exponga.

## 4. Identidad derivada

Si no existe ID nativo:

```text
derived_session_id = provider + capture_date + first_source_sha256_prefix + owner_namespace
```

El algoritmo concreto debe ser determinista, versionado y documentado. Una identidad derivada no se presenta como ID oficial del proveedor.

## 5. Actualizaciones

- Nunca se sobrescribe silenciosamente una captura.
- Una revisión nueva usa `supersedes_capture_ref`.
- Se conservan hashes de cada revisión.
- La deduplicación de objetos por SHA-256 no elimina las relaciones ni la procedencia.
- Si una exportación es parcial, se marca `capture_completeness=PARTIAL` con razón.

## 6. Pipeline futuro de importación

1. Recibir en un área temporal aislada, fuera de BoxGhost canónico.
2. Identificar proveedor, sesión y track.
3. Validar tipos, tamaños, rutas y archivo comprimido si aplica.
4. Clasificar sensibilidad.
5. Detectar secretos conforme a `SENSITIVITY_AND_SECRET_HANDLING_POLICY.md`.
6. Ante cualquier secreto, fallar cerradamente sin escritura parcial.
7. Validar manifiestos y calcular hashes.
8. Presentar el resultado para revisión humana cuando corresponda.
9. Promover como nueva captura inmutable.
10. Registrar evento y procedencia.

Este pipeline no forma parte del slice v0.1.

## 7. Archivos temporales

Todo archivo útil se clasifica antes de limpiar:

```text
temporary -> hash -> provenance -> track association -> promote or exclude with reason
```

Se promueven borradores útiles, parches, comandos, resultados, adjuntos y evidencias. Se excluyen secretos, cookies, tokens, cachés de navegador, `node_modules`, builds regenerables y archivos internos no expuestos.

## 8. Integridad y privacidad

- Los archivos se hashean antes de promoción.
- Los nombres no sustituyen la identidad por contenido.
- Los archivos comprimidos se validan contra zip-slip, bombas de compresión y rutas absolutas.
- Los valores sensibles no aparecen en logs.
- La sensibilidad del paquete es al menos la mayor de sus elementos.

## 9. Referencias

- Política de secretos: `SENSITIVITY_AND_SECRET_HANDLING_POLICY.md`.
- Destino y estructura: `BOXGHOST_STRUCTURE.md`.
- Retención: `BOXGHOST_OPERATIONS.md`.
- Aprobación humana: `APPROVAL_MODEL.md`.
