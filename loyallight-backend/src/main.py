import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
from typing import Optional
import random
import asyncio
from jose import JWTError, jwt
from passlib.context import CryptContext

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'

# Enable CORS
CORS(app, origins=["*"])

# Configuration
SECRET_KEY = "your-secret-key-here-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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

def get_current_user(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
    except JWTError:
        return None
    
    for user in db.users:
        if user["username"] == username:
            return user
    
    return None

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
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = None
    for u in db.users:
        if u["username"] == username:
            if verify_password(password, u["hashed_password"]):
                user = u
                break
    
    if not user:
        return jsonify({"detail": "Incorrect username or password"}), 401
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    
    return jsonify({
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    })

@app.route('/api/auth/me', methods=['GET'])
def read_users_me():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"detail": "Not authenticated"}), 401
    
    token = auth_header.split(' ')[1]
    user = get_current_user(token)
    if not user:
        return jsonify({"detail": "Not authenticated"}), 401
    
    return jsonify({
        "id": user["id"],
        "username": user["username"],
        "role": user["role"],
        "is_active": user.get("is_active", True)
    })

@app.route('/api/clients', methods=['GET'])
def get_clients():
    return jsonify([{
        **client,
        "fecha_registro": client["fecha_registro"].isoformat()
    } for client in db.clients])

@app.route('/api/clients', methods=['POST'])
def create_client():
    data = request.get_json()
    new_id = str(len(db.clients) + 1)
    client = {
        "id": new_id,
        "fecha_registro": datetime.now(),
        "total_compras": 0,
        "valor_total": 0.0,
        "churn_score": random.uniform(0.1, 0.3),
        **data
    }
    db.clients.append(client)
    return jsonify({
        **client,
        "fecha_registro": client["fecha_registro"].isoformat()
    })

@app.route('/api/purchases', methods=['GET'])
def get_purchases():
    return jsonify([{
        **purchase,
        "fecha": purchase["fecha"].isoformat()
    } for purchase in db.purchases])

@app.route('/api/purchases', methods=['POST'])
def create_purchase():
    data = request.get_json()
    new_id = str(len(db.purchases) + 1)
    
    # Get client info
    client = next((c for c in db.clients if c["id"] == data["cliente_id"]), None)
    
    purchase = {
        "id": new_id,
        "total": data["cantidad"] * data["precio_unitario"],
        "fecha": datetime.now(),
        "cliente_nombre": client["nombre"] if client else "Desconocido",
        "cliente_apellido": client["apellido"] if client else "",
        **data
    }
    db.purchases.append(purchase)
    return jsonify({
        **purchase,
        "fecha": purchase["fecha"].isoformat()
    })

@app.route('/api/stock', methods=['GET'])
def get_products():
    return jsonify([{
        **product,
        "fecha_creacion": product["fecha_creacion"].isoformat()
    } for product in db.products])

@app.route('/api/stock', methods=['POST'])
def create_product():
    data = request.get_json()
    new_id = str(len(db.products) + 1)
    product = {
        "id": new_id,
        "fecha_creacion": datetime.now(),
        **data
    }
    db.products.append(product)
    return jsonify({
        **product,
        "fecha_creacion": product["fecha_creacion"].isoformat()
    })

@app.route('/api/dashboard', methods=['GET'])
def get_dashboard():
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
    
    return jsonify({
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
        "top_clients": [{
            **client,
            "fecha_registro": client["fecha_registro"].isoformat()
        } for client in top_clients],
        "churn_analysis": [{
            **client,
            "fecha_registro": client["fecha_registro"].isoformat()
        } for client in churn_clients],
        "sales_chart": sales_data
    })

@app.route('/api/ai/churn-suggestions', methods=['POST'])
def get_churn_suggestions():
    return jsonify({"suggestions": random.choice(ai_responses["churn_suggestions"])})

@app.route('/api/ai/offer-suggestions', methods=['POST'])
def get_offer_suggestions():
    suggestions = random.sample(ai_responses["offer_suggestions"], min(3, len(ai_responses["offer_suggestions"])))
    return jsonify({"suggestions": "\\n\\n".join([f"{i+1}. {s}" for i, s in enumerate(suggestions)])})

@app.route('/api/ai/pricing-suggestions', methods=['POST'])
def get_pricing_suggestions():
    return jsonify({"suggestions": "Basado en el análisis de mercado, considera aumentar el precio en un 8-12% para maximizar márgenes."})

@app.route('/api/ai/restock-plan', methods=['POST'])
def get_restock_plan():
    return jsonify({"suggestions": "Plan de reposición mensual:\\n\\n1. Productos de alta rotación: reabastecer cada 2 semanas\\n2. Productos estacionales: aumentar stock 30% antes de temporada alta\\n3. Productos de baja rotación: revisar cada mes y ajustar según tendencias"})

@app.route('/api/ai/global-insights', methods=['POST'])
def get_global_insights():
    return jsonify({"insights": random.choice(ai_responses["global_insights"])})

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

