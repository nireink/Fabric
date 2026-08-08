# Configuración local de Codex

Codex puede cargar `.codex/config.toml` en proyectos que el usuario haya marcado
como confiables. `AGENTS.md` es la superficie principal para instrucciones
duraderas del proyecto.

Esta carpeta no debe contener autenticación, sesiones ni secretos. Las memorias
generadas de Codex pertenecen al estado local de Codex y requieren un respaldo
selectivo separado.

Subcarpetas reservadas:

- `agents/`: definiciones de roles aprobadas;
- `rules/`: reglas ejecutables aprobadas;
- `project-skills/`: skills propios versionados y auditados.

