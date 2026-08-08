# Fabric — continuidad y conocimiento de GYPPORT®

```text
ORGANIZATION=ISAGRUB CORPORACIÓN C.L.
COMMERCIAL_NAME=GYPPORT®
PRODUCT=GYPPORT® / Gystigo
STRUCTURE_STATUS=PROPOSED
CREATED_DATE=2026-07-30
SOURCES_IMPORTED=false
MEMORIES_IMPORTED=false
GYSTIGO_MODIFIED=false
GIT_ACTIONS_EXECUTED=false
```

`Fabric` conserva físicamente el conocimiento, la continuidad entre IAs y los
resultados derivados del proyecto. Está separado del código de producto
`Gystigo`.

## Alcance

- `AGENTS.md`: instrucciones compartidas y obligatorias para agentes.
- `.chatgpt/`: memoria canónica explícita, checkpoints y paquetes de continuidad.
- `.codex/`: configuración y extensiones locales del proyecto.
- `Governance/`: arquitectura, políticas y decisiones de gobierno.
- `Knowledge/`: fuentes, inventarios, procesamiento y documentos derivados.
- `AI_Workspace/`: handoffs, revisiones, auditorías y cierres entre IAs.
- `Private_State/`: respaldos privados que nunca deben publicarse.
- `Backup_Tooling/`: procedimientos de respaldo, integridad y restauración.

## Límite importante

`.chatgpt/` es una convención propia de GYPPORT®; no es la memoria automática de
la cuenta de ChatGPT. La continuidad obligatoria vive en archivos verificables,
principalmente `AGENTS.md`, `.chatgpt/CANONICAL_MEMORY.md`,
`.chatgpt/CURRENT_STATE.md` y `.chatgpt/DECISION_REGISTER.md`.

## Uso inicial

1. Copiar esta carpeta completa a la ubicación física aprobada.
2. Crear respaldo en un segundo dispositivo antes de importar fuentes.
3. Completar `PROJECT_CONTEXT.md` y `CURRENT_STATE.md`.
4. Registrar cada fuente antes de procesarla.
5. No guardar credenciales, tokens ni secretos dentro de esta estructura.

