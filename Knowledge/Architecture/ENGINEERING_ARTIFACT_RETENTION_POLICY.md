# GYPPORT® — Engineering Artifact Retention Policy

**Vive en:** `Fabric/Knowledge/Architecture/ENGINEERING_ARTIFACT_RETENTION_POLICY.md`
**Estado:** APROBADO
**Autoridad:** ADR-0001 (histórico)
**Vigente desde:** 2026-07-25
**Referenciado por:** ADR-0001
**Origen:** `Governance/GYPPORT_Governance_Architecture/governance/retention/ENGINEERING_ARTIFACT_RETENTION_POLICY.md` (repositorio heredado, alias GDA). Migrado el 2026-09-15 por `GYPPORT_CANONICAL_MEMORY_FOUNDATION_01` por seguir siendo aplicable y no estar contradicho; ver `Fabric/Knowledge/00-GYPPORT-UNIVERSE/GYPPORT_MEMORY_ARCHITECTURE.md`.

---

## 1. Candidatos confirmados (auditoría del zip real de Gystigo)

- **`.claude/worktrees/`** — 5 worktrees, ~28 MB. Git mismo marca 2 de ellos como `prunable`. Contienen árboles completos duplicados de código en distintos puntos de historia, incluida una carpeta `legacy/` con formularios antiguos en español.
- **`.gypport/operation/transaction/`** — 105 carpetas de snapshot, 3.5 MB. El propio toolchain acumula un snapshot por cada operación, sin política de retención hasta ahora.

## 2. Regla general de limpieza

Nunca borrado manual e indiscriminado. Siempre:

```
Inventariar
    ↓
Verificar referencia Git (¿contiene trabajo único sin mergear?)
    ↓
Confirmar que no hay evidencia que deba preservarse
    ↓
Eliminar mediante la herramienta propietaria
    ↓
Registrar evidencia de la limpieza
```

## 3. Worktrees — cerrar siempre con Git

Nunca borrar la carpeta a mano. Usar el flujo de Git:

```
git worktree list
git worktree remove <ruta>
git worktree prune
```

## 4. Snapshots de Toolchain — política de retención explícita

- **Conservar:** últimos 20 snapshots; snapshots asociados a operaciones abiertas; snapshots marcados explícitamente como evidencia.
- **Eliminar:** snapshots cerrados de más de 30 días; duplicados; transacciones incompletas sin referencia.
