# Instrucciones canónicas para agentes

## Identidad y alcance

- Organización responsable: ISAGRUB CORPORACIÓN C.L.
- Nombre comercial: GYPPORT®.
- Producto: GYPPORT® / Gystigo.
- Este directorio administra conocimiento y continuidad; no es el repositorio
  de código de producto.

## Lectura obligatoria

Antes de trabajar, leer en este orden:

1. `.chatgpt/PROJECT_CONTEXT.md`;
2. `.chatgpt/CANONICAL_MEMORY.md`;
3. `.chatgpt/CURRENT_STATE.md`;
4. `.chatgpt/DECISION_REGISTER.md`;
5. `.chatgpt/UNRESOLVED_REGISTER.md`;
6. los documentos de gobernanza aplicables al alcance.

Si un archivo está vacío o contiene marcadores pendientes, no inventar su
contenido. Registrar la ausencia como asunto no resuelto.

## Jerarquía de evidencia

1. archivos y pruebas verificables;
2. decisiones aprobadas registradas;
3. evidencia fuente y trazabilidad;
4. auditorías independientes;
5. handoffs de implementación;
6. resúmenes de conversación como contexto.

No tratar memoria automática, conversación o inferencia como sustituto de
evidencia física.

## Reglas de trabajo

- Respetar propiedad única de cada norma, dato y capacidad.
- Diferenciar fuente, interpretación, recomendación y decisión corporativa.
- Mantener estados exactos; inventariar no equivale a procesar.
- Evitar duplicación, sobreingeniería y arquitectura especulativa.
- No modificar fuentes originales durante el procesamiento.
- No mover contenido a `Gystigo` sin alcance aprobado por Eduardo.
- No ejecutar staging, commit o push sin autorización expresa de Eduardo.
- No almacenar credenciales, tokens, claves, archivos `.env` ni secretos.
- Registrar el resultado y el siguiente paso en `CURRENT_STATE.md` o en un
  checkpoint del track.

## Colaboración entre IAs

Cuando exista, aplicar:

`Governance/architecture/GYPPORT_AI_COLLABORATION_EXECUTION_ORDER_v1.0.md`

En ausencia del documento, detener decisiones que dependan de su contenido y
registrar el asunto en `.chatgpt/UNRESOLVED_REGISTER.md`.

## Persistencia

No afirmar que un archivo existe en el equipo del propietario, NAS, Git o
repositorio remoto sin haber verificado esa ubicación. Diferenciar siempre:

```text
WORKSPACE_STATE
PHYSICAL_PC_STATE
LIBRARY_STATE
GIT_LOCAL_STATE
GIT_REMOTE_STATE
BACKUP_STATE
```

