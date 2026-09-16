# -*- coding: utf-8 -*-
"""Pre-move manifest for the external source material that moves into GYPPORT_STORAGE."""
import hashlib, json, os, sys, time

P = r"D:\NZXTG7\GYPPORT\GYPPORT ERP"
SOURCES = {"DATOS EXTERNOS": os.path.join(P, "DATOS EXTERNOS"),
           "Documentacion Externa Ejemplos": os.path.join(P, "Documentacion Externa Ejemplos"),
           "Archivos GIt": os.path.join(P, "Archivos GIt"),
           "GestMechanical": os.path.join(P, "GestMechanical"),
           "estructura.txt": os.path.join(P, "estructura.txt"),
           "Transfer": os.path.join(P, "GYPPORT", "Transfer")}
HASH_EXT = {".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".sql", ".bak", ".mwb", ".gpkg", ".iso", ".dmp"}
HASH_MIN = 100 * 1024 * 1024


def want_hash(path, size):
    ext = os.path.splitext(path)[1].lower()
    return ext in HASH_EXT or size >= HASH_MIN or ".part" in ext


def entry(path, root):
    st = os.stat(path)
    rec = {"rel": os.path.relpath(path, root).replace("\\", "/"), "size": st.st_size, "mtime": int(st.st_mtime)}
    if want_hash(path, st.st_size):
        h = hashlib.sha256()
        with open(path, "rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 22), b""):
                h.update(chunk)
        rec["sha256"] = h.hexdigest()
    return rec


out, t0 = {}, time.time()
for name, root in SOURCES.items():
    if not os.path.exists(root):
        out[name] = {"present": False}
        continue
    files = []
    if os.path.isfile(root):
        files.append(entry(root, os.path.dirname(root)))
    else:
        for r, d, fs in os.walk(root):
            for f in fs:
                files.append(entry(os.path.join(r, f), root))
    out[name] = {"present": True, "root": root, "files": len(files),
                 "bytes": sum(f["size"] for f in files),
                 "hashed": sum(1 for f in files if "sha256" in f), "entries": files}
    print("%-32s files=%-6d bytes=%-14d hashed=%d" % (name, out[name]["files"], out[name]["bytes"], out[name]["hashed"]))
json.dump(out, open(sys.argv[1], "w", encoding="utf-8"), indent=1)
print("TOTAL files=%d bytes=%d elapsed=%ds -> %s" % (sum(v.get("files", 0) for v in out.values()),
                                                     sum(v.get("bytes", 0) for v in out.values()), time.time() - t0, sys.argv[1]))
