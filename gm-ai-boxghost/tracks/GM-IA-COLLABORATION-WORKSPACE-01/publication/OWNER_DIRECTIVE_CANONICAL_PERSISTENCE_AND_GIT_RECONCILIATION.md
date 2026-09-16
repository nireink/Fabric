# Directiva del propietario — Persistencia canónica, reconciliación y publicación

```text
TRACK=GM-IA-COLLABORATION-WORKSPACE-01
SCOPE_VERSION=v0.1
MODE=CANONICAL_PERSISTENCE_AND_GIT_RECONCILIATION
STATUS=OWNER_DIRECTIVE_ACTIVE
ACTOR=eduardo
ACTOR_TYPE=HUMAN
RECORDED_BY=codex
RECORDED_AT=2026-08-02T09:37:53-05:00
SENSITIVITY=INTERNAL
OWNER_AUTHORIZATION=ALREADY_GRANTED
OWNER_REAPPROVAL_REQUIRED=NO
STAGING_AUTHORIZED=YES
COMMIT_AUTHORIZED=YES
PUSH_AUTHORIZED=YES
LOCAL_PREVIOUS_HEAD=84feea2f5f4cfd2a6feb446eabc495f9e3a8c33d
FRESH_REMOTE_HEAD=479c1e87bfeb97820587b408ac4f9b2bc546fe1e
```

## Solicitud original completa

Eduardo ordena que toda la trazabilidad de cada implementación se conserve
permanentemente en:

```text
D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT\Fabric\gm-ai-boxghost
PERSISTENT_MEMORY=GM_AI_BOXGHOST
RETENTION=PERMANENT
BOXGHOST_CANONICAL=YES
CONVERSATION_ONLY_STATE_ALLOWED=NO
DO_NOT_MODIFY_UNRELATED_FABRIC_CONTENT
GM_AI_BOXGHOST_PROCESS_WRITES=REQUIRED
```

La persistencia incluye solicitud original, prompts, respuestas completas,
intervenciones, revisiones, alcance, aprobaciones y rechazos, comandos,
pruebas, compilaciones, estados Git, diffs, parches, manifiestos, hashes,
evidencias, checkpoints, bloqueos, intentos fallidos, reconciliaciones,
decisiones de cierre, commit, publicación y contexto de reanudación. También
incluye temporales con valor probatorio. Excluye contraseñas, tokens, cookies,
credenciales, secretos y cachés regenerables sin valor probatorio.

Los archivos de BoxGhost no deben entrar en el commit de
`Modules/gm-ai-workspace`. No se autoriza staging, commit ni push del
repositorio de Fabric.

Cada intervención debe persistir antes, durante y después: solicitud, prompt,
agente, alcance, autorización, estado inicial, HEAD y working tree; comandos,
resultados, evidencia, hallazgos, parches, checkpoints y bloqueos; respuesta
final, resultado técnico, hashes, estado actualizado, evento append-only y un
único siguiente paso. Ninguna intervención se considera completada si solo
existe en conversación.

Antes de reconciliar Git se debe registrar
`publication/PUBLICATION_ATTEMPT_02_REMOTE_DIVERGENCE_BLOCKED.md`, actualizar
`TRACK_STATE.md`, `CONTEXT_PACK.md`, `dialog/events.jsonl` y
`SOURCE_MANIFEST.json`, conservar `OWNER_REAPPROVAL_REQUIRED=NO`, y no marcar
la publicación como completada.

La verificación remota debe probar que la rama local es `master`, el HEAD
local es `84feea2f5f4cfd2a6feb446eabc495f9e3a8c33d`, `origin/master` es
`479c1e87bfeb97820587b408ac4f9b2bc546fe1e`, el commit remoto es hijo directo,
solo modifica `README.md`, agrega 26 líneas, no existen otros commits nuevos y
Fabric no fue modificado por ese commit. Deben conservarse metadatos, rutas,
diff remoto y su hash, estado local, diff local y hashes, después de verificar
que no contienen secretos.

La reconciliación debe proteger todos los cambios locales, avanzar `master`
por fast-forward, reaplicar la implementación auditada y conservar tanto las
26 líneas remotas como el contenido local v0.1. Se prohíben `git reset --hard`,
`git checkout --`, `git push --force` y `git push --force-with-lease`.

Si Git combina inequívocamente ambos cambios se continúa. Si hay contradicción
semántica debe detenerse sin staging, commit ni push con:

```text
VERDICT=BLOCKED
BLOCKER=README_SEMANTIC_CONFLICT_REQUIRES_OWNER_DECISION
```

En ese caso no se solicita aprobación general, únicamente una decisión puntual
sobre el contenido contradictorio.

Si la reconciliación fuera conforme, se deben ejecutar nuevamente backend
tests y build con Maven Wrapper, frontend tests y build, `npm audit` sin fix,
`git diff --check`, inspecciones completas del status, diff, no rastreados,
alcance v0.1, ausencia del iniciador v0.2 y conservación de los dos hallazgos
LOW. Solo después se autoriza staging selectivo, commit exacto
`feat(ai-workspace): implement read-only workspace v0.1` y push normal de
`master` a `origin/master`, sin force push ni PR salvo bloqueo por protección.

Después del resultado se deben persistir commit, padre, SHA, mensaje, archivos,
push, remote HEAD, pruebas, builds, working tree, fecha, agente y hashes, y
actualizar los cuatro archivos operativos. `PUBLISHED` solo puede declararse
si la persistencia final en BoxGhost fue completada.

## Procedencia

```text
SOURCE_KIND=OWNER_PASTED_DIRECTIVE
SOURCE_ATTACHMENT=C:\Users\elbur\.codex\attachments\05c4b81b-5673-4f7c-9c57-362ea5515e5a\pasted-text.txt
NOTE=El contenido se transcribió sin secretos. Esta copia canónica conserva todas las obligaciones operativas de la solicitud.
```
