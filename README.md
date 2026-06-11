# 🖥️ device_systems API — FastAPI v3.0.0

**Autora:** Sara García  
**Actividad:** GA1-220501096-01-AA1-EV09  
**Formación:** SENA — Análisis y Desarrollo de Software

---

## 📋 Descripción

**device_systems** es una API REST desarrollada con **FastAPI** para la gestión de usuarios del sistema device_systems. Este README documenta la evolución completa del proyecto a lo largo de tres versiones:

- **v1.0.0** — API REST básica con endpoints GET y POST, datos en memoria.
- **v2.0.0** — CRUD completo con PUT, PATCH, DELETE, manejo de errores, Dependency Injection y documentación Swagger/OpenAPI.
- **v3.0.0** — Persistencia real de datos mediante **SQLAlchemy** y **SQLite**. Los usuarios ya no se almacenan en memoria sino en una base de datos relacional.

---

## 🛠️ Tecnologías utilizadas

| Tecnología | Versión | Descripción |
|-----------|---------|-------------|
| Python | 3.10+ | Lenguaje de programación |
| FastAPI | 0.136+ | Framework web para APIs REST |
| Uvicorn | 0.47+ | Servidor ASGI |
| SQLAlchemy | 2.x | ORM para manejo de base de datos |
| SQLite | — | Base de datos relacional |
| Pydantic v2 | 2.x | Validación de datos y schemas |
| Git / GitHub | — | Control de versiones |

---

## 📁 Estructura del proyecto — v3.0.0

```
device_systems/
│── app/
│   │── main.py
│   │── database/
│   │   └── connection.py        ← Engine, SessionLocal y Base
│   │── models/
│   │   └── user_model.py        ← Modelo SQLAlchemy (tabla users)
│   │── schemas/
│   │   └── user_schema.py       ← Schemas Pydantic
│   │── services/
│   │   └── user_service.py      ← Lógica CRUD sobre base de datos
│   │── routes/
│   │   └── user_routes.py       ← Endpoints
│   └── dependencies/
│       └── database_dependency.py ← Depends(get_db)
│── capturas/                    ← Capturas de pantalla
│── device_systems.db            ← Base de datos SQLite (generada automáticamente)
│── requirements.txt
└── README.md
```

---

## ⚙️ Instalación y ejecución

### 1. Clona el repositorio
```bash
git clone https://github.com/urrego22/device_systems.git
cd device_systems
```

### 2. Crea y activa el entorno virtual
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Instala las dependencias
```bash
python -m pip install fastapi uvicorn sqlalchemy email-validator
```

### 4. Ejecuta el servidor
```bash
uvicorn app.main:app --reload
```

Al iniciar, SQLAlchemy crea automáticamente el archivo `device_systems.db` con la tabla `users`.

### 5. Documentación
- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

---

## 🔗 Tabla de Endpoints

| Método | Endpoint | Descripción | Código |
|--------|----------|-------------|--------|
| GET | `/users` | Listar usuarios (filtros y orden) | 200 |
| GET | `/users/{user_id}` | Consultar por ID | 200 |
| POST | `/users` | Crear usuario | 201 |
| PUT | `/users/{user_id}` | Actualizar completamente | 200 |
| PATCH | `/users/{user_id}` | Actualizar parcialmente | 200 |
| DELETE | `/users/{user_id}` | Eliminar usuario | 204 |

### Parámetros de filtro — GET /users

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `role` | string | Filtrar por: `admin`, `support`, `user` |
| `is_active` | boolean | Filtrar por estado: `true` o `false` |
| `order_by` | string | Ordenar por: `id`, `name`, `created_at` *(v3.0.0)* |

---

## 📊 Códigos de estado HTTP

| Código | Cuándo se usa |
|--------|---------------|
| 200 | GET, PUT, PATCH exitosos |
| 201 | POST exitoso |
| 204 | DELETE exitoso |
| 400 | Correo duplicado, PATCH vacío |
| 404 | Usuario no encontrado |
| 422 | Error de validación Pydantic |

---

## 🗄️ Modelo SQLAlchemy vs Schema Pydantic

Una diferencia fundamental en la v3.0.0 es separar el **modelo de base de datos** del **schema de la API**:

| | Modelo SQLAlchemy | Schema Pydantic |
|--|-------------------|-----------------|
| **Archivo** | `app/models/user_model.py` | `app/schemas/user_schema.py` |
| **Propósito** | Representa la tabla en la BD | Valida datos de entrada y salida de la API |
| **Hereda de** | `Base` (SQLAlchemy) | `BaseModel` (Pydantic) |
| **Define** | Columnas, tipos, constraints | Campos, validaciones, ejemplos |
| **Usado en** | `user_service.py` para queries | `user_routes.py` para request/response |

El modelo SQLAlchemy define cómo se almacena la información. El schema Pydantic define cómo se valida y comunica esa información con el cliente.

---

## 🧩 Dependency Injection con Depends() — v2.0.0

FastAPI permite inyectar lógica reutilizable en los endpoints usando `Depends()`. En la v2.0.0 se crearon las siguientes dependencias en `app/dependencies/user_dependencies.py`:

| Dependencia | Descripción |
|-------------|-------------|
| `get_user_or_404(user_id)` | Busca un usuario y lanza 404 automáticamente si no existe |
| `get_api_config()` | Retorna configuración general de la API |
| `verify_api_key(x_api_key)` | Simula autenticación básica mediante cabecera HTTP |

En la v3.0.0 se agrega `get_db()` en `app/dependencies/database_dependency.py` para inyectar la sesión de base de datos en cada endpoint.

---

## 🛡️ Manejo de errores

| Error | Código | Descripción |
|-------|--------|-------------|
| Usuario no encontrado | 404 | Al buscar, actualizar o eliminar ID inexistente |
| Correo duplicado | 400 | Email ya registrado |
| PATCH sin campos | 400 | Body vacío en PATCH |
| Datos inválidos | 422 | Validación Pydantic fallida |

---

## 📸 Evidencias

---

## 🔹 Versión 1.0.0 — API REST básica

### Captura 01 — Estructura del proyecto v1.0.0
> Organización inicial del proyecto con FastAPI, separando schemas, rutas y el punto de entrada en `main.py`.

![Estructura del proyecto](capturas/01_estructura_proyecto.png "Estructura del proyecto device_systems en VS Code — Sara García")

---

### Captura 02 — Swagger UI v1.0.0
> FastAPI genera esta documentación interactiva de forma automática. Desde aquí se pueden probar todos los endpoints sin necesidad de Postman.

![Swagger UI](capturas/02_swagger_inicio.png "Swagger UI - Pantalla principal — Sara García")

---

### Captura 03 — GET /users — Listado completo (200 OK)
> Endpoint para listar todos los usuarios registrados. Retorna un arreglo con los usuarios de prueba y código 200.

![GET todos los usuarios](capturas/03_get_users_todos.png "GET /users - Respuesta 200 con la lista de usuarios — Sara García")

---

### Captura 04 — GET /users?role=admin — Filtro por rol
> Usando un Query Parameter `role`, se filtran los usuarios por su rol. La API devuelve únicamente a Ana Torres, que es la única usuaria con ese rol.

![Filtro por rol admin](capturas/04_get_users_role_admin.png "GET /users?role=admin - Filtrado por rol — Sara García")

---

### Captura 05 — GET /users?is_active=false — Filtro por estado
> Con el Query Parameter `is_active=false` se filtran los usuarios inactivos. La API devuelve únicamente a María Pérez.

![Filtro usuarios inactivos](capturas/05_get_users_inactivos.png "GET /users?is_active=false - Filtrado por estado — Sara García")

---

### Captura 06 — GET /users/{user_id} — Buscar por ID (200 OK)
> Al enviar el ID 1 en la ruta `/users/1`, la API devuelve correctamente los datos de Ana Torres con código 200.

![GET usuario por ID](capturas/06_get_user_por_id.png "GET /users/1 - Respuesta 200 usuario encontrado — Sara García")

---

### Captura 07 — GET /users/999 — Error 404 usuario no encontrado
> Cuando se busca un ID que no existe, la API responde con código 404 y un mensaje de error estructurado.

![Error 404](capturas/07_get_user_404.png "GET /users/999 - Respuesta 404 usuario no encontrado — Sara García")

---

### Captura 08 — POST /users — Crear nuevo usuario (201 Created)
> Se envían los datos de Laura Gómez en el body. La API los valida, asigna un ID automático y devuelve el usuario creado con código 201.

![POST crear usuario](capturas/08_post_crear_usuario.png "POST /users - Respuesta 201 usuario creado — Sara García")

---

### Captura 09 — POST /users — Error 400 correo duplicado
> La API evita registrar correos duplicados. Al intentar crear otro usuario con el mismo email, responde con código 400.

![Error 400 correo duplicado](capturas/09_post_email_duplicado.png "POST /users - Respuesta 400 correo duplicado — Sara García")

---

### Captura 10 — POST /users — Error 422 validación Pydantic
> Cuando se envían datos inválidos, Pydantic rechaza la solicitud automáticamente con código 422 detallando exactamente qué campo falló.

![Error 422 validación](capturas/10_post_validacion_error.png "POST /users - Respuesta 422 validación Pydantic — Sara García")

---

## 🔹 Versión 2.0.0 — CRUD completo con Dependency Injection

### Captura 11 — Nueva estructura del proyecto v2.0.0
> Se agregaron las carpetas `services/`, `dependencies/` y `data/` para separar correctamente las responsabilidades del proyecto.

![Nueva estructura](capturas/capturas11_nueva_estructura.png "Nueva estructura del proyecto con services, dependencies y data — Sara García")

---

### Captura 12 — Swagger UI v2.0.0 — CRUD completo
> El Swagger muestra los 6 endpoints: GET, GET por ID, POST, PUT, PATCH y DELETE, todos organizados bajo el tag Users.

![Swagger CRUD completo](capturas/capturas12_swagger_crud_completo.png "Swagger UI con CRUD completo - PUT PATCH DELETE — Sara García")

---

### Captura 13 — PUT /users/{user_id} — Actualización completa (200 OK)
> Con PUT se reemplazan TODOS los campos del usuario. Se deben enviar todos los campos obligatoriamente. La API responde con 200 y los datos actualizados.

![PUT 200](capturas/capturas13_put_200.png "PUT /users/1 - Respuesta 200 actualización completa — Sara García")

---

### Captura 14 — PUT /users/{user_id} — No encontrado (404)
> Al intentar actualizar un usuario con ID inexistente, la dependencia `get_user_or_404` lanza el error 404 automáticamente.

![PUT 404](capturas/capturas14_put_404.png "PUT /users/999 - Respuesta 404 usuario no encontrado — Sara García")

---

### Captura 15 — PATCH /users/{user_id} — Actualización parcial (200 OK)
> Con PATCH solo se envían los campos que se quieren modificar. En este caso únicamente el rol; los demás campos quedan exactamente igual.

![PATCH 200](capturas/capturas15_patch_200.png "PATCH /users/2 - Respuesta 200 actualización parcial del rol — Sara García")

---

### Captura 16 — PATCH /users/{user_id} — Body vacío (400)
> Si se envía un body completamente vacío en PATCH, la API responde con 400 indicando que se debe enviar al menos un campo.

![PATCH 400 vacío](capturas/capturas16_patch_400_vacio.png "PATCH /users/2 - Respuesta 400 body vacío — Sara García")

---

### Captura 17 — DELETE /users/{user_id} — Eliminar usuario (204 No Content)
> El usuario es eliminado exitosamente. La respuesta 204 no tiene cuerpo, que es la práctica REST correcta para eliminaciones.

![DELETE 204](capturas/capturas17_delete_204.png "DELETE /users/3 - Respuesta 204 usuario eliminado — Sara García")

---

### Captura 18 — DELETE /users/{user_id} — No encontrado (404)
> Al intentar eliminar un ID que no existe, la API retorna 404 con el mensaje de error estructurado.

![DELETE 404](capturas/capturas18_delete_404.png "DELETE /users/999 - Respuesta 404 al eliminar usuario inexistente — Sara García")

---

### Captura 19 — ReDoc v2.0.0
> Vista alternativa de la documentación generada automáticamente por FastAPI con esquemas detallados de entrada y salida de cada endpoint.

![ReDoc](capturas/capturas19_redoc.png "ReDoc - Documentación interactiva de device_systems API — Sara García")

---

## 🔹 Versión 3.0.0 — Persistencia con SQLAlchemy y SQLite

### Captura 20 — Nueva estructura del proyecto v3.0.0
> Se agregaron las carpetas `database/` y `models/` y el archivo `device_systems.db` generado automáticamente por SQLAlchemy al iniciar la API.

![Estructura v3](capturas/20_estructura_v3.png "Nueva estructura del proyecto con SQLAlchemy — Sara García")

---

### Captura 21 — Base de datos SQLite creada automáticamente
> El archivo `device_systems.db` es generado por SQLAlchemy con `Base.metadata.create_all(bind=engine)` al iniciar el servidor por primera vez.

![Base de datos](capturas/21_base_de_datos_creada.png "Archivo device_systems.db creado automáticamente — Sara García")

---

### Captura 22 — Swagger UI v3.0.0
> Documentación automática mostrando los 6 endpoints y la descripción de la versión 3.0.0 con SQLAlchemy.

![Swagger v3](capturas/22_swagger_v3.png "Swagger UI versión 3.0.0 con SQLAlchemy — Sara García")

---

### Captura 23 — POST /users — Crear usuario con created_at (201)
> El campo `created_at` se asigna automáticamente por SQLAlchemy al momento de insertar el registro en la base de datos.

![POST 201](capturas/23_post_201_created_at.png "POST /users - Respuesta 201 con campo created_at — Sara García")

---

### Captura 24 — GET /users — Lista desde base de datos (200)
> Los usuarios ya no viven en memoria. Se consultan directamente desde la base de datos SQLite.

![GET BD](capturas/24_get_users_bd.png "GET /users - Lista de usuarios desde base de datos — Sara García")

---

### Captura 25 — GET /users?role=admin — Filtro por rol desde BD
> La consulta SQL filtra por el campo `role` directamente en la base de datos.

![GET filtro rol](capturas/25_get_filtro_rol.png "GET /users?role=admin - Filtrado por rol desde BD — Sara García")

---

### Captura 26 — GET /users?is_active=false — Filtro por estado inactivo
> La consulta SQL filtra por `is_active=false` directamente en la base de datos.

![GET filtro inactivo](capturas/26_get_filtro_inactivo.png "GET /users?is_active=false - Filtrado por estado — Sara García")

---

### Captura 27 — GET /users?order_by=name — Ordenado por nombre
> SQLAlchemy permite ordenar los resultados con `.order_by(User.name)`.

![GET order by](capturas/27_get_order_by_name.png "GET /users?order_by=name - Ordenado por nombre — Sara García")

---

### Captura 28 — GET /users/{user_id} — Consultar por ID (200)
> SQLAlchemy busca el registro con `.filter(User.id == user_id).first()`.

![GET ID](capturas/28_get_user_id_200.png "GET /users/1 - Respuesta 200 desde base de datos — Sara García")

---

### Captura 29 — GET /users/{user_id} — No encontrado (404)
> Si el ID no existe en la base de datos, el servicio lanza HTTPException 404.

![GET 404](capturas/29_get_user_404.png "GET /users/999 - Respuesta 404 usuario no encontrado — Sara García")

---

### Captura 30 — POST /users — Correo duplicado (400)
> SQLAlchemy tiene el constraint `unique=True` en el campo email. El servicio valida antes de insertar.

![POST 400](capturas/30_post_email_duplicado.png "POST /users - Respuesta 400 correo duplicado — Sara García")

---

### Captura 31 — PUT /users/{user_id} — Actualización completa (200)
> SQLAlchemy actualiza todos los campos del registro y hace commit a la base de datos.

![PUT 200](capturas/31_put_200.png "PUT /users/1 - Actualización completa en BD — Sara García")

---

### Captura 32 — PATCH /users/{user_id} — Actualización parcial (200)
> Solo se actualizan los campos enviados usando `setattr` sobre el modelo SQLAlchemy.

![PATCH 200](capturas/32_patch_200.png "PATCH /users/2 - Actualización parcial en BD — Sara García")

---

### Captura 33 — PATCH /users/{user_id} — Body vacío (400)
> Si no se envía ningún campo, el servicio lanza 400 antes de intentar actualizar.

![PATCH 400](capturas/33_patch_400_vacio.png "PATCH /users/2 - Respuesta 400 body vacío — Sara García")

---

### Captura 34 — DELETE /users/{user_id} — Eliminar (204)
> SQLAlchemy elimina el registro con `db.delete(user)` y confirma con `db.commit()`.

![DELETE 204](capturas/34_delete_204.png "DELETE /users/3 - Respuesta 204 usuario eliminado — Sara García")

---

### Captura 35 — Verificación: usuario eliminado ya no existe (404)
> Al consultar el ID 3 después de eliminarlo, la base de datos ya no lo encuentra y responde 404.

![DELETE verificación](capturas/35_delete_verificacion_404.png "GET /users/3 - Verificación 404 tras eliminación — Sara García")

---

### Captura 36 — ReDoc v3.0.0
> Vista alternativa de la documentación con schemas detallados incluyendo el nuevo campo `created_at`.

![ReDoc v3](capturas/36_redoc_v3.png "ReDoc v3.0.0 con SQLAlchemy — Sara García")

---

## 💭 Reflexión final

**v1.0.0 — Fundamentos:** Esta primera versión me permitió entender la estructura básica de una API REST con FastAPI: cómo definir rutas, validar datos con Pydantic y documentar automáticamente con Swagger. Trabajar con datos en memoria fue útil para enfocarse en los conceptos sin la complejidad de una base de datos.

**v2.0.0 — CRUD profesional:** Separar el código en `routes`, `schemas`, `services`, `dependencies` y `data` hace el proyecto mucho más fácil de mantener y escalar. `Depends()` elimina la duplicación de código siguiendo el principio DRY, y `HTTPException` permite devolver errores claros y estandarizados. Usar `201 Created` para POST, `204 No Content` para DELETE y `422` para validaciones hace la API predecible y profesional.

**v3.0.0 — Persistencia real:** Incorporar SQLAlchemy fue el cambio más importante. Los datos ahora persisten aunque el servidor se reinicie, se pueden aplicar constraints reales como `unique=True`, y las consultas son mucho más poderosas con filtros y ordenamiento directo en SQL. La separación entre modelo SQLAlchemy y schema Pydantic al principio puede parecer redundante, pero tiene mucho sentido: el modelo define cómo se guarda la información y el schema define cómo se valida y comunica con el cliente. Son responsabilidades diferentes y mantenerlas separadas hace el código más limpio y seguro.

---

## 🎬 Videos de demostración

[![Fundamentos de FastAPI: API REST para Gestión de Usuarios](https://img.shields.io/badge/YouTube-Fundamentos%20de%20FastAPI%3A%20API%20REST%20para%20Gestión%20de%20Usuarios-red?style=for-the-badge&logo=youtube)](https://youtu.be/54odRYQvzlw)

[![FastAPI Intermedio: Evolución de device_systems con CRUD Completo](https://img.shields.io/badge/YouTube-FastAPI%20Intermedio%3A%20Evolución%20device__systems-red?style=for-the-badge&logo=youtube)](https://youtu.be/JibMRVahbqg)

[![FastAPI con SQLAlchemy: Persistencia de Datos en device_systems](https://img.shields.io/badge/YouTube-FastAPI%20con%20SQLAlchemy%3A%20Persistencia%20de%20Datos-red?style=for-the-badge&logo=youtube)](https://youtu.be/e1cnjeBUlUU)

---

*Proyecto desarrollado por **Sara García** — SENA Análisis y Desarrollo de Software*