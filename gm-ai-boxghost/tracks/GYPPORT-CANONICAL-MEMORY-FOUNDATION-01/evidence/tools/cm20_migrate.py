# -*- coding: utf-8 -*-
"""GYPPORT_CANONICAL_MEMORY_FOUNDATION_01 - canonical memory migration executor.

    python cm20_migrate.py plan      build the operation list, check preconditions, write the manifest
    python cm20_migrate.py backup    copy every touched file into the scratchpad backup, byte-exact
    python cm20_migrate.py execute   perform the file operations (moves, duplicate removals, archives, banners)
    python cm20_migrate.py verify    re-hash the targets, prove byte preservation, rewrite the manifest

No git command is ever run. Nothing is deleted: removals move the file into the scratchpad.
"""
import datetime
import hashlib
import json
import os
import re
import shutil
import sys
import unicodedata

W = r"D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT"
S = r"D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT-Storage"
TMP = r"C:\Users\elbur\AppData\Local\Temp\claude\D--NZXTG7-GYPPORT-GYPPORT-ERP"
SP = os.path.join(TMP, "8142c294-1815-45b4-90ee-94d1198faa7d", "scratchpad")
FB = os.path.join(TMP, "f606bf51-4ad3-479f-9e08-3fe15dce65c0", "scratchpad", "fabric-backup")

G = os.path.join(W, "Gystigo")
F = os.path.join(W, "Fabric")
BG = os.path.join(F, "gm-ai-boxghost")
K = os.path.join(F, "Knowledge")
U = os.path.join(K, "00-GYPPORT-UNIVERSE")
TR = os.path.join(BG, "tracks")
LEG = os.path.join(W, "Governance", "GYPPORT_Governance_Architecture")
STEP_TRACK = "GYPPORT-CANONICAL-MEMORY-FOUNDATION-01"
IMP = os.path.join(BG, "imports", STEP_TRACK)
EV = os.path.join(TR, STEP_TRACK, "evidence")
RETIRED = os.path.join(TR, STEP_TRACK, "artifacts", "retired")
BASE_TRACK = "GYPPORT-UNIVERSAL-MDM-VERIFICATION-BASELINE-FOUNDATION-01"
PKG_TRACK = "GYPPORT-GLOBAL-ACCOUNT-TENANT-MEMBERSHIP-FOUNDATION-15"
BACKUP = os.path.join(SP, "cm_backup")
REMOVED = os.path.join(SP, "cm_removed")
RESULTS = os.path.join(SP, "cm20_results.json")
MANIFEST = os.path.join(EV, "MIGRATION_MANIFEST.md")
TRACK_RX = re.compile(r"^[A-Z0-9][A-Z0-9-]{2,99}$")
TODAY = "2026-09-15"

MEMARCH = "Fabric/Knowledge/00-GYPPORT-UNIVERSE/GYPPORT_MEMORY_ARCHITECTURE.md"


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def label(path):
    for root, name in ((W, "GYPPORT"), (S, "GYPPORT-Storage"), (TMP, "CLAUDE-TEMP")):
        if path.startswith(root):
            return (name + path[len(root):]).replace("\\", "/")
    return path.replace("\\", "/")


def repo_of(path):
    if path.startswith(LEG):
        return "GYPPORT_Governance_Architecture (git)"
    if path.startswith(G):
        return "Gystigo (git)"
    if path.startswith(F):
        return "Fabric (git)"
    if path.startswith(os.path.join(W, "Engineering")):
        return "Engineering (git)"
    if path.startswith(S):
        return "none (GYPPORT-Storage, Drive-synced)"
    if path.startswith(TMP):
        return "none (Claude scratchpad)"
    return "none (workspace root)"


def norm_track(raw):
    raw = raw.split(u"\u00b7")[0].split("**Step")[0]
    raw = raw.replace("*", "").replace("`", "").strip().rstrip(".").strip()
    raw = unicodedata.normalize("NFKD", raw).encode("ascii", "ignore").decode()
    return re.sub(r"[^A-Za-z0-9]+", "-", raw).strip("-").upper()


TRACK_PATTERNS = [re.compile(r"TRACK\s*=\s*([A-Za-z0-9_-]+)"),
                  re.compile(r"\*\*Track:\*\*\s*(.+)"),
                  re.compile(r"(?:^|\.\s|\s)Track:\s*(.+)")]


def declared_track(path):
    text = open(path, "rb").read().decode("utf-8", "replace").splitlines()[:45]
    for line in text:
        for rx in TRACK_PATTERNS:
            m = rx.search(line)
            if m:
                t = norm_track(m.group(1))
                if TRACK_RX.match(t):
                    return t
    return None


BANNER_HEAD = (u"> **HISTORICO - NO AUTORITATIVO (2026-09-15, GYPPORT_CANONICAL_MEMORY_FOUNDATION_01).** "
               u"Este documento se conserva como historia. El repositorio heredado `Governance/GYPPORT_Governance_Architecture` "
               u"no tiene autoridad activa: el conocimiento canonico de GYPPORT vive en `Fabric/Knowledge` y la arquitectura de "
               u"memoria en `" + MEMARCH + u"`.\n>\n> **Sustituido por:** ")

BANNERS = {
    os.path.join(LEG, "decisions", "adr", "ADR-0001-gypport-ecosystem-structure.md"):
        u"la decision del Owner del 2026-09-15 (Fabric = raiz unica de memoria: `Fabric/Knowledge` + `Fabric/gm-ai-boxghost`), "
        u"`Fabric/Knowledge/00-GYPPORT-UNIVERSE/GYPPORT_BUSINESS_PLATFORM_UNIVERSAL_CANONICAL_ARCHITECTURE_2026-09-12.md` y la "
        u"estructura real del workspace (`Gystigo/`, `Fabric/`, `Modules/gm-*`).",
    os.path.join(LEG, "architecture", "taxonomy", "GYPPORT_ARCHITECTURAL_TAXONOMY.md"):
        u"`" + MEMARCH + u"` (roles de Fabric/Knowledge, Fabric/gm-ai-boxghost, GYPPORT-Storage y Modules/gm-ai-workspace). "
        u"La definicion de Fabric como \"conocimiento candidato\" y de AIWS/GDA como memoria operativa/institucional ya no aplica.",
    os.path.join(LEG, "architecture", "data", "DATA_OWNERSHIP_CATALOG.md"):
        u"`Fabric/Knowledge/00-GYPPORT-UNIVERSE/GYPPORT_UNIVERSE_CANONICAL_BASELINE.md`, "
        u"`Fabric/Knowledge/00-GYPPORT-UNIVERSE/GYPPORT_BUSINESS_PLATFORM_UNIVERSAL_DATA_DOMAIN_CONTEXT_2026-09-13.md`, "
        u"los ADR-0014..ADR-0017 de `Gystigo/docs/architecture/decisions/` y las matrices de ownership de cada modulo. "
        u"Se conserva como instantanea fechada verificada contra `Dump20260716.sql`.",
    os.path.join(LEG, "standards", "DATABASE_MIGRATION_STANDARD.md"):
        u"la cadena de migraciones vigente en `Gystigo/database/core/migration` y `Gystigo/database/modules/<modulo>/migration` "
        u"(secuencia de versiones unica B17+V18..V58, aceptada por el Owner en los STEP 08-15). La extraccion fisica de la seccion 1 "
        u"si se ejecuto; el historial por componente de la seccion 4 no se adopto.",
    os.path.join(LEG, "standards", "MODULE_CONTRACT_STANDARD.md"):
        u"la implementacion vigente: las migraciones de modulo viven en el Host (`Gystigo/database/modules/`) con historial unico, "
        u"no existe `module.yaml` en ningun modulo y los repositorios usan `gm-<nombre>`. La reconciliacion pendiente esta registrada como "
        u"`MODULE_YAML_VS_CURRENT_GYSTIGO_RUNTIME_WIRING_RECONCILIATION=NOT_FULLY_CLOSED` en "
        u"`Engineering/Git/gypport-engineering-template/docs/governance/architecture/EXTERNAL_REFERENCES.md`.",
    os.path.join(LEG, "standards", "REPOSITORY_NAMING_STANDARD.md"):
        u"los repositorios reales `Modules/gm-<nombre>` (por ejemplo `gm-human-resources`, canonicalizacion del STEP 04 aceptada por el Owner "
        u"el 2026-09-10) y `Modules/gm-ai-workspace`. La convencion `GM_Pascal_Snake_Case` no esta en uso.",
    os.path.join(W, "Governance", "GYPPORT_AI_DEVELOPER_ENGINEERING_STANDARD_v1.0.md"):
        u"`Gystigo/docs/governance/engineering/standards/GYPPORT_AI_DEVELOPER_ENGINEERING_STANDARD_v1.1.md` (APPROVED 2026-07-28).",
}

DOCS_AI_TYPE = {"claude": "interventions/claude", "codex": "interventions/codex", "decisions": "decisions",
                "handoffs/codex-to-review": "handoffs/codex-to-review", "reviews/accepted": "audits/accepted"}
TRACK_OVERRIDE = {"handoffs/codex-to-review/BACKEND_BOUNDARY_OWNERSHIP_01_3_2026-07-26_CORRECTED.md":
                  ("BACKEND-CAPABILITY-INVENTORY-01",
                   "no declara track; el review aceptado del mismo STEP 01.3 "
                   "(BACKEND_BOUNDARY_OWNERSHIP_01_3_CLAUDE_VERIFICATION_2026-07-26.md) declara BACKEND-CAPABILITY-INVENTORY-01")}
CORPUS = {"ACTA_APROBACION_FASE1_Y_DOCUMENTOS_GYPPORT.md": "approvals",
          "DECISION_SUPPORT_BLOQUEADORES_UNR_GYPPORT.md": "decisions",
          "DOCUMENTO_MAESTRO_FASE1_BASE_CONOCIMIENTO_GYPPORT_v1.1_INCREMENTAL.md": "artifacts",
          "DOCUMENTO_MAESTRO_FASE1_BASE_DE_CONOCIMIENTO_GYPPORT.md": "artifacts",
          "ESPECIFICACION_RECEPCION_CORPUS_GYPPORT.md": "artifacts",
          "INDICE_MAESTRO_Y_GUIA_RAPIDA_GYPPORT.md": "artifacts",
          "PROTOCOLO_FASE2_MODELADO_DOMINIO_GYPPORT.md": "artifacts",
          "PROTOCOLO_FASE3_DOCUMENTACION_ESPECIALIZADA_GYPPORT.md": "artifacts"}
CORPUS_TRACK = "GYPPORT-KNOWLEDGE-CORPUS-DERIVED-STANDARDS-01"

CLASS_RULES = [
    (os.path.join(G, "docs", "ai"), "OPERATIONAL_MEMORY", "migrated to BoxGhost by this STEP (rows above)"),
    (os.path.join(G, ".claude", "worktrees"), "HISTORICAL_SUPERSEDED", "tool-managed git checkouts of older commits; non-authoritative copies"),
    (os.path.join(G, ".claude"), "REPOSITORY_TECHNICAL_ENTRYPOINT", "local Claude Code configuration of the Gystigo repository"),
    (os.path.join(G, "docs"), "PRODUCT_SPECIFIC_TECHNICAL_DOC", "product/platform engineering documentation versioned with the product"),
    (os.path.join(G, "database"), "PRODUCT_SPECIFIC_TECHNICAL_DOC", "product database migrations and analysis"),
    (G, "PRODUCT_SPECIFIC_TECHNICAL_DOC", "product code, migrations, tests and local agent entrypoints"),
    (os.path.join(F, "Knowledge"), "CANONICAL_KNOWLEDGE", "canonical knowledge root"),
    (os.path.join(F, "gm-ai-boxghost"), "OPERATIONAL_MEMORY", "operational memory root"),
    (os.path.join(F, "tools"), "CANONICAL_KNOWLEDGE", "tooling of the canonical verified-baseline procedure"),
    (os.path.join(F, ".claude"), "REPOSITORY_TECHNICAL_ENTRYPOINT", "local Claude Code configuration of the Fabric repository"),
    (F, "CANONICAL_KNOWLEDGE", "single GYPPORT memory root"),
    (os.path.join(W, "Modules", "gm-ai-workspace"), "REPOSITORY_TECHNICAL_ENTRYPOINT", "APPLICATION_AND_ORCHESTRATOR; unchanged by this STEP"),
    (os.path.join(W, "Modules"), "PRODUCT_SPECIFIC_TECHNICAL_DOC", "module repositories (code, docs, migrations)"),
    (os.path.join(W, "Engineering"), "PRODUCT_SPECIFIC_TECHNICAL_DOC", "repository template for GYPPORT repositories"),
    (LEG, "HISTORICAL_SUPERSEDED", "legacy governance repository; no active authority"),
    (os.path.join(W, "Governance"), "HISTORICAL_SUPERSEDED", "legacy governance area; no active authority"),
    (os.path.join(W, "Intelligence"), "HISTORICAL_SUPERSEDED", "legacy empty GAKS repository; knowledge lives in Fabric/Knowledge"),
    (os.path.join(W, "UI_Experiments"), "HISTORICAL_SUPERSEDED", "historical UI experiment clones; non-authoritative copies"),
    (os.path.join(W, "recovery"), "RAW_PERSISTENT_SOURCE", "raw repository recovery package (moved to GYPPORT-Storage by this STEP)"),
    (os.path.join(W, "Transfer"), "RAW_PERSISTENT_SOURCE", "raw migration archive; contains credentials (docker/.env, application.yaml): kept local until Owner sanitization"),
    (os.path.join(W, ".claude"), "REPOSITORY_TECHNICAL_ENTRYPOINT", "workspace-level Claude Code configuration"),
    (os.path.join(W, ".github"), "REPOSITORY_TECHNICAL_ENTRYPOINT", "workspace-level tooling configuration"),
    (os.path.join(W, ".vscode"), "REPOSITORY_TECHNICAL_ENTRYPOINT", "workspace-level editor configuration"),
    (os.path.join(W, "Angie Gisell"), "OUT_OF_SCOPE_PERSONAL", "personal file, not GYPPORT material; left untouched"),
    (os.path.join(S, "Fabric", "Inventory"), "RAW_PERSISTENT_SOURCE", "heavy track inventory packages (CSV datasets)"),
    (os.path.join(S, "Gystigo", "Inventory"), "RAW_PERSISTENT_SOURCE", "heavy track inventory packages (CSV datasets)"),
    (os.path.join(S, "Fabric", "Knowledge", "Standards"), "DUPLICATE", "byte-identical copies of Gystigo/docs/governance/standards (removed by this STEP)"),
    (os.path.join(S, "Fabric", "Knowledge", "AI"), "HISTORICAL_SUPERSEDED", "dated backup of a Fabric/Knowledge/AI document"),
    (os.path.join(S, "Fabric"), "RAW_PERSISTENT_SOURCE", "raw sources: books, PDFs, dumps, concept files"),
    (os.path.join(S, "Gystigo", "Nueva carpeta"), "HISTORICAL_SUPERSEDED", "dated backups of agent governance files"),
    (os.path.join(S, "Gystigo"), "HISTORICAL_SUPERSEDED", "dated backups and raw archives of the Gystigo repository"),
    (os.path.join(S, "IAs Agents", "20260728 Post"), "HISTORICAL_SUPERSEDED", "historical agent-governance and collaboration copies (2026-07-28)"),
    (os.path.join(S, "IAs Agents", "Codex"), "RAW_PERSISTENT_SOURCE", "archived Codex project bases (code snapshots)"),
    (os.path.join(S, "IAs Agents", "Claude"), "RAW_PERSISTENT_SOURCE", "archived Claude project bases"),
    (os.path.join(S, "IAs Agents"), "RAW_PERSISTENT_SOURCE", "archived AI project bases"),
    (S, "RAW_PERSISTENT_SOURCE", "raw persistent storage root"),
    (TMP, "TEMPORARY_DISPOSABLE", "Claude scratchpads: working files, tool outputs and source copies; not durable GYPPORT memory"),
]


def ops_list():
    ops = []

    def add(mode, src, dst, action, classification, role, reason, twin=None):
        ops.append({"id": "OP%03d" % (len(ops) + 1), "mode": mode, "src": src, "dst": dst, "action": action,
                    "classification": classification, "role": role, "reason": reason, "twin": twin})

    # --- A. Gystigo/docs/ai -------------------------------------------------
    ai = os.path.join(G, "docs", "ai")
    for root, dirs, files in os.walk(ai):
        for f in sorted(files):
            src = os.path.join(root, f)
            rel = os.path.relpath(src, ai).replace("\\", "/")
            if rel == "shared/AI_COLLABORATION.md":
                continue  # handled in section D
            if rel in ("README.md", "shared/README_UIX_AGENT_UPDATE.md"):
                add("move", src, os.path.join(IMP, "gystigo", "docs", "ai", *rel.split("/")),
                    "MOVE_BYTE_EXACT", "OPERATIONAL_MEMORY",
                    "index/note of the retired docs/ai folder",
                    "operational AI artifact without a declared track: imported byte-exact, source path preserved")
                continue
            folder = rel.rsplit("/", 1)[0]
            typ = DOCS_AI_TYPE.get(folder)
            if typ is None:
                raise SystemExit("unmapped docs/ai file: " + rel)
            if rel in TRACK_OVERRIDE:
                track, why = TRACK_OVERRIDE[rel]
            else:
                track, why = declared_track(src), "declared Track header in the document"
            if not track:
                raise SystemExit("no declared track for " + rel)
            add("move", src, os.path.join(TR, track, *typ.split("/"), f),
                "MOVE_BYTE_EXACT", "OPERATIONAL_MEMORY",
                {"interventions/claude": "durable instruction/prompt to Claude",
                 "interventions/codex": "durable instruction/prompt to Codex",
                 "decisions": "Owner decision/acceptance record",
                 "handoffs/codex-to-review": "Codex handoff for review",
                 "audits/accepted": "accepted independent review/audit"}[typ],
                "operational execution history belongs to BoxGhost; track from " + why)

    # --- B. Gystigo/docs/guide/chats_importantes ----------------------------
    ch = os.path.join(G, "docs", "guide", "chats_importantes")
    for f in sorted(os.listdir(ch)):
        add("move", os.path.join(ch, f), os.path.join(IMP, "gystigo", "docs", "guide", "chats_importantes", f),
            "MOVE_BYTE_EXACT", "OPERATIONAL_MEMORY", "AI conversation kept as an important chat",
            "conversations are operational memory; no declared track, imported byte-exact with its source path")

    # --- C. agent files and the Gystigo rules pointer ------------------------
    for name in ("AGENTS", "CLAUDE", "CHATGPT", "CODEX"):
        add("archive_copy", os.path.join(G, name + ".md"), os.path.join(S, "Gystigo", name + "_Backup_20260915.md"),
            "ARCHIVE_AS_HISTORY", "HISTORICAL_SUPERSEDED", "pre-migration agent file (Owner WIP, not in git)",
            "byte-exact pre-migration copy kept in the Owner's archive convention before the file is replaced or removed")
    for name in ("CHATGPT", "CODEX"):
        add("move_removed", os.path.join(G, name + ".md"), None,
            "REMOVE_OBSOLETE_DUPLICATE", "DUPLICATE",
            "agent governance file duplicated in the product repository",
            "no tool discovers it (Codex reads AGENTS.md only; ChatGPT has no filesystem discovery); canonical content now in "
            "Fabric/Knowledge/00-GYPPORT-UNIVERSE/agents/" + name + ".md")
    add("move_removed", os.path.join(G, "Reglas.md"), None, "REMOVE_OBSOLETE_DUPLICATE", "DUPLICATE",
        "compatibility pointer to the canonical rules log",
        "no tool requires it; the generator defaults to and only accepts the canonical log; transitional pointers are not allowed")
    for name in ("AGENTS", "CLAUDE"):
        add("replace", os.path.join(G, name + ".md"), os.path.join(G, name + ".md"),
            "REPLACE_WITH_FINAL_CANONICAL_VERSION", "REPOSITORY_TECHNICAL_ENTRYPOINT",
            "local agent entrypoint of the product repository",
            "AGENTS.md is required by Codex discovery and by the Gystigo Toolchain root marker; CLAUDE.md is required by Claude Code "
            "discovery; both keep only pointer + local technical notes, no governance text")

    # --- D. collaboration governance ----------------------------------------
    add("move", os.path.join(G, "docs", "architecture", "GYPPORT_AI_COLLABORATION_EXECUTION_ORDER_v1.0.md"),
        os.path.join(U, "ai-collaboration", "GYPPORT_AI_COLLABORATION_EXECUTION_ORDER_v1.0.md"),
        "MOVE_WITH_MINIMAL_REFERENCE_UPDATE", "CANONICAL_KNOWLEDGE", "approved canonical AI collaboration execution order",
        "collaboration governance is canonical knowledge; only its own location line and the operational paths of section 12.1 are updated")
    add("move", os.path.join(G, "docs", "ai", "shared", "AI_COLLABORATION.md"),
        os.path.join(U, "ai-collaboration", "AI_COLLABORATION.md"),
        "MOVE_WITH_MINIMAL_REFERENCE_UPDATE", "CANONICAL_KNOWLEDGE", "English entry point of the collaboration standard",
        "collaboration governance is canonical knowledge; only the references to the execution order and to the dialog record are updated")

    # --- E. Knowledge housekeeping ------------------------------------------
    add("move", os.path.join(U, "README_INSTALLACION.md"), os.path.join(RETIRED, "README_INSTALLACION.md"),
        "ARCHIVE_AS_HISTORY", "HISTORICAL_SUPERSEDED", "install note placing the agent files in Gystigo",
        "superseded by the canonical agents folder and the Gystigo entrypoints; kept byte-exact as retired operational artifact")
    add("move_contained", os.path.join(U, "GYPPORT_MDM_FOUNDATION_MEMORY_2026-09-11_Backup.md"), None,
        "REMOVE_OBSOLETE_DUPLICATE", "DUPLICATE", "backup copy of an MDM foundation memory document",
        "every non-empty line is present in GYPPORT_MDM_FOUNDATION_MEMORY_2026-09-11.md: no unique content",
        twin=os.path.join(U, "GYPPORT_MDM_FOUNDATION_MEMORY_2026-09-11.md"))

    # --- F. Fabric root housekeeping ----------------------------------------
    add("move", os.path.join(F, "Governance", "policies", "GYPPORT_SAAS_DEPLOYMENT_DISTRIBUTION_AND_DEPENDENCY_GOVERNANCE_STANDARD_v1.0.md"),
        os.path.join(K, "Architecture", "GYPPORT_SAAS_DEPLOYMENT_DISTRIBUTION_AND_DEPENDENCY_GOVERNANCE_STANDARD_v1.0.md"),
        "MOVE_BYTE_EXACT", "CANONICAL_KNOWLEDGE", "proposed canonical SaaS deployment standard",
        "a second governance location inside Fabric is not allowed: canonical knowledge lives under Fabric/Knowledge")
    for rel in [",caludecode", "AI_Research", "Assets", "Private_State", ".codex", ".chatgpt", "Governance",
                os.path.join("Knowledge", "Books"), os.path.join("Knowledge", "Sources"),
                os.path.join("Knowledge", "Processing"), os.path.join("Knowledge", "Corpus")]:
        add("rmdir", os.path.join(F, rel), None, "REMOVE_OBSOLETE_DUPLICATE", "TEMPORARY_DISPOSABLE",
            "empty placeholder directory",
            "empty scaffolding whose role is owned elsewhere under the 2026-09-15 model (raw sources -> GYPPORT-Storage, "
            "processing/registers -> BoxGhost, governance -> Fabric/Knowledge)")

    # --- G. legacy governance ------------------------------------------------
    add("move", os.path.join(LEG, "governance", "retention", "ENGINEERING_ARTIFACT_RETENTION_POLICY.md"),
        os.path.join(K, "Architecture", "ENGINEERING_ARTIFACT_RETENTION_POLICY.md"),
        "MOVE_WITH_MINIMAL_REFERENCE_UPDATE", "CANONICAL_KNOWLEDGE", "approved engineering artifact retention policy",
        "still applicable and not contradicted (5 worktrees and 104 toolchain snapshots exist today); canonical knowledge now lives in Fabric/Knowledge")
    for path in BANNERS:
        add("banner", path, path, "ARCHIVE_AS_HISTORY", "HISTORICAL_SUPERSEDED", "approved legacy governance document",
            "kept as history with an explicit non-authoritative status banner; git history untouched")

    # --- H. GYPPORT-Storage ---------------------------------------------------
    std = os.path.join(S, "Fabric", "Knowledge", "Standards")
    for f in sorted(os.listdir(std)):
        add("move_dup", os.path.join(std, f), None, "REMOVE_OBSOLETE_DUPLICATE", "DUPLICATE",
            "\"Master\" copy of a Gystigo standards document",
            "byte-identical to the git-tracked Gystigo/docs/governance/standards copy; GYPPORT-Storage must not hold a duplicate canonical role",
            twin=os.path.join(G, "docs", "governance", "standards", f))
    add("move_dup", os.path.join(S, "IAs Agents", "gm-ai-workspace", "CLAUDE_CHAT_CRITICAL_CLASSIFICATION_REVIEW.md"), None,
        "REMOVE_OBSOLETE_DUPLICATE", "DUPLICATE", "copy of a BoxGhost intervention record",
        "byte-identical to the git-tracked BoxGhost copy already committed in Fabric",
        twin=os.path.join(BG, "tracks", "CONCEPTOS-INICIALES-CONTENT-ORGANIZATION-01", "interventions", "claude-chat",
                          "critical-classification-review", "CLAUDE_CHAT_CRITICAL_CLASSIFICATION_REVIEW.md"))
    lin = os.path.join(S, "IAs Agents", "GYPPORT Lineamientos Desarrollo ERP")
    for root, dirs, files in os.walk(lin):
        dirs[:] = [d for d in dirs if d not in ("Data", ".claude")]
        for f in sorted(files):
            if not f.lower().endswith(".md"):
                continue
            src = os.path.join(root, f)
            rel = os.path.relpath(src, lin)
            add("move", src, os.path.join(IMP, "gypport-storage", "IAs Agents", "GYPPORT Lineamientos Desarrollo ERP", rel),
                "MOVE_BYTE_EXACT", "OPERATIONAL_MEMORY",
                "multi-agent dialog record, durable prompts and agent responses (2026-07-26)",
                "raw AI collaboration history is operational memory, not raw storage; no declared track, imported byte-exact with its source path")
    cor = os.path.join(S, "IAs Agents", "Claude", "GYPPORT Corpus")
    for f in sorted(os.listdir(cor)):
        add("move", os.path.join(cor, f), os.path.join(TR, CORPUS_TRACK, CORPUS[f], f),
            "MOVE_BYTE_EXACT", "OPERATIONAL_MEMORY", "knowledge-corpus track deliverable, approval or decision packet",
            "approvals, decision packets and intervention deliverables are operational memory; track declared inside the package")
    rec = os.path.join(W, "recovery", "AIWS-004-NATIVE-RECOVERY")
    for f in sorted(os.listdir(rec)):
        add("move", os.path.join(rec, f), os.path.join(S, "Gystigo", "Recovery", "AIWS-004-NATIVE-RECOVERY", f),
            "MOVE_BYTE_EXACT", "RAW_PERSISTENT_SOURCE", "raw repository recovery package (2026-07-18)",
            "raw and heavy originals belong to GYPPORT-Storage, not to an arbitrary workspace folder; no secret pattern found")
    add("rmdir", os.path.join(W, "recovery"), None, "REMOVE_OBSOLETE_DUPLICATE", "TEMPORARY_DISPOSABLE",
        "empty folder after the recovery package moved", "empty directory")
    for src, dst in [(os.path.join(FB, "GYPPORT_MODULE_NAVIGATION_HIERARCHY.md"),
                      os.path.join(S, "Fabric", "Knowledge", "UIX", "GYPPORT_MODULE_NAVIGATION_HIERARCHY_BACKUP_20260908.md")),
                     (os.path.join(FB, "GYPPORT_UIX_IMPLEMENTATION_AND_COMPLIANCE_GUIDE.md"),
                      os.path.join(S, "Fabric", "Knowledge", "UIX", "GYPPORT_UIX_IMPLEMENTATION_AND_COMPLIANCE_GUIDE_BACKUP_20260909.md")),
                     (os.path.join(FB, "GYPPORT_ORGANIZATION_CONTROL_FOUNDATION.md"),
                      os.path.join(S, "Fabric", "Knowledge", "Security", "GYPPORT_ORGANIZATION_CONTROL_FOUNDATION_BACKUP_20260908.md"))]:
        add("move", src, dst, "MOVE_BYTE_EXACT", "HISTORICAL_SUPERSEDED",
            "pre-edit copy of a canonical Knowledge document, kept only in a Claude scratchpad",
            "valuable temp-only artifact promoted to the Owner's archive convention in GYPPORT-Storage")

    # --- H2. directories left empty by the migration --------------------------
    for path, why in [(os.path.join(G, "docs", "ai"),
                       "the AI operational folder of the product repository is retired; its content lives in BoxGhost"),
                      (os.path.join(G, "docs", "guide"),
                       "empty after the important chats moved to BoxGhost"),
                      (os.path.join(S, "IAs Agents", "gm-ai-workspace"),
                       "empty after the duplicated BoxGhost record was removed"),
                      (os.path.join(S, "Fabric", "Knowledge", "Standards"),
                       "empty after the duplicated standards copies were removed; GYPPORT-Storage is not a standards master"),
                      (os.path.join(S, "IAs Agents", "Claude", "GYPPORT Corpus"),
                       "empty after the knowledge-corpus track records moved to BoxGhost"),
                      (os.path.join(S, "IAs Agents", "GYPPORT Lineamientos Desarrollo ERP", "Claude"),
                       "empty after the agent response record moved to BoxGhost"),
                      (os.path.join(S, "IAs Agents", "GYPPORT Lineamientos Desarrollo ERP", "Codex"),
                       "empty after the agent response record moved to BoxGhost")]:
        add("rmdir", path, None, "REMOVE_OBSOLETE_DUPLICATE", "TEMPORARY_DISPOSABLE",
            "directory left empty by this migration", why)

    # --- I. evidence promotion ------------------------------------------------
    for f in sorted(os.listdir(SP)):
        p = os.path.join(SP, f)
        if not os.path.isfile(p):
            continue
        if f.startswith("s15k_"):
            add("move", p, os.path.join(TR, PKG_TRACK, "evidence", "PKG-2C-COMMIT-GATE-2026-09-15", f),
                "MOVE_BYTE_EXACT", "OPERATIONAL_MEMORY", "PKG-2C commit-gate verification evidence",
                "the evidence behind the Owner-accepted PKG-2C gate and its verified baseline belongs to BoxGhost, not to a scratchpad")
        elif f in ("bl01_evidence_pkg2c.json", "bl01_generator_tests.py", "bl02_generator_tests.py", "bl02_real_writes.py",
                   "bl02_pre_result.txt", "bl02_post_result.txt", "bl01_docs_check.py", "bl01_docs_check_result.txt",
                   "bl02_docs_check.py", "bl02_docs_check_result.txt", "bl01_fingerprint_before.txt", "bl01_fingerprint_after.txt",
                   "bl01_fingerprint_final.txt", "bl02_fingerprint_before.txt", "bl02_fingerprint_after.txt"):
            add("move", p, os.path.join(TR, BASE_TRACK, "evidence", f),
                "MOVE_BYTE_EXACT", "OPERATIONAL_MEMORY", "verified-baseline foundation evidence (generator input, tests, results)",
                "evidence of an Owner-reviewed STEP belongs to BoxGhost, not to a scratchpad")
        elif f in ("cm01_fingerprint_before.txt", "cm02_fingerprint_premigration.txt", "cm02_pkg2c_premigration.txt",
                   "cm04_refsearch_full.txt"):
            add("move", p, os.path.join(EV, f), "MOVE_BYTE_EXACT", "OPERATIONAL_MEMORY",
                "this STEP's pre-migration state and workspace search evidence",
                "created during this STEP; promoted to its canonical owner path before the STEP closes")
    return ops


def preflight(ops):
    problems = []
    seen_dst = {}
    moving = {os.path.normcase(o["src"]) for o in ops
              if o["mode"] in ("move", "move_dup", "move_contained", "move_removed")}
    for op in ops:
        if op["mode"] in ("create", "modify", "append", "keep"):
            continue
        if op["mode"] == "rmdir":
            if os.path.isdir(op["src"]):
                files = [os.path.join(r, f) for r, d, fs in os.walk(op["src"]) for f in fs
                         if os.path.normcase(os.path.join(r, f)) not in moving]
                if files:
                    problems.append("not empty after the planned moves: %s (%d files: %s)"
                                    % (label(op["src"]), len(files), label(files[0])))
            continue
        if not os.path.isfile(op["src"]):
            problems.append("missing source: " + label(op["src"]))
            continue
        if op["dst"]:
            if op["dst"] in seen_dst:
                problems.append("duplicate target: " + label(op["dst"]))
            seen_dst[op["dst"]] = op["id"]
            if os.path.exists(op["dst"]) and op["mode"] not in ("replace", "banner"):
                problems.append("target exists: " + label(op["dst"]))
        if op["mode"] == "move_dup":
            if not os.path.isfile(op["twin"]):
                problems.append("twin missing: " + label(op["twin"]))
            elif sha(op["twin"]) != sha(op["src"]):
                problems.append("twin differs: " + label(op["src"]))
        if op["mode"] == "move_contained":
            norm = lambda s: re.sub(r"\s+", " ", s).strip()
            keep = {norm(l) for l in open(op["twin"], "rb").read().decode("utf-8", "replace").splitlines() if norm(l)}
            miss = [l for l in open(op["src"], "rb").read().decode("utf-8", "replace").splitlines() if norm(l) and norm(l) not in keep]
            if miss:
                problems.append("not contained (%d unique lines): %s" % (len(miss), label(op["src"])))
    return problems


def coverage(ops):
    covered = set()
    for op in ops:
        for k in ("src", "dst", "twin"):
            if op.get(k):
                covered.add(os.path.normcase(op[k]))
    scope = []
    for root in (os.path.join(G, "docs", "ai"), F, os.path.join(W, "Governance"), os.path.join(W, "Intelligence"), S):
        for r, d, fs in os.walk(root):
            d[:] = [x for x in d if x != ".git"]
            scope += [os.path.join(r, f) for f in fs]
    hits = os.path.join(SP, "cm04_refsearch_full.txt")
    if os.path.isfile(hits):
        for line in open(hits, encoding="utf-8", errors="replace"):
            m = re.match(r"^  (.+?) :", line)
            if m:
                scope.append(os.path.join(W, m.group(1)))
    uncovered = []
    for p in scope:
        if os.path.normcase(p) in covered:
            continue
        if not any(os.path.normcase(p).startswith(os.path.normcase(pref) + os.sep) or os.path.normcase(p) == os.path.normcase(pref)
                   for pref, _, _ in CLASS_RULES):
            uncovered.append(p)
    return sorted(set(uncovered)), len(set(scope))


def manifest(ops, results, scope_count, uncovered, status):
    heads = json.load(open(os.path.join(SP, "cm20_heads.json"), encoding="utf-8")) if os.path.isfile(os.path.join(SP, "cm20_heads.json")) else {}
    out = []
    A = out.append
    A("# GYPPORT canonical memory migration manifest\n")
    A("```text")
    A("TRACK=GYPPORT_CANONICAL_MEMORY_FOUNDATION_01")
    A("MODE=OWNER_APPROVED_FULL_CANONICAL_MIGRATION")
    A("DATE=" + TODAY)
    A("STATUS=" + status)
    A("CANONICAL_KNOWLEDGE_ROOT=Fabric/Knowledge")
    A("OPERATIONAL_MEMORY_ROOT=Fabric/gm-ai-boxghost")
    A("RAW_PERSISTENT_STORAGE_ROOT=D:\\NZXTG7\\GYPPORT\\GYPPORT ERP\\GYPPORT-Storage")
    A("GM_AI_WORKSPACE_ROOT=Modules/gm-ai-workspace")
    A("OPERATIONS=%d" % len(ops))
    A("RELEVANT_FILES_IN_SCOPE=%d" % scope_count)
    A("UNCLASSIFIED_RELEVANT_FILES=%d" % len(uncovered))
    A("```\n")
    if heads:
        A("## Repository state before the migration\n")
        A("```text")
        for k in sorted(heads):
            A("%s=%s" % (k, heads[k]))
        A("```\n")
    A("## Per-artifact manifest\n")
    A("| ID | CURRENT_PATH | CURRENT_REPOSITORY | CONTENT_HASH | SIZE | CURRENT_ROLE | CLASSIFICATION | TARGET_PATH | ACTION | REASON |")
    A("|---|---|---|---|---|---|---|---|---|---|")
    for op in ops:
        r = results.get(op["id"], {})
        h = r.get("src_sha", "")
        A("| %s | `%s` | %s | `%s` | %s | %s | %s | `%s` | %s | %s |" % (
            op["id"], label(op["src"]), repo_of(op["src"]), h[:16], r.get("src_size", ""), op["role"],
            op["classification"], label(op["dst"]) if op["dst"] else (label(os.path.join(REMOVED, "…")) if op["mode"].startswith("move_") and not op["dst"] else "-"),
            op["action"], op["reason"]))
    A("\n## Gystigo/docs/ai detail (byte preservation)\n")
    A("| OLD_PATH | NEW_PATH | OLD_HASH | NEW_HASH | CLASSIFICATION | BYTE_PRESERVING | WHY |")
    A("|---|---|---|---|---|---|---|")
    for op in ops:
        if os.path.join(G, "docs", "ai") in op["src"] and op["mode"] == "move":
            r = results.get(op["id"], {})
            A("| `%s` | `%s` | `%s` | `%s` | %s | %s | %s |" % (
                label(op["src"]), label(op["dst"]), r.get("src_sha", "")[:16], r.get("dst_sha", "")[:16],
                op["classification"], r.get("byte_preserving", "pending"), op["reason"]))
    A("\n## Class-level classification of the remaining scope\n")
    A("| AREA | CLASSIFICATION | REASON |")
    A("|---|---|---|")
    for pref, cls, why in CLASS_RULES:
        A("| `%s` | %s | %s |" % (label(pref), cls, why))
    if uncovered:
        A("\n## UNCLASSIFIED (must be empty)\n")
        for p in uncovered[:200]:
            A("- `%s`" % label(p))
    os.makedirs(os.path.dirname(MANIFEST), exist_ok=True)
    open(MANIFEST, "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
    json.dump({"track": STEP_TRACK, "date": TODAY, "status": status,
               "operations": [dict(op, src=label(op["src"]), dst=label(op["dst"]) if op["dst"] else None,
                                   twin=label(op["twin"]) if op["twin"] else None, result=results.get(op["id"], {}))
                              for op in ops],
               "class_rules": [{"area": label(p), "classification": c, "reason": w} for p, c, w in CLASS_RULES],
               "unclassified": [label(p) for p in uncovered]},
              open(os.path.join(EV, "MIGRATION_MANIFEST.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)


def main():
    phase = sys.argv[1]
    ops_file = os.path.join(SP, "cm20_ops.json")
    if phase == "plan" or not os.path.isfile(ops_file):
        ops = ops_list()
        json.dump(ops, open(ops_file, "w", encoding="utf-8"), indent=1)
    else:
        ops = json.load(open(ops_file, encoding="utf-8"))
    results = json.load(open(RESULTS, encoding="utf-8")) if os.path.isfile(RESULTS) else {}
    if phase == "plan":
        problems = preflight(ops)
        for op in ops:
            if os.path.isfile(op["src"]):
                results.setdefault(op["id"], {}).update({"src_sha": sha(op["src"]), "src_size": os.path.getsize(op["src"])})
        uncovered, n = coverage(ops)
        manifest(ops, results, n, uncovered, "PLANNED")
        json.dump(results, open(RESULTS, "w", encoding="utf-8"), indent=1)
        print("OPERATIONS=%d PROBLEMS=%d SCOPE=%d UNCLASSIFIED=%d" % (len(ops), len(problems), n, len(uncovered)))
        for p in problems[:40]:
            print("  PROBLEM " + p)
        for p in uncovered[:40]:
            print("  UNCLASSIFIED " + label(p))
        counts = {}
        for op in ops:
            counts[op["action"]] = counts.get(op["action"], 0) + 1
        print("ACTIONS=" + json.dumps(counts))
    elif phase == "backup":
        n = 0
        for op in ops:
            if op["mode"] in ("rmdir", "keep", "create"):
                continue
            if os.path.isfile(op["src"]):
                dst = os.path.join(BACKUP, label(op["src"]).replace("/", os.sep))
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                if not os.path.exists(dst):
                    shutil.copy2(op["src"], dst)
                    assert sha(dst) == sha(op["src"])
                n += 1
        print("BACKED_UP=%d ROOT=%s" % (n, BACKUP))
    elif phase == "execute":
        done = 0
        for op in ops:
            if op["id"] in results and results[op["id"]].get("executed"):
                continue
            m, src, dst = op["mode"], op["src"], op["dst"]
            if m in ("keep", "create", "modify", "append", "replace"):
                continue
            if m == "rmdir":
                note = "removed"
                if os.path.isdir(src):
                    files = [f for r, d, fs in os.walk(src) for f in fs]
                    assert not files, "directory not empty: " + src
                    try:
                        shutil.rmtree(src)
                    except PermissionError:
                        # Google Drive keeps a handle on freshly emptied folders inside GYPPORT-Storage
                        note = "EMPTY_DIRECTORY_KEPT: locked by the Drive sync client (no data; access denied on rmdir)"
                        print("  " + note + ": " + label(src))
                results.setdefault(op["id"], {}).update({"executed": True, "removed_dir": note == "removed", "note": note})
            elif m in ("move", "archive_copy"):
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                assert not os.path.exists(dst), "target exists: " + dst
                shutil.copy2(src, dst)
                s1, s2 = sha(src), sha(dst)
                assert s1 == s2, "hash mismatch: " + src
                if m == "move":
                    os.remove(src)
                results.setdefault(op["id"], {}).update({"executed": True, "src_sha": s1, "dst_sha": s2, "byte_preserving": True})
            elif m in ("move_dup", "move_contained", "move_removed"):
                keep_copy = os.path.join(REMOVED, label(src).replace("/", os.sep))
                os.makedirs(os.path.dirname(keep_copy), exist_ok=True)
                shutil.copy2(src, keep_copy)
                s1 = sha(src)
                assert sha(keep_copy) == s1
                os.remove(src)
                results.setdefault(op["id"], {}).update({"executed": True, "src_sha": s1, "removed_to": label(keep_copy)})
            elif m == "banner":
                raw = open(src, "rb").read()
                bom = b"\xef\xbb\xbf" if raw.startswith(b"\xef\xbb\xbf") else b""
                body = raw[len(bom):]
                banner = (BANNER_HEAD + BANNERS[src] + u"\n\n").encode("utf-8")
                assert b"HISTORICO - NO AUTORITATIVO" not in body, "banner already present: " + src
                open(src, "wb").write(bom + banner + body)
                results.setdefault(op["id"], {}).update({"executed": True, "dst_sha": sha(src), "byte_preserving": False,
                                                         "note": "status banner prepended; original content unchanged below it"})
            done += 1
            json.dump(results, open(RESULTS, "w", encoding="utf-8"), indent=1)
        print("EXECUTED=%d" % done)
    elif phase == "verify":
        bad = []
        for op in ops:
            r = results.get(op["id"], {})
            if op["mode"] in ("move", "archive_copy"):
                if not os.path.isfile(op["dst"]):
                    bad.append("target missing " + label(op["dst"]))
                elif r.get("src_sha") and sha(op["dst"]) != r["src_sha"]:
                    if op["action"] == "MOVE_WITH_MINIMAL_REFERENCE_UPDATE":
                        results[op["id"]].update({"dst_sha": sha(op["dst"]), "byte_preserving": False,
                                                  "note": "moved byte-exact, then a minimal reference update was applied"})
                    else:
                        bad.append("hash changed " + label(op["dst"]))
                if op["mode"] == "move" and os.path.exists(op["src"]):
                    bad.append("source still present " + label(op["src"]))
            if op["mode"] in ("move_dup", "move_contained", "move_removed") and os.path.exists(op["src"]):
                bad.append("source still present " + label(op["src"]))
            if op["mode"] == "rmdir" and os.path.isdir(op["src"]):
                if str(r.get("note", "")).startswith("EMPTY_DIRECTORY_KEPT"):
                    files = [f for _, _, fs in os.walk(op["src"]) for f in fs]
                    if files:
                        bad.append("directory not empty " + label(op["src"]))
                else:
                    bad.append("directory still present " + label(op["src"]))
            if op["mode"] in ("replace", "banner") and os.path.isfile(op["src"]):
                results.setdefault(op["id"], {})["dst_sha"] = sha(op["src"])
        uncovered, n = coverage(ops)
        manifest(ops, results, n, uncovered, "EXECUTED" if not bad else "EXECUTED_WITH_PROBLEMS")
        json.dump(results, open(RESULTS, "w", encoding="utf-8"), indent=1)
        print("VERIFY_PROBLEMS=%d UNCLASSIFIED=%d" % (len(bad), len(uncovered)))
        for b in bad[:40]:
            print("  " + b)
    else:
        raise SystemExit("unknown phase")


if __name__ == "__main__":
    main()
