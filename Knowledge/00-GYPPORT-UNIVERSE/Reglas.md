
GYPPORT® Platform Foundation v1.0
GYPPORT® Platform OS
GYPPORT® Developer Platform
            Tool Source Framework
GYPPORT® Developer Toolchain

Architecture Freeze 1.0

La arquitectura no se diseña para el primer desarrollador; se diseña para el desarrollador número 50, que llegará dentro de cinco años y no conocerá ninguna decisión que tomamos hoy.


Nunca construiremos algo únicamente porque hoy funciona; siempre preguntaremos cómo evolucionará dentro de cinco años.

Una operación de Toolchain no puede modificar un archivo fuera del proyecto autorizado.

Todo lo que se ejecuta durante el desarrollo (generadores, validadores, migraciones, CLI, verificadores y automatizaciones) vive en tool/. Todo lo que se ejecuta como parte del Platform OS vive en engine/.


Cuando una estructura se repite más de tres veces, deja de ser una implementación y pasa a ser parte del Framework.




Lo más importante

Quiero hacer una autocrítica como Chief Software Architect.

Durante semanas estuvimos solucionando problemas manualmente.

Hoy cambió nuestra forma de trabajar.

Cada vez que aparezca una tarea repetitiva nos haremos esta pregunta:

¿Esto debe hacerlo un desarrollador o debe hacerlo el Toolchain?

Si la respuesta es "siempre hacemos lo mismo", entonces no la volveremos a hacer manualmente.

La convertiremos en una herramienta.


Ningún componente del Toolchain implementará lógica arquitectónica directamente. Toda la inteligencia vivirá en el Architecture Policy Engine, y el resto de herramientas (Doctor, CLI, Scaffold, Migration, Validation, futuras extensiones de VS Code o CI/CD) actuarán únicamente como consumidores de ese motor.

Cuando un archivo cambia, debo generar el archivo completo nuevamente, listo para copiar y pegar. Nunca debo entregar solamente fragmentos o indicar "agrega esto".

Doctor no conoce las políticas.
Doctor no conoce las reglas.
Doctor solo ejecuta el motor de arquitectura y presenta el resultado.

El mayor cambio conceptual

Hay algo que tampoco quiero que vuelva a ocurrir.

Por ejemplo, hoy tenemos:

ArchitecturePolicyEngine

Pero mañana tendremos:

DoctorEngine

Después:

ScaffoldEngine

Después:

MigrationEngine

Eso significa que estamos repitiendo un patrón.

Cuando un patrón aparece tres veces, deja de ser una implementación y pasa a ser una abstracción.


Toda capacidad del Toolchain será un Framework registrado en el Tool Kernel. Ningún comando de la CLI importará directamente un Framework. Toda resolución pasará por el Framework Registry.


Nueva regla de oro

No debemos crear Policies únicamente para validar el proyecto.

Debemos crear Policies para validar nuestras propias decisiones arquitectónicas.

Es decir:

Cada vez que detectemos un error de diseño que pueda repetirse, no lo corregimos solamente. Lo convertimos en una Policy del Toolchain.



La regla nueva que propongo

A partir de hoy, antes de crear una carpeta dentro de cualquier Framework del Toolchain, nos preguntaremos:

¿Esto pertenece a Architecture?

o

¿Esto pertenece al ADN de todos los Frameworks?

Si pertenece a todos, vive en tool/core.

Si pertenece únicamente a uno, vive en tool/framework/<framework>.

Regla Oficial #32 — Framework Independence
Ningún Framework del Toolchain puede importar directamente otro Framework.

Toda comunicación entre Frameworks deberá realizarse a través del Tool Kernel o del Framework Registry.


Regla Oficial #33 — Separación de Plataformas

GYPPORT® se divide en dos plataformas independientes:

Platform OS
Developer Platform

Ninguna depende físicamente de la otra.

La Developer Platform construye y protege el Platform OS.


Regla Oficial #34 — Responsabilidad del Server

Server es el Host de Servicios del Platform OS.

No representa únicamente una API.

Toda capacidad de backend vive dentro del Server.

Regla Oficial #35 — Responsabilidad del Studio

Studio es el Host de Experiencia del Platform OS.

No representa una tecnología específica.

React, Flutter, Electron, Tauri y cualquier otra UI futura son únicamente renderizadores del Studio.

Regla Oficial #36 — Independencia Tecnológica

Ninguna decisión arquitectónica podrá depender de React, Spring Boot o Flutter.

Las tecnologías implementan el Platform OS.

Nunca lo definen.


Regla Oficial #37 — Persistencia del Toolchain

Todo archivo persistente generado por el Developer Toolchain
deberá almacenarse dentro del Toolchain Workspace.

Ningún Framework podrá crear archivos temporales,
baselines, reportes, cachés o snapshots fuera de workspace/.

Regla Oficial #38 — Automatización del Toolchain

Ningún componente repetitivo del Developer Toolchain se construirá manualmente más de una vez. En cuanto una estructura, patrón o flujo se repita en tres o más Frameworks, deberá convertirse en una capacidad oficial del Toolchain y ser generado automáticamente mediante Scaffold.

Regla Oficial #39 — El Toolchain también sigue arquitectura empresarial


Regla Oficial #40 — La arquitectura solo inspecciona código fuente

El Architecture Policy Engine nunca analizará directorios generados automáticamente por herramientas de compilación o construcción.

Regla Oficial #41 — Contrato Único de Análisis

Todo Framework del GYPPORT® Developer Toolchain que genere resultados de inspección, validación o diagnóstico deberá producir un ToolAnalysisReport. Ningún Framework podrá definir un formato propio de reporte.

Regla Oficial #42 — Nunca asumir la estructura

Antes de proponer una operación que modifique archivos o carpetas (renombrar, mover o eliminar), el Toolchain deberá verificar la estructura actual del proyecto. No se permitirán instrucciones basadas en una estructura recordada o asumida.


Regla Oficial #43 — El recorrido del código fuente es único

Ningún Framework del Developer Toolchain recorrerá directamente el sistema de archivos.

Todos utilizarán el:

Tool Source Scanner

Regla Oficial #44 — Las Policies son puras

Ninguna Policy del Developer Toolchain accederá directamente al sistema de archivos (fs), a rutas (path) ni recorrerá el árbol del proyecto. Todas recibirán únicamente datos preparados por el Tool Source Framework.

Regla Oficial #45 — Todo Framework declara su Scope

Ningún Framework del Developer Toolchain analizará directamente el árbol completo del proyecto. Todo Framework declarará explícitamente el Scope sobre el que trabaja y el Tool Scope Framework resolverá el conjunto de entradas correspondiente.


GYPPORT® Architecture Evolution Rule

Ningún cambio estructural importante se realizará únicamente por una idea teórica.


GYPPORT® Platform OS tiene un único Kernel independiente en engine/kernel/. Core lo consume mediante @kernel; Core no lo contiene, no lo replica y no lo reexporta como @core/kernel.




Estado que debemos reconocer ahora
Toolchain:
activo y principal

Dashboard Engine:
activo y paralelo

Runtime recovery:
solo para cerrar los bloqueos ya abiertos

Legacy UI / Journey / Module UI migration:
congelado

App composition:
congelado, salvo decidir cómo resolver installedPlugins sin materializar
una arquitectura no autorizada

Theme:
congelado

La verdad es exactamente la que indicaste:

Dashboard Engine estaba autorizado como boundary paralelo independiente. Nunca estuvo autorizada la reorganización completa de Studio.

Esa debe convertirse ahora en una regla escrita, incluida en la gobernanza y comprobada por cada agente antes de ejecutar cualquier STEP.




La arquitectura de GYPPORT® no puede cambiar como consecuencia de un hallazgo técnico. Un hallazgo solo puede generar evidencia y una propuesta de STEP; nunca autoriza por sí mismo una expansión del boundary activo.

Boundary Expansion Rule

Ningún hallazgo técnico autoriza por sí mismo la expansión del boundary activo del proyecto. Todo hallazgo fuera del boundary debe registrarse como evidencia y convertirse, si corresponde, en un STEP independiente sujeto a aprobación.


No volveremos a crear documentación "por anticipado". Solo documentaremos aquello que ya haya quedado estabilizado y aprobado.


Toolchain continúa siendo el track principal. Dashboard Engine puede desarrollarse en paralelo como boundary aislado y contract-first. Ningún otro frente estructural de Platform OS se abre automáticamente por el hecho de haber autorizado Dashboard.

Regla Oficial #47 — Gobernanza de programación de Studio

La decisión arquitectónica aceptada sobre el modelo híbrido de programación y
el ownership del ciclo de vida de plugins está en
`docs/architecture/decisions/ADR-0001-studio-programming-model-and-plugin-lifecycle-ownership.md`.
La guía operativa está en
`docs/architecture/studio/STUDIO_PROGRAMMING_GUIDE.md`. Estas fuentes se
referencian sin duplicar su contenido.

Nunca empezaremos un STEP escribiendo código. Siempre empezaremos entendiendo el dominio, definiendo el objetivo, delimitando el alcance y acordando la arquitectura.

Regla AIWS-001

Ninguna conversación será considerada fuente de verdad.

Las conversaciones sirven para:

discutir;
analizar;
aprender;
decidir.

Cuando una decisión se aprueba, sale del chat y pasa al repositorio.



Un dato maestro, estable y reutilizado por distintos contextos debe tener una única identidad canónica y un único propietario. Los demás dominios lo referencian; no lo duplican como otra fuente de verdad.

Toda persona que usa GYPPORT entra mediante un UserAccount y, una vez resuelta su identidad, corresponde a una única MdmParty PERSON. Esa misma Persona puede tener su perfil personal y también un RUC de Persona Natural, sin crear otra identidad ni una Organization. Ese RUC personal puede tener uno o muchos establecimientos SRI. Además, la Persona puede crear o relacionarse con una o varias MdmParty ORGANIZATION, cada una con su propio RUC empresarial y sus propios establecimientos.



2026-09-13 — GYPPORT® Universe / Regla de precedencia y reconciliación

Una propuesta nueva nunca puede borrar, simplificar ni reemplazar una decisión
anterior únicamente por comodidad técnica.

Cuando exista conflicto entre intención histórica, documentación canónica,
ADRs, esquema, código, pruebas o una propuesta nueva, el agente deberá detener
la ejecución de la parte conflictiva.

El agente deberá:

- presentar la evidencia;
- explicar el impacto;
- mostrar alternativas de reconciliación;
- recomendar una opción con sus razones;
- esperar una decisión explícita del Owner.

Formato mínimo:

```text
HISTORICAL_INTENT=
CURRENT_CANONICAL_DOCUMENT=
CURRENT_SCHEMA=
CURRENT_CODE=
CURRENT_TEST_EVIDENCE=
CONFLICT=
IMPACT=
RECONCILIATION_OPTIONS=
RECOMMENDED_RECONCILIATION=
RECOMMENDATION_REASON=
OWNER_DECISION_REQUIRED=
EXECUTION_STATUS=STOPPED_PENDING_OWNER_REVIEW
```

La detección del conflicto no autoriza a resolverlo por cuenta propia.


2026-09-13 — GYPPORT® Universe / Regla de reanudación después de Owner Review

Cuando el Owner resuelva un conflicto, el agente no reiniciará el STEP ni
reinterpretará la decisión.

Antes de continuar deberá revalidar:

```text
CURRENT_HEAD=
CURRENT_MIGRATION_HEAD=
WORKING_TREE_RECHECKED=YES
DRIFT_SINCE_STOP=YES|NO
```

Luego deberá reanudar desde el punto detenido:

```text
RESUME_FROM=
RESTART_FROM_ZERO=NO
```

Si apareció drift que cambia la validez de la decisión, deberá detenerse
nuevamente para Owner Review.


2026-09-13 — GYPPORT® Universe / Regla de granularidad de auditoría y provenance

La granularidad histórica, de auditoría y de provenance no podrá simplificarse
únicamente porque una estructura nueva permita usar menos campos.

Los campos que responden a preguntas diferentes deberán conservar su semántica,
por ejemplo:

```text
WHO
WHAT
WHERE
WHEN
WHY
SOURCE
UNDER_WHICH_CONTEXT
BEFORE
AFTER
REQUEST / CORRELATION
```

Campos de actor, tenant, organización, sesión, source, provenance, reason,
request/correlation, old/new values, IP, user agent y timestamps no deberán
colapsarse sin demostrar primero que representan exactamente la misma verdad de
dominio.


2026-09-13 — GYPPORT® Universe / Regla de actor global y contexto tenant

Los campos de actor histórico como:

```text
created_by_user_account_id
updated_by_user_account_id
assigned_by_user_account_id
granted_by_user_account_id
revoked_by_user_account_id
verified_by_user_account_id
approved_by_user_account_id
submitted_by_user_account_id
```

representan por defecto a la cuenta global que ejecutó la acción.

Regla canónica:

```text
AUDIT / ACTION ACTOR
→ Global UserAccount

TENANT
→ contexto / provenance de la acción

ORGANIZATION
→ contexto operacional más específico cuando aplica

MEMBERSHIP
→ prueba de que una cuenta puede operar en un tenant
```

`Actor != Membership`.

No se moverá automáticamente un actor histórico a `UserTenantMembership` por
el solo hecho de que la acción tenga `tenant_id`.

Un Platform Admin puede ser actor legítimo sobre un tenant sin tener una
membership de cliente en ese tenant.


2026-09-13 — GYPPORT® Universe / Regla de Foreign Keys por semántica

Dos Foreign Keys que tienen la misma forma física no se consideran
semánticamente equivalentes.

Antes de mover, reemplazar o eliminar una FK deberán revisarse individualmente:

```text
TABLE=
COLUMN=
FIELD_SEMANTICS=
DOMAIN_OWNER=
HISTORICAL_INTENT=
FABRIC_EVIDENCE=
ADR_EVIDENCE=
CURRENT_SCHEMA=
CURRENT_CODE_USAGE=
AUDIT_IMPACT=
SECURITY_IMPACT=
RECOMMENDED_TARGET=
```

Las relaciones de acceso/participación pueden depender de
`UserTenantMembership`.

Las referencias históricas de actor no se convertirán automáticamente en
membership.


2026-09-13 — GYPPORT® Universe / Regla de UserTenantMembership

`UserTenantMembership` representa solamente:

```text
ACCOUNT_TO_TENANT_ACCESS
```

Responde:

> ¿Puede este UserAccount operar en este tenant?

No representa:

```text
PERSONAL
BUSINESS
HOME
Organization
Employment
TaxSubject
Role
identidad del actor
```

No se añadirá clasificación PERSONAL/BUSINESS/HOME a Membership por comodidad
de navegación o login.


2026-09-13 — GYPPORT® Universe / Regla de representación legal

Un representante legal puede ser:

```text
MdmParty PERSON
o
MdmParty ORGANIZATION
```

Nunca se diseñará la foundation de representación legal suponiendo que el
representante siempre es una Persona.

No se deberá crear una relación rígida equivalente a
`legal_representative_person_id` como modelo universal.


2026-09-13 — GYPPORT® Universe / Regla del documento maestro de contexto

El documento:

```text
Fabric/Knowledge/00-GYPPORT-UNIVERSE/
GYPPORT_BUSINESS_PLATFORM_UNIVERSAL_DATA_DOMAIN_CONTEXT_2026-09-13.md
```

es el contexto canónico Owner-approved para comprender el Universo de Datos,
MDM, Party, seguridad, fiscalidad, historial, provenance y granularidad de
GYPPORT antes de proponer cambios estructurales.

Los agentes deberán leerlo junto con:

- `GYPPORT_UNIVERSE_CANONICAL_BASELINE.md`;
- `Reglas.md`;
- ADRs relevantes;
- ownership docs;
- schema/código/pruebas reales.

La memoria conversacional por sí sola no reemplaza esta lectura.


2026-09-13 — GYPPORT® Universe / Regla de naturaleza de Reglas.md

`Reglas.md` es una bitácora histórica acumulativa de reglas, decisiones,
principios y estados surgidos durante las conversaciones y STEPs.

Debe conservarse como historia:

```text
PRESERVE_EXISTING_TEXT=YES
APPEND_ONLY=YES
RENUMBER_EXISTING_RULES=NO
REORGANIZE_EXISTING_HISTORY=NO
CONSOLIDATE_OLD_RULES=NO
DELETE_SUPERSEDED_RULES=NO
```

Cuando una regla nueva sustituya una anterior, la regla anterior permanecerá
como evidencia histórica y la nueva deberá indicar expresamente la sustitución.

Cuando `Reglas.md` cambie, deberá generarse el archivo completo nuevamente,
listo para copiar y pegar.


2026-09-13 — gm-expenses / Regla de revisión de gastos

Aprobar, Observar y Rechazar son decisiones distintas sobre un gasto:

```text
APROBAR  = el gasto se acepta.
OBSERVAR = el gasto tiene un problema corregible y vuelve al responsable.
RECHAZAR = el gasto no se acepta y su revisión termina.
```

RECHAZADO ES TERMINAL PARA ESE GASTO: no admite corrección, no vuelve a
revisión, no muestra formulario de corrección y no puede revivirse por ninguna
vía. Si corresponde, se registra un gasto nuevo.

"Corregir gasto" existe solamente para un gasto OBSERVADO. Un gasto rechazado
se muestra en solo lectura: motivo, detalle, quién lo rechazó, fecha y la
opción de volver al expediente.

Para gm-expenses, esta regla sustituye el comportamiento anterior que permitía
corregir un gasto rechazado y devolverlo a revisión.


2026-09-13 — gm-expenses / Regla de trazabilidad de la revisión

```text
CERRADO PARA EDICIÓN != ELIMINADO DE TRAZABILIDAD
```

Toda decisión de revisión conserva quién la tomó, cuándo, el motivo y el
detalle. El historial completo del gasto permanece visible aunque el gasto
quede aprobado o rechazado, y se conserva para reportes, métricas y la calidad
de presentación de gastos. El historial nunca se fabrica para completar datos
antiguos.

Observar y Rechazar registran un motivo estructurado (código de catálogo) y un
detalle opcional; el detalle es obligatorio cuando el motivo es OTRO. Motivos
de rechazo:

```text
GASTO_NO_PERMITIDO
NO_CORRESPONDE_AL_EXPEDIENTE
COMPROBANTE_INVALIDO
INFORMACION_INCONSISTENTE
GASTO_DUPLICADO
FUERA_DE_POLITICA
OTRO
```


2026-09-13 — gm-expenses / Regla de cierre del expediente

Un expediente no se cierra mientras tenga gastos sin decisión final
(REGISTRADO, PENDIENTE_REVISION u OBSERVADO). APROBADO y RECHAZADO son
decisiones finales y no bloquean el cierre.

El mensaje nombra la causa concreta. Nunca se usa "pendientes de resolución":

```text
El expediente tiene gastos pendientes de aprobación.
El expediente tiene gastos observados pendientes de corrección.
El expediente tiene gastos pendientes de revisión o corrección.
```

Un gasto rechazado no forma parte del total gastado ni del total justificado.


2026-09-13 — gm-expenses / Regla de anticipos, rendición y total justificado

```text
UNA FUNCIÓN OPERATIVA = UN LUGAR CLARO PARA EJECUTARLA
```

No se crean caminos paralelos para resolver lo mismo.

El Anticipo gestiona su creación, autorización y entrega. El Expediente es el
centro de la rendición: devolución, reembolso, conciliación y cierre. El
Anticipo puede mostrar un resumen informativo de su rendición y el acceso
"Ver expediente de gastos →".

No existe una acción de usuario "Recalcular". El total justificado se
actualiza automáticamente y sin inconsistencias.


2026-09-13 — gm-expenses / Regla de categorías favoritas

Favorita es una ayuda para elegir, no parte de la categoría. La lista abierta
puede mostrar primero las favoritas, pero el valor elegido se muestra y se
registra solamente como la categoría ("Combustible"), nunca como
"Favorita · Combustible" ni "★ Combustible".


2026-09-15 — GYPPORT® Universe / Regla de VERIFIED_BASELINE_REUSE

Un STEP aceptado por el Owner y committed localmente no vuelve a ejecutar
automáticamente su regresión histórica completa mientras su Verified Baseline
aceptado siga siendo válido.

Todo STEP futuro que toque un área con Verified Baseline deberá clasificar ese
baseline e informar:

```text
BASELINE_FOUND=YES|NO
BASELINE_ID=
BASELINE_REUSE_DECISION=REUSE|PARTIAL_INVALIDATION|FULL_INVALIDATION
BASELINE_REUSE_REASON=
```

Con REUSE:

```text
FULL_HISTORICAL_REGRESSION_RERUN=NO
```

y se ejecutan solamente las pruebas del STEP actual, las pruebas seleccionadas
por análisis de impacto y el smoke de integración requerido.

Una regresión completa exige un análisis de impacto concreto. "Ejecutar todo de
nuevo por seguridad" no es razón suficiente.

La evidencia primaria de un baseline son los SHA de sus commits aceptados. Son
evidencia secundaria el manifiesto de rutas, los hashes de blobs o archivos, los
resúmenes de pruebas, el head de migraciones, las deudas conocidas y la
evidencia de la matriz de runtime. El scratchpad y el historial de conversación
no son almacenamiento canónico de baselines.

Cierre de un STEP:

```text
IMPLEMENT
→ VERIFY
→ OWNER REVIEW
→ CONTROLLED COMMIT
→ POST-COMMIT SMOKE
→ GENERATE VERIFIED BASELINE
→ REGISTER BASELINE IN Reglas.md
→ OWNER REVIEW
→ NEXT STEP
```

Este cierre amplía, sin reemplazarla, la secuencia ONE STEP → VERIFY → OWNER
REVIEW → CONTROLLED COMMIT → NEXT STEP: añade los pasos posteriores al commit.
Generar y registrar un baseline no lo aprueba, no hace commit ni push, no
ejecuta pruebas y no inicia el siguiente STEP.

Política, automatización y generador:

```text
Fabric/Knowledge/00-GYPPORT-UNIVERSE/verification-baselines/VERIFIED_BASELINE_REUSE.md
Fabric/Knowledge/00-GYPPORT-UNIVERSE/verification-baselines/GYPPORT_VERIFIED_BASELINE_AUTOMATION.md
Fabric/tools/verification/New-GypportVerifiedBaseline.ps1
```


2026-09-15 — GYPPORT® Universe / Registro de Verified Baseline PKG2C

Verified Baseline de un STEP aceptado por el Owner y committed localmente.
Se reutiliza según VERIFIED_BASELINE_REUSE.

```text
BASELINE_ID=GYPPORT-PKG2C-VERIFIED-BASELINE-2026-09-15
BASELINE_PATH=Fabric/Knowledge/00-GYPPORT-UNIVERSE/verification-baselines/GYPPORT_PKG2C_VERIFIED_BASELINE_2026-09-15.md
STEP=GYPPORT_GLOBAL_ACCOUNT_TENANT_MEMBERSHIP_FOUNDATION_15
PHASE=PKG_2C_CONTEXTUAL_ACCESS_AND_FK_RECONCILIATION
STATUS=OWNER_ACCEPTED_COMMITTED_LOCAL
ACCEPTED_COMMITS=gm-entities=e6d3cbcc5e004e8fbd11c78dc1817b5a00e6bffb; gm-security=1654f271711e96761ae7d5470dce3d161cb4333b; Gystigo=a3b7bfeb1b52f06110cd08af185b04f3690b4a43
MIGRATION_HEAD=V58
VERIFIED_FILE_COUNT=52
BASELINE_REUSE_ALLOWED=YES
```

GYPPORT Brain es la capa de inteligencia y orquestación de contexto que transforma la memoria completa e inmutable de GYPPORT en contextos pequeños, relevantes y verificables para cada IA, sin destruir ni sustituir la información original.

egla ya la habíamos establecido: si una base/documentación se corrige, se corrige de una vez; no se deja deuda arquitectónica artificial para futuro.


2026-09-15 — GYPPORT® Universe / Regla de arquitectura canónica de memoria GYPPORT

Decisión del Owner: Fabric es la única raíz de memoria de GYPPORT. El conocimiento canónico vive en
Fabric/Knowledge, la memoria operativa en Fabric/gm-ai-boxghost y las fuentes crudas, originales y
pesadas en GYPPORT-Storage. Gystigo es el producto y Host, y Modules/gm-ai-workspace es únicamente
la aplicación que lee y orquesta esa memoria. Esta entrada fija dónde vive cada artefacto duradero
de GYPPORT y reemplaza explícitamente los arreglos anteriores que se listan abajo.

```text
FABRIC_IS_SINGLE_GYPPORT_MEMORY_ROOT=YES
CANONICAL_KNOWLEDGE_ROOT=Fabric/Knowledge
OPERATIONAL_MEMORY_ROOT=Fabric/gm-ai-boxghost
RAW_PERSISTENT_STORAGE_ROOT=D:\NZXTG7\GYPPORT\GYPPORT ERP\GYPPORT-Storage
VERIFICATION_BASELINE_REUSE=YES
RAW_OPERATIONAL_MEMORY_MUST_NOT_BE_REPLACED_BY_SUMMARY=YES
SUMMARIES_ARE_DERIVED=YES
CONTEXT_PACKS_ARE_REGENERABLE=YES
PROVIDER_CACHE_IS_NOT_GYPPORT_MEMORY=YES
AI_TEMP_STORAGE_IS_NOT_DURABLE_GYPPORT_MEMORY=YES
NEW_DURABLE_GYPPORT_ARTIFACTS_MUST_USE_CANONICAL_OWNER_PATH=YES
FULL_CANONICAL_MIGRATION_IN_SAME_STEP=YES
NO_DEFERRED_ARCHITECTURAL_CLEANUP=YES
```

Documentos canónicos que fija esta decisión:

```text
MEMORY_ARCHITECTURE_DOC=Fabric/Knowledge/00-GYPPORT-UNIVERSE/GYPPORT_MEMORY_ARCHITECTURE.md
CANONICAL_AGENT_ROOT=Fabric/Knowledge/00-GYPPORT-UNIVERSE/agents/
CANONICAL_AI_COLLABORATION_ROOT=Fabric/Knowledge/00-GYPPORT-UNIVERSE/ai-collaboration/
BOXGHOST_STRUCTURE_DOC=Fabric/gm-ai-boxghost/BOXGHOST_STRUCTURE.md
GYPPORT_BRAIN_CONTRACT=seccion 8 de GYPPORT_MEMORY_ARCHITECTURE.md
GYPPORT_BRAIN_IMPLEMENTED=NO
```

Lo que esta decisión reemplaza de forma explícita:

```text
Gystigo/Reglas.md                     -> retirado; el log canónico es Fabric/Knowledge/00-GYPPORT-UNIVERSE/Reglas.md
Gystigo/CHATGPT.md y Gystigo/CODEX.md -> retirados; su contenido canónico vive en agents/
Gystigo/AGENTS.md y Gystigo/CLAUDE.md -> solo entrypoints tecnicos (Codex y Toolchain; Claude Code), sin gobernanza
Gystigo/docs/ai/                      -> retirada; la historia operativa de agentes vive en Fabric/gm-ai-boxghost
Gystigo/docs/architecture/GYPPORT_AI_COLLABORATION_EXECUTION_ORDER_v1.0.md -> ai-collaboration/
Fabric/Governance/                    -> retirada; la gobernanza canonica vive en Fabric/Knowledge
Fabric/Knowledge/{Sources,Processing,Corpus} (protocolo 2026-08-01) -> fuentes crudas a GYPPORT-Storage; procesamiento y registros a BoxGhost
GYPPORT-Storage\Fabric\Knowledge\Standards ("Master") -> retirada; la ubicacion unica es Gystigo/docs/governance/standards
Governance/GYPPORT_Governance_Architecture -> historico, sin autoridad activa (ENGINEERING_ARTIFACT_RETENTION_POLICY.md se conservo en Fabric/Knowledge/Architecture)
```

La memoria cruda no se sustituye por resúmenes: un resumen es derivado y debe poder señalar su
fuente, un context pack es derivado y regenerable, la caché y la compactación del proveedor no son
memoria de GYPPORT, y el scratchpad, AppData\Local\Temp y las carpetas temporales de Codex no son
memoria duradera. Todo artefacto duradero nuevo se crea directamente en su ruta canónica, y lo
valioso que quede en almacenamiento temporal se promueve antes de cerrar el STEP.



2026-09-15 — GYPPORT® Universe / Regla de ubicación fisica, CURRENT_STEP y cierre de la fundación de memoria

Decision del Owner que cierra la fundacion de memoria de GYPPORT. La identidad logica del
almacenamiento se separa de su ubicacion fisica: la arquitectura habla de GYPPORT_STORAGE y solo un
registro sabe donde vive hoy. Google Drive queda fuera de la arquitectura de memoria y de
almacenamiento: no es backend, no es backup y no es una dependencia de sincronizacion. Ademas se fija
un unico CURRENT_STEP global como puntero de continuidad, el descubrimiento automatico de los agentes
y el enrutamiento permanente de artefactos.

```text
DATE=2026-09-15
GYPPORT_STORAGE_ID=GYPPORT_STORAGE
GYPPORT_LOCATION_REGISTRY=Fabric/Knowledge/00-GYPPORT-UNIVERSE/GYPPORT_LOCATIONS.properties
GYPPORT_STORAGE_GOOGLE_DRIVE_SYNC=DISABLED
PHYSICAL_STORAGE_LOCATION_IS_CONFIGURABLE=YES
STORAGE_LOCATION_SINGLE_SOURCE=YES
STORAGE_UNAVAILABLE_FALLBACK_CREATION=NO
FUTURE_NAS_MOVE_REQUIRES_ARCHITECTURE_CHANGE=NO
CURRENT_STEP_GLOBAL=YES
CURRENT_STEP_PATH=Fabric/Knowledge/00-GYPPORT-UNIVERSE/active-work/CURRENT_STEP.md
AGENT_AUTO_DISCOVERY_ENABLED=YES
PERMANENT_ARTIFACT_ROUTING_ENABLED=YES
AUTO_CURRENT_STEP_PREPARATION=YES
AUTO_IMPLEMENT_NEXT_STEP=NO
GYPPORT_STORAGE_SOURCE_MIGRATION_COMPLETE=YES
UNMERGED_UNIQUE_BOXGHOST_MEMORY=0
BOXGHOST_OPERATIONAL_HISTORY_COMPLETE=YES
GYPPORT_BRAIN_IMPLEMENTATION=DEFERRED
GYPPORT_BRAIN_STORAGE_MODEL=KNOWLEDGE_PLUS_BOXGHOST_PLUS_LOGICAL_GYPPORT_STORAGE
```

Lo que esta entrada reemplaza de forma explicita:

```text
RAW_PERSISTENT_STORAGE_ROOT=<ruta literal de la entrada anterior del 2026-09-15>
  -> sustituido por GYPPORT_STORAGE_ID + GYPPORT_LOCATION_REGISTRY.
     La ruta fisica vive unicamente en el registro; la gobernanza activa no la repite.
```

Siguen vigentes sin cambio las claves de la entrada anterior del 2026-09-15:
FABRIC_IS_SINGLE_GYPPORT_MEMORY_ROOT, CANONICAL_KNOWLEDGE_ROOT, OPERATIONAL_MEMORY_ROOT,
VERIFICATION_BASELINE_REUSE, RAW_OPERATIONAL_MEMORY_MUST_NOT_BE_REPLACED_BY_SUMMARY,
SUMMARIES_ARE_DERIVED, CONTEXT_PACKS_ARE_REGENERABLE, PROVIDER_CACHE_IS_NOT_GYPPORT_MEMORY,
AI_TEMP_STORAGE_IS_NOT_DURABLE_GYPPORT_MEMORY, NEW_DURABLE_GYPPORT_ARTIFACTS_MUST_USE_CANONICAL_OWNER_PATH,
FULL_CANONICAL_MIGRATION_IN_SAME_STEP y NO_DEFERRED_ARCHITECTURAL_CLEANUP.

El material externo crudo (coleccion externa, documentacion de ejemplo, plantillas y el archivo
sensible de migracion) vive ahora dentro de GYPPORT_STORAGE; el archivo con credenciales queda en su
area restringida, sin ingestion automatica de contexto ni sincronizacion externa. La memoria
operativa unica de BoxGhost recupero, byte a byte, la historia que solo existia en la rama Fabric
docs/gm-ai-workspace-canonical-unification-01 (d43b4fd), sin fusionarla y sin borrarla.


2026-09-15 — GYPPORT® Universe / Registro de Verified Baseline CANONICAL-MEMORY-FOUNDATION

Verified Baseline de un STEP aceptado por el Owner y committed localmente.
Se reutiliza según VERIFIED_BASELINE_REUSE.

```text
BASELINE_ID=GYPPORT-CANONICAL-MEMORY-FOUNDATION-VERIFIED-BASELINE-2026-09-15
BASELINE_PATH=Fabric/Knowledge/00-GYPPORT-UNIVERSE/verification-baselines/GYPPORT_CANONICAL_MEMORY_FOUNDATION_VERIFIED_BASELINE_2026-09-15.md
STEP=GYPPORT_CANONICAL_MEMORY_FOUNDATION_01
PHASE=FINAL_CANONICAL_MEMORY_FOUNDATION
STATUS=OWNER_ACCEPTED_COMMITTED_LOCAL
ACCEPTED_COMMITS=Fabric=fcb79cd23e0210731f83eda4697aea2a3e90e6f6; Gystigo=0544e2ec9dcf7bc883e8f57c498e7ac5fb23cbeb; GYPPORT_Governance_Architecture=2844695d670e6a276b01abde4073f07f7bcb029f
MIGRATION_HEAD=V58
VERIFIED_FILE_COUNT=434
BASELINE_REUSE_ALLOWED=YES
```

