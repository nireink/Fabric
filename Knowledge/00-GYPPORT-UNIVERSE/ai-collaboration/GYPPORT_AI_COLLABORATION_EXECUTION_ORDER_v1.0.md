# GYPPORT® AI COLLABORATION — CANONICAL EXECUTION ORDER

**Organización responsable:** ISAGRUB CORPORACIÓN C.L. — GYPPORT®  
**Document ID:** GYPPORT-AI-GOV-EXECUTION-ORDER-001  
**Versión:** 1.0  
**Fecha original:** 2026-07-28  
**Fecha de regeneración:** 2026-07-30  
**Clasificación:** Governance  
**Estado:** APPROVED  
**Propietario y autoridad final:** Eduardo Luis Burgasi Pullaguari  
**Aprobado por:** Eduardo Luis Burgasi Pullaguari  
**Fecha de aprobación y entrada en vigor:** 2026-07-28  
**Ubicación canónica:** `Fabric/Knowledge/00-GYPPORT-UNIVERSE/ai-collaboration/GYPPORT_AI_COLLABORATION_EXECUTION_ORDER_v1.0.md`  
**Ubicación hasta 2026-09-15:** `Gystigo/docs/architecture/GYPPORT_AI_COLLABORATION_EXECUTION_ORDER_v1.0.md`

---

## 1. Propósito

Este documento define el orden obligatorio de colaboración entre las IAs que
participan en la construcción del conocimiento, las decisiones, las
verificaciones, las implementaciones y las auditorías de GYPPORT®.

Se aplica a:

- construcción y actualización del corpus de conocimiento de GYPPORT®;
- creación o actualización de estándares, guías y playbooks;
- decisiones arquitectónicas y de gobernanza;
- modelos de datos y contratos;
- creación o modificación de documentación;
- creación o modificación de código, configuración o estructura del
  repositorio;
- verificaciones técnicas y auditorías;
- cierre de tracks y autorización de operaciones Git protegidas.

Su objetivo es establecer una secuencia trazable que:

- preserve el intercambio crítico entre las IAs;
- separe propuesta, verificación, aprobación, implementación y auditoría;
- evite que una IA apruebe su propio trabajo;
- impida repetir una aprobación ya concedida para el mismo alcance;
- mantenga a Eduardo como autoridad final;
- produzca evidencia transferible entre cada intervención.

---

## 2. Regla canónica resumida

El proceso completo contiene **10 intervenciones técnicas y una compuerta única
del propietario**:

> **Eduardo inicia el tema → ChatGPT presenta la propuesta inicial → Claude Chat
> realiza la crítica arquitectónica → ChatGPT presenta la propuesta revisada →
> Claude Chat consolida la decisión provisional → ChatGPT Work prepara el
> handoff técnico → Claude Code verifica el repositorio en modo read-only →
> Eduardo aprueba una sola vez el alcance exacto → Codex implementa y prueba →
> Claude Code audita la implementación → Claude Chat realiza el cierre
> arquitectónico y funcional → ChatGPT Work cruza la evidencia y recomienda el
> cierre.**

La compuerta de Eduardo:

- ocurre después de la verificación técnica previa de Claude Code;
- ocurre antes de que Codex modifique el repositorio;
- autoriza únicamente el alcance exacto aprobado;
- no debe solicitarse nuevamente mientras ese alcance no cambie;
- no autoriza por sí sola staging, commit, push, merge o despliegue.

---

## 3. Principios rectores

### 3.1. Autoridad humana

Eduardo determina que un tema será trabajado, establece el objetivo y conserva
la autoridad final sobre:

- arquitectura;
- gobernanza;
- alcance;
- seguridad;
- datos canónicos;
- ownership;
- tecnología base;
- staging;
- commit;
- push;
- merge;
- publicación y despliegue.

El inicio de un tema autoriza el análisis y la preparación de propuestas. No
autoriza automáticamente modificaciones en el repositorio.

### 3.2. Colaboración secuencial

Las IAs no negocian autónomamente entre sí. La colaboración es:

- secuencial;
- mediada por Eduardo o por ChatGPT Work;
- documentada mediante resultados autocontenidos;
- trazable contra corpus, archivos, Git, pruebas y decisiones;
- limitada al rol de cada participante.

Cada intervención debe terminar con:

- resultado;
- estado;
- evidencia utilizada;
- asuntos no confirmados;
- contradicciones abiertas;
- único siguiente paso;
- siguiente agente responsable.

### 3.3. Separación de funciones

No se debe confundir:

- propuesta con decisión;
- borrador con archivo implementado;
- conocimiento del corpus con evidencia del repositorio;
- verificación previa con auditoría posterior;
- validación propia de Codex con aceptación independiente;
- aprobación del alcance con aprobación del resultado;
- aprobación de implementación con autorización Git;
- commit local con push;
- cierre recomendado con cierre autorizado.

### 3.4. Evidencia antes que memoria

Las conversaciones, memorias y resúmenes aportan contexto, pero no sustituyen:

- archivos canónicos;
- repositorio real;
- contratos ejecutables;
- pruebas reproducibles;
- diff;
- estado de Git;
- decisiones formalmente aprobadas.

Si un dato no puede comprobarse, debe marcarse `NOT_CONFIRMED`.

---

## 4. Responsabilidades permanentes

| Participante | Responsabilidad principal | No debe hacer |
|---|---|---|
| **Eduardo / Project Owner** | Iniciar el tema, aprobar el alcance exacto y ejercer la autoridad final | Delegar implícitamente decisiones protegidas a una IA |
| **ChatGPT** | Organizar el corpus, sintetizar, proponer, responder objeciones y revisar la propuesta | Presentar hipótesis como hechos confirmados |
| **Claude Chat** | Realizar crítica conceptual, consolidar el modelo provisional y cerrar arquitectónica y funcionalmente | Modificar el repositorio o sustituir la auditoría directa |
| **ChatGPT Work** | Cruzar intervenciones, preparar el handoff verificable y realizar el cruce final de evidencia | Introducir una arquitectura nueva durante el handoff o autoautorizar cambios |
| **Claude Code** | Verificar antes y auditar después en modo read-only contra evidencia real | Modificar archivos, implementar o redefinir unilateralmente el alcance |
| **Codex** | Implementar el alcance aprobado, ejecutar pruebas y entregar evidencia | Ampliar el alcance, autoaprobarse o actuar como auditor independiente |

La validación propia de Codex es obligatoria, pero nunca reemplaza la auditoría
independiente de Claude Code.

---

## 5. Flujo completo obligatorio

### INICIO — Decisión de Eduardo

Eduardo determina:

- el tema que será trabajado;
- el objetivo;
- las fuentes o el corpus inicial;
- las restricciones conocidas;
- el resultado esperado.

**Efecto:** autoriza el inicio del análisis.

**No autoriza todavía:**

- crear o modificar archivos;
- cambiar arquitectura;
- ejecutar staging;
- crear commits;
- hacer push;
- realizar merge o despliegue.

---

### FASE 1 — EXPLORACIÓN, CRÍTICA Y DECISIÓN CONCEPTUAL

#### Intervención 1 — ChatGPT: propuesta inicial

**Salida obligatoria:** `INITIAL_PROPOSAL`

ChatGPT organiza el corpus disponible, que puede incluir:

- libros;
- documentos;
- guías;
- videos;
- conversaciones;
- decisiones anteriores;
- archivos canónicos;
- evidencia técnica disponible.

Debe:

- definir el problema;
- reconstruir el objetivo de Eduardo;
- clasificar las fuentes;
- diferenciar conocimiento general de reglas propias de GYPPORT®;
- identificar coincidencias y contradicciones;
- declarar supuestos;
- sintetizar principios aplicables;
- proponer alternativas;
- exponer riesgos;
- formular una propuesta inicial;
- indicar qué archivos podrían crearse o actualizarse;
- declarar las preguntas estrictamente necesarias.

ChatGPT no ordena todavía una implementación.

---

#### Intervención 2 — Claude Chat: crítica arquitectónica

**Salida obligatoria:** `ARCHITECTURAL_CRITIQUE`

Claude Chat realiza una revisión crítica conceptual y arquitectónica de la
propuesta inicial.

Debe cuestionar:

- supuestos;
- coherencia arquitectónica;
- contradicciones entre fuentes;
- complejidad accidental;
- capas o abstracciones innecesarias;
- duplicación;
- sobreingeniería;
- acoplamiento;
- seguridad;
- mantenibilidad;
- reversibilidad;
- impacto futuro;
- aplicabilidad real a GYPPORT®;
- omisiones y riesgos.

Debe distinguir:

- objeciones bloqueantes;
- correcciones necesarias;
- mejoras recomendadas;
- preguntas abiertas;
- observaciones no aplicables.

Claude Chat no modifica el repositorio.

---

#### Intervención 3 — ChatGPT: propuesta revisada

**Salida obligatoria:** `REVISED_PROPOSAL`

ChatGPT cruza la crítica de Claude Chat con el corpus completo.

Debe:

- responder cada objeción;
- aceptar, rechazar o ajustar cada observación;
- justificar cada decisión;
- corregir contradicciones;
- reducir complejidad cuando sea posible;
- descartar alternativas inviables;
- declarar riesgos residuales;
- presentar una propuesta revisada;
- identificar asuntos todavía no resueltos.

La propuesta revisada continúa siendo conceptual. No autoriza implementación.

---

#### Intervención 4 — Claude Chat: decisión provisional

**Salida obligatoria:** `PROVISIONAL_DECISION`

Claude Chat revisa la propuesta corregida y consolida únicamente los puntos que
hayan convergido.

Debe:

- separar decisiones de hipótesis;
- definir el modelo provisional;
- declarar límites y exclusiones;
- definir criterios de aceptación;
- identificar dependencias;
- registrar contradicciones pendientes;
- evitar presentar como hecho aquello que todavía no se verificó en el
  repositorio.

Cuando corresponda, Claude Chat puede elaborar:

- modelo arquitectónico;
- estructura documental;
- esquema de archivos;
- contratos e interfaces;
- reglas;
- pseudocódigo;
- ejemplos;
- contenido técnico;
- borrador de documento;
- código sugerido que posteriormente implementará Codex.

Claude Chat no crea ni modifica archivos en el repositorio.

La `PROVISIONAL_DECISION` autoriza preparar la verificación técnica. No autoriza
la implementación.

---

### FASE 2 — PREPARACIÓN Y VERIFICACIÓN TÉCNICA PREVIA

#### Intervención 5 — ChatGPT Work: handoff de verificación

**Salida obligatoria:** `TECHNICAL_VERIFICATION_HANDOFF`

ChatGPT Work cruza:

- el objetivo definido por Eduardo;
- el corpus organizado;
- `INITIAL_PROPOSAL`;
- `ARCHITECTURAL_CRITIQUE`;
- `REVISED_PROPOSAL`;
- `PROVISIONAL_DECISION`.

Convierte la decisión provisional en un alcance técnico concreto y verificable
para Claude Code.

El handoff debe especificar:

- repositorio y ruta esperados;
- rama y `HEAD`, si están confirmados;
- archivos propuestos;
- archivos que podrían crearse o modificarse;
- afirmaciones que deben verificarse;
- contenido o comportamiento propuesto;
- fuentes utilizadas;
- contratos y dependencias;
- reglas que deben conservarse;
- límites de ownership;
- archivos protegidos;
- comandos read-only permitidos;
- pruebas requeridas;
- riesgos por contrastar;
- exclusiones;
- contradicciones pendientes;
- criterios de aceptación;
- condiciones de parada;
- acciones todavía no autorizadas;
- formato y destino del informe.

Este handoff no es evidencia técnica y no autoriza modificaciones.

---

#### Intervención 6 — Claude Code: verificación independiente previa

**Salida obligatoria:** `TECHNICAL_VERIFICATION_REPORT`

Claude Code opera en modo read-only y verifica la propuesta contra:

- ruta e identidad del repositorio real;
- rama y `HEAD`;
- estado del working tree;
- archivos existentes;
- arquitectura vigente;
- referencias canónicas;
- historial Git relevante;
- dependencias;
- contratos;
- configuración;
- pruebas reproducibles;
- límites de ownership;
- archivos protegidos;
- compatibilidad entre la decisión provisional y la realidad técnica.

Claude Code debe identificar:

- archivos que realmente puede implementar Codex;
- archivos que no deben tocarse;
- diferencias entre lo propuesto y lo existente;
- riesgos o colisiones;
- pruebas obligatorias;
- correcciones necesarias al alcance;
- bloqueos verificables.

Claude Code no implementa, no modifica archivos y no sustituye la aprobación de
Eduardo.

**Veredictos permitidos:**

- `READY_FOR_OWNER_APPROVAL`
- `READY_WITH_FINDINGS`
- `BLOCKED`
- `RETURN_TO_DECISION`

`READY_FOR_OWNER_APPROVAL` permite presentar el alcance exacto a Eduardo.

`READY_WITH_FINDINGS` exige enumerar los hallazgos y reflejarlos expresamente en
el alcance que recibirá Eduardo.

`BLOCKED` detiene el flujo.

`RETURN_TO_DECISION` devuelve el asunto a la intervención conceptual
correspondiente porque la evidencia invalida un supuesto o exige cambiar la
decisión.

---

### COMPUERTA ÚNICA DEL PROPIETARIO — Eduardo

**Salida obligatoria:** `OWNER_SCOPE_APPROVAL`

Eduardo revisa:

- la decisión provisional;
- el handoff técnico;
- el informe independiente de Claude Code;
- los hallazgos y límites;
- el alcance exacto propuesto.

Eduardo aprueba una sola vez el alcance exacto que podrá implementar Codex.

La aprobación debe delimitar, cuando corresponda:

- archivos que podrán crearse;
- archivos que podrán modificarse;
- contenido autorizado;
- comportamiento esperado;
- contratos afectados;
- dependencias permitidas;
- pruebas obligatorias;
- exclusiones;
- archivos protegidos;
- límites de implementación.

### Regla de no repetición

No debe solicitarse nuevamente la aprobación de Eduardo cuando:

- el alcance es exactamente el mismo;
- los archivos autorizados no cambiaron;
- no aparecieron nuevos riesgos bloqueantes;
- la implementación continúa dentro de la decisión aprobada.

Debe solicitarse una nueva decisión solamente si:

- el alcance cambia materialmente;
- se requiere modificar otro archivo;
- aparece una dependencia no aprobada;
- la evidencia invalida la solución;
- se requiere una decisión arquitectónica nueva;
- la corrección excede el límite autorizado.

### Límite de la aprobación

La aprobación de alcance:

- sí autoriza a Codex a implementar exactamente ese alcance;
- no autoriza staging;
- no autoriza commit;
- no autoriza push;
- no autoriza merge;
- no autoriza publicación;
- no autoriza despliegue.

Estas acciones requieren autorización expresa y diferenciada de Eduardo.

---

### FASE 3 — IMPLEMENTACIÓN

#### Intervención 7 — Codex: implementación y pruebas

**Salida obligatoria:** `IMPLEMENTATION_HANDOFF`

Antes de modificar, Codex debe confirmar:

- repositorio correcto;
- rama esperada;
- `HEAD` esperado o diferencia explicada;
- working tree compatible con el alcance;
- aprobación exacta de Eduardo;
- archivos autorizados;
- archivos protegidos;
- ausencia de bloqueos materiales.

Codex utiliza como insumos:

- corpus organizado;
- propuesta revisada;
- decisión provisional de Claude Chat;
- handoff técnico de ChatGPT Work;
- verificación previa de Claude Code;
- aprobación exacta de Eduardo.

Codex debe:

- implementar exclusivamente el alcance aprobado;
- preservar cambios preexistentes del usuario;
- evitar ampliar la arquitectura;
- crear o modificar solo los archivos autorizados;
- ejecutar las pruebas requeridas;
- revisar el diff;
- ejecutar `git diff --check` cuando aplique;
- documentar comandos y resultados;
- registrar riesgos residuales;
- preparar rollback o declarar `NOT_APPLICABLE` con justificación;
- entregar evidencia para Claude Code.

Codex no puede:

- rediseñar autónomamente la solución;
- ampliar el alcance;
- modificar archivos no autorizados;
- incorporar mejoras incidentales fuera del track;
- ocultar fallos de pruebas;
- aprobar su propia implementación;
- ejecutar staging, commit, push, merge o despliegue sin autorización expresa.

**Resultados permitidos:**

- `IMPLEMENTED_READY_FOR_AUDIT`
- `PARTIALLY_IMPLEMENTED_BLOCKED`
- `NOT_IMPLEMENTED`

Codex nunca declara su propio trabajo como `ACCEPTED`.

---

### FASE 4 — AUDITORÍA INDEPENDIENTE POSTERIOR

#### Intervención 8 — Claude Code: auditoría postimplementación

**Salida obligatoria:** `IMPLEMENTATION_AUDIT_REPORT`

Claude Code vuelve a operar en modo read-only.

Debe verificar:

- repositorio, rama y `HEAD` auditados;
- estado real del working tree;
- diff completo;
- archivos creados o modificados;
- correspondencia con la aprobación de Eduardo;
- cumplimiento de la decisión provisional;
- contratos;
- dependencias;
- pruebas reproducibles;
- regresiones;
- seguridad;
- ownership;
- archivos protegidos;
- riesgos residuales;
- acciones Git realizadas o no realizadas.

Claude Code distingue:

- defectos bloqueantes;
- desviaciones de alcance;
- correcciones obligatorias;
- hallazgos no bloqueantes;
- mejoras futuras.

Claude Code no corrige directamente los archivos auditados.

**Veredictos permitidos:**

- `ACCEPTED`
- `ACCEPTED_WITH_FINDINGS`
- `REJECTED`

`REJECTED` devuelve el trabajo a Codex si la corrección permanece dentro del
alcance ya aprobado.

Si corregir exige cambiar arquitectura, ampliar el alcance o modificar archivos
no autorizados, el asunto vuelve a la intervención correspondiente y requiere
una nueva decisión de Eduardo.

`ACCEPTED_WITH_FINDINGS` debe identificar severidad, responsable y tratamiento
de cada hallazgo. No puede utilizarse para ocultar un defecto bloqueante.

---

### FASE 5 — CIERRE ARQUITECTÓNICO, FUNCIONAL Y DE EVIDENCIA

#### Intervención 9 — Claude Chat: cierre arquitectónico y funcional

**Salida obligatoria:** `ARCHITECTURAL_FUNCTIONAL_CLOSURE`

Claude Chat revisa:

- la decisión provisional;
- el alcance aprobado por Eduardo;
- la implementación de Codex;
- la auditoría posterior de Claude Code.

Determina si el resultado cumple:

- fundamentos derivados del corpus;
- arquitectura;
- alcance aprobado;
- contratos;
- propósito funcional;
- criterios de aceptación;
- restricciones y exclusiones.

Si existen hallazgos, debe distinguir:

- correcciones obligatorias;
- mejoras futuras;
- observaciones no bloqueantes;
- asuntos que requieren una nueva decisión.

Claude Chat no sustituye la auditoría técnica de Claude Code y no modifica el
repositorio.

---

#### Intervención 10 — ChatGPT Work: cruce final de evidencia

**Salida obligatoria:** `FINAL_EVIDENCE_RECONCILIATION`

ChatGPT Work cruza:

- objetivo establecido por Eduardo;
- corpus organizado;
- propuesta inicial;
- crítica arquitectónica;
- propuesta revisada;
- decisión provisional;
- handoff técnico;
- verificación previa de Claude Code;
- aprobación exacta de Eduardo;
- informe de implementación de Codex;
- auditoría posterior de Claude Code;
- cierre arquitectónico y funcional de Claude Chat;
- estado de Git informado.

ChatGPT Work debe:

- identificar qué quedó realmente implementado;
- distinguir información de evidencia confirmada;
- resolver o declarar contradicciones;
- confirmar el estado de la cadena;
- registrar riesgos o pendientes;
- determinar si el track puede cerrarse;
- definir un único siguiente paso.

**Estados permitidos:**

- `READY_TO_CLOSE`
- `READY_TO_CLOSE_WITH_FINDINGS`
- `RETURN_TO_CODEX`
- `RETURN_TO_DECISION`
- `BLOCKED`

ChatGPT Work recomienda el cierre, pero no autoriza staging, commit, push, merge
o despliegue.

---

## 6. Flujo visual resumido

```text
Eduardo inicia el tema
→ ChatGPT: INITIAL_PROPOSAL
→ Claude Chat: ARCHITECTURAL_CRITIQUE
→ ChatGPT: REVISED_PROPOSAL
→ Claude Chat: PROVISIONAL_DECISION
→ ChatGPT Work: TECHNICAL_VERIFICATION_HANDOFF
→ Claude Code: TECHNICAL_VERIFICATION_REPORT
→ Eduardo: OWNER_SCOPE_APPROVAL
→ Codex: IMPLEMENTATION_HANDOFF
→ Claude Code: IMPLEMENTATION_AUDIT_REPORT
→ Claude Chat: ARCHITECTURAL_FUNCTIONAL_CLOSURE
→ ChatGPT Work: FINAL_EVIDENCE_RECONCILIATION
```

---

## 7. Cuándo puede abreviarse el flujo

### 7.1. Consulta o explicación sin cambios

No requiere las diez intervenciones si:

- no produce una decisión normativa;
- no crea una orden de implementación;
- no modifica archivos;
- no altera arquitectura, gobernanza o alcance.

### 7.2. Continuación de un alcance ya aprobado

Las intervenciones ya completadas no deben repetirse cuando existe evidencia
inequívoca de:

- decisión aprobada;
- verificación previa vigente;
- aprobación exacta de Eduardo;
- mismo repositorio, rama y alcance;
- ausencia de un cambio material.

En ese caso se continúa desde la intervención pendiente.

La autorización aprobada no se pierde por:

- cambiar de conversación;
- abrir una rama nueva de conversación;
- transferir el resultado a la siguiente IA;
- reanudar el trabajo posteriormente.

La continuidad debe reconstruirse mediante un `CONTINUITY PACKET`, sin pedir
otra vez una aprobación válida para el mismo alcance.

### 7.3. Corrección dentro del alcance aprobado

Si Claude Code emite `REJECTED`, Codex puede corregir sin una nueva compuerta
cuando:

- la corrección afecta solo archivos ya autorizados;
- no cambia la arquitectura;
- no introduce dependencias nuevas;
- no amplía el comportamiento aprobado;
- no contradice una decisión de Eduardo.

Después de la corrección, Claude Code debe repetir la auditoría.

### 7.4. Nueva decisión o cambio material

El proceso vuelve a la intervención correspondiente cuando:

- cambia el objetivo;
- cambia el modelo arquitectónico;
- aumenta el alcance;
- se agregan archivos;
- se introducen dependencias nuevas;
- la evidencia contradice la decisión;
- aparece un riesgo bloqueante.

No puede presentarse un cambio material como una corrección menor para evitar
la deliberación o la aprobación.

---

## 8. Condiciones de parada

Ninguna IA debe avanzar cuando:

- no puede confirmar el repositorio correcto;
- la rama no corresponde al track;
- el `HEAD` cambió y vuelve obsoleta la evidencia recibida;
- existen cambios locales que colisionan con el alcance;
- el límite autorizado es ambiguo;
- falta la aprobación de Eduardo antes de implementar;
- se requieren credenciales, permisos o accesos no autorizados;
- una prueba crítica falla;
- existe una contradicción material no resuelta;
- el rollback material no está definido;
- Claude Code emitió `BLOCKED` o `RETURN_TO_DECISION`;
- implementar una corrección exige ampliar el alcance.

Los hallazgos fuera de alcance se registran para otro STEP o track. No se
implementan incidentalmente.

---

## 9. Estados de evidencia

Cada hecho debe clasificarse, cuando corresponda, mediante uno de los siguientes
estados:

- `INFORMED`
- `DIRECTLY_CONFIRMED`
- `PROPOSED`
- `IMPLEMENTED`
- `AUDITED`
- `OWNER_APPROVED`
- `COMMITTED`
- `PUSHED`
- `BLOCKED`
- `SUPERSEDED`
- `NOT_CONFIRMED`

No se debe confundir:

- `INFORMED` con `DIRECTLY_CONFIRMED`;
- `PROPOSED` con `IMPLEMENTED`;
- `IMPLEMENTED` con `AUDITED`;
- `AUDITED` con `OWNER_APPROVED`;
- `OWNER_APPROVED` con `COMMITTED`;
- `COMMITTED` con `PUSHED`.

---

## 10. Evidencia mínima obligatoria

Toda intervención técnica debe registrar, cuando aplique:

- Track;
- Step;
- modo;
- agente real;
- fecha;
- repositorio y ruta;
- rama;
- `HEAD` inicial;
- estado del working tree;
- alcance autorizado;
- archivos protegidos;
- archivos creados;
- archivos modificados;
- comandos ejecutados;
- pruebas y resultados;
- `HEAD` final;
- diff o commits relacionados;
- riesgos residuales;
- rollback;
- veredicto;
- siguiente agente responsable.

### 10.1. Orden operativo de evidencia

Para verificar hechos sobre el estado actual del repositorio:

1. filesystem actual;
2. código y configuración actuales;
3. contratos ejecutables y pruebas reproducidas;
4. Git: `status`, `diff`, `log`, rama y `HEAD`;
5. documentación vigente aplicable;
6. investigaciones históricas;
7. memoria y conversaciones de IA.

Este orden determina qué demuestra que algo existe o cómo se comporta. La
validez normativa y la resolución de contradicciones se rigen por:

`Gystigo/docs/architecture/ARCHITECTURE_GOVERNANCE.md`

---

## 11. Encabezado operativo obligatorio

Cada bloque transferido a otra IA debe comenzar con:

```text
PEGAR EN: CHATGPT / CHATGPT WORK / CLAUDE CHAT / CLAUDE CODE / CODEX / NO PEGAR
Track:
Step:
Mode:
Agent:
Status:
Repository:
Branch:
HEAD:
Authorized Boundary:
Protected Files:
Architecture Change: YES / NO
Next Responsible Agent:
```

Si un campo técnico todavía no puede conocerse, se escribe:

`PENDING_VERIFICATION`

Nunca debe inventarse.

---

## 12. Artefactos y responsables

| Orden | Artefacto | Responsable |
|---:|---|---|
| 1 | `INITIAL_PROPOSAL` | ChatGPT |
| 2 | `ARCHITECTURAL_CRITIQUE` | Claude Chat |
| 3 | `REVISED_PROPOSAL` | ChatGPT |
| 4 | `PROVISIONAL_DECISION` | Claude Chat |
| 5 | `TECHNICAL_VERIFICATION_HANDOFF` | ChatGPT Work |
| 6 | `TECHNICAL_VERIFICATION_REPORT` | Claude Code |
| Compuerta | `OWNER_SCOPE_APPROVAL` | Eduardo |
| 7 | `IMPLEMENTATION_HANDOFF` | Codex |
| 8 | `IMPLEMENTATION_AUDIT_REPORT` | Claude Code |
| 9 | `ARCHITECTURAL_FUNCTIONAL_CLOSURE` | Claude Chat |
| 10 | `FINAL_EVIDENCE_RECONCILIATION` | ChatGPT Work |

### 12.1. Ubicaciones operativas

Desde 2026-09-15 estos artefactos viven en la memoria operativa (BoxGhost), por track:

- informes de Codex:
  `Fabric/gm-ai-boxghost/tracks/<TRACK-ID>/handoffs/codex-to-review/`;
- auditorías formales de Claude Code:
  `Fabric/gm-ai-boxghost/tracks/<TRACK-ID>/audits/accepted/`;
- decisiones:
  `Fabric/gm-ai-boxghost/tracks/<TRACK-ID>/decisions/`;
- bitácora:
  `Fabric/Knowledge/00-GYPPORT-UNIVERSE/Reglas.md`, el log canónico append-only.

Hasta 2026-09-15 estas rutas fueron `docs/ai/handoffs/codex-to-review/`,
`docs/ai/reviews/accepted/` y `docs/ai/decisions/` dentro de Gystigo.

Las conversaciones cotidianas no sustituyen los artefactos formales.

---

## 13. Reglas obligatorias

- Eduardo inicia el proceso y conserva la autoridad final.
- El intercambio conceptual inicial de cuatro intervenciones no puede omitirse
  para una decisión nueva.
- ChatGPT organiza y sintetiza el corpus antes de proponer.
- Claude Chat critica y consolida el modelo, pero no modifica el repositorio.
- ChatGPT Work convierte la decisión conceptual en un handoff verificable.
- Claude Code verifica la propuesta antes de la aprobación de Eduardo.
- Eduardo aprueba una sola vez el alcance exacto.
- Codex implementa exclusivamente el alcance aprobado.
- Claude Code audita independientemente la implementación.
- Claude Chat realiza el cierre arquitectónico y funcional.
- ChatGPT Work cruza toda la evidencia y recomienda el cierre.
- No se permite negociación autónoma entre las IAs.
- No se adelantan varias intervenciones como si ya hubieran ocurrido.
- No se envía una idea inicial directamente a Codex.
- No se trata un borrador de Claude Chat como un archivo implementado.
- No se confunde la verificación previa con la auditoría posterior.
- No se solicita repetidamente una aprobación ya concedida para el mismo
  alcance.
- Una nueva aprobación solo corresponde cuando cambia materialmente el alcance.
- Ninguna IA autoriza su propio trabajo.
- Solo Eduardo autoriza staging, commit, push, merge o despliegue.

---

## 14. Regla frente a flujos históricos

El esquema histórico:

```text
ChatGPT → Claude Chat → ChatGPT → Claude Chat
→ Claude Code implementa → Codex valida/implementa
```

queda `SUPERSEDED` porque:

- atribuye implementación a Claude Code;
- no contiene una verificación read-only previa correctamente separada;
- mezcla validación propia y aceptación independiente;
- no coloca la compuerta única de Eduardo antes de la implementación;
- no incluye la auditoría posterior;
- no incluye el cierre arquitectónico y funcional;
- no incluye el cruce final de evidencia de ChatGPT Work.

También queda superado cualquier resumen reducido que omita:

- las cuatro intervenciones conceptuales;
- el handoff técnico de ChatGPT Work;
- la verificación previa de Claude Code;
- la compuerta única de Eduardo;
- la auditoría posterior de Claude Code;
- el cierre de Claude Chat;
- la reconciliación final de ChatGPT Work.

Las entradas históricas no deben borrarse. Deben conservarse como evidencia,
marcarse `HISTORICAL_WORKFLOW` o `SUPERSEDED` y enlazar esta norma.

---

## 15. Recordatorio de una línea

> **ChatGPT propone; Claude Chat critica; ChatGPT revisa; Claude Chat consolida;
> ChatGPT Work prepara; Claude Code verifica; Eduardo aprueba una sola vez;
> Codex implementa; Claude Code audita; Claude Chat cierra; ChatGPT Work cruza
> la evidencia; y solo Eduardo autoriza Git protegido.**

---

## 16. Registro de aprobación

| Campo | Valor |
|---|---|
| Decisión del propietario | `APPROVED` |
| Aprobador | Eduardo Luis Burgasi Pullaguari |
| Fecha de aprobación | 2026-07-28 |
| Fecha de regeneración documental | 2026-07-30 |
| Alcance de la aprobación | Norma canónica de colaboración multiagente de GYPPORT® |
| Versión aprobada | 1.0 |
| Ubicación canónica | `Fabric/Knowledge/00-GYPPORT-UNIVERSE/ai-collaboration/GYPPORT_AI_COLLABORATION_EXECUTION_ORDER_v1.0.md` (aprobado en 2026-07-28 como `docs/architecture/GYPPORT_AI_COLLABORATION_EXECUTION_ORDER_v1.0.md`) |

Esta aprobación convierte el documento en norma vigente.

Su incorporación al repositorio, así como la actualización de referencias en
otros archivos, debe ejecutarse mediante el flujo técnico y las autorizaciones
definidas en este mismo documento.
