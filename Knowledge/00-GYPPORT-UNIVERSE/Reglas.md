
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


2026-09-15 — GYPPORT® Universe / Registro de Verified Baseline CANONICAL-MEMORY-FOUNDATION-CLOSEOUT

Verified Baseline de un STEP aceptado por el Owner y committed localmente.
Se reutiliza según VERIFIED_BASELINE_REUSE.

```text
BASELINE_ID=GYPPORT-CANONICAL-MEMORY-FOUNDATION-CLOSEOUT-VERIFIED-BASELINE-2026-09-15
BASELINE_PATH=Fabric/Knowledge/00-GYPPORT-UNIVERSE/verification-baselines/GYPPORT_CANONICAL_MEMORY_FOUNDATION_CLOSEOUT_VERIFIED_BASELINE_2026-09-15.md
STEP=GYPPORT_CANONICAL_MEMORY_FOUNDATION_01
PHASE=FINAL_CANONICAL_MEMORY_FOUNDATION_CLOSEOUT_CORRECTION
STATUS=OWNER_ACCEPTED_COMMITTED_LOCAL
ACCEPTED_COMMITS=Fabric=80e7035052492372f99e36e509a3298eab07f784; gypport-engineering-template=74ff60cd6a789083db30488f5ac0f46dbf1cf86b
MIGRATION_HEAD=V58
VERIFIED_FILE_COUNT=2
BASELINE_REUSE_ALLOWED=YES
SUPERSEDES_BASELINE_ID=GYPPORT-CANONICAL-MEMORY-FOUNDATION-VERIFIED-BASELINE-2026-09-15
```


2026-09-15 — GYPPORT® Universe / Reglas de reutilización de la cuenta global entre tenants (PKG-2D)

Una cuenta global GYPPORT no pertenece a un tenant. Puede participar en varios, y la pertenencia la
prueba siempre `user_tenant_memberships`, nunca el tenant de origen de la cuenta. El Owner cierra con
estas decisiones la ambigüedad heredada de `user_accounts.tenant_id` y `user_accounts.party_id`, y
prohibe dejar como deuda futura cualquier problema ya conocido de PKG-2D.

La adopción de una cuenta existente en otro tenant crea acceso, no identidad: solo la membresía y su
evento. La proyección de Party sigue siendo perezosa y explícita, y la realiza el flujo de negocio que
la necesita, nunca seguridad y nunca una lectura.

El inicio de sesión deja de elegir el tenant de origen. Los tenants candidatos son las membresías
ACTIVE: ninguna, el comportamiento actual sin acceso; una, entra directo; varias, el servidor responde
TENANT_SELECTION_REQUIRED y el cliente envía una selección explícita que el servidor verifica contra la
membresía. Un tenant enviado por el cliente nunca se acepta sin esa verificación. El Platform Admin
conserva su sesión PLATFORM sin tenant y sin membresía de cliente.

```text
ADOPTED_MEMBERSHIP_INITIAL_STATUS=ACTIVE
PKG2D_INTRODUCES_INVITATION_WORKFLOW=NO
MULTIPLE_ACTIVE_MEMBERSHIPS_BEHAVIOR=EXPLICIT_TENANT_SELECTION
TENANT_SELECTION_CHOOSER_SESSION=NO
MY_PROFILE_MODEL=GLOBAL_IDENTITY_PLUS_CURRENT_TENANT_CONTEXT
CONTEXTUAL_PARTY_MAY_BE_ABSENT=YES
MEMBERSHIP_ADOPTION_CREATES_PARTY=NO
ADOPTION_CREATES_ACCOUNT=NO
ADOPTION_CREATES_MDM_PARTY=NO
ADOPTION_CREATES_CREDENTIAL=NO
GLOBAL_USER_ACCOUNT_TENANT_OWNED=NO
USER_ACCOUNTS_ORIGIN_COLUMNS=origin_tenant_id,origin_party_id
CURRENT_TENANT_FROM_ORIGIN_TENANT=NO
CURRENT_PARTY_FROM_ORIGIN_PARTY=NO
MVP_USERNAME_MODEL=EMAIL_ALIAS
USERNAME_EQUALS_NORMALIZED_EMAIL=YES
CUSTOM_USERNAME_SUPPORT=NO
GLOBAL_USERNAME_LOOKUP_MATCHES_GLOBAL_UNIQUENESS=YES
EVC_ACCOUNT_REFERENCE_GLOBAL=YES
PRC_ACCOUNT_REFERENCE_GLOBAL=YES
IDENTITY_LINK_ACCOUNT_LOOKUP_GLOBAL=YES
PLATFORM_ADMIN_REQUIRES_CLIENT_MEMBERSHIP=NO
PARTY_PROJECTION_POLICY=LAZY_EXPLICIT
LOGIN_CREATES_PARTY=NO
AUTH_ME_CREATES_PARTY=NO
AUTHORIZATION_READ_CREATES_PARTY=NO
NO_DEFERRED_PKG2D_CLEANUP=YES
KNOWN_ARCHITECTURAL_PROBLEM_IN_CURRENT_SCOPE=FIX_NOW
```


2026-09-16 — GYPPORT® Universe / Registro de Verified Baseline PKG2D-CROSS-TENANT-GLOBAL-ACCOUNT

Verified Baseline de un STEP aceptado por el Owner y committed localmente.
Se reutiliza según VERIFIED_BASELINE_REUSE.

```text
BASELINE_ID=GYPPORT-PKG2D-CROSS-TENANT-GLOBAL-ACCOUNT-VERIFIED-BASELINE-2026-09-16
BASELINE_PATH=Fabric/Knowledge/00-GYPPORT-UNIVERSE/verification-baselines/GYPPORT_PKG2D_CROSS_TENANT_GLOBAL_ACCOUNT_VERIFIED_BASELINE_2026-09-16.md
STEP=GYPPORT_GLOBAL_ACCOUNT_TENANT_MEMBERSHIP_FOUNDATION_15
PHASE=PKG_2D_COMPLETE_CROSS_TENANT_GLOBAL_ACCOUNT_REUSE_AND_ADOPTION
STATUS=OWNER_ACCEPTED_COMMITTED_LOCAL
ACCEPTED_COMMITS=gm-security=d3fa0b470cb117fb5c1620b6860ecc34ad73a50d; Gystigo=d9f3ddecc76d81993168de7536f756c7c4d0a3ac; Fabric=cc194e4d3d63bed4369fbc934ca0695d8fc6a990
MIGRATION_HEAD=V61
VERIFIED_FILE_COUNT=101
BASELINE_REUSE_ALLOWED=YES
```


2026-09-16 — gm-expenses / Reglas de rendición unificada, anticipo activo único y presentación financiera

Decisiones del Owner aceptadas en GM_EXPENSES_FINAL_ADJUSTMENT_V62_04, GM_EXPENSES_UNIFIED_RECONCILIATION_V63_05,
GM_EXPENSES_ONE_ACTIVE_ADVANCE_PER_CASE_CURRENCY_06 y GM_EXPENSES_MVP_FINAL_RELEASE_CONSOLIDATION_07. Completan la
Regla de anticipos, rendición y total justificado del 2026-09-13, que sigue vigente. El detalle canónico vive en
Fabric/Knowledge/gm-expenses/01-domain/GYPPORT_GM_EXPENSES_DOMAIN_BASELINE_v1.0.md.

```text
PLAN_DE_ENTREGA=método de entrega y días para rendir se registran con el anticipo (V62)
PLAN_INMUTABLE_TRAS_CREACION=YES (para cambiarlo se cancela el BORRADOR y se crea otro anticipo)
BORRADOR_ANTERIOR_A_V62=pide método y días en Confirmar entrega, sin valores inventados y sin reescribir filas históricas
RN001=anticipo + reembolsado = justificado + devuelto + ajustes autorizados (V63)
DEVOLUCION_Y_REEMBOLSO_COEXISTEN=YES
REVERSION_AUTOMATICA_DE_DEVOLUCION=NO
UN_ANTICIPO_FINANCIERAMENTE_ACTIVO_POR_EXPEDIENTE_Y_MONEDA=YES
ESTADOS_ACTIVOS=BORRADOR,ENTREGADO,EN_RENDICION,OBSERVADO,RENDIDO
ESTADOS_NO_ACTIVOS=CANCELADO,CERRADO
REGLA_PROSPECTIVA=YES
DATOS_HEREDADOS_MULTI_ANTICIPO=PRESERVAR_Y_SOPORTAR
RESTRICCION_DE_UNICIDAD_EN_BASE_DE_DATOS=NO
FIFO=SOLO_COMPATIBILIDAD_NO_CANONICO
CIERRE_MVP=centrado en el expediente; sin comandos "Cerrar anticipo", "Cerrar rendición" ni "Finalizar anticipo"
```

Mensajes de rechazo del anticipo activo único:

```text
Este expediente ya tiene un anticipo activo en USD. Resuelve el anticipo actual antes de registrar otro.
Este expediente ya tiene otro anticipo activo en USD. Resuelve ese anticipo antes de confirmar esta entrega.
```

La tarjeta del expediente, su detalle y los reportes usan un solo vocabulario financiero. Toda superficie que
muestra una dirección muestra también los movimientos que la explican:
Entregado + Reembolsado = Justificado + Devuelto (+ Ajuste autorizado) + la posición. La dirección es siempre el
saldo del backend: nunca se calcula como Entregado − Usado, y Usado y Justificado no se fusionan.

```text
Entregado · Usado · Justificado · Devuelto · Reembolsado
Por justificar o devolver   saldo mayor que 0
Por reembolsar              saldo menor que 0
Pendiente de conciliar      saldo igual a 0 (USD 0.00); sin anticipo entregado: No aplica
```

Esta regla sustituye la etiqueta "Diferencia USD 0.00" aceptada en GM_EXPENSES_UNIFIED_RECONCILIATION_V63_05. No
se usa "Diferencia" sin contexto, ni "Saldo", ni "Exceso gastado" como obligación de rendición. En un expediente
heredado con varios anticipos, la tarjeta y el resumen muestran la posición neta del expediente y cada anticipo
conserva su propia dirección.


2026-09-16 — GYPPORT® Universe / Regla de migración controlada de Shared DEV y datos heredados

Decisión del Owner en GM_EXPENSES_RUNTIME_REHEARSAL_03 y GM_EXPENSES_MVP_FINAL_RELEASE_CONSOLIDATION_07. Shared
DEV es compartido: se ensaya primero sobre una copia desechable, nunca en su puerto, y la migración real solo se
ejecuta en un STEP que el Owner autoriza expresamente, en este orden.

```text
1  commits controlados de los bytes exactos ensayados y finales
2  respaldo fresco de Shared DEV inmediatamente antes de migrar
3  nueva verificación de la versión Flyway y de los conteos de Shared DEV
4  comparación con la huella de origen del ensayo
5  backend construido DESDE el commit aceptado
6  verificación de los hashes empaquetados
7  migración de Shared DEV
8  reconstrucción o recreación del backend oficial de DEV
9  smoke del Owner con inicio de sesión real
10 solo entonces Shared DEV se declara alineado
```

Los datos heredados de Shared DEV no se reparan en silencio: no se completa historial de revisión, no se cambian
estados de anticipos, no se cancelan borradores y no se borran registros. Su limpieza es un STEP separado
controlado por el Owner. Un tenant sin evidencia del Owner queda UNKNOWN: no se clasifica como prueba ni como real y
sus registros no se limpian.

```text
DATOS_HEREDADOS_SE_REPARAN_EN_SILENCIO=NO
LIMPIEZA_DE_DATOS_HEREDADOS=STEP_SEPARADO_CONTROLADO_POR_EL_OWNER
TENANT_SIN_EVIDENCIA_DEL_OWNER=UNKNOWN
```


2026-09-16 — gm-expenses / Regla de varios anticipos por expediente y barra del expediente cerrado

Decisión del Owner en GM_EXPENSES_CLOSED_PROGRESS_AND_MULTIPLE_ADVANCES_FIX_10. Sustituye, de la entrada
"2026-09-16 — gm-expenses / Reglas de rendición unificada, anticipo activo único y presentación financiera", las
claves del anticipo activo único, sus dos mensajes de rechazo y la clave FIFO. El resto de esa entrada sigue vigente.

```text
VARIOS_ANTICIPOS_POR_EXPEDIENTE=VALIDOS en cualquier número y moneda
EXPEDIENTE=centro de financiamiento y de rendición
ANTICIPOS=tramos de financiamiento del expediente
GASTOS=pertenecen al expediente, nunca a un anticipo
REGISTRO_O_ENTREGA_BLOQUEADOS_POR_OTRO_ANTICIPO=NO
BORRADOR_BLOQUEA=solo el cierre del expediente
REPARTO_POR_ORDEN_DE_ENTREGA=mecanismo para conciliar cada rendición, no política de negocio
```

Lo que esta entrada sustituye de forma explícita:

```text
UN_ANTICIPO_FINANCIERAMENTE_ACTIVO_POR_EXPEDIENTE_Y_MONEDA=YES -> NO
ESTADOS_ACTIVOS, ESTADOS_NO_ACTIVOS, REGLA_PROSPECTIVA, DATOS_HEREDADOS_MULTI_ANTICIPO -> sin efecto
FIFO=SOLO_COMPATIBILIDAD_NO_CANONICO -> REPARTO_POR_ORDEN_DE_ENTREGA (arriba)
"Este expediente ya tiene un anticipo activo en USD. Resuelve el anticipo actual antes de registrar otro." -> retirado
"Este expediente ya tiene otro anticipo activo en USD. Resuelve ese anticipo antes de confirmar esta entrega." -> retirado
```

La tarjeta del expediente tiene una sola barra de avance. Mientras el expediente está abierto, la barra es Uso
(Usado / Entregado). Cuando está cerrado, su ciclo financiero ya se resolvió: la barra es Conciliado, 100 % si no
queda nada por justificar, devolver o reembolsar, y Uso se muestra como una cifra más.

```text
BARRA_EXPEDIENTE_ABIERTO=Uso
BARRA_EXPEDIENTE_CERRADO=Conciliado (100 % sin montos pendientes)
USO_EN_EXPEDIENTE_CERRADO=cifra sin barra
OTRO_AVANCE_NO_MODELADO=no se muestra
```


2026-09-16 — gm-expenses / Regla de rendición a nivel del expediente

Decisión del Owner en GM_EXPENSES_CASE_LEVEL_RENDITION_CANONICALIZATION_11. El expediente es el centro de
financiamiento y de rendición: sus anticipos son tramos de financiamiento, sus gastos le pertenecen y su rendición es
una sola por moneda. El detalle canónico vive en
Fabric/Knowledge/gm-expenses/01-domain/GYPPORT_GM_EXPENSES_DOMAIN_BASELINE_v1.0.md (§5, Case-level rendition).

```text
EXPEDIENTE=centro de financiamiento y de rendición
ANTICIPOS=tramos de financiamiento del expediente (varios, también en la misma moneda)
GASTOS=pertenecen al expediente
RENDICION=del expediente, una por moneda
SALDO_DEL_EXPEDIENTE=entregado + reembolsado - justificado - devuelto - ajustes autorizados
TOTAL_ENTREGADO=suma de los anticipos entregados del expediente
TOTAL_JUSTIFICADO=suma de los gastos APROBADO del expediente (0 mientras no hay anticipo entregado)
FIFO=NO_CANONICO, sin código de compatibilidad
JUSTIFICADO_POR_ANTICIPO=no es verdad de negocio y no se muestra
DEVOLUCION_REEMBOLSO_CONCILIAR=comandos del expediente por moneda; ninguno nombra un anticipo
CONCILIAR=solo con el saldo del expediente igual a 0
V63=se evalúa a nivel del expediente; cada fila técnica conciliada sigue cumpliendo la restricción
FILAS_ADVANCE_SETTLEMENT=portadoras técnicas, invisibles y no autoritativas
API_POR_ANTICIPO_PARA_UN_ANTICIPO_DE_EXPEDIENTE=rechazada, lecturas incluidas
CIERRE=gastos -> comprobantes -> borradores -> observados -> expediente cuadrado -> Conciliar -> Cerrar expediente
CERRAR_EXPEDIENTE_CIERRA=cada fila conciliada y cada anticipo del expediente, en la misma transacción
ANTICIPO_ADICIONAL=solo suma a lo entregado; no reasigna gastos
REPORTES=dirección de cada expediente antes de sumar (+30 y -20 nunca netean a 10)
MIGRACION=NO (V62 y V63 sin cambios)
```

Mensajes:

```text
Hay 1 anticipo en borrador por USD X.XX. Confirma su entrega o cancélalo antes de cerrar el expediente.
Hay N anticipos en borrador por un total de USD X.XX. Confirma su entrega o cancélalos antes de cerrar el expediente.
La rendición del expediente tiene saldo pendiente; registra la devolución o el reembolso y vuelve a conciliar.
Concilia la rendición del expediente antes de cerrarlo.
La rendición de este anticipo se gestiona desde su expediente.
Rendición: Se gestiona desde el expediente
```

Sin anticipo entregado (opción B), la tarjeta y el detalle del expediente muestran ceros (Entregado USD 0.00,
Justificado USD 0.00, Devuelto USD 0.00, Reembolsado USD 0.00, Pendiente de conciliar USD 0.00) y Uso 0 % con la
barra vacía y su riel visible. Uso puede superar 100 %: el texto conserva el porcentaje y solo el relleno se detiene.
Los reportes conservan No aplica.

```text
USO_SIN_ANTICIPO_ENTREGADO=0 % con barra vacía y riel visible
USO_MAYOR_A_100=permitido (texto 110 %, relleno máximo 100 %)
MONTOS_SIN_ANTICIPO_ENTREGADO=ceros en la tarjeta y el detalle; No aplica en los reportes
```

Lo que esta entrada sustituye de forma explícita:

```text
REPARTO_POR_ORDEN_DE_ENTREGA=mecanismo para conciliar cada rendición (2026-09-16, FIX_10) -> sin efecto
FIFO=SOLO_COMPATIBILIDAD_NO_CANONICO (2026-09-16, V63_05) -> FIFO=NO_CANONICO, sin código de compatibilidad
"cada anticipo conserva su propia dirección" (2026-09-16, V63_05 y MVP_07) -> ningún anticipo muestra dirección propia
"Pendiente de conciliar ... sin anticipo entregado: No aplica" en la tarjeta y el detalle -> USD 0.00 (opción B)
"El expediente tiene anticipos en borrador; confirma su entrega o cancélalos." -> mensajes con cantidad y monto
"El Anticipo puede mostrar un resumen informativo de su rendición" (2026-09-13) -> Rendición: Se gestiona desde el expediente
```

Sigue vigente de la regla del 2026-09-13: el Anticipo gestiona su creación, autorización y entrega; el Expediente es el
único lugar de la devolución, el reembolso, la conciliación y el cierre; no existe una acción "Recalcular".


2026-09-17 — gm-expenses / Regla de valores en cero en los reportes

Decisión del Owner en GM_EXPENSES_RUNTIME_REHEARSAL_FINAL_12. Los reportes usan el mismo vocabulario numérico que la
tarjeta y el detalle del expediente. Sin anticipo entregado, los campos de financiamiento se muestran en cero y nunca
como "No aplica" ni "—". Usado conserva el monto real de los gastos. Es una normalización de presentación: el cálculo
y las escrituras financieras no cambian.

```text
REPORTES_SIN_ANTICIPO_ENTREGADO=Entregado USD 0.00 · Usado (monto real) · Justificado USD 0.00 · Devuelto USD 0.00 · Reembolsado USD 0.00 · Pendiente de conciliar USD 0.00
REPORTES_NO_APLICA=NO
REPORTES_GUION=NO
USADO_SIN_ANTICIPO=monto real de los gastos no rechazados ni excluidos
CAMBIO_DE_ESCRITURA_FINANCIERA=NO
```

Lo que esta entrada sustituye de forma explícita:

```text
"Los reportes conservan No aplica." (2026-09-16, CASE_LEVEL_RENDITION_CANONICALIZATION_11) -> ceros numéricos
MONTOS_SIN_ANTICIPO_ENTREGADO=ceros en la tarjeta y el detalle; No aplica en los reportes -> ceros en la tarjeta, el detalle y los reportes
```


2026-09-17 — GYPPORT® Universe / Regla de entorno local sin herencia de Shared DEV

Decisión del Owner en GYPPORT_PRE_COMMIT_ENV_UI_AUDIT_HARDENING_13. Ninguna variable global de Windows, de Usuario o de
Máquina, puede dejar a Shared DEV como datasource por defecto del desarrollo normal: todo lanzador, IDE o
`mvn spring-boot:run` la heredaría sin que nadie lo decida. Las variables de Usuario `SPRING_DATASOURCE_URL`,
`SPRING_DATASOURCE_USERNAME` y `SPRING_DATASOURCE_PASSWORD`, que apuntaban a Shared DEV, se retiraron el 2026-09-17; las
credenciales de Shared DEV siguen solo en el `.env` del compose de DEV, ignorado por git, y en sus contenedores.

```text
DATASOURCE_GLOBAL_DE_WINDOWS_HACIA_SHARED_DEV=PROHIBIDO (Usuario y Máquina)
PROCESO_NUEVO_HEREDA_SHARED_DEV=NO
RUNTIME_LOCAL=configuración explícita del propio proceso
ENV=LOCAL_EDUARDO
DB_HOST=127.0.0.1
DB_PORT=3310
DB_NAME=gypport_runtime_local
CREDENCIALES_DEL_RUNTIME_LOCAL=se leen del contenedor gypport-runtime-local-mysql al iniciar; nunca variables de Windows
EL_LANZADOR_MUESTRA_ANTES_DE_JAVA=ENV, DB_HOST, DB_PORT, DB_NAME (nunca contraseñas)
GUARDIA_OBLIGATORIA=rechaza un datasource con :3308, gypport-mysql-dev o core_business_dev
MENSAJE_DE_RECHAZO=Local runtime refused to start because the datasource points to Shared DEV.
SHARED_DEV=solo en un proceso explícito autorizado por el Owner
```


2026-09-17 — gm-expenses / Regla de indicadores independientes Conciliado y Uso

Decisión del Owner en GYPPORT_PRE_COMMIT_ENV_UI_AUDIT_HARDENING_13. La tarjeta del expediente muestra, por moneda, dos
indicadores independientes con su propio riel compacto, Conciliado y Uso, tanto si el expediente está abierto como
cerrado. Conciliado no inventa un porcentaje intermedio: solo un expediente cerrado sin montos pendientes está conciliado.

```text
INDICADORES_DE_LA_TARJETA=Conciliado y Uso, independientes, cada uno con su barra
CONCILIADO_EXPEDIENTE_CERRADO_SIN_PENDIENTES=100 % con la barra llena
CONCILIADO_EXPEDIENTE_ABIERTO=Pendiente con la barra vacía (sin porcentaje intermedio, nunca un 100 % falso)
CONCILIADO_EXPEDIENTE_CERRADO_CON_MONTO_PENDIENTE=Pendiente con la barra vacía (solo datos heredados)
USO=Usado / Entregado con su valor real (29 %, 87 %, 110 %)
USO_MAYOR_A_100=el texto conserva el porcentaje; el relleno se detiene en 100 %
USO_SIN_ANTICIPO_ENTREGADO=0 % con la barra vacía
PANTALLAS_ANGOSTAS=los dos indicadores lado a lado bajo los montos, sin desborde horizontal
```

Lo que esta entrada sustituye de forma explícita:

```text
"La tarjeta del expediente tiene una sola barra de avance." (2026-09-16, FIX_10) -> dos indicadores independientes
BARRA_EXPEDIENTE_ABIERTO=Uso (2026-09-16, FIX_10) -> Conciliado Pendiente y Uso, cada uno con su barra
BARRA_EXPEDIENTE_CERRADO=Conciliado (100 % sin montos pendientes) (2026-09-16, FIX_10) -> Conciliado 100 % y Uso, cada uno con su barra
USO_EN_EXPEDIENTE_CERRADO=cifra sin barra (2026-09-16, FIX_10) -> Uso con su propia barra
```


2026-09-17 — gm-expenses / Regla de integridad del historial de revisión

Decisión del Owner en GYPPORT_PRE_COMMIT_ENV_UI_AUDIT_HARDENING_13. Un gasto OBSERVADO moderno siempre tiene su evento
OBSERVED inmutable, escrito en la misma transacción que el cambio de estado. El detalle canónico vive en
Fabric/Knowledge/gm-expenses/01-domain/GYPPORT_GM_EXPENSES_DOMAIN_BASELINE_v1.0.md (§4, Review history integrity).

```text
OBSERVADO_REQUIERE_EVENTO_OBSERVED=SI, en la misma transacción
FALLA_AL_ESCRIBIR_EL_HISTORIAL=revierte toda la decisión (mismo estado, misma versión, sin recibo de idempotencia)
ACTOR_DEL_EVENTO=UserAccount global autenticada de la sesión, nunca el responsable ni una Persona
MOMENTO_DEL_EVENTO=reloj del servidor en la solicitud, nunca un valor del cliente
HISTORIAL_DE_REVISION=solo se agrega (los triggers rechazan UPDATE y DELETE)
OBSERVADO_A_RECHAZADO=no existe; el gasto observado se corrige y luego se decide
RECHAZADO=final
OBSERVADO_SIN_EVENTO=solo datos heredados anteriores al historial (antes del 2026-09-03); nunca se fabrica historial
LIMPIEZA_DE_ESOS_DATOS=operación controlada de datos DEV autorizada por el Owner y registrada como evidencia; no es regla del producto
```

Evidencia de limpieza de datos DEV, no regla del producto: el gasto de prueba 5E63494AA2564C1E847CD54A6ED67A51 (tenant 1),
OBSERVADO sin historial desde 2026-08-30, pasó a RECHAZADO solo en la base local aislada 127.0.0.1:3310, el 2026-09-17 a
las 12:55:25 UTC, con una actualización guardada: sin evento de revisión y sin revisor, motivo ni fecha histórica
fabricados. El detalle está en
gm-ai-boxghost/tracks/GM-EXPENSES-RELEASE-READINESS/evidence/PRE-COMMIT-ENV-UI-AUDIT-HARDENING-13-2026-09-17/. Shared DEV
conserva ese registro sin cambios hasta un STEP explícito de limpieza.


2026-09-17 — GYPPORT® Universe / Regla de reutilización de la auditoría existente

Decisión del Owner en GYPPORT_FINAL_PRECOMMIT_AUDIT_AND_UI_ALIGNMENT_14. GYPPORT ya tiene su arquitectura de auditoría y
se reutiliza: la historia semántica de cada dominio más la auditoría global. No se crea una arquitectura paralela, ni
una tabla nueva, ni columnas genéricas como updated_by, ni una V64, solo porque falte un campo. Un vacío bloquea solo si
existe una pregunta real de negocio o de auditoría que la arquitectura actual no responde. El detalle vive en
Fabric/Knowledge/gm-expenses/02-persistence/GYPPORT_GM_EXPENSES_PERSISTENCE_BASELINE_v1.0.md (§10.1) y en el baseline de
dominio (§4).

```text
HISTORIA_DE_DOMINIO=tablas semánticas append-only del módulo (en gm-expenses: expense_review_event, expense_revision_event, expense_advance_assignment_event, settlement_adjustment_event, settlement_balance_event, expense_command_receipt)
AUDITORIA_GLOBAL=audit_logs con el catálogo audit_action_types (V1; clave de actor global desde V58)
AUDITORIA_GLOBAL_REGISTRA=operaciones administrativas o de sistema: contexto de tenant, actor, acción, entidad, antes y después, correlación, momento
EVENTOS_DE_DOMINIO_DUPLICADOS_EN_AUDIT_LOGS=NO
ACTOR_DE_AUDITORIA=UserAccount global del contexto de ejecución, nunca un participante del negocio (responsable, supervisor, empleado, receptor)
ACTOR_NULL_EN_AUDIT_LOGS=evento de sistema (Foundation Register §6.4); nunca se fabrica una cuenta para llenar el campo
REVISION_DE_GASTO=ExpenseRevisionChange con snapshots anterior y nuevo en expense_revision_event, en la misma transacción
OBSERVADO_Y_OBSERVED=atómicos (regla del 2026-09-17, integridad del historial de revisión)
ARQUITECTURA_DE_AUDITORIA_PARALELA=NO
V64_O_COLUMNAS_DE_AUDITORIA_NUEVAS=NO sin un vacío bloqueante probado y aprobación separada del Owner
VACIOS_DE_AUDITORIA_BLOQUEANTES_MVP=NINGUNO
```

Estado verificado el 2026-09-17, sin bloquear el MVP: ningún puerto, servicio o adaptador de la aplicación escribe aún
audit_logs (ADR-0010 sigue PROPOSED) y la tabla no tiene triggers append-only. El primer registro es la auditoría de la
limpieza de datos DEV de GYPPORT_PRE_COMMIT_ENV_UI_AUDIT_HARDENING_13, solo en la copia local 3310: acción
LEGACY_DEV_TEST_DATA_REGULARIZATION, actor NULL y la hora real de la limpieza en new_values.


2026-09-17 — GYPPORT® Universe / Lanzador local canónico versionado

Decisión del Owner en GYPPORT_FINAL_PRECOMMIT_AUDIT_AND_UI_ALIGNMENT_14. Complementa la "Regla de entorno local sin
herencia de Shared DEV" del 2026-09-17: el control de seguridad no puede vivir solo en target/, que `mvn clean` borra.

```text
LANZADOR_LOCAL_CANONICO=Gystigo/platform_os/server/scripts/start-runtime-local.ps1
DETENCION=Gystigo/platform_os/server/scripts/stop-runtime-local.ps1
LANZADORES_LOCALES=uno solo (las copias de target/runtime-local se retiraron)
ESTADO_EN_TARGET=target/runtime-local: jar preparado en app/, logs, access-logs, backend.pid y documentos locales
MVN_CLEAN_BORRA_EL_LANZADOR=NO
SECRETOS_EN_EL_REPOSITORIO=NO (la contraseña se lee del contenedor gypport-runtime-local-mysql al iniciar)
GUARDIA_SHARED_DEV=la misma regla y el mismo mensaje, antes de iniciar Java
```


2026-09-17 — gm-expenses / Regla de ubicación de Conciliado y Uso en la tarjeta

Decisión del Owner en GYPPORT_FINAL_PRECOMMIT_AUDIT_AND_UI_ALIGNMENT_14. Los dos indicadores independientes siguen
siendo correctos; cambia su lugar. Cada uno vive en su región semántica y nunca forman un bloque combinado que cruce el
divisor de Finanzas.

```text
CONCILIADO=indicador del ciclo de vida del expediente, uno por expediente
UBICACION_DE_CONCILIADO=cabecera de la tarjeta, junto al estado Abierto / Cerrado, sobre el divisor
UBICACION_DE_USO=Finanzas, uno por moneda, junto a Entregado, Usado y Justificado, bajo el divisor
CONCILIADO_EXPEDIENTE_CERRADO_SIN_PENDIENTES=100 % con la barra llena (sin pendientes en ninguna moneda)
CONCILIADO_EXPEDIENTE_ABIERTO=Pendiente con la barra vacía
USO_MAYOR_A_100=el texto conserva el porcentaje; el relleno se detiene en 100 %
PANTALLAS_ANGOSTAS=Conciliado sigue bajo el estado en la cabecera; Uso sigue en Finanzas; sin desborde horizontal
```

Lo que esta entrada sustituye de forma explícita:

```text
"La tarjeta del expediente muestra, por moneda, dos indicadores independientes con su propio riel compacto" (2026-09-17, HARDENING_13) -> Conciliado uno por expediente en la cabecera; Uso uno por moneda en Finanzas
PANTALLAS_ANGOSTAS=los dos indicadores lado a lado bajo los montos, sin desborde horizontal (2026-09-17, HARDENING_13) -> Conciliado bajo el estado y Uso en Finanzas
```


2026-09-17 — GYPPORT® Universe / Regla de fin de línea en commits controlados

Decisión del Owner en GM_EXPENSES_MVP_CONTROLLED_COMMIT_GATE_17. Un commit controlado acepta la conversión a LF que
Git aplica según los atributos del repositorio y no agrega una política -text solo para conservar hashes antiguos del
árbol de trabajo con CRLF. El Verified Baseline registra los hashes de los blobs preparados o commiteados.

```text
CONVERSION_GIT_A_LF=ACEPTADA
POLITICA_TEXT_ESPECIAL_PARA_CONSERVAR_CRLF=NO
ARCHIVO_CONVERTIDO=se registra PRE_STAGE_WORKTREE_SHA256, STAGED_BLOB_SHA256 y NORMALIZATION=CRLF_TO_LF
HASHES_DEL_VERIFIED_BASELINE=blobs preparados o commiteados, nunca hashes anteriores del árbol de trabajo
HASHES_DE_EVIDENCIA_HISTORICA=siguen válidos como evidencia anterior a la conversión
REESCRIBIR_EVIDENCIA_PARA_OCULTAR_LA_CONVERSION=NO
EVIDENCIA_BINARIA=se commitea con sus bytes existentes, sin recodificar
```


2026-09-17 — GYPPORT® Universe / Registro de Verified Baseline GM-EXPENSES-MVP-RELEASE

Verified Baseline de un STEP aceptado por el Owner y committed localmente.
Se reutiliza según VERIFIED_BASELINE_REUSE.

```text
BASELINE_ID=GYPPORT-GM-EXPENSES-MVP-RELEASE-VERIFIED-BASELINE-2026-09-17
BASELINE_PATH=Fabric/Knowledge/00-GYPPORT-UNIVERSE/verification-baselines/GYPPORT_GM_EXPENSES_MVP_RELEASE_VERIFIED_BASELINE_2026-09-17.md
STEP=GM_EXPENSES_MVP_CONTROLLED_COMMIT_GATE_17
PHASE=GM_EXPENSES_RELEASE_READINESS_MVP
STATUS=OWNER_ACCEPTED_COMMITTED_LOCAL
ACCEPTED_COMMITS=gm-expenses=545eae0fb287f8e04f7f1b4ac73780304ec53f22; Gystigo=bcb959158b781e3fcd876bacc6fcf0f1f1c79b9f
MIGRATION_HEAD=V63
VERIFIED_FILE_COUNT=132
BASELINE_REUSE_ALLOWED=YES
```

