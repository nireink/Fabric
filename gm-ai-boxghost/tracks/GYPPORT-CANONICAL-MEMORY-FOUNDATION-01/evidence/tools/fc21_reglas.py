# -*- coding: utf-8 -*-
"""Final Owner entry in the canonical Reglas log: byte-level append, new keys only."""
import hashlib, os

F3 = chr(96) * 3
P = os.path.join("D:" + os.sep, "NZXTG7", "GYPPORT", "GYPPORT ERP", "GYPPORT", "Fabric", "Knowledge",
                 "00-GYPPORT-UNIVERSE", "Reglas.md")
HEADING = "2026-09-15 - GYPPORT(R) Universe / Regla de ubicacion fisica, CURRENT_STEP y cierre de la fundacion de memoria"
HEADING = HEADING.replace("GYPPORT(R)", "GYPPORT®").replace(" - ", " — ").replace("ubicacion", "ubicación").replace("fundacion", "fundación")

NEW_KEYS = ["GYPPORT_STORAGE_ID", "GYPPORT_LOCATION_REGISTRY", "GYPPORT_STORAGE_GOOGLE_DRIVE_SYNC",
            "PHYSICAL_STORAGE_LOCATION_IS_CONFIGURABLE", "FUTURE_NAS_MOVE_REQUIRES_ARCHITECTURE_CHANGE",
            "CURRENT_STEP_GLOBAL", "CURRENT_STEP_PATH", "AGENT_AUTO_DISCOVERY_ENABLED",
            "PERMANENT_ARTIFACT_ROUTING_ENABLED", "AUTO_CURRENT_STEP_PREPARATION", "AUTO_IMPLEMENT_NEXT_STEP",
            "GYPPORT_BRAIN_IMPLEMENTATION", "GYPPORT_BRAIN_STORAGE_MODEL", "STORAGE_LOCATION_SINGLE_SOURCE",
            "STORAGE_UNAVAILABLE_FALLBACK_CREATION", "GYPPORT_STORAGE_SOURCE_MIGRATION_COMPLETE",
            "UNMERGED_UNIQUE_BOXGHOST_MEMORY", "BOXGHOST_OPERATIONAL_HISTORY_COMPLETE"]

raw = open(P, "rb").read()
text = raw.decode("utf-8")
if HEADING in text:
    raise SystemExit("ALREADY_PRESENT=YES")
for k in NEW_KEYS:
    n = sum(1 for l in text.splitlines() if l.strip().startswith(k + "="))
    if n:
        print("WARNING key already present %s x%d" % (k, n))

body = u"""{h}

Decision del Owner que cierra la fundacion de memoria de GYPPORT. La identidad logica del
almacenamiento se separa de su ubicacion fisica: la arquitectura habla de GYPPORT_STORAGE y solo un
registro sabe donde vive hoy. Google Drive queda fuera de la arquitectura de memoria y de
almacenamiento: no es backend, no es backup y no es una dependencia de sincronizacion. Ademas se fija
un unico CURRENT_STEP global como puntero de continuidad, el descubrimiento automatico de los agentes
y el enrutamiento permanente de artefactos.

{f}text
DATE=2026-09-15
GYPPORT_STORAGE_ID=GYPPORT_STORAGE
GYPPORT_LOCATION_REGISTRY=Fabric/Knowledge/00-GYPPORT-UNIVERSE/GYPPORT_LOCATIONS.properties
GYPPORT_STORAGE_GOOGLE_DRIVE_SYNC=DISABLED
PHYSICAL_STORAGE_LOCATION_IS_CONFIGURABLE=YES
STORAGE_LOCATION_SINGLE_SOURCE=YES
STORAGE_UNAVAILABLE_FALLBACK_CREATION=NO
FUTURE_NAS_MOVE_REQUIRES_ARCHITECTURE_CHANGE=NO
CURRENT_STEP_GLOBAL=YES
CURRENT_STEP_PATH=Fabric/Knowledge/00-GYPPORT-UNIVERSE/active-work/CURRENT_STEP.md
AGENT_AUTO_DISCOVERY_ENABLED=YES
PERMANENT_ARTIFACT_ROUTING_ENABLED=YES
AUTO_CURRENT_STEP_PREPARATION=YES
AUTO_IMPLEMENT_NEXT_STEP=NO
GYPPORT_STORAGE_SOURCE_MIGRATION_COMPLETE=YES
UNMERGED_UNIQUE_BOXGHOST_MEMORY=0
BOXGHOST_OPERATIONAL_HISTORY_COMPLETE=YES
GYPPORT_BRAIN_IMPLEMENTATION=DEFERRED
GYPPORT_BRAIN_STORAGE_MODEL=KNOWLEDGE_PLUS_BOXGHOST_PLUS_LOGICAL_GYPPORT_STORAGE
{f}

Lo que esta entrada reemplaza de forma explicita:

{f}text
RAW_PERSISTENT_STORAGE_ROOT=<ruta literal de la entrada anterior del 2026-09-15>
  -> sustituido por GYPPORT_STORAGE_ID + GYPPORT_LOCATION_REGISTRY.
     La ruta fisica vive unicamente en el registro; la gobernanza activa no la repite.
{f}

Siguen vigentes sin cambio las claves de la entrada anterior del 2026-09-15:
FABRIC_IS_SINGLE_GYPPORT_MEMORY_ROOT, CANONICAL_KNOWLEDGE_ROOT, OPERATIONAL_MEMORY_ROOT,
VERIFICATION_BASELINE_REUSE, RAW_OPERATIONAL_MEMORY_MUST_NOT_BE_REPLACED_BY_SUMMARY,
SUMMARIES_ARE_DERIVED, CONTEXT_PACKS_ARE_REGENERABLE, PROVIDER_CACHE_IS_NOT_GYPPORT_MEMORY,
AI_TEMP_STORAGE_IS_NOT_DURABLE_GYPPORT_MEMORY, NEW_DURABLE_GYPPORT_ARTIFACTS_MUST_USE_CANONICAL_OWNER_PATH,
FULL_CANONICAL_MIGRATION_IN_SAME_STEP y NO_DEFERRED_ARCHITECTURAL_CLEANUP.

El material externo crudo (coleccion externa, documentacion de ejemplo, plantillas y el archivo
sensible de migracion) vive ahora dentro de GYPPORT_STORAGE; el archivo con credenciales queda en su
area restringida, sin ingestion automatica de contexto ni sincronizacion externa. La memoria
operativa unica de BoxGhost recupero, byte a byte, la historia que solo existia en la rama Fabric
docs/gm-ai-workspace-canonical-unification-01 (d43b4fd), sin fusionarla y sin borrarla.
""".format(h=HEADING, f=F3)

eol = "\r\n" if "\r\n" in text else "\n"
payload = ((eol * 3) + body.replace("\n", eol)).encode("utf-8")
open(P, "ab").write(payload)
new = open(P, "rb").read()
assert new.startswith(raw), "prefix not preserved"
after = new.decode("utf-8")
print("APPENDED bytes_before=%d bytes_after=%d prefix_preserved=YES" % (len(raw), len(new)))
print("sha_before=%s sha_after=%s" % (hashlib.sha256(raw).hexdigest()[:16], hashlib.sha256(new).hexdigest()[:16]))
for k in NEW_KEYS:
    print("KEY_ONCE %-46s %d" % (k, sum(1 for l in after.splitlines() if l.strip().startswith(k + "="))))
