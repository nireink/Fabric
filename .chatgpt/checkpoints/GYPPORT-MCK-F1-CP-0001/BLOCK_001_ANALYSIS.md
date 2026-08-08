# GYPPORT® - Modelo Corporativo de Conocimiento

## Checkpoint documental GYPPORT-MCK-F1-CP-0001

```text
PROTOCOL_VERSION=1.0
CHECKPOINT_DATE=2026-08-01
TIMEZONE=America/Guayaquil
STATE=IN_PROGRESS_PROVISIONAL
GLOBAL_CONCLUSIONS_ALLOWED=false
SOURCE_FILES_MODIFIED=false
CODE_ANALYZED=false
GYSTIGO_MODIFIED=false
STAGING=false
COMMIT=false
PUSH=false
```

Este checkpoint ejecuta de manera incremental la Fase 1 solicitada. No declara
completado el corpus ni emite conclusiones globales: el inventario físico está
fijado, pero el análisis profundo cubre todavía 2 de 175 binarios PDF únicos.

## 1. Inventario documental físico

### 1.1. Alcance verificado

| Raíz | PDF físicos |
|---|---:|
| `D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT\Fabric` | 232 |
| `D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT\Gystigo\docs` | 1 |
| **Total** | **233** |

Resumen de identidad binaria:

- 233 archivos físicos;
- 175 binarios SHA-256 únicos;
- 58 grupos de duplicados exactos;
- 58 copias físicas adicionales;
- 47.404 páginas físicas;
- 31.118 páginas únicas por identidad binaria;
- 2.833.870.450 bytes físicos;
- 1.595.362.761 bytes únicos;
- 0 PDF ilegibles al abrir y contar páginas.

El inventario completo, con ruta, páginas, tamaño, SHA-256, grupo binario,
metadatos y estado de lectura, se conserva en
`PHYSICAL_PDF_INVENTORY_2026-08-01.csv`. El resumen reproducible está en
`MANIFEST_2026-08-01.json`.

### 1.2. Alcance corporativo prioritario

El bloque identificado por rutas y títulos propios de GYPPORT contiene 88 PDF,
2.981 páginas y 2.515.007 caracteres extraíbles. Incluye:

- `Base_Iincial_GYPPORT`;
- exportaciones `OneNote` de GYPPORT;
- `Organizacion Fabric.pdf`;
- el organigrama legado disponible en `Gystigo/docs`.

Este subconjunto se prioriza antes de libros generales porque contiene
conocimiento propio del producto. La prioridad no equivale a aprobación ni a
vigencia.

### 1.3. Dependencias documentales globales detectadas

- `Organizacion Fabric.pdf` remite a documentación oficial sobre memorias y
  superficies de configuración, pero esas referencias no forman parte del PDF
  como anexos verificables.
- `GYPPORT_Legacy_UI_Organigrama.pdf` remite a una "sección 11 del documento",
  Toolchain STEP 47-53, Dashboard STEP 2-3C.2 y decisiones TAX-01/AUTH-01, sin
  identificar dentro del propio PDF el documento completo del que depende.
- No se identificó evidencia documental suficiente para afirmar que alguno de
  estos dos PDF reemplaza formalmente a otro documento.

## 2. Análisis individual - `Organizacion Fabric.pdf`

### 2.1. Identificación

| Campo | Valor |
|---|---|
| Nombre | `Organizacion Fabric.pdf` |
| Ruta | `D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT\Fabric\Organizacion Fabric.pdf` |
| Páginas | 6 |
| Tipo | Propuesta/recomendación de organización, continuidad y respaldo |
| Fecha de metadatos | 2026-07-31 UTC |
| Autor | No identificado en metadatos |
| Institución | GYPPORT® mencionada; autoría institucional no demostrada |
| Versión | No indicada |
| Estado | A validar; parcialmente materializado físicamente |
| SHA-256 | `80014994dc03292359fc7671bf4c1ea1dac65cd76ad23e85fa350a4b1efe1a64` |

### 2.2. Resumen ejecutivo

El documento propone separar tres clases de memoria: memoria de ChatGPT
asociada a la cuenta/workspace, memoria local de Codex en el perfil de Windows
y memoria canónica de GYPPORT en archivos físicos. Define una estructura para
conservar contexto, decisiones, checkpoints, fuentes, procesamiento,
derivados, trabajo entre IAs, estado privado y respaldo. Declara que `.chatgpt`
es una convención propia y no el almacén automático de ChatGPT. Recomienda
versionar contenido no sensible, excluir credenciales y mantener tres copias.
Finaliza proponiendo crear la estructura sin mover fuentes ni modificar
Gystigo.

La inspección física actual confirma que una parte relevante de la estructura
existe, pero no confirma respaldos externos, repositorio privado ni la
existencia de todos los derivados declarados en el estado operativo.

### 2.3. Índice reconstruido

1. Tipos de memoria y riesgo de pérdida.
2. Estructura física recomendada de Fabric.
3. Función de `.chatgpt`.
4. Responsabilidad de archivos raíz.
5. Respaldo selectivo de memoria local de Codex.
6. Exclusiones de secretos.
7. Estrategia de tres copias.
8. Resultado esperado ante formateo.
9. Siguiente paso recomendado.

### 2.4. Temas y modelo de conocimiento

- Continuidad
  - memoria automática;
  - memoria local;
  - memoria canónica verificable.
- Organización física
  - gobernanza;
  - fuentes, corpus, procesamiento y derivados;
  - espacios de colaboración entre IAs;
  - estado privado;
  - herramientas de respaldo.
- Seguridad
  - autenticación, tokens y secretos fuera de Git;
  - restauración selectiva, no copia indiscriminada.
- Persistencia
  - copia local;
  - NAS propuesto;
  - repositorio privado o respaldo cifrado externo.

Actores/roles: Eduardo como propietario implícito de decisiones; ChatGPT,
Claude y Codex como consumidores de archivos canónicos. Objetos: memorias,
fuentes, inventarios, KN, decisiones, checkpoints, derivados y respaldos.

### 2.5. Procesos y metodologías

Proceso documental propuesto:

`FUENTES -> INVENTARIO -> ESTADO_DE_PROCESAMIENTO -> UNIDADES_KN -> DECISIONES
-> CHECKPOINTS -> BORRADORES -> REVISIONES -> DOCUMENTOS_APROBADOS ->
CONTINUIDAD_ENTRE_IAS`.

Entradas: documentación y memoria de trabajo. Actividades: inventariar,
procesar, decidir, registrar y respaldar. Validaciones: trazabilidad física y
exclusión de secretos. Salida: continuidad recuperable. Dependencias no
resueltas: destino secundario y política de versionado.

### 2.6. Contenido visual y datos importantes

Las páginas 1-3 contienen árboles de directorios. Las páginas 4-5 incluyen
tablas de responsabilidades y listas de exclusión. La página 5 presenta una
estrategia de tres copias. La página 6 presenta la cadena documental final.
Los 6 renders son legibles; el renderizador notificó fuentes Symbol y
ArialUnicode no disponibles, sin pérdida observada de los conceptos centrales.

Datos: tres clases de memoria, tres copias propuestas y una secuencia de diez
estados documentales.

### 2.7. Importancia documental por sección

- Crítica: distinción entre memoria auxiliar y memoria canónica; secretos fuera
  de Git.
- Alta: estructura de continuidad, trazabilidad y respaldo.
- Media: nombres y distribución exacta de carpetas, porque son propuesta.
- Baja: ninguna sección identificada.

### 2.8. Abstracción e ideas clave

El conocimiento central es que la continuidad del proyecto no debe depender de
la memoria automática de una IA ni de un único disco. La idea reutilizable es
separar evidencia, conocimiento procesado, decisiones y estado privado, con
trazabilidad y respaldo.

### 2.9. Palabras clave

GYPPORT, Fabric, memoria canónica, ChatGPT, Codex, continuidad, respaldo,
fuentes, corpus, inventario, unidades de conocimiento, decisiones, checkpoints,
derivados, gobernanza, secretos, Git privado, NAS, cifrado, restauración,
AGENTS.md, CURRENT_STATE, trazabilidad, persistencia, tres copias.

### 2.10. Preguntas que responde

- ¿Qué tipos de memoria intervienen en el proyecto?
- ¿Para qué sirve `.chatgpt`?
- ¿Qué debe conservarse físicamente?
- ¿Qué no debe almacenarse en Git?
- ¿Cómo podría reconstruirse el contexto tras una reinstalación?

### 2.11. Lagunas, preguntas abiertas y calidad

Lagunas:

- no define RPO, RTO, frecuencia de respaldo ni prueba de restauración;
- no identifica el repositorio privado o dispositivo secundario;
- no aporta evidencia de que las tres copias existan;
- no define aprobación formal ni versión del propio documento;
- los enlaces a documentación oficial no quedan identificados con precisión.

Preguntas abiertas:

- ¿Cuál es el destino físico definitivo de la segunda copia?
- ¿Qué contenido exacto de `.chatgpt` se versionará?
- ¿Quién ejecuta y audita las restauraciones?

Calidad: claridad alta, profundidad media, coherencia alta, actualidad media y
utilidad alta. La falta de versión, autoría y evidencia de implementación reduce
su confianza como norma vigente.

## 3. Análisis individual - `GYPPORT_Legacy_UI_Organigrama.pdf`

### 3.1. Identificación

| Campo | Valor |
|---|---|
| Nombre | `GYPPORT_Legacy_UI_Organigrama.pdf` |
| Ruta | `D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT\Gystigo\docs\investigations\legacy-ui\GYPPORT_Legacy_UI_Organigrama.pdf` |
| Páginas | 4 |
| Tipo | Investigación técnica y organigrama de migración legado |
| Fecha de metadatos | 2026-07-10 (UTC-05:00) |
| Autor | `anonymous` en metadatos |
| Institución | GYPPORT® Platform OS |
| Versión | No indicada |
| Estado | A validar contra código en fase posterior |
| SHA-256 | `b995216bb3c8bff67fb1da008873c3d9bb6b89c57b54c8eddf107f9f41269dc6` |

### 3.2. Resumen ejecutivo

El documento describe el destino arquitectónico de nueve archivos JSX legacy.
Afirma que la migración física fue ejecutada y verificada, mientras la
integración funcional permanece pendiente. Organiza `platform_os/studio` en
engine, journey, module y channel/browser/shell; asigna archivos a party, tax,
workforce/employee, authentication, onboarding y archivo histórico. Mantiene
abiertas TAX-01, AUTH-01, Page vs Workspace, App.jsx vs AppRuntime.jsx y el
cableado de ReactRenderer.js.

La fuente declarada es inspección directa de código. Como el protocolo actual
prohíbe analizar código, las afirmaciones de ejecución se conservan como hechos
documentales, pero su vigencia técnica queda pendiente de validación.

### 3.3. Índice reconstruido

1. Portada, alcance, leyenda y estado declarado.
2. Boundaries objetivo de `platform_os/studio`.
3. Mapeo de los nueve archivos.
4. Decisiones pendientes y secuencia recomendada.

### 3.4. Temas y modelo de conocimiento

- Boundaries
  - engine: capacidad genérica/runtime;
  - journey: recorridos cross-domain;
  - module: ownership de capacidad de negocio;
  - channel/browser/shell: adaptador tecnológico React.
- Dominios mencionados
  - party;
  - tax;
  - workforce/employee;
  - authentication;
  - onboarding;
  - commercial.
- Integración pendiente
  - root de aplicación;
  - renderer;
  - bootstrap/workspaces;
  - desacoplamiento de localStorage/fetch.

Actores técnicos: responsables de Toolchain, Dashboard y tracks TAX/AUTH.
Objetos: archivos JSX, boundaries, imports, renderer, runtime y archivo
histórico. Evento principal: migración física. Estado posterior: integración
pendiente.

### 3.5. Procesos y metodologías

Proceso documentado: identificar archivo legacy, seleccionar boundary, mover o
archivar, corregir import/alias cuando aplica, verificar construcción y luego
integrar en runtime/shell. La validación declarada usa esbuild, pero no se
incluyen comando, salida, commit o fecha de la prueba.

Secuencia declarada: Party, Workforce, Tax, Auth/Onboarding, Archive,
Integración y Shell. Las cinco decisiones abiertas condicionan la terminación
funcional.

### 3.6. Contenido visual y datos importantes

- Página 2: árbol de cuatro boundaries con estados por color.
- Página 3: nueve mapeos origen-destino y estado individual.
- Página 4: cinco decisiones pendientes y siete pasos de secuencia.

Los 4 renders son legibles. Datos: 9 archivos movidos/archivados; 4 grandes
boundaries; 5 decisiones abiertas; 7 pasos de secuencia; 0 consumidores
declarados para `AppRuntime.jsx` y `ReactRenderer.js`.

### 3.7. Importancia documental por sección

- Crítica: estado de integración funcional pendiente.
- Alta: mapeo de archivos y decisiones abiertas.
- Media: boundaries objetivo hasta validación posterior.
- Baja: ninguna sección identificada.

### 3.8. Abstracción e ideas clave

El documento intenta enseñar que mover archivos no equivale a completar una
migración funcional. La propiedad arquitectónica y el cableado del runtime son
dimensiones distintas que deben validarse por separado.

### 3.9. Palabras clave

GYPPORT Platform OS, legacy UI, migración física, integración funcional,
platform_os/studio, engine, journey, module, channel, browser shell, Party,
Tax, Workforce, Employee, Authentication, Onboarding, ReactRenderer,
AppRuntime, App.jsx, imports, alias, esbuild, boundary, runtime, archivo
histórico, localStorage, fetch, Dashboard Engine, Toolchain.

### 3.10. Preguntas que responde

- ¿Qué destino documental se asignó a cada archivo legacy?
- ¿Qué diferencia existe entre migración física e integración funcional?
- ¿Qué decisiones permanecían abiertas al emitir el PDF?
- ¿Qué secuencia técnica se recomendaba?

### 3.11. Lagunas, preguntas abiertas y calidad

Lagunas:

- falta el documento que contiene la sección 11 referenciada;
- no aporta commit, HEAD, comandos ni resultados de esbuild;
- no identifica responsables ni fechas de cierre de cada decisión;
- no define criterios de aceptación de la integración;
- no demuestra vigencia actual.

Preguntas abiertas:

- ¿Cuál es hoy el estado de TAX-01 y AUTH-01?
- ¿Qué root y renderer quedaron finalmente activos?
- ¿El mapeo tentativo `EmployeeTeamPage.jsx` fue confirmado?
- ¿La migración permanece intacta en el checkout actual?

Calidad: claridad alta, profundidad media, coherencia media-alta, actualidad
indeterminada y utilidad alta como evidencia histórica. La trazabilidad técnica
insuficiente impide elevar su confianza a muy alta.

## 4. Comparación global provisional

Coincidencias: ambos documentos separan estados que no deben confundirse. El
primero distingue memoria auxiliar de memoria canónica; el segundo distingue
migración física de integración funcional.

Diferencias: `Organizacion Fabric.pdf` trata continuidad y gobernanza de
conocimiento; el organigrama trata una investigación técnica localizada.

Contradicciones/inconsistencias:

- no existe contradicción directa entre ambos documentos;
- el título de página 4 del organigrama dice "antes de ejecutar la migración",
  mientras el cuerpo y las páginas 1 y 3 declaran la migración física
  completada. Se conserva como inconsistencia editorial, no como refutación del
  estado declarado;
- `CURRENT_STATE.md` declara 15 KN y seis documentos maestros entregados, pero
  no se encontraron físicamente en Fabric. Este hallazgo es externo a los PDF y
  se registra como asunto no resuelto, no como conocimiento del dominio.

Complementariedad: el primer documento define dónde debería persistir el
conocimiento; el segundo es un ejemplo de evidencia técnica que debería
incorporarse al corpus con estado y trazabilidad.

Evolución provisional: el organigrama (julio 10) antecede a la propuesta de
Fabric (julio 31). No hay evidencia suficiente para declarar reemplazo.

## 5. Normalización terminológica

| Término fuente | Término normalizado | Nota |
|---|---|---|
| memoria de ChatGPT | memoria automática auxiliar | Asociada a cuenta/workspace |
| memorias locales de Codex | memoria local de herramienta | Ubicada en perfil de usuario |
| memoria canónica | conocimiento persistente verificable | Archivos físicos versionables |
| migración física | reubicación estructural | No implica activación funcional |
| integración funcional | activación en runtime | Requiere consumidores y cableado |
| boundary | límite de ownership/capacidad | Término técnico conservado |
| root | raíz de aplicación | App.jsx o AppRuntime.jsx |

## 6. Catálogo provisional de Unidades de Conocimiento

Los identificadores `KN-000001` a `KN-000015` quedan reservados porque
`CURRENT_STATE.md` afirma que existían previamente, aunque sus archivos no están
presentes. No se reutilizan hasta recuperar o invalidar formalmente esa
afirmación.

### KN-000016

- Enunciado: La continuidad documental distingue memoria automática de
  ChatGPT, memoria local de Codex y memoria canónica física de GYPPORT.
- Naturaleza: Hecho documental.
- Evidencia: `Organizacion Fabric.pdf`, p. 1.
- Clasificación: Gobernanza / Infraestructura.
- Prioridad de negocio: Crítico.
- Nivel de confianza: Alto.
- Estado: Pendiente de validar corporativamente.
- Versión: v1.
- Relaciones: base de KN-000017 y KN-000018.

### KN-000017

- Enunciado: `.chatgpt` se propone como convención física de GYPPORT y no como
  almacenamiento automático oficial de la memoria de ChatGPT.
- Naturaleza: Hecho documental.
- Evidencia: `Organizacion Fabric.pdf`, p. 3.
- Clasificación: Gobernanza.
- Prioridad de negocio: Alto.
- Nivel de confianza: Muy alto.
- Estado: Vigente como descripción documental; aprobación normativa pendiente.
- Versión: v1.
- Relaciones: depende de KN-000016; extiende KN-000018.

### KN-000018

- Enunciado: El flujo propuesto separa fuentes, corpus, procesamiento,
  conocimiento derivado, decisiones, checkpoints y continuidad entre IAs.
- Naturaleza: Hecho documental.
- Evidencia: `Organizacion Fabric.pdf`, pp. 2-3 y 5-6.
- Clasificación: Procesos / Gobernanza.
- Prioridad de negocio: Crítico.
- Nivel de confianza: Alto.
- Estado: Pendiente de validar corporativamente.
- Versión: v1.
- Relaciones: depende de KN-000016; extendido por KN-000017.

### KN-000019

- Enunciado: Credenciales, tokens, archivos `.env`, autenticación y secretos no
  deben almacenarse en Git ni copiarse indiscriminadamente con el estado local.
- Naturaleza: Hecho documental.
- Evidencia: `Organizacion Fabric.pdf`, pp. 4-5.
- Clasificación: Seguridad.
- Prioridad de negocio: Crítico.
- Nivel de confianza: Muy alto.
- Estado: Pendiente de validar corporativamente.
- Versión: v1.
- Relaciones: depende de KN-000016.

### KN-000020

- Enunciado: La estrategia documental propone tres copias: PC local, NAS y
  repositorio privado o respaldo cifrado externo.
- Naturaleza: Hecho documental.
- Evidencia: `Organizacion Fabric.pdf`, p. 5.
- Clasificación: Infraestructura.
- Prioridad de negocio: Alto.
- Nivel de confianza: Alto.
- Estado: Pendiente de validar; destinos no decididos.
- Versión: v1.
- Relaciones: depende de KN-000016; requiere UNR-000001 a UNR-000003.

### KN-000021

- Enunciado: El organigrama declara que nueve archivos JSX legacy fueron
  movidos o archivados hacia boundaries objetivo.
- Naturaleza: Hecho documental, no verificado contra código en esta fase.
- Evidencia: `GYPPORT_Legacy_UI_Organigrama.pdf`, pp. 1 y 3.
- Clasificación: Arquitectura.
- Prioridad de negocio: Alto.
- Nivel de confianza: Medio.
- Estado: Pendiente de validar contra código.
- Versión: v1.
- Relaciones: depende de KN-000022; extendido por KN-000023.

### KN-000022

- Enunciado: `platform_os/studio` se representa mediante boundaries engine,
  journey, module y channel/browser/shell con responsabilidades diferenciadas.
- Naturaleza: Hecho documental.
- Evidencia: `GYPPORT_Legacy_UI_Organigrama.pdf`, p. 2.
- Clasificación: Arquitectura.
- Prioridad de negocio: Alto.
- Nivel de confianza: Medio.
- Estado: Pendiente de validar contra código y autoridad vigente.
- Versión: v1.
- Relaciones: contexto de KN-000021 y KN-000023.

### KN-000023

- Enunciado: La migración física declarada no completa la integración
  funcional; runtime, App.jsx, renderer y desacoplamiento de localStorage/fetch
  permanecen pendientes en el documento.
- Naturaleza: Hecho documental.
- Evidencia: `GYPPORT_Legacy_UI_Organigrama.pdf`, pp. 1, 3 y 4.
- Clasificación: Arquitectura / Integración.
- Prioridad de negocio: Crítico.
- Nivel de confianza: Alto como contenido; medio como estado actual.
- Estado: Pendiente de validar contra código.
- Versión: v1.
- Relaciones: extiende KN-000021; depende de KN-000024 y KN-000025.

### KN-000024

- Enunciado: TAX-01 y AUTH-01 permanecen abiertas en el organigrama y condicionan
  la confirmación de boundaries Tax y Auth/Onboarding.
- Naturaleza: Hecho documental.
- Evidencia: `GYPPORT_Legacy_UI_Organigrama.pdf`, pp. 2-4.
- Clasificación: Arquitectura / Seguridad.
- Prioridad de negocio: Alto.
- Nivel de confianza: Medio.
- Estado: Pendiente de validar.
- Versión: v1.
- Relaciones: condiciona KN-000023.

### KN-000025

- Enunciado: El documento deja sin resolver Page vs Workspace, App.jsx vs
  AppRuntime.jsx y el cableado de ReactRenderer.js.
- Naturaleza: Hecho documental.
- Evidencia: `GYPPORT_Legacy_UI_Organigrama.pdf`, p. 4.
- Clasificación: Arquitectura / Integración.
- Prioridad de negocio: Alto.
- Nivel de confianza: Medio.
- Estado: Pendiente de validar.
- Versión: v1.
- Relaciones: condiciona KN-000023.

### KN-000026

- Enunciado: El mapeo de `ModuloEquipo.jsx` a `EmployeeTeamPage.jsx` es tentativo
  hasta decidir si la superficie es Page o Workspace.
- Naturaleza: Hecho documental.
- Evidencia: `GYPPORT_Legacy_UI_Organigrama.pdf`, pp. 3-4.
- Clasificación: Arquitectura.
- Prioridad de negocio: Normal.
- Nivel de confianza: Alto.
- Estado: Pendiente de validar.
- Versión: v1.
- Relaciones: depende de KN-000025.

### KN-000027

- Enunciado: Inventariar o mover físicamente contenido no equivale a procesarlo,
  validarlo ni activarlo funcionalmente.
- Naturaleza: Interpretación sustentada por ambos documentos.
- Evidencia: `Organizacion Fabric.pdf`, pp. 5-6;
  `GYPPORT_Legacy_UI_Organigrama.pdf`, pp. 1 y 3-4.
- Clasificación: Procesos / Gobernanza.
- Prioridad de negocio: Crítico.
- Nivel de confianza: Alto.
- Estado: Pendiente de aprobación como principio corporativo.
- Versión: v1.
- Relaciones: extiende KN-000018 y KN-000023.

## 7. Mapa conceptual e índice semántico

Mapa conceptual:

`Fuente PDF -> inventario físico -> identidad SHA-256 -> análisis documental ->
KN provisional -> revisión -> decisión de Eduardo -> conocimiento aprobado`.

`Archivo legacy -> boundary objetivo -> movimiento físico -> verificación
declarada -> integración runtime pendiente -> validación futura contra código`.

Índice semántico:

| Término | Documento(s) |
|---|---|
| memoria canónica | `Organizacion Fabric.pdf` |
| `.chatgpt` | `Organizacion Fabric.pdf` |
| secretos / tokens | `Organizacion Fabric.pdf` |
| tres copias | `Organizacion Fabric.pdf` |
| legacy UI | `GYPPORT_Legacy_UI_Organigrama.pdf` |
| boundary | `GYPPORT_Legacy_UI_Organigrama.pdf` |
| integración funcional | `GYPPORT_Legacy_UI_Organigrama.pdf` |
| Party / Tax / Workforce | `GYPPORT_Legacy_UI_Organigrama.pdf` |

Grafo KN:

```text
KN-000016 -> KN-000017
KN-000016 -> KN-000018 -> KN-000027
KN-000016 -> KN-000019
KN-000016 -> KN-000020
KN-000022 -> KN-000021 -> KN-000023 -> KN-000027
KN-000024 -> KN-000023
KN-000025 -> KN-000023
KN-000025 -> KN-000026
```

## 8. Matriz de trazabilidad

| KN | Concepto | Documento/páginas | Estado |
|---|---|---|---|
| KN-000016 | Tipos de memoria | Organizacion Fabric, p. 1 | Pendiente |
| KN-000017 | Función de `.chatgpt` | Organizacion Fabric, p. 3 | Pendiente |
| KN-000018 | Cadena documental | Organizacion Fabric, pp. 2-3, 5-6 | Pendiente |
| KN-000019 | Exclusión de secretos | Organizacion Fabric, pp. 4-5 | Pendiente |
| KN-000020 | Tres copias | Organizacion Fabric, p. 5 | Pendiente |
| KN-000021 | Nueve archivos migrados | Legacy UI, pp. 1, 3 | Validación código pendiente |
| KN-000022 | Boundaries objetivo | Legacy UI, p. 2 | Validación código pendiente |
| KN-000023 | Integración pendiente | Legacy UI, pp. 1, 3-4 | Validación código pendiente |
| KN-000024 | TAX-01/AUTH-01 | Legacy UI, pp. 2-4 | Pendiente |
| KN-000025 | Decisiones shell/runtime | Legacy UI, p. 4 | Pendiente |
| KN-000026 | Page vs Workspace | Legacy UI, pp. 3-4 | Pendiente |
| KN-000027 | Inventario no es activación | Ambos documentos | Provisional |

## 9. Validación de comprensión e índice de cobertura

Resultados de Etapa 6 para este bloque:

- actores: parcialmente identificados; faltan responsables nominales;
- procesos: los inicios y fines están descritos a nivel general, no con criterios
  de aceptación completos;
- reglas sin proceso: la regla de tres copias carece de operación definida;
- entidades sin definición: `workspace`, `experience`, `journey` y `boundary`
  requieren autoridad conceptual adicional;
- procesos sin responsable: respaldo, restauración, TAX-01, AUTH-01 e
  integración;
- decisiones sin justificación completa: los destinos arquitectónicos resumen
  el resultado, pero no incluyen el análisis completo;
- conceptos de una sola fuente: casi todos, por tratarse de un bloque inicial;
- baja cobertura: negocio ERP, tributación, seguridad funcional, integraciones
  externas y operación.

Cobertura cuantitativa del corpus:

| Dimensión | Cobertura | Confianza |
|---|---:|---|
| Inventario físico por archivo | 233/233 = 100% | Muy alta |
| Identidad binaria SHA-256 | 233/233 = 100% | Muy alta |
| Análisis profundo por PDF único | 2/175 = 1,14% | Muy alta para el conteo |
| Páginas analizadas profundamente | 10/31.118 = 0,032% | Muy alta para el conteo |
| Comprensión global del dominio | No calculable todavía | Indeterminada |

No se asignan porcentajes de dominio aparentes: hacerlo con 0,032% de las
páginas únicas sería una falsa precisión.

## 10. Glosario

- Base de Conocimiento: conjunto vivo de KN y relaciones, no colección de PDF.
- Boundary: límite documentado de responsabilidad/capacidad.
- Checkpoint: estado verificable e incremental del procesamiento.
- Evidencia: documento y localización que sustentan un enunciado.
- Integración funcional: activación efectiva mediante runtime y consumidores.
- KN: Unidad de Conocimiento trazable.
- Memoria automática auxiliar: contexto asociado a una herramienta/cuenta.
- Memoria canónica: conocimiento persistente en archivos verificables.
- Migración física: movimiento o renombrado estructural de archivos.
- SSOT: fuente única autorizada de verdad una vez aprobada.

## 11. Conocimiento pendiente y preguntas abiertas

1. Recuperar o localizar los 15 KN y seis documentos maestros declarados en
   `CURRENT_STATE.md`.
2. Identificar el documento que contiene la sección 11 citada por el organigrama.
3. Resolver el estado actual de TAX-01, AUTH-01, Page vs Workspace,
   App.jsx/AppRuntime.jsx y ReactRenderer.js.
4. Confirmar ruta definitiva, repositorio privado y segunda copia de respaldo.
5. Determinar aprobación, autoría y versión de `Organizacion Fabric.pdf`.
6. Procesar los 173 binarios PDF únicos restantes antes de cualquier conclusión
   global.

## 12. Preparación para validación contra código

Esta lista no analiza código; prepara una fase posterior:

- KN-000021: comprobar los nueve movimientos/archivo.
- KN-000022: comprobar boundaries y ownership vigentes.
- KN-000023: comprobar integración real en runtime/App/renderer.
- KN-000024: comprobar estado y autoridad de TAX-01/AUTH-01.
- KN-000025: comprobar root activo y consumidores de ReactRenderer.js.
- KN-000026: comprobar resolución final de EmployeeTeam Page/Workspace.

Condición previa: autorización explícita para una fase de validación de código.

## 13. Registro de versiones de la Base de Conocimiento

| Versión | Fecha | Incorporación | Cambio |
|---|---|---|---|
| v0.1-provisional | 2026-08-01 | Inventario físico + 2 PDF de control | Se fijan 12 KN provisionales, duplicados exactos y cobertura real |

Los KN-000016 a KN-000027 están en v1. Los KN-000001 a KN-000015 permanecen
reservados hasta resolver su ausencia física.

## 14. Único siguiente paso

Procesar el siguiente bloque corporativo de seis exportaciones OneNote de
GYPPORT (1.432 páginas), empezando por `QUE ES GYPPORT.pdf`, y actualizar este
MCK incrementalmente sin reescribir el inventario ni emitir conclusiones
globales.
