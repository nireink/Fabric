# -*- coding: utf-8 -*-
"""Append the 2026-09-15 canonical memory decision to the canonical Reglas log.

Byte-level append: the existing bytes stay an exact prefix, the entry uses the file's own line
ending and the log's separation of two blank lines. Refuses to run twice.
"""
import hashlib
import os
import sys

REGLAS = (r"D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT\Fabric\Knowledge\00-GYPPORT-UNIVERSE\Reglas.md")
HEADING = u"2026-09-15 — GYPPORT® Universe / Regla de arquitectura canónica de memoria GYPPORT"

KEYS = ["FABRIC_IS_SINGLE_GYPPORT_MEMORY_ROOT", "CANONICAL_KNOWLEDGE_ROOT", "OPERATIONAL_MEMORY_ROOT",
        "RAW_PERSISTENT_STORAGE_ROOT", "VERIFICATION_BASELINE_REUSE",
        "RAW_OPERATIONAL_MEMORY_MUST_NOT_BE_REPLACED_BY_SUMMARY", "SUMMARIES_ARE_DERIVED",
        "CONTEXT_PACKS_ARE_REGENERABLE", "PROVIDER_CACHE_IS_NOT_GYPPORT_MEMORY",
        "AI_TEMP_STORAGE_IS_NOT_DURABLE_GYPPORT_MEMORY",
        "NEW_DURABLE_GYPPORT_ARTIFACTS_MUST_USE_CANONICAL_OWNER_PATH",
        "FULL_CANONICAL_MIGRATION_IN_SAME_STEP", "NO_DEFERRED_ARCHITECTURAL_CLEANUP"]

ENTRY = u"""2026-09-15 — GYPPORT® Universe / Regla de arquitectura canónica de memoria GYPPORT

Decisión del Owner: Fabric es la única raíz de memoria de GYPPORT. El conocimiento canónico vive en
Fabric/Knowledge, la memoria operativa en Fabric/gm-ai-boxghost y las fuentes crudas, originales y
pesadas en GYPPORT-Storage. Gystigo es el producto y Host, y Modules/gm-ai-workspace es únicamente
la aplicación que lee y orquesta esa memoria. Esta entrada fija dónde vive cada artefacto duradero
de GYPPORT y reemplaza explícitamente los arreglos anteriores que se listan abajo.

```text
FABRIC_IS_SINGLE_GYPPORT_MEMORY_ROOT=YES
CANONICAL_KNOWLEDGE_ROOT=Fabric/Knowledge
OPERATIONAL_MEMORY_ROOT=Fabric/gm-ai-boxghost
RAW_PERSISTENT_STORAGE_ROOT=D:\\NZXTG7\\GYPPORT\\GYPPORT ERP\\GYPPORT-Storage
VERIFICATION_BASELINE_REUSE=YES
RAW_OPERATIONAL_MEMORY_MUST_NOT_BE_REPLACED_BY_SUMMARY=YES
SUMMARIES_ARE_DERIVED=YES
CONTEXT_PACKS_ARE_REGENERABLE=YES
PROVIDER_CACHE_IS_NOT_GYPPORT_MEMORY=YES
AI_TEMP_STORAGE_IS_NOT_DURABLE_GYPPORT_MEMORY=YES
NEW_DURABLE_GYPPORT_ARTIFACTS_MUST_USE_CANONICAL_OWNER_PATH=YES
FULL_CANONICAL_MIGRATION_IN_SAME_STEP=YES
NO_DEFERRED_ARCHITECTURAL_CLEANUP=YES
```

Documentos canónicos que fija esta decisión:

```text
MEMORY_ARCHITECTURE_DOC=Fabric/Knowledge/00-GYPPORT-UNIVERSE/GYPPORT_MEMORY_ARCHITECTURE.md
CANONICAL_AGENT_ROOT=Fabric/Knowledge/00-GYPPORT-UNIVERSE/agents/
CANONICAL_AI_COLLABORATION_ROOT=Fabric/Knowledge/00-GYPPORT-UNIVERSE/ai-collaboration/
BOXGHOST_STRUCTURE_DOC=Fabric/gm-ai-boxghost/BOXGHOST_STRUCTURE.md
GYPPORT_BRAIN_CONTRACT=seccion 8 de GYPPORT_MEMORY_ARCHITECTURE.md
GYPPORT_BRAIN_IMPLEMENTED=NO
```

Lo que esta decisión reemplaza de forma explícita:

```text
Gystigo/Reglas.md                     -> retirado; el log canónico es Fabric/Knowledge/00-GYPPORT-UNIVERSE/Reglas.md
Gystigo/CHATGPT.md y Gystigo/CODEX.md -> retirados; su contenido canónico vive en agents/
Gystigo/AGENTS.md y Gystigo/CLAUDE.md -> solo entrypoints tecnicos (Codex y Toolchain; Claude Code), sin gobernanza
Gystigo/docs/ai/                      -> retirada; la historia operativa de agentes vive en Fabric/gm-ai-boxghost
Gystigo/docs/architecture/GYPPORT_AI_COLLABORATION_EXECUTION_ORDER_v1.0.md -> ai-collaboration/
Fabric/Governance/                    -> retirada; la gobernanza canonica vive en Fabric/Knowledge
Fabric/Knowledge/{Sources,Processing,Corpus} (protocolo 2026-08-01) -> fuentes crudas a GYPPORT-Storage; procesamiento y registros a BoxGhost
GYPPORT-Storage\\Fabric\\Knowledge\\Standards ("Master") -> retirada; la ubicacion unica es Gystigo/docs/governance/standards
Governance/GYPPORT_Governance_Architecture -> historico, sin autoridad activa (ENGINEERING_ARTIFACT_RETENTION_POLICY.md se conservo en Fabric/Knowledge/Architecture)
```

La memoria cruda no se sustituye por resúmenes: un resumen es derivado y debe poder señalar su
fuente, un context pack es derivado y regenerable, la caché y la compactación del proveedor no son
memoria de GYPPORT, y el scratchpad, AppData\\Local\\Temp y las carpetas temporales de Codex no son
memoria duradera. Todo artefacto duradero nuevo se crea directamente en su ruta canónica, y lo
valioso que quede en almacenamiento temporal se promueve antes de cerrar el STEP.
"""


def main():
    raw = open(REGLAS, "rb").read()
    text = raw.decode("utf-8")
    if HEADING in text:
        print("ALREADY_PRESENT=YES (no change)")
        return
    eol = "\r\n" if "\r\n" in text else "\n"
    entry = ENTRY.replace("\n", eol)
    payload = (eol * 3) + entry
    before = hashlib.sha256(raw).hexdigest()
    if "--write" not in sys.argv:
        print("DRY RUN: would append %d bytes after %d (sha %s)" % (len(payload.encode("utf-8")), len(raw), before[:16]))
        return
    with open(REGLAS, "ab") as fh:
        fh.write(payload.encode("utf-8"))
    new = open(REGLAS, "rb").read()
    assert new.startswith(raw), "existing bytes are no longer an exact prefix"
    after_text = new.decode("utf-8")
    print("APPENDED bytes_before=%d bytes_after=%d prefix_preserved=YES" % (len(raw), len(new)))
    print("sha_before=%s sha_after=%s" % (before[:16], hashlib.sha256(new).hexdigest()[:16]))
    for k in KEYS:
        n = sum(1 for line in after_text.splitlines() if line.strip().startswith(k + "="))
        print("KEY_ONCE %-58s %d" % (k, n))


if __name__ == "__main__":
    main()
