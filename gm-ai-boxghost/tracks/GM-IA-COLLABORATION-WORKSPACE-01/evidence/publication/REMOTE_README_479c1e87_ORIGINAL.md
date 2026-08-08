# gm-ai-workspace
# ARCHIVED / SUPERSEDED

Este repositorio ya no es la arquitectura canónica de AI Workspace y no es fuente canónica ni fuente de verdad vigente. No debe recibir nuevas funcionalidades ni utilizarse para definir nueva gobernanza.

Su contenido se conserva como evidencia histórica y referencia técnica. La arquitectura canónica está prevista dentro de Gystigo/docs, incluyendo gobernanza, arquitectura, contexto y memoria operativa versionada.

Cualquier reutilización debe realizarse mediante una migración explícita, adaptada y auditada. No copiar automáticamente archivos, contratos o decisiones desde este repositorio.

Configuración de gyp-ai
gyp-ai requiere que GYPPORT_AI_ROOT apunte mediante una ruta absoluta al workspace operativo de IA:

GYPPORT_AI_ROOT=<absolute-path-to-operational-ai-workspace>
Ejemplo genérico para PowerShell:

$env:GYPPORT_AI_ROOT = "D:\path\to\GYPPORT\docs\ai"
La ruta debe existir y contener config/, findings/, reviews/ y decisions/. La herramienta falla explícitamente si falta la variable o la estructura requerida; no crea un workspace docs/ai alternativo.

GM_AI_Workspace
Sistema transversal de GYPPORT® para coordinar múltiples agentes de inteligencia artificial y participantes humanos sobre varios repositorios.

Estado actual
Repositorio inicializado.
Sin implementación funcional.
Arquitectura en fase de bootstrap.
Integración con GDA pendiente.
Workspace operativo externo: D:\docs\ai
