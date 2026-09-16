# -*- coding: utf-8 -*-
import os
G = os.path.join("D:" + os.sep, "NZXTG7", "GYPPORT", "GYPPORT ERP", "GYPPORT", "Gystigo")
P = os.path.join(G, "AGENTS.md")
lines = open(P, encoding="utf-8").read().split("\n")
hits = [i for i, l in enumerate(lines) if l.startswith("RAW_PERSISTENT_STORAGE_ROOT=")]
assert len(hits) == 1, hits
print("replacing line %d: %s" % (hits[0] + 1, lines[hits[0]][:60]))
lines[hits[0]:hits[0] + 1] = ["GYPPORT_STORAGE_ID=GYPPORT_STORAGE",
                              "GYPPORT_LOCATION_REGISTRY=Fabric/Knowledge/00-GYPPORT-UNIVERSE/GYPPORT_LOCATIONS.properties",
                              "ACTIVE_WORK_ROOT=Fabric/Knowledge/00-GYPPORT-UNIVERSE/active-work"]
open(P, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
t = open(P, encoding="utf-8").read()
print("hardcoded path remaining:", "NZXTG7" in t, "bytes:", len(t.encode("utf-8")))
