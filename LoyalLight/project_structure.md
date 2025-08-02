# Estructura del Proyecto LoyalLight MVP

## Arquitectura General

```
LoyalLight/
├── backend/                     # Backend FastAPI
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py             # Punto de entrada FastAPI
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py       # Configuración de la aplicación
│   │   │   ├── database.py     # Conexión a MongoDB
│   │   │   ├── auth.py         # Sistema de autenticación
│   │   │   └── ai_service.py   # Servicio de IA con PDFs
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py         # Modelo de usuario
│   │   │   ├── client.py       # Modelo de cliente
│   │   │   ├── purchase.py     # Modelo de compra
│   │   │   ├── product.py      # Modelo de producto/stock
│   │   │   └── dashboard.py    # Modelos del dashboard
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py         # Endpoints de autenticación
│   │   │   ├── clients.py      # Endpoints de clientes
│   │   │   ├── purchases.py    # Endpoints de compras
│   │   │   ├── stock.py        # Endpoints de stock
│   │   │   ├── dashboard.py    # Endpoints del dashboard
│   │   │   └── ai.py           # Endpoints de IA
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py # Lógica de autenticación
│   │   │   ├── client_service.py # Lógica de clientes
│   │   │   ├── purchase_service.py # Lógica de compras
│   │   │   ├── stock_service.py # Lógica de stock
│   │   │   ├── dashboard_service.py # Lógica del dashboard
│   │   │   └── ai_service.py   # Lógica de IA
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── security.py     # Utilidades de seguridad
│   │       ├── rate_limiter.py # Control de consumo API
│   │       └── cache.py        # Sistema de caché
│   ├── requirements.txt        # Dependencias Python
│   └── .env.example           # Variables de entorno ejemplo
├── frontend/                   # Frontend React
│   ├── src/
│   │   ├── components/
│   │   │   ├── common/
│   │   │   │   ├── Sidebar.js  # Navegación lateral
│   │   │   │   ├── Header.js   # Cabecera
│   │   │   │   └── Logo.js     # Componente del logo
│   │   │   ├── auth/
│   │   │   │   └── Login.js    # Página de login
│   │   │   ├── dashboard/
│   │   │   │   ├── Dashboard.js # Dashboard principal
│   │   │   │   ├── Alerts.js   # Bloque de alertas
│   │   │   │   ├── TopClients.js # Top 5 clientes
│   │   │   │   ├── ChurnAnalysis.js # Análisis de churn
│   │   │   │   └── AIInsights.js # Sugerencias IA
│   │   │   ├── clients/
│   │   │   │   ├── ClientList.js # Lista de clientes
│   │   │   │   └── ClientForm.js # Formulario de cliente
│   │   │   ├── purchases/
│   │   │   │   ├── PurchaseList.js # Lista de compras
│   │   │   │   └── PurchaseForm.js # Formulario de compra
│   │   │   └── stock/
│   │   │       ├── StockList.js # Lista de stock
│   │   │       ├── StockForm.js # Formulario de stock
│   │   │       └── StockCharts.js # Gráficos de stock
│   │   ├── pages/
│   │   │   ├── LoginPage.js    # Página de login
│   │   │   ├── DashboardPage.js # Página del dashboard
│   │   │   ├── ClientsPage.js  # Página de clientes
│   │   │   ├── PurchasesPage.js # Página de compras
│   │   │   └── StockPage.js    # Página de stock
│   │   ├── services/
│   │   │   ├── api.js          # Cliente API
│   │   │   ├── auth.js         # Servicios de autenticación
│   │   │   └── ai.js           # Servicios de IA
│   │   ├── hooks/
│   │   │   ├── useAuth.js      # Hook de autenticación
│   │   │   └── useAPI.js       # Hook para API calls
│   │   ├── utils/
│   │   │   ├── constants.js    # Constantes
│   │   │   └── helpers.js      # Funciones auxiliares
│   │   ├── styles/
│   │   │   ├── globals.css     # Estilos globales
│   │   │   └── components.css  # Estilos de componentes
│   │   ├── App.js              # Componente principal
│   │   └── index.js            # Punto de entrada React
│   ├── public/
│   │   ├── index.html          # Template HTML
│   │   └── logo.png            # Logo de la aplicación
│   ├── package.json            # Dependencias Node.js
│   ├── tailwind.config.js      # Configuración Tailwind
│   └── .env.example           # Variables de entorno ejemplo
├── ai_knowledge/               # PDFs de conocimiento IA
│   ├── Customer_loyalty_in_retail_banking.pdf
│   └── customer-experience-excellence-report-2023-24-WA1.pdf
├── run_local.py               # Script para ejecutar localmente
├── README.md                  # Documentación del proyecto
└── .env.example              # Variables de entorno globales
```

## Modelos de Datos

### Usuario (User)
```python
{
    "id": "uuid",
    "username": "string",
    "password_hash": "string",
    "role": "admin|client",
    "created_at": "datetime"
}
```

### Cliente (Client)
```python
{
    "id": "uuid",
    "nombre": "string",
    "apellido": "string",
    "correo_electronico": "string",
    "fecha_registro": "datetime",
    "churn_score": "float",
    "total_compras": "int",
    "valor_total": "float"
}
```

### Compra (Purchase)
```python
{
    "id": "uuid",
    "producto_comprado": "string",
    "cliente_id": "uuid",
    "cantidad": "int",
    "fecha": "datetime",
    "precio_unitario": "float",
    "total": "float"
}
```

### Producto/Stock (Product)
```python
{
    "id": "uuid",
    "nombre_producto": "string",
    "precio": "float",
    "stock_actual": "int",
    "stock_minimo": "int",
    "imagen_url": "string",
    "fecha_creacion": "datetime"
}
```

## API Endpoints

### Autenticación
- `POST /api/auth/login` - Iniciar sesión
- `POST /api/auth/logout` - Cerrar sesión
- `GET /api/auth/me` - Obtener usuario actual

### Clientes
- `GET /api/clients` - Listar clientes
- `POST /api/clients` - Crear cliente
- `GET /api/clients/{id}` - Obtener cliente
- `PUT /api/clients/{id}` - Actualizar cliente
- `DELETE /api/clients/{id}` - Eliminar cliente

### Compras
- `GET /api/purchases` - Listar compras
- `POST /api/purchases` - Crear compra
- `GET /api/purchases/{id}` - Obtener compra
- `PUT /api/purchases/{id}` - Actualizar compra
- `DELETE /api/purchases/{id}` - Eliminar compra

### Stock
- `GET /api/stock` - Listar productos
- `POST /api/stock` - Crear producto
- `GET /api/stock/{id}` - Obtener producto
- `PUT /api/stock/{id}` - Actualizar producto
- `DELETE /api/stock/{id}` - Eliminar producto
- `POST /api/stock/{id}/upload-image` - Subir imagen

### Dashboard
- `GET /api/dashboard/alerts` - Obtener alertas
- `GET /api/dashboard/top-clients` - Top 5 clientes fieles
- `GET /api/dashboard/churn-analysis` - Análisis de churn
- `GET /api/dashboard/metrics` - Métricas generales

### IA
- `POST /api/ai/churn-suggestions` - Sugerencias para reducir churn
- `POST /api/ai/offer-suggestions` - Sugerencias de ofertas
- `POST /api/ai/pricing-suggestions` - Sugerencias de precios
- `POST /api/ai/restock-plan` - Plan de reposición mensual
- `POST /api/ai/global-insights` - Insights globales

## Tecnologías Utilizadas

### Backend
- **FastAPI** - Framework web moderno
- **MongoDB** - Base de datos NoSQL
- **Motor** - Driver async para MongoDB
- **Pydantic** - Validación de datos
- **Passlib** - Hashing de contraseñas
- **OpenAI** - API de IA
- **Sentence Transformers** - Embeddings para PDFs

### Frontend
- **React 18** - Biblioteca de UI
- **React Router** - Enrutamiento
- **Axios** - Cliente HTTP
- **Tailwind CSS** - Framework CSS
- **Chart.js** - Gráficos
- **React Hook Form** - Manejo de formularios

### Herramientas
- **Uvicorn** - Servidor ASGI
- **Vercel** - Plataforma de despliegue
- **Git** - Control de versiones

