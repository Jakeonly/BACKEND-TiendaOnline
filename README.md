# BACKEND-TiendaOnline

## Descripción
Este proyecto es el backend de una aplicación web de tienda en línea (Tienda Online). Proporciona una API RESTful para gestionar productos, usuarios, pedidos y otras funcionalidades esenciales de un e-commerce. Está desarrollado con Node.js y Express, utilizando una base de datos para almacenar datos persistentes.

## Características
- Gestión de productos: Crear, leer, actualizar y eliminar productos.
- Gestión de usuarios: Registro, autenticación y perfiles de usuario.
- Gestión de pedidos: Crear pedidos, ver historial y actualizar estados.
- Autenticación JWT para seguridad.
- Integración con base de datos (ej. MongoDB o PostgreSQL).
- Validación de datos y manejo de errores.
- Documentación de API con Swagger (opcional).

## Tecnologías Utilizadas
- **Node.js**: Entorno de ejecución para JavaScript en el servidor.
- **Express.js**: Framework web para Node.js.
- **MongoDB/PostgreSQL**: Base de datos para almacenamiento de datos.
- **JWT**: Para autenticación.
- **bcrypt**: Para hashing de contraseñas.
- **Mongoose/Sequelize**: ORM para interactuar con la base de datos.
- **Nodemon**: Para desarrollo con recarga automática.

## Requisitos Previos
- Node.js (versión 14 o superior)
- npm o yarn
- Una base de datos (MongoDB o PostgreSQL) instalada y configurada.

## Instalación
1. Clona el repositorio:
   ```
   git clone https://github.com/Jakeonly/BACKEND-TiendaOnline.git
   ```

2. Instala las dependencias:
   ```
   npm install
   ```

3. Configura las variables de entorno: Crea un archivo `.env` en la raíz del proyecto y agrega las siguientes variables:
   ```
   PORT=3000
   DATABASE_URL=mongodb://localhost:27017/tiendaonline  # O la URL de tu base de datos
   JWT_SECRET=tu_clave_secreta_jwt
   ```

4. Inicia la base de datos si es necesario (ej. MongoDB).

5. Ejecuta el servidor en modo desarrollo:
   ```
   npm run dev
   ```

El servidor debería estar corriendo en `http://localhost:3000`.

## Uso
- **Desarrollo**: Usa `npm run dev` para ejecutar con Nodemon.
- **Producción**: Usa `npm start` para ejecutar el servidor.
- Accede a la API en `http://localhost:3000/api`.

### Endpoints Principales
- `GET /api/products`: Obtener lista de productos.
- `POST /api/products`: Crear un nuevo producto (requiere autenticación).
- `GET /api/users`: Obtener lista de usuarios (requiere autenticación admin).
- `POST /api/auth/login`: Iniciar sesión.
- `POST /api/orders`: Crear un pedido (requiere autenticación).

Para una documentación completa, consulta la documentación de Swagger en `/api-docs` si está habilitada.

## Estructura del Proyecto
```
BACKEND-TiendaOnline/
├── src/
│   ├── controllers/     # Controladores de la API
│   ├── models/          # Modelos de datos
│   ├── routes/          # Definición de rutas
│   ├── middleware/      # Middleware personalizado
│   └── utils/           # Utilidades
├── config/              # Configuraciones (ej. base de datos)
├── tests/               # Pruebas unitarias
├── .env                 # Variables de entorno
├── package.json         # Dependencias y scripts
└── README.md            # Este archivo
```

## Pruebas
Ejecuta las pruebas con:
```
npm test
```

## Contribución
1. Haz un fork del proyecto.
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`).
3. Haz commit de tus cambios (`git commit -am 'Agrega nueva funcionalidad'`).
4. Push a la rama (`git push origin feature/nueva-funcionalidad`).
5. Abre un Pull Request.

## Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

## Contacto
Para preguntas o soporte, contacta a [catanoandres131@gmail.com][cristianrestrepo0825@gmail.com] o abre un issue en el repositorio.
