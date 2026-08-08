# Decisión del propietario — Reactivación del repositorio v0.1

```text
TRACK=GM-IA-COLLABORATION-WORKSPACE-01
SCOPE_VERSION=v0.1
DECISION_OWNER=eduardo
RECORDED_BY=codex
RECORDED_AT=2026-08-02T10:22:09-05:00
OWNER_DECISION=REACTIVATE_EXISTING_REPOSITORY
CANONICAL_REPOSITORY=Modules/gm-ai-workspace
ARCHIVED_DECLARATION_STATUS=SUPERSEDED
REMOTE_COMMIT_PRESERVED=YES
NEW_REPOSITORY_REQUIRED=NO
OWNER_REAPPROVAL_REQUIRED=NO
SENSITIVITY=INTERNAL
```

## Decisión

La implementación funcional read-only v0.1 reactiva el repositorio existente
`gm-ai-workspace` como repositorio canónico del producto. Las declaraciones
`ARCHIVED / SUPERSEDED`, la prohibición general de nuevas funcionalidades y
`Sin implementación funcional` describen un estado histórico anterior y dejan
de ser afirmaciones vigentes.

El commit remoto `479c1e87bfeb97820587b408ac4f9b2bc546fe1e` debe conservarse
íntegro en el historial. Su README original y diff están preservados en:

- `evidence/publication/REMOTE_README_479c1e87_ORIGINAL.md`;
- `evidence/publication/REMOTE_README_DIFF_84feea2f_TO_479c1e87.patch`.

El README final debe presentar el repositorio como activo y canónico, explicar
la relación de lectura con `gm-ai-boxghost`, describir únicamente las
capacidades y límites auditados de v0.1, excluir v0.2 y no corregir los dos
hallazgos LOW. Puede incluir una nota histórica breve sobre la reactivación.

## Efecto operativo

La contradicción semántica anterior queda resuelta. La publicación conserva la
autorización ya concedida para reconciliación, staging selectivo, commit y push
normal. No autoriza force push, reescritura del commit remoto ni un repositorio
nuevo.

```text
SOURCE_REF=attachments/codex/85035a06-ade3-4c4b-b5dc-0de25d8feded/pasted-text.txt
SOURCE_SHA256=7787c09be4339aad495960de24590762912a3ff5a0004bbe90fad1cc09535cfe
```
