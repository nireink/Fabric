# 🏗️ PROMPT PROFESIONAL - DESARROLLO GYPPORT ERP

**Versión:** 1.0  
**Fecha:** 2026-07-26  
**Estado:** ACTIVO  
**Destinatarios:** IAs, Developers, Equipos de desarrollo

---

## 📖 Propósito

Este documento establece lineamientos claros, estándares de calidad y mejores prácticas para garantizar que el desarrollo del ERP GYPPORT sea:
- ✅ **Profesional:** Código limpio, organizado y escalable
- ✅ **Seguro:** Protección de datos, autenticación, validación
- ✅ **Eficiente:** Evitar código espaguetti, redundancias y errores
- ✅ **Mantenible:** Documentación clara, modularización, patrones conocidos
- ✅ **Normalizado:** Seguir estándares de industria en BD, APIs y arquitectura

---

## 🎯 Principios Fundamentales

### 1. Arquitectura Limpia (Clean Architecture)
```
┌─────────────────────────────────────────┐
│         PRESENTATION LAYER              │
│  (Controllers, Views, APIs)             │
├─────────────────────────────────────────┤
│         APPLICATION LAYER               │
│  (Use Cases, Services, Business Logic)  │
├─────────────────────────────────────────┤
│         DOMAIN LAYER                    │
│  (Entities, Value Objects)              │
├─────────────────────────────────────────┤
│         INFRASTRUCTURE LAYER            │
│  (Databases, External Services)         │
└─────────────────────────────────────────┘
```

**Regla:** Las dependencias apuntan hacia el interior. Nunca hacia afuera.

### 2. SOLID Principles

| Principio | Definición | Aplicación |
|-----------|-----------|-----------|
| **S**ingle Responsibility | Una clase = una razón para cambiar | Módulos especializados |
| **O**pen/Closed | Abierto para extensión, cerrado para modificación | Usar abstracciones |
| **L**iskov Substitution | Subclases intercambiables | Contracts bien definidos |
| **I**nterface Segregation | Muchas interfaces específicas, no una genérica | APIs limpias |
| **D**ependency Inversion | Depender de abstracciones, no implementaciones | Inyección de dependencias |

### 3. DRY (Don't Repeat Yourself)
- ❌ Copiar-pegar código
- ✅ Abstraer en funciones/métodos/módulos reutilizables

### 4. KISS (Keep It Simple, Stupid)
- ❌ Soluciones complejas y abstractas
- ✅ Código legible, directo, mantenible

---

## 📂 Estructura de Carpetas

```
GYPPORT/
├── backend/
│   ├── src/
│   │   ├── api/
│   │   │   ├── v1/
│   │   │   │   ├── routes/
│   │   │   │   │   ├── productos.routes.ts
│   │   │   │   │   ├── clientes.routes.ts
│   │   │   │   │   └── ...
│   │   │   │   ├── controllers/
│   │   │   │   │   ├── productos.controller.ts
│   │   │   │   │   ├── clientes.controller.ts
│   │   │   │   │   └── ...
│   │   │   │   └── middleware/
│   │   │   │       ├── auth.middleware.ts
│   │   │   │       ├── validation.middleware.ts
│   │   │   │       └── error-handler.middleware.ts
│   │   ├── domain/
│   │   │   ├── entities/
│   │   │   │   ├── producto.entity.ts
│   │   │   │   ├── cliente.entity.ts
│   │   │   │   └── ...
│   │   │   ├── interfaces/
│   │   │   │   ├── irepository.ts
│   │   │   │   ├── iservice.ts
│   │   │   │   └── ...
│   │   │   └── enums/
│   │   │       ├── status.enum.ts
│   │   │       ├── roles.enum.ts
│   │   │       └── ...
│   │   ├── application/
│   │   │   ├── services/
│   │   │   │   ├── producto.service.ts
│   │   │   │   ├── cliente.service.ts
│   │   │   │   └── ...
│   │   │   ├── dto/
│   │   │   │   ├── crear-producto.dto.ts
│   │   │   │   ├── actualizar-cliente.dto.ts
│   │   │   │   └── ...
│   │   │   └── mappers/
│   │   │       ├── producto.mapper.ts
│   │   │       └── ...
│   │   ├── infrastructure/
│   │   │   ├── database/
│   │   │   │   ├── connection.ts
│   │   │   │   ├── migrations/
│   │   │   │   │   ├── 001_create_tables.sql
│   │   │   │   │   ├── 002_add_constraints.sql
│   │   │   │   │   └── ...
│   │   │   │   └── seeds/
│   │   │   ├── repositories/
│   │   │   │   ├── producto.repository.ts
│   │   │   │   ├── cliente.repository.ts
│   │   │   │   └── ...
│   │   │   ├── cache/
│   │   │   │   └── redis.cache.ts
│   │   │   └── external/
│   │   │       └── payment-gateway.service.ts
│   │   ├── config/
│   │   │   ├── database.config.ts
│   │   │   ├── auth.config.ts
│   │   │   └── app.config.ts
│   │   ├── utils/
│   │   │   ├── validators.ts
│   │   │   ├── formatters.ts
│   │   │   └── helpers.ts
│   │   ├── app.ts
│   │   └── main.ts
│   ├── test/
│   │   ├── unit/
│   │   ├── integration/
│   │   └── e2e/
│   ├── .env.example
│   ├── package.json
│   └── tsconfig.json
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── store/
│   │   ├── utils/
│   │   └── ...
│   └── ...
├── docs/
│   ├── api-spec.openapi.yaml
│   ├── architecture.md
│   ├── database-design.md
│   └── ...
└── PROYECTO-LINEAMIENTOS.md
```

**Reglas:**
- Max 5 niveles de profundidad
- No repetir nombres de archivos
- Carpetas por funcionalidad/módulo
- Archivos cortos (max 150 líneas excepto modelos)

---

## 🗄️ Base de Datos

### Principios de Normalización

#### 1️⃣ Primera Forma Normal (1FN)
- Eliminar grupos repetidos
- Un solo valor por celda
- Atomicidad de datos

#### 2️⃣ Segunda Forma Normal (2FN)
- Cumplir 1FN
- Eliminar dependencias parciales
- Cada atributo no-clave depende de toda la clave

#### 3️⃣ Tercera Forma Normal (3FN) ✅ ESTÁNDAR MÍNIMO
- Cumplir 2FN
- Eliminar dependencias transitivas
- No hay atributos que dependan de otros atributos no-clave

### Estructura de Tablas

```sql
-- ✅ BIEN: Normalizado 3FN
CREATE TABLE clientes (
  id_cliente INT PRIMARY KEY AUTO_INCREMENT,
  nombre VARCHAR(100) NOT NULL,
  email VARCHAR(100) UNIQUE NOT NULL,
  telefono VARCHAR(15),
  estado ENUM('activo', 'inactivo') NOT NULL DEFAULT 'activo',
  fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT uk_email UNIQUE (email),
  CONSTRAINT chk_nombre_length CHECK (LENGTH(nombre) > 0)
);

CREATE TABLE pedidos (
  id_pedido INT PRIMARY KEY AUTO_INCREMENT,
  id_cliente INT NOT NULL,
  fecha_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  monto_total DECIMAL(10, 2) NOT NULL,
  estado ENUM('pendiente', 'confirmado', 'enviado', 'entregado') DEFAULT 'pendiente',
  FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente) ON DELETE CASCADE,
  CONSTRAINT chk_monto_positivo CHECK (monto_total >= 0)
);

-- ❌ MAL: Datos duplicados, no normalizado
CREATE TABLE pedidos_denormalizado (
  id_pedido INT,
  nombre_cliente VARCHAR(100),  -- DUPLICADO
  email_cliente VARCHAR(100),    -- DUPLICADO
  telefono_cliente VARCHAR(15),  -- DUPLICADO
  fecha_pedido TIMESTAMP,
  monto_total DECIMAL(10, 2)
);
```

### Convenciones de Nombres

| Elemento | Convención | Ejemplo |
|----------|-----------|---------|
| Tablas | singular_snake_case | `cliente`, `pedido`, `producto` |
| Columnas ID | id_entidad | `id_cliente`, `id_pedido` |
| FK | id_entidad_relacionada | `id_cliente`, `id_producto` |
| Booleanos | is_estado / has_atributo | `is_activo`, `has_comentarios` |
| Timestamps | fecha_accion / fecha_entidad | `fecha_creacion`, `fecha_actualizacion` |
| Índices | idx_tabla_columna | `idx_cliente_email` |
| PK Constraints | pk_tabla | `pk_cliente` |
| FK Constraints | fk_tabla_tabla_relacionada | `fk_pedido_cliente` |
| Unique | uk_tabla_columna | `uk_cliente_email` |

---

## 🔌 API RESTful

### Métodos HTTP

| Método | Acción | Idempotente | Seguro | Ejemplo |
|--------|--------|-----------|--------|---------|
| **GET** | Obtener recurso | ✅ | ✅ | `GET /api/v1/clientes/123` |
| **POST** | Crear recurso | ❌ | ❌ | `POST /api/v1/clientes` |
| **PUT** | Reemplazar completo | ✅ | ❌ | `PUT /api/v1/clientes/123` |
| **PATCH** | Actualizar parcial | ✅ | ❌ | `PATCH /api/v1/clientes/123` |
| **DELETE** | Eliminar recurso | ✅ | ❌ | `DELETE /api/v1/clientes/123` |

### Códigos de Estado HTTP

```
2xx - ÉXITO
  200 OK                    → GET exitoso
  201 Created               → POST exitoso, recurso creado
  204 No Content            → Operación exitosa, sin contenido

4xx - ERROR DEL CLIENTE
  400 Bad Request           → Datos inválidos
  401 Unauthorized          → Sin autenticación
  403 Forbidden             → Sin autorización
  404 Not Found             → Recurso no existe
  409 Conflict              → Conflicto (ej: recurso duplicado)
  422 Unprocessable Entity  → Validación falló

5xx - ERROR DEL SERVIDOR
  500 Internal Server Error → Error interno del servidor
  503 Service Unavailable   → Servicio no disponible
```

### Estructura de Respuestas

```typescript
// ✅ BIEN: Consistente, informativo, tipado

// Éxito con datos
{
  "success": true,
  "status": 200,
  "data": {
    "id_cliente": 123,
    "nombre": "Juan Pérez",
    "email": "juan@example.com"
  },
  "meta": {
    "timestamp": "2026-07-26T18:30:00Z",
    "version": "1.0"
  }
}

// Éxito sin datos
{
  "success": true,
  "status": 204,
  "message": "Recurso actualizado correctamente"
}

// Error
{
  "success": false,
  "status": 400,
  "error": {
    "code": "INVALID_EMAIL",
    "message": "El email no es válido",
    "field": "email",
    "details": "El formato debe ser: usuario@dominio.com"
  },
  "meta": {
    "timestamp": "2026-07-26T18:30:00Z",
    "version": "1.0",
    "requestId": "req_abc123"
  }
}

// Errores de validación múltiples
{
  "success": false,
  "status": 422,
  "errors": [
    {
      "field": "nombre",
      "message": "Es requerido",
      "code": "REQUIRED"
    },
    {
      "field": "email",
      "message": "Ya existe",
      "code": "DUPLICATE"
    }
  ]
}
```

### Versionado y Documentación

```typescript
// ✅ BIEN: API versionada
GET /api/v1/clientes       → Versión 1
GET /api/v2/clientes       → Versión 2 (si cambios breaking)

// Documentación OBLIGATORIA
// Archivo: docs/api-spec.openapi.yaml
```

---

## 🔐 Seguridad

### Checklist de Seguridad

- [ ] **HTTPS obligatorio** en producción
- [ ] **Autenticación** en todos los endpoints protegidos (JWT, OAuth2)
- [ ] **Validación de entrada** en formularios, APIs, campos
- [ ] **SQL Injection prevention** → Prepared statements, ORMs
- [ ] **XSS prevention** → Sanitizar output, CSP headers
- [ ] **CORS correctamente configurado** → No `*` en producción
- [ ] **Rate limiting** en APIs públicas
- [ ] **Encriptación de datos sensibles** → contraseñas (bcrypt), PII
- [ ] **Secrets management** → .env, vaults (no hardcoded)
- [ ] **OWASP Top 10** → Revisar anualmente
- [ ] **SQL injection tests** en testing
- [ ] **Logging y monitoring** de eventos de seguridad

### Ejemplo: Validación y Sanitización

```typescript
// ❌ MAL
app.get('/cliente/:id', (req, res) => {
  const id = req.params.id;  // No validado
  db.query(`SELECT * FROM clientes WHERE id = ${id}`, (err, result) => {
    // SQL INJECTION VULNERABLE
    res.json(result);
  });
});

// ✅ BIEN
import { param, validationResult } from 'express-validator';
import crypto from 'crypto';

app.get(
  '/api/v1/cliente/:id',
  param('id').isInt().toInt(),  // Validación
  (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    const id = req.params.id;
    // Prepared statement - SEGURO
    db.query('SELECT * FROM clientes WHERE id = ?', [id], (err, result) => {
      if (err) {
        return res.status(500).json({ error: 'Database error' });
      }
      res.json({ success: true, data: result });
    });
  }
);
```

---

## 📝 Código: Mejores Prácticas

### Longitud de Archivos

```
✅ IDEAL:     50-100 líneas
✅ ACEPTABLE: 100-150 líneas
❌ MALO:      > 200 líneas

Excepciones:
- Modelos de datos (entidades)
- Migrations de BD
- Seeders
```

### Nombres Significativos

```typescript
// ❌ MAL
function proc(d: any) {
  let a = d.map(x => x * 2);
  return a;
}

// ✅ BIEN
function doubleProductPrices(products: Product[]): number[] {
  return products.map(product => product.price * 2);
}
```

### Funciones y Métodos

```typescript
// ❌ MAL: Hace demasiadas cosas
function procesarCliente(datos: any) {
  // Validar
  if (!datos.email) throw new Error('Email requerido');
  
  // Guardar en BD
  const cliente = db.create(datos);
  
  // Enviar email
  mailer.send(datos.email, 'Welcome!');
  
  // Log
  logger.info('Cliente creado');
  
  return cliente;
}

// ✅ BIEN: SRP - Una responsabilidad
async function crearCliente(datos: CreateClienteDTO): Promise<Cliente> {
  validarDatosCliente(datos);
  const cliente = await clienteRepository.create(datos);
  return cliente;
}

async function enviarEmailBienvenida(cliente: Cliente): Promise<void> {
  await mailerService.sendWelcome(cliente.email, cliente.nombre);
}

async function registrarCliente(datos: CreateClienteDTO): Promise<Cliente> {
  const cliente = await crearCliente(datos);
  await enviarEmailBienvenida(cliente);
  logger.info(`Cliente creado: ${cliente.id}`);
  return cliente;
}
```

### Manejo de Errores

```typescript
// ❌ MAL: Silenciar errores
try {
  const resultado = await operacionCompleja();
} catch (e) {
  // Ignorar
}

// ✅ BIEN: Registrar y propagar
try {
  const resultado = await operacionCompleja();
  return resultado;
} catch (error) {
  logger.error('Error en operación compleja', {
    error: error.message,
    stack: error.stack,
    context: { userId, operationType }
  });
  throw new ApplicationError(
    'No se pudo completar la operación',
    'OPERATION_FAILED',
    500
  );
}
```

### Async/Await vs Callbacks

```typescript
// ❌ VIEJO: Callback Hell
function obtenerDatos(callback) {
  db.query('SELECT * FROM clientes', (err, clientes) => {
    if (err) callback(err);
    else {
      db.query('SELECT * FROM pedidos WHERE id = ?', [clientes[0].id], 
        (err, pedidos) => {
          if (err) callback(err);
          else callback(null, { clientes, pedidos });
        }
      );
    }
  });
}

// ✅ MODERNO: Async/Await
async function obtenerDatos(): Promise<{ clientes: Cliente[], pedidos: Pedido[] }> {
  const clientes = await db.query('SELECT * FROM clientes');
  const pedidos = await db.query(
    'SELECT * FROM pedidos WHERE id = ?', 
    [clientes[0].id]
  );
  return { clientes, pedidos };
}
```

---

## 🧪 Testing

### Nivel de Cobertura Mínimo

- **Crítico:** > 90% (autenticación, pagos, cálculos)
- **Importante:** > 70% (servicios, lógica de negocio)
- **General:** > 50% (helpers, utilidades)

### Tipos de Tests

```typescript
// UNIT TEST - Función aislada
describe('doubleProductPrices', () => {
  it('should double product prices correctly', () => {
    const products = [{ id: 1, price: 100 }, { id: 2, price: 50 }];
    const result = doubleProductPrices(products);
    expect(result).toEqual([200, 100]);
  });
});

// INTEGRATION TEST - Servicio + Repositorio
describe('ClienteService', () => {
  it('should create cliente and send welcome email', async () => {
    const nuevoCliente = await clienteService.crearCliente({
      nombre: 'Juan',
      email: 'juan@test.com'
    });
    expect(nuevoCliente.id).toBeDefined();
    expect(mailerService.send).toHaveBeenCalledWith('juan@test.com', expect.anything());
  });
});

// E2E TEST - API completa
describe('POST /api/v1/clientes', () => {
  it('should create a cliente and return 201', async () => {
    const response = await request(app)
      .post('/api/v1/clientes')
      .send({ nombre: 'María', email: 'maria@test.com' });
    
    expect(response.status).toBe(201);
    expect(response.body.data.id).toBeDefined();
  });
});
```

---

## 📋 Documentación

### Documentar

✅ **SÍ:**
- Funciones complejas
- Decisiones arquitectónicas
- APIs (OpenAPI/Swagger)
- Procesos de instalación/deployment
- Trade-offs y alternativas consideradas

❌ **NO:**
- Código auto-explicativo
- Lógica simple obvia
- Redundancia (código + comentarios idénticos)

### Formato de Comentarios

```typescript
/**
 * Calcula el total de un pedido incluyendo impuestos y descuentos.
 * 
 * @param items - Array de items del pedido
 * @param descuentoPorcentaje - Descuento como porcentaje (0-100)
 * @param incluirImpuestos - Si debe incluir impuestos locales
 * @returns Total del pedido en pesos
 * 
 * @example
 * calcularTotalPedido(
 *   [{ precio: 100, cantidad: 2 }],
 *   10,
 *   true
 * ) // => 198 (200 - 10% + 8% impuesto)
 * 
 * @throws {ValidationError} Si items está vacío
 */
function calcularTotalPedido(
  items: CartItem[],
  descuentoPorcentaje: number,
  incluirImpuestos: boolean
): number {
  // Implementación...
}
```

### README Mínimo

```markdown
# GYPPORT ERP Backend

## Descripción
Servicio backend del ERP GYPPORT.

## Stack
- Node.js 18+
- TypeScript
- Express
- PostgreSQL 13+

## Instalación

```bash
npm install
cp .env.example .env  # Configurar variables
npm run migrate
npm run dev
```

## API Docs
- OpenAPI: http://localhost:3000/api-docs

## Testing

```bash
npm run test      # Unit tests
npm run test:int  # Integration tests
npm run test:cov  # Coverage
```

## Estructura
Ver docs/architecture.md

## Guía de Contribución
Ver CONTRIBUTING.md
```

---

## 🚀 Deployment y DevOps

### CI/CD Pipeline

```yaml
# .github/workflows/deploy.yml
name: Deploy
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: npm install
      - run: npm run lint
      - run: npm run test:cov
  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - run: npm run build
      - run: npm run migrate
      - run: npm start
```

### Logs y Monitoring

```typescript
import winston from 'winston';

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' })
  ]
});

// Uso
logger.info('Operación exitosa', { userId, operationType });
logger.error('Error crítico', { error: e.message, stack: e.stack });
logger.warn('Advertencia', { resource: 'memory', usage: '85%' });
```

---

## ✅ Checklist de Desarrollo

Antes de hacer commit:

- [ ] Código formateado (Prettier, ESLint)
- [ ] Tests pasando (coverage > 70%)
- [ ] Tipos TypeScript correctos (no `any`)
- [ ] Sin `console.log` en producción
- [ ] Documentación actualizada
- [ ] Secrets NO están en código (.env)
- [ ] HTTPS en endpoints sensibles
- [ ] Validación de entrada
- [ ] Manejo de errores apropiado
- [ ] SQL uses prepared statements
- [ ] No hay duplicidad de código
- [ ] Nombres significativos
- [ ] Máx 150 líneas por archivo
- [ ] SRP respetado
- [ ] Archivos en estructura correcta

---

## 📞 Preguntas Frecuentes

**P: ¿Puedo usar JavaScript en lugar de TypeScript?**  
R: No. TypeScript es obligatorio para evitar errores en tiempo de ejecución.

**P: ¿Qué si tengo que repetir código?**  
R: Abstraer en función/método/servicio. Si no puede abstraerse, documentar por qué.

**P: ¿Level de normalización?**  
R: Mínimo 3FN. Si necesitas más, documentar en ADR.

**P: ¿Necesito tests para todo?**  
R: Crítico: >90%, Importante: >70%, General: >50%. Documentar excepciones.

**P: ¿Comentarios en código?**  
R: Solo lógica compleja o decisiones arquitectónicas. Código = auto-documentación.

---

## 🔗 Referencias

- OWASP Top 10: https://owasp.org/www-project-top-ten/
- OpenAPI 3.0: https://spec.openapis.org/oas/v3.0.3
- TypeScript Handbook: https://www.typescriptlang.org/docs/
- Express Best Practices: https://expressjs.com/en/advanced/best-practice-security.html
- Fabric/Knowledge/Books/Databases/

---

**Versión:** 1.0  
**Última actualización:** 2026-07-26  
**Autor:** CLAUDE (IA Agent)  
**Estado:** 🟢 ACTIVO - Listo para implementación

