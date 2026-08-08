# Scripts de respaldo

## Respaldo selectivo de memorias locales de Codex

```powershell
.\Backup-CodexMemories.ps1
```

Copia únicamente `%USERPROFILE%\.codex\memories\` hacia
`Private_State\codex-memory-backup\<fecha-hora>\` y genera hashes SHA-256.
No copia autenticación, sesiones ni la configuración global completa.

## Respaldo fechado de Fabric

```powershell
.\Backup-Fabric.ps1 -DestinationRoot "Z:\GYPPORT_Backups"
```

Reemplace la ruta por el destino real del NAS o disco secundario. El script crea
una nueva carpeta fechada y no elimina respaldos anteriores.

## Seguridad

- Revisar el destino antes de ejecutar.
- No versionar `Private_State/`.
- No compartir respaldos sin revisar su contenido.
- No ejecutar scripts de restauración no auditados.

