# GYPPORT® — Reglas Canónicas de Arquitectura, Dominio y UIX

**Estado:** Documento de trabajo canónico  
**Propósito:** Consolidar las reglas arquitectónicas, de identidad, modularidad, trazabilidad y navegación UIX acordadas para GYPPORT antes de seguir ampliando módulos y flujos.

---

## 1. Principio general

GYPPORT debe crecer como un **ERP SaaS modular**, evitando duplicación de datos, módulos “cajón de sastre” y navegación que tenga que rehacerse cada vez que aparezca una nueva capacidad.

Regla base:

> **Un dato maestro, estable y reutilizado por distintos contextos debe tener una única identidad canónica y un único propietario. Los demás dominios lo referencian; no lo duplican como otra fuente de verdad.**

Esto aplica a conceptos como:

- Person
- Organization
- Employee
- UserAccount
- Role
- Permission
- Vehicle
- Department
- CostCenter
- otros maestros o entidades estables

No aplica automáticamente a cualquier campo simple. Un valor como `color = AMARILLO` no necesita una entidad propia salvo que exista una razón real de dominio para darle identidad y ciclo de vida.

---

## 2. Identidad canónica y reutilización

Los datos se capturan una sola vez y luego se reutilizan desde distintos contextos.

```text
Person #125
    ├── puede ser Owner
    ├── puede ser Employee
    ├── puede ser Driver
    ├── puede ser Customer
    └── puede tener UserAccount
```

No deben existir cinco personas distintas por cinco contextos distintos.

### Regla de referencia

```text
gm-entities
Person #125
      ↓
gm-human-resources
Employee #72
      ↓
gm-security
UserAccount #84
      ↓
Role #7
      ↓
Permission #19
```

Los módulos consumidores deben referenciar IDs canónicos y no recrear nombres, códigos o entidades como otra fuente de verdad.

---

## 3. Fronteras canónicas de módulos

### 3.1 `gm-entities`

Responsabilidad:

> **Quién existe.**

Propietario de identidad maestra:

- Person
- Organization/Party
- identificadores
- relaciones MDM
- identidad transversal

Una Persona puede luego participar en muchos contextos sin duplicarse.

### 3.2 `gm-organizations`

Responsabilidad:

> **Cómo está estructurada una organización.**

Ejemplos:

- Departments
- Cost Centers
- Branches
- Establishments
- Organization Settings
- estructura organizativa

RRHH puede asignar empleados a estas estructuras, pero no debe duplicarlas ni convertirse en su dueño.

### 3.3 `gm-human-resources`

Responsabilidad:

> **Qué relación laboral tiene una Persona con una organización.**

Ejemplos:

- Employee
- Employment
- Position / Puesto
- fecha de ingreso
- fecha de salida
- estado laboral
- supervisor
- movimientos laborales
- asignaciones del empleado

Regla:

```text
Person ≠ Employee
```

`Employee` referencia a una `Person` canónica de `gm-entities`.

### 3.4 `gm-security`

Responsabilidad:

> **Quién puede entrar a GYPPORT y qué puede hacer.**

Propietario canónico de:

- UserAccount / identidad de acceso
- OrganizationAccess / membresía de acceso
- Roles
- Permissions
- UserRole
- RolePermission
- Scopes
- políticas y consultas de autorización

Regla:

```text
Employee ≠ UserAccount
```

Puede existir `Person + Employee` sin acceso al ERP. También puede existir `Person + UserAccount` sin relación laboral.

### 3.5 Gystigo

Gystigo debe actuar principalmente como **Host/orquestador**.

Puede conservar infraestructura técnica como:

- Spring Security
- SecurityFilterChain
- JWT
- sesiones
- cookies
- CORS
- CSRF
- filtros HTTP
- adapters HTTP
- wiring de beans
- infraestructura de runtime

La infraestructura técnica no implica ownership del dominio.

```text
gm-security
= qué acceso tiene el usuario

Gystigo
= cómo se aplica técnicamente ese acceso
```

### 3.6 `gm-configurations`

Responsabilidad:

> **Configuración reusable de GYPPORT y composición de superficies administrativas.**

Debe existir como módulo reutilizable, pero no convertirse en un “God Module”.

Puede organizar:

- preferencias
- parámetros
- configuración por tenant
- configuración por módulo
- integraciones
- seguridad configurable
- superficies administrativas reutilizables

Pero los datos siguen perteneciendo a sus dominios reales.

---

## 4. Trazabilidad canónica

La cadena que GYPPORT debe preservar es:

```text
Person
  ↓
Employee (si aplica)
  ↓
UserAccount (si tiene acceso)
  ↓
OrganizationAccess
  ↓
Roles
  ↓
Permissions
  ↓
Scopes
  ↓
Audit Actor
```

La auditoría debe poder responder:

- qué persona actuó
- con qué cuenta
- dentro de qué tenant u organización
- con qué permisos
- sobre qué recurso
- en qué momento
- con qué resultado

Mover ownership de código entre módulos **no obliga a recrear registros ni cambiar IDs**.

---

## 5. Ownership lógico vs ubicación física de tablas

GYPPORT usa un esquema compartido multitenant.

Tablas como:

```text
user_accounts
roles
permissions
user_roles
organization_access
employees
fleet_vehicle
...
```

pueden permanecer físicamente en la misma base.

Cambiar ownership significa que cambia el módulo responsable del dominio y de sus invariantes, no que se copien o renombren necesariamente las tablas.

Regla:

> **No mover ni renombrar físicamente tablas solo para demostrar ownership.**

Solo se debe migrar estructura cuando exista una necesidad técnica real.

---

## 6. Puesto de RRHH vs Rol de seguridad

No son lo mismo.

```text
PUESTO
= función laboral

ROL
= capacidad funcional dentro de GYPPORT

PERMISO
= operación concreta autorizada
```

Ejemplo:

```text
Puesto RRHH:
Jefe de Bodega
        ↓
puede sugerir
        ↓
Perfil / Rol de acceso:
Supervisor de Inventario
        ↓
Permisos:
inventory.stock.read
inventory.stock.manage
```

Un cambio de puesto no debe otorgar automáticamente privilegios sin una regla explícita y controlada.

---

## 7. UIX: navegación y ownership de dominio no son lo mismo

La ubicación de una función en el menú no determina qué módulo es dueño del dato.

Ejemplo:

```text
Configuración
└── Equipo
    ├── Miembros
    ├── Roles
    └── Permisos
```

puede consumir `gm-entities`, `gm-human-resources`, `gm-security` y `gm-configurations` sin duplicar información.

---

## 8. Estructura UI objetivo actual

### Entidades

```text
Entidades
├── Personas
└── Organizaciones
```

Responsabilidad visible:

- registrar identidad de personas
- registrar identidad de organizaciones
- activar luego capacidades adicionales desde otros módulos

Registrar una organización no significa activar automáticamente todos sus módulos.

### Recursos Humanos

```text
Recursos Humanos
├── Empleados
├── Puestos
└── demás procesos RRHH
```

Una Persona se convierte en Employee solo cuando existe relación laboral.

### Configuración

```text
Configuración
└── Equipo
    ├── Miembros
    ├── Roles
    └── Permisos
```

`Equipo` administra acceso al ERP, no RRHH.

Preferencia de término:

- `Miembros` cuando se quiera incluir owners, administradores, empleados, consultores u otros usuarios autorizados.
- Evitar usar `Empleados` en esta sección si puede confundirse con el verdadero `Employee` de RRHH.

---

## 9. Regla UIX de niveles

Baseline canónico:

```text
Nivel 1 = Módulo
Nivel 2 = Sección
Nivel 3 = navegación local dentro de la página
```

No crear niveles adicionales innecesarios en el sidebar.

Regla:

> **El Nivel 2 debe representar una capacidad suficientemente amplia para sobrevivir al crecimiento futuro del módulo. El Nivel 3 organiza subcapacidades concretas.**

Esto evita rehacer navegación cuando aparezcan nuevas funciones.

---

## 10. Regla “modelo futuro”

Cada módulo debe diseñarse pensando en:

```text
Dominio / capacidad principal
    ↓
Maestros
Operaciones
Historiales
Configuraciones
Reportes
```

No se debe nombrar una sección principal únicamente por la primera función disponible hoy.

Ejemplo correcto:

```text
Descargas
├── Medidores de descarga
└── Operaciones de descarga
```

El flujo y las UIs definitivas del Owner tienen prioridad sobre esta guía.

---

## 11. Regla UIX transversal

Estilo:

> **Executive Technology**

Características:

- serio
- contemporáneo
- limpio
- preciso
- silencioso
- tecnológico

Principio:

> **El usuario debería aprender una sola vez dónde está cada cosa y conservar ese modelo mental en todos los módulos.**

Baseline visual:

- Primary CTA: gradiente `#0057FF → #076EDB`
- ángulo: `135deg`
- texto blanco
- button weight: `600`
- button/input: `14px / 20px`
- control height: `44px`
- active nav/filter:
  - background `#EAF1FD`
  - text `#06204D`
  - accent `#29A9E0`

---

## 12. Aplicación a `gm-fuel-stations`

### Sidebar Nivel 2

```text
Estaciones de combustible
├── Estaciones
├── Transporte
└── Descargas
```

### 12.1 Estaciones

Representa infraestructura fija.

```text
Estaciones
├── Puntos receptores
└── Tanques receptores
```

**Tanque receptor:** tanque fijo asociado a una estación o punto receptor.

### 12.2 Transporte

Representa unidades móviles de combustible.

```text
Transporte
└── Tanqueros
```

`Tanqueros` debe ser navegación local Nivel 3, no otro nivel del sidebar.

Terminología UI preferida:

```text
Transporte

Tanqueros

Tanqueros registrados

+ Nuevo tanquero
```

Detalle:

```text
Tanquero
├── Vehículo
├── Tanque de transporte
└── Compartimentos
```

Distinción:

```text
Tanquero
= unidad operativa entendida por el usuario

TransportTank / Tanque de transporte
= componente técnico del dominio vinculado al Vehicle
```

### 12.3 Descargas

`Descargas` debe permanecer como sección Nivel 2 porque en el futuro cubrirá más que medidores.

```text
Descargas
├── Medidores de descarga
└── Operaciones de descarga
```

Detalle del medidor:

```text
Medidor
├── Datos
├── Propietario
├── Ubicación
├── Calibraciones
└── Sellos
```

Modelo futuro:

```text
Medidor de descarga
        ↓
Lecturas / tickets
        ↓
Operación de descarga
        ↓
Tanque receptor
```

---

## 13. Diferencia entre los dos tipos de tanque

### Tanque receptor

```text
Estaciones
→ infraestructura fija
→ Tanque receptor
```

### Tanque de transporte

```text
Transporte
→ Tanquero
→ Tanque de transporte
→ Compartimentos
```

No deben presentarse como el mismo concepto.

---

## 14. Regla para módulos operativos futuros

Cada módulo debe intentar distinguir claramente:

### Maestros

Objetos con identidad relativamente estable.

Ejemplos:

- Vehicle
- Tank
- Meter
- Person
- Role
- Employee

### Operaciones

Eventos o procesos que ocurren sobre los maestros.

Ejemplos:

- Expense
- Fuel discharge
- Ownership change
- Settlement
- Vehicle assignment

### Historiales

Cambios temporales o trazabilidad:

- propietarios
- conductores
- ubicaciones
- calibraciones
- estados
- asignaciones

### Configuración

Políticas o parámetros que controlan cómo funciona el módulo.

### Reportes

Lecturas derivadas de los datos operativos, sin convertirse en dueños del dato fuente.

---

## 15. Regla de no duplicación entre módulos

Ejemplo con Flotas:

```text
gm-fleets
Vehicle #53
```

Otros módulos deben referenciar ese `Vehicle #53`.

```text
gm-expenses
gm-fuel-stations
gm-service-management
```

No deben crear otra entidad paralela para representar el mismo vehículo.

---

## 16. ADN del vehículo

Para `gm-fleets`, el ADN canónico acordado es:

```text
1. Plate
2. Brand
3. Model
4. Chassis
5. Year
```

Estos campos no son editables mediante la operación normal `Editar vehículo`.

Los datos mutables se administran por separado.

---

## 17. Correcciones excepcionales vs edición normal

Si un dato de identidad canónica fue registrado incorrectamente, no debe abrirse como edición libre.

Para registros legacy incompletos puede existir una operación `fill-only-if-null`.

Regla:

> **No convertir una corrección excepcional en edición cotidiana.**

---

## 18. Regla de crecimiento modular

Antes de añadir una nueva capacidad:

1. identificar quién es dueño del dato;
2. verificar si ya existe una identidad canónica;
3. evitar crear un duplicado;
4. determinar si es Maestro, Operación, Historial, Configuración o Reporte;
5. ubicarla correctamente en Nivel 2 o Nivel 3;
6. dejar espacio conceptual para crecimiento futuro;
7. preservar trazabilidad e IDs existentes;
8. no acoplar un dominio global a terminología local innecesaria.

---

## 19. SaaS global y contexto local

GYPPORT es SaaS global.

Por tanto:

- los dominios canónicos deben usar conceptos neutrales cuando sea posible;
- las reglas específicas de Ecuador deben modelarse como contexto fiscal/jurisdiccional;
- un término local no debe deformar el núcleo global.

Ejemplo: `Polarizado` puede ser información registral local del vehículo, pero no forma parte de su ADN global.

---

## 20. Principio final

```text
gm-entities
= quién existe

gm-organizations
= cómo se estructura la organización

gm-human-resources
= qué relación laboral existe

gm-security
= quién puede entrar y qué puede hacer

gm-configurations
= cómo se configura GYPPORT

módulos operativos
= qué ocurre en el negocio

Gystigo
= Host/orquestador técnico

Studio / futuras interfaces
= cómo interactúa el usuario con todo lo anterior
```

Regla transversal:

> **Capturar una vez, identificar correctamente, reutilizar por referencia, mantener ownership claro y diseñar la UI pensando en el flujo actual y en el modelo futuro.**
