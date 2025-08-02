# LoyalLight - Sistema de Gestión de Clientes

## 🚀 Aplicación Desplegada

**URL de producción:** https://qjh9iec5pdpo.manus.space

### Credenciales de Prueba
- **Administrador:** `admin` / `secret`
- **Clientes:** `cliente1` a `cliente10` / `secret`

## 📋 Descripción

LoyalLight es un sistema completo de gestión de clientes que incluye:

- **Dashboard** con métricas, alertas y análisis de churn
- **Gestión de Clientes** con CRUD completo
- **Gestión de Compras** con sugerencias de ofertas IA
- **Gestión de Stock** con análisis de precios y reposición IA
- **Autenticación JWT** segura
- **Tema claro/oscuro** con persistencia
- **Diseño responsive** y moderno

## 🛠️ Tecnologías Utilizadas

### Backend
- **Flask** - Framework web
- **JWT** - Autenticación
- **bcrypt** - Hash de contraseñas
- **CORS** - Comunicación frontend-backend

### Frontend
- **React** - Framework de UI
- **Tailwind CSS** - Estilos
- **Axios** - Cliente HTTP
- **Lucide React** - Iconos

### IA y Análisis
- **Análisis de churn** con scoring automático
- **Sugerencias de ofertas** personalizadas
- **Optimización de precios** basada en IA
- **Planes de reposición** inteligentes

## 🏗️ Arquitectura

```
LoyalLight/
├── backend/                 # Backend original FastAPI
├── backend_simple/         # Backend simplificado FastAPI
├── frontend/               # Frontend React
├── ai_knowledge/          # PDFs de conocimiento IA
├── loyallight-backend/    # Backend Flask desplegado
└── project_structure.md   # Documentación de arquitectura
```

## 🚀 Ejecución Local

### Opción 1: Aplicación Completa (Recomendada)

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/mago8bueno/LoyalLight.git
   cd LoyalLight
   ```

2. **Ejecutar el backend:**
   ```bash
   cd backend_simple
   python main.py
   ```
   El backend estará disponible en `http://localhost:8001`

3. **Ejecutar el frontend:**
   ```bash
   cd frontend
   npm install
   npm start
   ```
   El frontend estará disponible en `http://localhost:3000`

### Opción 2: Aplicación Integrada (Flask)

1. **Navegar al directorio Flask:**
   ```bash
   cd loyallight-backend
   ```

2. **Activar el entorno virtual:**
   ```bash
   source venv/bin/activate
   ```

3. **Ejecutar la aplicación:**
   ```bash
   python src/main.py
   ```
   La aplicación completa estará disponible en `http://localhost:5000`

## 📱 Funcionalidades Principales

### Dashboard
- **Métricas clave:** Total clientes, ventas, productos activos
- **Alertas del sistema:** Stock bajo, riesgo de churn
- **Top 5 clientes fieles** por valor de compras
- **Análisis de churn** con sugerencias IA por cliente
- **Gráfico de ventas** de los últimos 7 días
- **Insights globales de IA** actualizables

### Gestión de Clientes
- **Lista completa** con información de contacto
- **Formulario de registro** (Nombre, Apellido, Email)
- **Indicadores de riesgo** de churn con colores
- **Historial de compras** por cliente

### Gestión de Compras
- **Formulario completo** de registro de compras
- **Selección de cliente** desde dropdown
- **Cálculo automático** de totales
- **Sugerencias de ofertas IA** contextuales
- **Historial de compras** con filtros

### Gestión de Stock
- **Formulario de productos** con subida de imágenes
- **Control de stock** actual y mínimo
- **Sugerencias de precios IA** basadas en mercado
- **Plan de reposición mensual** automatizado
- **Gráficos de stock** interactivos

## 🤖 Integración de IA

### Características de IA Implementadas

1. **Análisis de Churn:**
   - Scoring automático de riesgo de abandono
   - Sugerencias personalizadas por cliente
   - Identificación de patrones de comportamiento

2. **Optimización de Ofertas:**
   - Promociones contextuales
   - Análisis de preferencias de compra
   - Estrategias de retención personalizadas

3. **Gestión de Inventario:**
   - Sugerencias de precios competitivos
   - Planes de reposición basados en demanda
   - Análisis de rotación de productos

4. **Insights Globales:**
   - Tendencias de mercado identificadas
   - Recomendaciones estratégicas
   - Análisis de patrones estacionales

### Base de Conocimiento
- **PDFs integrados** con conocimiento especializado
- **Respuestas contextuales** sin citar fuentes
- **Caché de respuestas** para optimización
- **Rate limiting** para control de uso

## 🔐 Seguridad

- **Autenticación JWT** con tokens seguros
- **Contraseñas hasheadas** con bcrypt + salt
- **CORS configurado** para comunicación segura
- **Validación de entrada** en todos los endpoints
- **Sesiones persistentes** con renovación automática

## 🎨 Diseño y UX

### Características de Diseño
- **Tema claro/oscuro** con persistencia en localStorage
- **Diseño responsive** para desktop y móvil
- **Navegación lateral fija** con logo corporativo
- **Iconografía consistente** con Lucide React
- **Paleta de colores** profesional y accesible

### Experiencia de Usuario
- **Feedback visual** en todas las acciones
- **Estados de carga** para operaciones asíncronas
- **Validación en tiempo real** de formularios
- **Mensajes de error** informativos
- **Navegación intuitiva** entre secciones

## 📊 Datos de Prueba

### Usuarios Predefinidos
- **admin:** Acceso completo al sistema
- **cliente1-cliente10:** Usuarios de prueba con diferentes perfiles

### Datos de Ejemplo
- **3 clientes** con diferentes niveles de riesgo de churn
- **3 productos** con variaciones de stock
- **2 compras** de ejemplo con diferentes valores
- **Métricas calculadas** automáticamente

## 🔧 Configuración Avanzada

### Variables de Entorno
```bash
# Backend
SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Frontend
REACT_APP_API_URL=http://localhost:8001
```

### Personalización
- **Logos:** Reemplazar archivos en `/frontend/public/`
- **Colores:** Modificar `tailwind.config.js`
- **Datos:** Actualizar mock database en backend
- **IA:** Configurar respuestas en `ai_responses`

## 📈 Métricas y Análisis

### KPIs Implementados
- **Valor promedio de pedido** calculado dinámicamente
- **Tasa de churn** por cliente con scoring
- **Rotación de inventario** por producto
- **Tendencias de ventas** con gráficos temporales

### Reportes Disponibles
- **Dashboard ejecutivo** con métricas clave
- **Análisis de clientes** con segmentación
- **Rendimiento de productos** con alertas
- **Proyecciones de IA** para toma de decisiones

## 🚀 Despliegue en Producción

### Aplicación Desplegada
La aplicación está disponible en: **https://qjh9iec5pdpo.manus.space**

### Características del Despliegue
- **Backend Flask** optimizado para producción
- **Frontend React** compilado y optimizado
- **Servicio integrado** en un solo dominio
- **HTTPS** habilitado por defecto
- **CDN** para recursos estáticos

## 🤝 Contribución

### Estructura del Código
- **Componentes modulares** en React
- **Separación de responsabilidades** en backend
- **Documentación inline** en código crítico
- **Convenciones de naming** consistentes

### Próximas Mejoras
- [ ] Base de datos persistente (PostgreSQL/MongoDB)
- [ ] Autenticación OAuth2
- [ ] Notificaciones push
- [ ] Exportación de reportes PDF
- [ ] API de terceros para análisis avanzado

## 📞 Soporte

Para soporte técnico o consultas sobre la implementación:
- **Repositorio:** https://github.com/mago8bueno/LoyalLight
- **Documentación:** Ver archivos en `/docs/`
- **Issues:** Reportar en GitHub Issues

---

**Desarrollado con ❤️ para la gestión eficiente de clientes**

