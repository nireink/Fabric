# GYPPORT_STORAGE source migration

```text
TRACK=GYPPORT_CANONICAL_MEMORY_FOUNDATION_01
DATE=2026-09-15
GYPPORT_STORAGE_ID=GYPPORT_STORAGE
GYPPORT_LOCATION_REGISTRY=Fabric/Knowledge/00-GYPPORT-UNIVERSE/GYPPORT_LOCATIONS.properties
RESOLVED_AT_MIGRATION_TIME=<resolved through the registry, not hardcoded>
METHOD=same-volume rename (no byte copying, file identity preserved)
VERIFICATION=relative path + size + mtime for every file, sha256 for archives, dumps and files over 100 MB
GYPPORT_STORAGE_SOURCE_MIGRATION_COMPLETE=YES
RAW_SOURCE_FILES_LOST=0
PERMANENT_DUPLICATE_SOURCE_TREES=0
GOOGLE_DRIVE_SYNC=DISABLED
```

| SOURCE | FILES | BYTES | HASHED | DESTINATION |
|---|---|---|---|---|
| DATOS EXTERNOS | 234 | 12075889643 | 67 | External/DATOS EXTERNOS |
| Documentacion Externa Ejemplos | 25366 | 717962487 | 24 | External/Documentacion Externa Ejemplos |
| Archivos GIt | 171 | 134485469 | 0 | External/Archivos GIt |
| GestMechanical | 1 | 136983 | 0 | External/GestMechanical |
| estructura.txt | 1 | 15501950 | 0 | External/estructura.txt |
| Transfer | 1 | 38985099 | 1 | Restricted/Gystigo/Gystigo_migrated_2026-07-28.zip |
| **total** | **25774** | **12982961631** | **92** | |

Verification after the move compared every one of the 25774 files with the pre-move manifest:
VERIFIED_FILES=25774, PROBLEMS=0. Source directories were removed only after that proof.

## Sensitive archive

```text
ARTIFACT=Gystigo_migrated_2026-07-28.zip
CLASSIFICATION=SENSITIVE_ARCHIVE
REASON=the archive contains docker/.env and application.yaml entries
LOCATION=Restricted/Gystigo/ inside the resolved GYPPORT_STORAGE root
SIZE=38985099
SHA256=0198216070ffd9a1ed57f69f7ec7e61b3d04cae449813ec20f0de9479fb128ac
SECRET_VALUES_PRINTED=NO
RESTRICTED_SOURCE_AUTOMATIC_CONTEXT_INGESTION=NO
RESTRICTED_SOURCE_AUTOMATIC_EXTERNAL_SYNC=NO
```

The file names inside the archive were listed only to classify it; no content was read or
printed. It is not copied into canonical knowledge, and a future Brain may index that it exists
without reading it.
