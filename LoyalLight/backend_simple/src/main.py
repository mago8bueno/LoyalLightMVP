"""
Simplified FastAPI backend for LoyalLight MVP
"""
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime, timedelta
import random
import asyncio
from jose import JWTError, jwt
from passlib.context import CryptContext

# Configuration
SECRET_KEY = "your-secret-key-here-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

# Create FastAPI app
app = FastAPI(
    title="LoyalLight API",
    description="Customer Management System with AI Integration",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

class User(BaseModel):
    id: str
    username: str
    role: str
    is_active: bool

class ClientCreate(BaseModel):
    nombre: str
    apellido: str
    correo_electronico: EmailStr

class Client(BaseModel):
    id: str
    nombre: str
    apellido: str
    correo_electronico: str
    fecha_registro: datetime
    total_compras: int
    valor_total: float
    churn_score: float

class PurchaseCreate(BaseModel):
    producto_comprado: str
    cliente_id: str
    cantidad: int
    precio_unitario: float

class Purchase(BaseModel):
    id: str
    producto_comprado: str
    cliente_id: str
    cliente_nombre: str
    cliente_apellido: str
    cantidad: int
    precio_unitario: float
    total: float
    fecha: datetime

class ProductCreate(BaseModel):
    nombre_producto: str
    precio: float
    stock_actual: int
    stock_minimo: int

class Product(BaseModel):
    id: str
    nombre_producto: str
    precio: float
    stock_actual: int
    stock_minimo: int
    fecha_creacion: datetime

# Mock Database
class MockDB:
    def __init__(self):
        self.users = [
            {
                "id": "1",
                "username": "admin",
                "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # secret
                "role": "admin",
                "is_active": True
            }
        ]
        
        # Add client users
        for i in range(1, 11):
            self.users.append({
                "id": str(i + 1),
                "username": f"cliente{i}",
                "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # secret
                "role": "client",
                "is_active": True
            })
        
        self.clients = [
            {
                "id": "1",
                "nombre": "Juan",
                "apellido": "Pérez",
                "correo_electronico": "juan.perez@email.com",
                "fecha_registro": datetime.now() - timedelta(days=30),
                "total_compras": 5,
                "valor_total": 1250.50,
                "churn_score": 0.2
            },
            {
                "id": "2",
                "nombre": "María",
                "apellido": "García",
                "correo_electronico": "maria.garcia@email.com",
                "fecha_registro": datetime.now() - timedelta(days=45),
                "total_compras": 8,
                "valor_total": 2100.75,
                "churn_score": 0.1
            },
            {
                "id": "3",
                "nombre": "Carlos",
                "apellido": "López",
                "correo_electronico": "carlos.lopez@email.com",
                "fecha_registro": datetime.now() - timedelta(days=60),
                "total_compras": 2,
                "valor_total": 450.25,
                "churn_score": 0.8
            }
        ]
        
        self.products = [
            {
                "id": "1",
                "nombre_producto": "Laptop Gaming",
                "precio": 1299.99,
                "stock_actual": 15,
                "stock_minimo": 5,
                "fecha_creacion": datetime.now() - timedelta(days=20)
            },
            {
                "id": "2",
                "nombre_producto": "Mouse Inalámbrico",
                "precio": 49.99,
                "stock_actual": 3,
                "stock_minimo": 10,
                "fecha_creacion": datetime.now() - timedelta(days=15)
            },
            {
                "id": "3",
                "nombre_producto": "Teclado Mecánico",
                "precio": 129.99,
                "stock_actual": 25,
                "stock_minimo": 8,
                "fecha_creacion": datetime.now() - timedelta(days=10)
            }
        ]
        
        self.purchases = [
            {
                "id": "1",
                "producto_comprado": "Laptop Gaming",
                "cliente_id": "1",
                "cantidad": 1,
                "precio_unitario": 1299.99,
                "total": 1299.99,
                "fecha": datetime.now() - timedelta(days=5),
                "cliente_nombre": "Juan",
                "cliente_apellido": "Pérez"
            },
            {
                "id": "2",
                "producto_comprado": "Mouse Inalámbrico",
                "cliente_id": "2",
                "cantidad": 2,
                "precio_unitario": 49.99,
                "total": 99.98,
                "fecha": datetime.now() - timedelta(days=3),
                "cliente_nombre": "María",
                "cliente_apellido": "García"
            }
        ]

db = MockDB()

# Auth functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    for user in db.users:
        if user["username"] == username:
            return user
    
    raise credentials_exception

# Mock AI responses
ai_responses = {
    "churn_suggestions": [
        "Considera ofrecer un descuento del 15% en su próxima compra para incentivar la retención.",
        "Envía un email personalizado con productos relacionados a sus compras anteriores.",
        "Programa una llamada de seguimiento para entender mejor sus necesidades actuales.",
        "Ofrece un programa de fidelidad con puntos acumulables por cada compra.",
        "Proporciona acceso exclusivo a nuevos productos antes del lanzamiento público."
    ],
    "offer_suggestions": [
        "Promoción 2x1 en productos de temporada para aumentar el volumen de ventas.",
        "Descuento del 20% para clientes que compren más de $100 en una sola transacción.",
        "Bundle de productos complementarios con 15% de descuento.",
        "Programa de referidos: 10% de descuento por cada nuevo cliente referido.",
        "Oferta especial de fin de mes: envío gratis en todas las compras."
    ],
    "global_insights": [
        "Análisis global del negocio:\\n\\n📊 Tendencias identificadas:\\n• Los clientes muestran mayor preferencia por compras en línea\\n• Incremento del 15% en ventas durante fines de semana\\n• Los productos con mejor margen tienen menor rotación\\n\\n🎯 Recomendaciones estratégicas:\\n• Implementar programa de fidelización para aumentar retención\\n• Optimizar inventario basado en patrones estacionales\\n• Desarrollar estrategia de marketing digital más agresiva\\n• Considerar expansión de líneas de productos complementarios"
    ]
}

# Routes
@app.get("/")
async def root():
    return {"message": "LoyalLight API", "version": "1.0.0", "status": "running"}

@app.post("/api/auth/login", response_model=Token)
async def login(user_credentials: UserLogin):
    user = None
    for u in db.users:
        if u["username"] == user_credentials.username:
            if verify_password(user_credentials.password, u["hashed_password"]):
                user = u
                break
    
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }

@app.get("/api/auth/me", response_model=User)
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return User(
        id=current_user["id"],
        username=current_user["username"],
        role=current_user["role"],
        is_active=current_user.get("is_active", True)
    )

@app.get("/api/clients", response_model=List[Client])
async def get_clients(current_user: dict = Depends(get_current_user)):
    return [Client(**client) for client in db.clients]

@app.post("/api/clients", response_model=Client)
async def create_client(client_data: ClientCreate, current_user: dict = Depends(get_current_user)):
    new_id = str(len(db.clients) + 1)
    client = {
        "id": new_id,
        "fecha_registro": datetime.now(),
        "total_compras": 0,
        "valor_total": 0.0,
        "churn_score": random.uniform(0.1, 0.3),
        **client_data.dict()
    }
    db.clients.append(client)
    return Client(**client)

@app.get("/api/purchases", response_model=List[Purchase])
async def get_purchases(current_user: dict = Depends(get_current_user)):
    return [Purchase(**purchase) for purchase in db.purchases]

@app.post("/api/purchases", response_model=Purchase)
async def create_purchase(purchase_data: PurchaseCreate, current_user: dict = Depends(get_current_user)):
    new_id = str(len(db.purchases) + 1)
    
    # Get client info
    client = next((c for c in db.clients if c["id"] == purchase_data.cliente_id), None)
    
    purchase = {
        "id": new_id,
        "total": purchase_data.cantidad * purchase_data.precio_unitario,
        "fecha": datetime.now(),
        "cliente_nombre": client["nombre"] if client else "Desconocido",
        "cliente_apellido": client["apellido"] if client else "",
        **purchase_data.dict()
    }
    db.purchases.append(purchase)
    return Purchase(**purchase)

@app.get("/api/stock", response_model=List[Product])
async def get_products(current_user: dict = Depends(get_current_user)):
    return [Product(**product) for product in db.products]

@app.post("/api/stock", response_model=Product)
async def create_product(product_data: ProductCreate, current_user: dict = Depends(get_current_user)):
    new_id = str(len(db.products) + 1)
    product = {
        "id": new_id,
        "fecha_creacion": datetime.now(),
        **product_data.dict()
    }
    db.products.append(product)
    return Product(**product)

@app.get("/api/dashboard")
async def get_dashboard(current_user: dict = Depends(get_current_user)):
    total_clients = len(db.clients)
    total_sales = sum(p["total"] for p in db.purchases)
    avg_order_value = total_sales / len(db.purchases) if db.purchases else 0
    
    # Top clients by value
    top_clients = sorted(db.clients, key=lambda x: x["valor_total"], reverse=True)[:5]
    
    # High churn clients
    churn_clients = [c for c in db.clients if c["churn_score"] > 0.5][:5]
    
    # Low stock alerts
    low_stock = [p for p in db.products if p["stock_actual"] <= p["stock_minimo"]]
    
    # Sales data for chart (last 7 days)
    sales_data = []
    for i in range(7):
        date = datetime.now() - timedelta(days=i)
        daily_sales = sum(p["total"] for p in db.purchases if p["fecha"].date() == date.date())
        sales_data.append({
            "date": date.strftime("%Y-%m-%d"),
            "sales": daily_sales
        })
    
    return {
        "metrics": {
            "total_clients": total_clients,
            "total_sales": total_sales,
            "avg_order_value": avg_order_value,
            "active_products": len(db.products)
        },
        "alerts": {
            "low_stock": len(low_stock),
            "high_churn": len(churn_clients),
            "pending_orders": 0
        },
        "top_clients": top_clients,
        "churn_analysis": churn_clients,
        "sales_chart": sales_data
    }

@app.post("/api/ai/churn-suggestions")
async def get_churn_suggestions(data: dict, current_user: dict = Depends(get_current_user)):
    await asyncio.sleep(0.5)  # Simulate AI processing
    return {"suggestions": random.choice(ai_responses["churn_suggestions"])}

@app.post("/api/ai/offer-suggestions")
async def get_offer_suggestions(data: dict, current_user: dict = Depends(get_current_user)):
    await asyncio.sleep(0.7)  # Simulate AI processing
    suggestions = random.sample(ai_responses["offer_suggestions"], min(3, len(ai_responses["offer_suggestions"])))
    return {"suggestions": "\\n\\n".join([f"{i+1}. {s}" for i, s in enumerate(suggestions)])}

@app.post("/api/ai/pricing-suggestions")
async def get_pricing_suggestions(data: dict, current_user: dict = Depends(get_current_user)):
    await asyncio.sleep(0.6)  # Simulate AI processing
    return {"suggestions": "Basado en el análisis de mercado, considera aumentar el precio en un 8-12% para maximizar márgenes."}

@app.post("/api/ai/restock-plan")
async def get_restock_plan(current_user: dict = Depends(get_current_user)):
    await asyncio.sleep(0.8)  # Simulate AI processing
    return {"suggestions": "Plan de reposición mensual:\\n\\n1. Productos de alta rotación: reabastecer cada 2 semanas\\n2. Productos estacionales: aumentar stock 30% antes de temporada alta\\n3. Productos de baja rotación: revisar cada mes y ajustar según tendencias"}

@app.post("/api/ai/global-insights")
async def get_global_insights(current_user: dict = Depends(get_current_user)):
    await asyncio.sleep(1.0)  # Simulate AI processing
    return {"insights": random.choice(ai_responses["global_insights"])}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

