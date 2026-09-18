# GYPPORT_GM_ACCOUNTING_GENERAL_MODULE_MODEL_EXECUTION_PROMPT_v1.2

```text
PEGAR EN: CHATGPT WORK — MODELO GENERAL CONSOLIDADO DE gm-accounting

Track: GM-ACCOUNTING-GENERAL-MODULE-MODEL-01
Step: CONSOLIDATED GENERAL MODULE MODEL
Mode: READ-ONLY / ANALYSIS / ARCHITECTURE DESIGN / NO DDL / NO IMPLEMENTATION
Agent: CHATGPT WORK
Owner: Eduardo Luis Burgasi Pullaguari
Depends-on: GM-ACCOUNTING-KNOWLEDGE-RECONSTRUCTION-01
Mandatory-input: GYPPORT_ACCOUNTING_HISTORICAL_KNOWLEDGE_BASELINE_v1.0.md
Required-output: GYPPORT_GM_ACCOUNTING_GENERAL_MODULE_MODEL_v0.1.md
Prompt-version: 1.2
Status: OWNER-DIRECTED / READY-FOR-EXECUTION
```

## 1. Propósito

Construye el modelo general funcional, conceptual, modular y de ownership de
`gm-accounting` a partir de la baseline histórica y de todas las fuentes adjuntas.

El resultado debe organizar y reconciliar el conocimiento disponible para definir:

- los submódulos de `gm-accounting`;
- sus responsabilidades y límites;
- los objetos de negocio conceptuales;
- el ownership de cada verdad;
- los flujos entre documentos, obligaciones, fondos, asientos y reportes;
- las reglas contables, operativas, tributarias, de integridad y auditoría;
- la evidencia contable inmutable;
- la custodia y retención de comprobantes;
- la reproducción funcional y versionada de formularios del SRI;
- las contradicciones, vacíos y decisiones todavía reservadas al propietario;
- las condiciones necesarias para autorizar el futuro modelo lógico de datos.

Este Track 02 no es un resumen superficial y tampoco es todavía un modelo de base
de datos. Debe producir el plano general del módulo que permita decidir qué se
modelará posteriormente sin adelantar su traducción relacional.

## 2. Resultado obligatorio

Genera un único documento:

```text
GYPPORT_GM_ACCOUNTING_GENERAL_MODULE_MODEL_v0.1.md
```

El documento debe ser autosuficiente para auditoría, pero no debe copiar íntegramente
la baseline. Debe citar y reconciliar sus identificadores.

No generes archivos alternativos, anexos operativos separados ni enmiendas sueltas.
Si la respuesta excede una entrega, continúa por partes conservando exactamente el
mismo documento, índice e identificadores, y al final entrega una versión consolidada
sin reglas duplicadas.

## 3. Prohibiciones de alcance

No crear todavía:

- tablas;
- nombres físicos de tablas;
- columnas;
- tipos SQL;
- claves primarias;
- claves foráneas;
- índices;
- constraints;
- DDL;
- migraciones Flyway;
- entidades Java;
- repositorios `JdbcTemplate`;
- servicios;
- controladores;
- endpoints;
- contratos API implementables;
- eventos técnicos definitivos;
- código frontend;
- formularios visuales implementados;
- infraestructura de almacenamiento;
- scripts de importación;
- una base de datos separada para el módulo.

Los nombres de información incluidos en este prompt son requisitos conceptuales,
no autorizaciones de columnas ni de diseño físico.

No conviertas una propuesta histórica, un ejemplo, una tabla legacy, una conversación
parcial o una recomendación anterior de IA en decisión vigente sin evidencia.

## 4. Compuerta de entrada obligatoria

Antes de modelar, confirma acceso íntegro a:

```text
GYPPORT_ACCOUNTING_HISTORICAL_KNOWLEDGE_BASELINE_v1.0.md
```

Declara:

```text
BASELINE_ACCESS=FULL|PARTIAL|NONE
BASELINE_VERSION=...
BASELINE_PHASES_AVAILABLE=...
SUPPLEMENTAL_SOURCE_COUNT=...
SUPPLEMENTAL_SOURCE_COVERAGE=FULL|PARTIAL|NONE
```

Si `BASELINE_ACCESS` no es `FULL`, detente y solicita el archivo correcto. No
reconstruyas la baseline desde memoria, resúmenes ni teoría contable general.

Después, inventaría todas las fuentes adjuntas y registra por cada una:

- nombre exacto;
- versión o fecha;
- tipo;
- cobertura;
- nivel de evidencia;
- autoridad;
- integridad de lectura;
- relación con otras versiones;
- temas cubiertos;
- limitaciones;
- estado: vigente, duplicada, histórica, reemplazada, contradictoria o solo
  referencial.

No declares que revisaste todas las conversaciones históricas si únicamente existe
una recuperación parcial.

## 5. Jerarquía de autoridad

Aplica la siguiente precedencia:

1. directiva actual y explícita del propietario;
2. decisión canónica aprobada y vigente;
3. baseline histórica indicada como entrada obligatoria;
4. fuente normativa primaria vigente;
5. archivo primario íntegro adjunto;
6. evidencia técnica verificable;
7. conversación completa recuperada;
8. conversación o memoria parcial;
9. propuesta anterior de IA;
10. inferencia nueva.

Una fuente posterior no reemplaza automáticamente a otra. Usa `SUPERSEDED` solo
cuando exista sustitución real y demostrable. Una corrección de estado, una anulación
o una relación comercial no son por sí mismas versionado documental.

## 6. Etiquetas obligatorias de evidencia y decisión

Clasifica cada conclusión relevante con una o más etiquetas:

```text
[DECISIÓN_DEL_PROPIETARIO]
[CONFIRMADO_EN_BASELINE]
[CONFIRMADO_POR_FUENTE_OFICIAL]
[CONFIRMADO_EN_FUENTE_PRIMARIA]
[CONFIRMADO_EN_EVIDENCIA_TÉCNICA]
[CONFIRMADO_EN_HISTORIAL]
[EJEMPLO_OPERATIVO]
[PROPUESTA_NUEVA]
[INFERENCIA_RAZONABLE]
[DECISIÓN_PENDIENTE]
[REQUIERE_VALIDACIÓN_CONTABLE]
[REQUIERE_VALIDACIÓN_TRIBUTARIA]
[REQUIERE_VALIDACIÓN_LEGAL]
[INFORMACIÓN_NO_ENCONTRADA]
[CONTRADICCIÓN_DETECTADA]
[REGLA_INTERNA_NO_SRI]
[SUPERSEDED]
```

No uses `[CONFIRMADO_EN_BASELINE]` para elementos que la baseline marcó como
`NEW_PROPOSAL`, `PARTIAL`, `OPEN`, `BLOCKED` o pendientes de aprobación.

## 7. Arquitectura heredada

Conserva como contexto vigente, salvo evidencia canónica posterior:

```text
HOST_APPLICATION=GYSTIGO
ARCHITECTURE=MODULAR_MONOLITH
MODULE_RUNTIME=INTERNAL_JAR
INDEPENDENT_PROCESS=NO
INDEPENDENT_PORT=NO
INDEPENDENT_DATABASE=NO
DATABASE=MYSQL_8.4.10
DATA_ACCESS=JDBCTEMPLATE
ORM=NO
BACKEND=JAVA_25.0.4
FRAMEWORK=SPRING_BOOT_4.1.0
MULTITENANCY=SHARED_SCHEMA
TENANT_ISOLATION=tenant_id
OWNER_FINAL_AUTHORITY=EDUARDO_LUIS_BURGASI_PULLAGUARI
```

No diseñes `gm-accounting` como microservicio, aplicación autónoma, contenedor
independiente o base separada. Una modificación de estas condiciones requiere un ADR
y aprobación expresa del propietario.

No dupliques Party Model, personas, organizaciones, usuarios, autenticación, roles,
tenants, establecimientos, sucursales, departamentos o centros de costos compartidos.
Determina qué autoridad externa los posee y cómo `gm-accounting` los referencia.

## 8. Reconciliación obligatoria con Track 01

La baseline contiene identificadores `SRC-`, `HIS-`, `DEC-`, `MOD-`, `ENT-`,
`UC-ACC-`, `RULE-`, `CON-`, `GAP-`, `RPT-`, `QUERY-`, `Q-OWNER-` y `GATE-`.
No los renumeres, recicles ni reutilices con otro significado.

Para los nuevos elementos de Track 02 utiliza:

```text
SUBMOD-ACC-XXXX   submódulo
BOBJ-ACC-XXXX     objeto de negocio
FLOW-ACC-XXXX     flujo funcional
RULE-ACC-XXXX     regla del modelo general
REPORT-ACC-XXXX   salida o reporte
INTEG-ACC-XXXX    frontera de integración
OWNERQ-ACC-XXXX   decisión de ownership o política reservada
```

Para el dominio tributario puede especializarse sin crear un namespace paralelo:

```text
SUBMOD-ACC-TAX-XXXX
BOBJ-ACC-TAX-XXXX
FLOW-ACC-TAX-XXXX
RULE-ACC-TAX-XXXX
OWNERQ-ACC-TAX-XXXX
```

Cada nuevo identificador debe declarar una relación con Track 01:

```text
ADOPTS: <ID Track 01>
REFINES: <ID Track 01>
SPLITS: <ID Track 01>
MERGES: <IDs Track 01>
NEW_WITHOUT_TRACK01_PREDECESSOR
```

Semántica:

- `ADOPTS`: conserva exactamente el significado anterior;
- `REFINES`: añade precisión sin contradecirlo;
- `SPLITS`: separa un elemento anterior en varios objetos o submódulos;
- `MERGES`: demuestra que varios antecedentes representan una sola capacidad;
- `NEW_WITHOUT_TRACK01_PREDECESSOR`: no existe antecedente demostrable y debe
  marcarse como propuesta nueva.

Los números de mensajes, respuestas o intervenciones de esta conversación son solo
trazabilidad de trabajo. No forman parte del namespace canónico.

## 9. Principios funcionales no negociables

El modelo debe preservar estas separaciones:

```text
DOCUMENTO_OPERATIVO != EVIDENCIA_CONTABLE
DOCUMENTO_OPERATIVO != OBLIGACIÓN
OBLIGACIÓN != CUOTA
PAGO_O_COBRO != APLICACIÓN
CONDICIÓN_DE_PAGO != INSTRUMENTO
INSTRUMENTO != MOVIMIENTO_DE_FONDOS
MOVIMIENTO_BANCARIO != CONCILIACIÓN
ASIENTO != MAYOR
MAYOR != SNAPSHOT
SALDO_CALCULADO != SALDO_ALMACENADO
ESTIMACIÓN_TRIBUTARIA != DECLARACIÓN
DECLARACIÓN != OBLIGACIÓN_TRIBUTARIA
OBLIGACIÓN_TRIBUTARIA != PAGO
DECLARACIÓN_ORIGINAL != DECLARACIÓN_SUSTITUTIVA
ANULACIÓN != SUSTITUCIÓN
NOTA_DE_CRÉDITO != NUEVA_VERSIÓN_DE_FACTURA
```

La cadena integral que el modelo debe explicar es:

```text
Hecho económico
→ documento operativo
→ evidencia congelada
→ derecho u obligación
→ subledger CxC/CxP
→ pago o cobro
→ aplicación
→ caja o banco
→ contabilización
→ asiento inmutable
→ mayor
→ saldo o proyección
→ reporte financiero
→ posición tributaria
→ borrador de declaración
→ declaración presentada
→ obligación tributaria
→ pago y conciliación
```

## 10. Submódulos candidatos que deben evaluarse

No asumas que todos pertenecen internamente a `gm-accounting`. Para cada uno define
si es `INTERNAL_SUBDOMAIN`, `INTERNAL_COMPONENT`,
`INTEGRATION_WITH_ANOTHER_MODULE`, `SHARED_PLATFORM_CAPABILITY`,
`REPORTING_CAPABILITY` o `UNRESOLVED`.

Evalúa, como mínimo:

1. Accounting Core y configuración contable;
2. Plan de Cuentas;
3. Periodos y cierres;
4. Libro Diario, contabilización, reversos y ajustes;
5. Libro Mayor y saldos;
6. Cuentas por Cobrar;
7. Cuentas por Pagar;
8. Pagos, cobros, anticipos y aplicaciones;
9. Tesorería y métodos/instrumentos;
10. Bancos y conciliación bancaria;
11. Caja, sesiones, arqueo y cierre;
12. Caja Chica, reposición y liquidación;
13. Costos y dimensiones contables;
14. Retenciones y cumplimiento tributario;
15. Posición tributaria semanal;
16. Formularios y declaraciones del SRI;
17. Operaciones intercompañía;
18. Propietario, patrimonio, aportes y retiros;
19. Reportes financieros;
20. Auditoría y evidencia contable.

Si `GM_Tax_Management`, `gm-e-documents`, Sales, Purchases, POS, Inventory,
Payments, Banking, Party/Core o Audit son autoridades hermanas, conserva esa frontera.
No absorbas sus documentos, reglas o ciclos de vida dentro de `gm-accounting`.

## 11. Ficha obligatoria por submódulo

Para cada `SUBMOD-ACC-XXXX`, documenta:

1. ID y nombre;
2. relación con Track 01;
3. propósito;
4. responsabilidades;
5. exclusiones explícitas;
6. clasificación modular;
7. owner propuesto o confirmado;
8. tenant y entidad legal aplicables;
9. objetos de negocio propios;
10. objetos externos consumidos;
11. entradas;
12. salidas;
13. flujos en los que participa;
14. reglas esenciales;
15. estados conceptuales;
16. eventos de negocio conceptuales;
17. reportes y consultas;
18. integraciones;
19. evidencia y auditoría;
20. dependencia normativa;
21. contradicciones y vacíos;
22. preguntas del propietario;
23. estado de definición;
24. condición para avanzar al modelo lógico.

## 12. Ficha obligatoria por objeto de negocio

Para cada `BOBJ-ACC-XXXX`, documenta sin traducirlo a tabla:

1. ID y nombre;
2. relación con Track 01;
3. definición semántica;
4. owner de la verdad;
5. alcance tenant/entidad legal;
6. origen;
7. ciclo de vida conceptual;
8. mutabilidad;
9. relaciones con otros objetos;
10. invariantes;
11. evidencia requerida;
12. auditoría mínima;
13. integraciones;
14. clasificación de evidencia;
15. decisiones pendientes;
16. estado.

No confundas un objeto conceptual con una tabla. No conviertas cada objeto en una
entidad persistente sin análisis posterior.

## 13. Ownership obligatorio

Construye una matriz con:

```text
CAPACIDAD | VERDAD | OWNER | CONSUMIDORES | MUTABILIDAD |
INTEGRACIÓN | EVIDENCIA | DECISIÓN PENDIENTE
```

Como mínimo, resuelve o registra como `OWNERQ-ACC`:

- quién posee el documento de venta;
- quién posee el documento de compra;
- quién posee el XML firmado y autorizado;
- quién conserva la evidencia contable congelada;
- quién crea CxC y CxP;
- quién registra pagos y cobros;
- quién aplica pagos a obligaciones;
- quién posee movimientos bancarios;
- quién confirma conciliaciones;
- quién posee sesiones y cierres de caja;
- quién genera y contabiliza asientos;
- quién conserva el mayor;
- quién define formularios tributarios normativamente;
- quién mantiene su representación interna versionada;
- quién calcula la posición tributaria;
- quién posee la declaración presentada;
- quién genera la obligación tributaria;
- quién registra y concilia su pago;
- quién administra retención y legal hold.

La autoridad normativa de formularios ecuatorianos es el SRI. El modelo interno no
puede presentarse como definición jurídica propia de GYPPORT.

Reconcilia expresamente la decisión histórica de que Accounting, Tax Management y
Electronic Documents son autoridades hermanas con el requerimiento actual de incluir
la experiencia tributaria dentro del modelo general. Si la propiedad interna de los
formularios o cálculos continúa ambigua, crea `OWNERQ-ACC-TAX` y no dupliques la
capacidad.

## 14. Libro Diario, contabilización e inmutabilidad

El modelo debe definir conceptualmente:

- asiento borrador;
- asiento contabilizado;
- líneas del asiento;
- origen;
- evidencia;
- contabilización automática;
- asiento manual autorizado;
- reverso;
- ajuste;
- reclasificación;
- relación entre asiento original y reverso;
- periodo contable;
- bloqueo y reapertura autorizada;
- idempotencia del origen;
- auditoría de aprobación.

Reglas obligatorias:

```text
POSTED_ENTRY_MUTABLE=NO
POSTED_ENTRY_DELETABLE=NO
CORRECTION_METHOD=REVERSAL_OR_NEW_ADJUSTING_ENTRY
DOUBLE_ENTRY_VALIDATION_REQUIRED=YES
SOURCE_TRACEABILITY_REQUIRED=YES
```

Un asiento manual puede existir únicamente bajo una política explícita que determine:

- actores autorizados;
- motivo;
- evidencia mínima;
- aprobación;
- periodo permitido;
- materialidad;
- auditoría;
- reversión.

No presentes un asiento manual autorizado como asiento “sin evidencia”. Su evidencia
puede ser una orden, memoria de cálculo, acta, conciliación, soporte interno o aprobación,
según política validada.

## 15. CxC, CxP, pagos y aplicaciones

El modelo debe soportar:

- obligaciones independientes del documento operativo;
- cuotas y vencimientos;
- débitos y créditos;
- pagos parciales;
- pagos mixtos;
- cobros parciales;
- anticipos;
- aplicaciones parciales o múltiples;
- devoluciones;
- notas de crédito y débito;
- reversos;
- sobreaplicaciones y saldos no aplicados;
- conciliación con caja y banco;
- trazabilidad al asiento.

No utilices un único estado de factura como verdad del saldo. No reescribas
silenciosamente CxC/CxP cuando el documento cambia. Cualquier corrección debe quedar
explicada por objetos y eventos trazables.

## 16. Evidencia contable inmutable

Modela una capacidad de evidencia congelada que preserve exactamente la información
usada para reconocer, contabilizar, revertir o auditar un hecho económico.

La separación mínima de ownership es:

```text
SALES_OR_PURCHASES_OWNER=OPERATIONAL_DOCUMENT
GM_E_DOCUMENTS_OWNER=SIGNED_XML_SIGNATURE_AND_AUTHORIZATION
GM_ACCOUNTING_OWNER=ACCOUNTING_EVIDENCE_USED_FOR_POSTING
```

Esta clasificación no autoriza duplicación automática. Debe reconciliarse con las
políticas de custodia siguientes.

La evidencia conceptual debe poder identificar, como categorías de información:

- tenant y entidad legal;
- módulo y documento fuente;
- tipo e identidad estable del documento;
- clave de acceso y autorización cuando correspondan;
- fecha de emisión y autorización;
- estado documental en el momento de captura;
- emisor y receptor;
- moneda y totales relevantes;
- desglose tributario utilizado;
- hash criptográfico;
- referencia de almacenamiento;
- fecha, actor y motivo de captura;
- evento contable;
- asiento relacionado;
- política de retención aplicada;
- legal hold;
- versión o sucesión de la instantánea.

Son requisitos de información, no columnas aprobadas.

Una evidencia utilizada para contabilizar:

- no se sobrescribe;
- no se sincroniza mediante `UPDATE` destructivo;
- no cambia si el documento operativo cambia posteriormente;
- puede ser sucedida por otra instantánea sin alterar la anterior;
- mantiene trazabilidad hacia el documento y asiento correspondientes.

Evalúa estas políticas:

### POLICY_A_REFERENCE_AND_HASH

`gm-accounting` conserva referencia, hash y metadatos. Solo es admisible si
`gm-e-documents` garantiza contractualmente conservación legal, disponibilidad,
integridad, respaldo, recuperación, exportación, preservación tras anulación y
continuidad aunque el módulo cambie o se desactive.

Si no existe evidencia de esas garantías:

```text
POLICY_A_STATUS=NO_APROBADA_SIN_GARANTÍA_DE_CUSTODIA
```

### POLICY_B_ACCOUNTING_EVIDENCE_COPY

`gm-accounting` conserva una copia inmutable del XML y metadatos exactamente usados
al contabilizar. Esta copia es evidencia contable, no documento operativo ni nueva
autoridad tributaria.

### POLICY_C_IMMUTABLE_EVIDENCE_VAULT

Un componente especializado conserva la evidencia inmutable y los módulos la
referencian. Deben definirse ownership, SLA, aislamiento, cifrado, versionado,
exportación, respaldo, recuperación, auditoría y legal hold.

Crea una `OWNERQ-ACC` para seleccionar la política, el momento de captura, el nivel
de detalle, la retención, la exportación y la integración con `gm-e-documents`.

## 17. Estados, anulación y relaciones documentales

Separa obligatoriamente:

```text
DOCUMENT_STATUS
DOCUMENT_RELATION
ACCOUNTING_EFFECT
JOURNAL_ENTRY_STATUS
```

### 17.1 Estado del mismo documento

`CANCELLED` es un estado o evento del mismo comprobante. Una anulación:

- no crea automáticamente un sustituto;
- no elimina la evidencia histórica;
- no permite editar el original;
- conserva fecha, motivo, actor, origen y evidencia;
- puede producir consecuencias contables independientes.

No utilices `REPLACED` ni `SUPERSEDED` como sinónimo de `CANCELLED`.

### 17.2 Documentos tributarios independientes

Una nota de crédito:

- es otro documento;
- tiene identidad, autorización y ciclo de vida propios;
- no es una versión de la factura;
- no sobrescribe el original;
- afecta total o parcialmente sus consecuencias económicas;
- produce su propio efecto contable.

Trata `CREDIT_NOTE_FOR`, `DEBIT_NOTE_FOR` y `WITHHOLDING_FOR` como relaciones
candidatas sujetas a validación por tipo documental y normativa vigente.

### 17.3 Trazabilidad interna

Cuando el negocio necesite relacionar una reemisión sin afirmar un efecto legal del
SRI, usa conceptos como:

```text
REISSUED_AFTER
BUSINESS_REISSUANCE_OF
INTERNAL_SUCCESSOR_OF
```

con:

```text
LEGAL_OR_TAX_EFFECT=NONE
RELATION_SCOPE=INTERNAL_TRACEABILITY
SRI_DEFINED_RELATION=NO
```

### 17.4 Efecto contable

Si el documento se anula antes de contabilizar, define la política para cancelar el
borrador. Si ya existe un asiento contabilizado, conserva el asiento y genera el
reverso o ajuste correspondiente. Nunca elimines ni edites sus líneas contabilizadas.

## 18. Retención legal y custodia

Registra la siguiente matriz normativa como punto de partida verificado para Ecuador:

```text
ARTICLE_41:
RULE=MINIMUM_RETENTION_7_YEARS
START_BASIS=NOT_SPECIFIED
SCOPE=GENERAL

ARTICLE_42:
RULE=MINIMUM_RETENTION_7_YEARS_FROM_ISSUANCE
START_BASIS=ISSUANCE_DATE
SCOPE=EXPRESSLY_AUTHORIZED_NO_COPY_SCENARIO
PROMOTABLE_TO_GENERAL_RULE=NO

ARTICLE_50:
RULE=ANNULLED_DOCUMENT_RETENTION_7_YEARS
ORIGINAL_AND_COPIES_REQUIRED=YES
CHRONOLOGICAL_ORDER_REQUIRED=YES
START_BASIS=NOT_SPECIFIED
PRIMARY_SOURCE=REGULATION_ARTICLE_50
```

Fuente primaria inicial:

```text
Reglamento de Comprobantes de Venta, Retención y Documentos Complementarios
https://www.sri.gob.ec/o/sri-portlet-biblioteca-alfresco-internet/descargar/fc9f2c55-fc0d-41d1-a834-797b202b4d11/Reglamento_comprobantes_ventaydc_ultima%20modificacion_09022024.pdf
```

La Resolución `NAC-DGERCGC25-00000014` regula el procedimiento vigente de anulación
electrónica dentro de su ámbito; no la presentes como fuente primaria de la regla
general de conservación de siete años.

Reglas del modelo:

```text
LEGAL_RETENTION_MINIMUM_YEARS=7
ELECTRONIC_MAGNETIC_ARCHIVE_REQUIRED=YES
GENERAL_RETENTION_START_BASIS=REQUIRES_CURRENT_LEGAL_AND_TAX_VALIDATION
AUTO_PURGE=NO
PURGE_REQUIRES_EXPLICIT_AUTHORIZATION=YES
LEGAL_HOLD_OVERRIDES_PURGE=YES
RETENTION_POLICY_MUST_BE_VERSIONED=YES
```

Si se usa la fecha de emisión como referencia provisional fuera del alcance expreso
del artículo 42:

```text
CLASSIFICATION=INFERENCIA_RAZONABLE
LEGAL_CONFIRMATION=NO
PURGE_ELIGIBILITY_DERIVED_FROM_INFERENCE=NO
```

No inventes otra fórmula general de cómputo. No autorices borrado con una inferencia.
Permite conservar más tiempo por auditoría, declaración, proceso administrativo,
litigio, contrato o legal hold.

## 19. Formularios SRI y posición tributaria

El requerimiento de producto es:

> No espere al cierre mensual para saber cuánto debe pagar. GYPPORT calcula
> semanalmente su posición tributaria, identifica saldos a favor, documentos
> pendientes, inconsistencias y oportunidades legales de optimización.

La solución no debe copiar únicamente la apariencia de un formulario. Debe modelar
conceptualmente y mediante metadatos versionados:

- definición de formulario;
- versión;
- vigencia;
- régimen y tipo de contribuyente;
- periodicidad;
- secciones;
- casilleros;
- concepto tributario canónico;
- mapeo concepto-casillero;
- regla de cálculo;
- validación y dependencia;
- periodo tributario;
- posición tributaria estimada;
- borrador de declaración;
- valores del borrador;
- ajuste manual autorizado;
- revisión y aprobación;
- presentación;
- acuse o comprobante;
- obligación tributaria;
- pago y aplicación;
- saldo a favor o arrastre;
- conciliación;
- evidencia.

Estos son objetos conceptuales candidatos, no tablas ni campos aprobados.

El modelo debe permitir que un concepto tributario cambie de casillero entre versiones
sin perder continuidad histórica.

### 19.1 Compuerta de fuente obligatoria

Antes de modelar un casillero o fórmula específicos, declara:

```text
FORM_STRUCTURE_SOURCE_CLASS=
NORMATIVE_ACT|OFFICIAL_SRI_FORM_GUIDE_OR_SCHEMA|SECONDARY_SOURCE|NOT_FOUND

FORM_STRUCTURE_SOURCE_STATUS=
CONFIRMED_PRIMARY|SECONDARY_PENDING_VALIDATION|NOT_FOUND
```

Registra formulario, versión, vigencia, fuente oficial, norma, guía o esquema,
fecha de publicación y verificación, casilleros cubiertos, reglas cubiertas y vacíos.

Si la fuente es secundaria, solo permite inventario preliminar no canónico. Si no se
encuentra fuente:

```text
FORM_SPECIFIC_FIELD_MODELING=BLOCKED
FORM_SPECIFIC_RULE_MODELING=BLOCKED
READY_FOR_LOGICAL_DATA_MODEL=NO
```

Fuente oficial inicial para la estructura funcional de IVA:

```text
Guía para el llenado del Formulario de Impuesto al Valor Agregado
https://www.sri.gob.ec/o/sri-portlet-biblioteca-alfresco-internet/descargar/e084fae5-9677-450c-8161-21e7c3a9f65b/Gu%C3%ADa%20para%20el%20llenado%20del%20Formulario%20Impuesto%20al%20Valor%20Agregado%20IVA.PDF
```

Una guía oficial puede explicar el uso de casilleros, pero cada regla con efecto
tributario debe mantener también el fundamento normativo aplicable.

### 19.2 Trazabilidad de casilleros

Cada valor debe poder explicar conceptualmente:

- concepto tributario;
- versión de formulario;
- fórmula y regla;
- fuente normativa;
- documentos incluidos;
- XML y evidencia;
- asientos y líneas de origen;
- documentos excluidos;
- ajustes manuales;
- autor y aprobación;
- momento de cálculo;
- tenant, entidad y periodo;
- estado estimado, revisado o declarado.

### 19.3 Posición semanal

Debe contemplar, al menos:

- ventas y compras acumuladas;
- IVA generado y pagado;
- crédito tributario;
- retenciones efectuadas y recibidas;
- saldos a favor anteriores;
- documentos pendientes, anulados o sin autorización;
- inconsistencias;
- impuesto proyectado;
- variación frente al periodo anterior.

Clasificación:

```text
TAX_POSITION_TYPE=ESTIMATE
ESTIMATE_IS_OFFICIAL_RETURN=NO
```

### 19.4 Declaración e inmutabilidad

Estados conceptuales candidatos:

```text
DRAFT
CALCULATED
UNDER_REVIEW
APPROVED
READY_TO_FILE
FILED
ACCEPTED
REJECTED
AMENDED
```

`FILED` y `ACCEPTED` requieren evidencia externa verificable del SRI.

Una sustitutiva es una declaración independiente. Conserva la original, sus valores,
evidencia y obligación; usa una relación conceptual como `AMENDS/AMENDED_BY` y no
un `UPDATE` destructivo.

### 19.5 Salvaguarda visual

Todo borrador debe mostrar permanentemente:

```text
PREPARADO POR GYPPORT — NO PRESENTADO ANTE EL SRI
```

Mientras no exista evidencia externa:

- no simular `FILED` o `ACCEPTED`;
- no simular número de declaración;
- no simular acuse, sello, QR o confirmación oficial;
- no utilizar una apariencia confundible con un comprobante emitido por el SRI.

La interfaz futura puede reproducir funcionalmente secciones, casilleros,
instrucciones, cálculos, validaciones y navegación, pero debe preservar:

```text
GYPPORT_TAX_RETURN_DRAFT != SRI_OFFICIAL_FILING_RECEIPT
```

## 20. Flujos obligatorios

Documenta con `FLOW-ACC-XXXX`, como mínimo:

1. venta de contado;
2. venta a crédito;
3. venta con pago mixto;
4. cobro parcial y aplicación;
5. anticipo de cliente y aplicación;
6. nota de crédito de venta;
7. compra de contado;
8. compra a crédito;
9. retención practicada;
10. pago parcial a proveedor;
11. anticipo a proveedor y aplicación;
12. nota de crédito de compra;
13. apertura, movimiento, arqueo y cierre de caja;
14. depósito de efectivo en banco;
15. movimiento bancario y conciliación;
16. contabilización automática;
17. asiento manual autorizado;
18. reverso y ajuste;
19. cierre y reapertura de periodo;
20. anulación de documento antes y después de contabilizar;
21. captura y sucesión de evidencia;
22. cálculo semanal de posición tributaria;
23. borrador, revisión, presentación y sustitutiva;
24. obligación tributaria, pago y conciliación;
25. préstamo intercompañía, intereses y pago, si existe evidencia suficiente.

Por cada flujo indica actores, trigger, precondiciones, entradas, objetos, pasos,
alternativas, excepciones, estados, owner, evidencia, efecto contable, efecto
tributario, integraciones, idempotencia conceptual y preguntas pendientes.

No inventes asientos modelo cuando la baseline exige validación del contador.

## 21. Reglas, reportes y consultas

Consolida las reglas de Track 01 sin renumerarlas y crea nuevas `RULE-ACC` solo cuando
aporten una precisión real.

Clasifica reglas como:

- contables;
- operativas;
- tributarias;
- integridad;
- ownership;
- auditoría;
- seguridad;
- retención;
- reportes.

Para reglas legales registra jurisdicción, norma, disposición, publicación, vigencia,
fuente oficial, fecha de verificación, interpretación y estado de validación.

Modela conceptualmente reportes financieros, operativos y tributarios, incluyendo:

- diario;
- mayor;
- balance de comprobación;
- estado de situación financiera;
- estado de resultados;
- flujo de efectivo;
- auxiliares CxC/CxP;
- antigüedad de saldos;
- conciliación bancaria;
- cierre de caja;
- posición tributaria semanal;
- conciliación formulario-contabilidad;
- borrador de formulario;
- trazabilidad de casillero;
- auditoría de evidencia y asientos.

No diseñes SQL ni índices en este track.

## 22. Contradicciones, vacíos y decisiones del propietario

No cierres silenciosamente `CON-`, `GAP-`, `Q-OWNER-` o `GATE-` de la baseline.

Para cada contradicción indica:

- posiciones;
- fuentes;
- autoridad;
- impacto;
- resolución propuesta;
- decisión requerida;
- si la directiva actual la resuelve o continúa abierta.

Para cada vacío indica:

- información faltante;
- por qué importa;
- riesgo;
- fuente necesaria;
- owner de la decisión;
- qué parte del Track 03 bloquea.

Agrupa las nuevas preguntas bajo `OWNERQ-ACC-XXXX` sin reemplazar las
`Q-OWNER-XXXX` existentes.

Como mínimo, el propietario debe decidir o aceptar explícitamente:

- ownership definitivo;
- catálogo de submódulos;
- catálogo de objetos;
- política de evidencia A/B/C;
- momento de captura;
- nivel de detalle;
- custodia y exportación;
- retención y legal hold;
- integración con `gm-e-documents`;
- contrato con Sales/Purchases/Tax/Payments/POS/Banking;
- política de asientos manuales;
- política de periodos y reversos;
- moneda, precisión y redondeo;
- alcance de formularios SRI;
- owner de actualización normativa;
- condiciones para una futura purga autorizada.

## 23. Estructura obligatoria del documento de salida

El documento debe contener, en este orden:

1. portada y metadatos;
2. resumen ejecutivo;
3. declaración de acceso y cobertura;
4. inventario y autoridad de fuentes;
5. reglas de precedencia y reconciliación;
6. delta Track 01 → Track 02;
7. mapa general de dominios y fronteras;
8. catálogo de submódulos;
9. catálogo de objetos de negocio;
10. matriz de ownership;
11. cadena integral de negocio y datos;
12. catálogo de flujos;
13. reglas contables y operativas;
14. evidencia contable inmutable;
15. estados y relaciones documentales;
16. retención legal y custodia;
17. formularios SRI y posición tributaria;
18. reportes y consultas conceptuales;
19. contradicciones y vacíos;
20. preguntas del propietario;
21. criterios de aceptación;
22. estado final y recomendación.

## 24. Control de calidad obligatorio

Antes de cerrar, verifica:

- todo `SUBMOD-ACC` y `BOBJ-ACC` tiene relación con Track 01 o está marcado como
  nuevo;
- no se renumeraron IDs de la baseline;
- no se filtraron números de conversación al namespace canónico;
- no se crearon tablas, columnas, PK, FK, DDL ni migraciones;
- no se duplicó Party/Core;
- no se creó una base o servicio independiente;
- el documento operativo conserva su owner;
- el XML conserva su owner;
- la evidencia contable no se sobrescribe;
- `CANCELLED` no significa `SUPERSEDED`;
- una nota de crédito no es versión de factura;
- la reemisión interna no se presenta como figura del SRI;
- los asientos contabilizados no se modifican ni eliminan;
- CxC/CxP no se reescribe silenciosamente;
- pagos y aplicaciones están separados;
- la política de retención general no inventa su fecha inicial;
- el artículo 42 no fue generalizado;
- ninguna inferencia habilita purga;
- los formularios son versionados por metadatos;
- los casilleros específicos tienen compuerta de fuente;
- `FILED/ACCEPTED` requieren evidencia real;
- el borrador GYPPORT no imita un acuse oficial;
- las decisiones contables y tributarias pendientes continúan visibles;
- Track 03 no se autoriza implícitamente.

## 25. Matriz final obligatoria

Emite al final:

```text
TRACK=GM-ACCOUNTING-GENERAL-MODULE-MODEL-01
OUTPUT_FILE=GYPPORT_GM_ACCOUNTING_GENERAL_MODULE_MODEL_v0.1.md
BASELINE_ACCESS=FULL|PARTIAL|NONE
SOURCE_COVERAGE=FULL|PARTIAL
TRACK01_RECONCILIATION=PASS|FAIL|CONDITIONAL
SUBMODULE_CATALOG_STATUS=COMPLETE|PARTIAL|BLOCKED
BUSINESS_OBJECT_CATALOG_STATUS=COMPLETE|PARTIAL|BLOCKED
OWNERSHIP_STATUS=APPROVED|PARTIAL|UNRESOLVED
EVIDENCE_POLICY_STATUS=APPROVED|PARTIAL|UNRESOLVED
SRI_FORM_CAPABILITY_STATUS=COMPLETE|PARTIAL|BLOCKED
FORM_STRUCTURE_SOURCE_STATUS=CONFIRMED_PRIMARY|SECONDARY_PENDING_VALIDATION|NOT_FOUND|MIXED
RETENTION_MINIMUM_YEARS_CONFIRMED=YES
GENERAL_RETENTION_START_BASIS_CONFIRMED=YES|NO
ARTICLE_42_GENERALIZED=NO
AUTO_PURGE_ALLOWED=NO
LEGAL_HOLD_SUPPORTED=YES|NO|PENDING
DOCUMENT_MUTABILITY_POLICY_DEFINED=YES|NO
CANCELLATION_MODELED_AS_UPDATE=NO
CREDIT_NOTE_MODELED_AS_SEPARATE_DOCUMENT=YES|NO
POSTED_ENTRY_MUTABLE=NO
POSTED_ENTRY_WITHOUT_SOURCE_EVIDENCE=0_EXCEPT_AUTHORIZED_MANUAL_ENTRIES_WITH_INTERNAL_EVIDENCE
MANUAL_ENTRY_SUPPORT_POLICY_DEFINED=YES|NO
CXC_CXP_SILENT_REWRITE_ALLOWED=NO
EVIDENCE_STORAGE_POLICY_DECIDED_OR_REGISTERED_AS_OWNER_QUESTION=YES|NO
UI_SAFEGUARD_REQUIREMENT_STATUS=DEFINED|PARTIAL|MISSING
UNRESOLVED_CONTRADICTION_COUNT=...
UNRESOLVED_GAP_COUNT=...
OWNER_QUESTION_COUNT=...
IMPLEMENTATION_AUTHORIZED=NO
LOGICAL_MODEL_AUTHORIZED=NO
READY_FOR_LOGICAL_MODEL=YES|NO|CONDITIONAL
```

Si `READY_FOR_LOGICAL_MODEL=CONDITIONAL`, enumera exactamente las decisiones que
faltan. Si cualquier elemento crítico de ownership, evidencia, retención, formularios,
ledger, moneda o contratos permanece sin definir, no declares `YES`.

## 26. Condición de salida

El Track 03 solo podrá iniciarse después de:

1. auditoría independiente del documento resultante;
2. resolución o aceptación explícita de los bloqueos críticos;
3. aprobación del propietario;
4. autorización separada para `GM-ACCOUNTING-LOGICAL-DATA-MODEL-01`.

La aprobación de este prompt no aprueba DDL ni implementación.

## 27. Instrucción de inicio

Comienza por la compuerta de entrada de la Sección 4. Después inventaría las fuentes,
declara cobertura y presenta un índice propuesto del documento de salida.

No modeles submódulos ni objetos hasta haber confirmado:

```text
BASELINE_ACCESS=FULL
```

Estado inicial:

```text
GM_ACCOUNTING_GENERAL_MODULE_MODEL=IN_PROGRESS
TRACK_03_STATUS=BLOCKED_PENDING_TRACK_02_AUDIT_AND_OWNER_APPROVAL
```

