"""
AI service with PDF knowledge integration.
"""
import os
import json
import hashlib
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import openai
from sentence_transformers import SentenceTransformer
import PyPDF2
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from .config import settings
from .database import get_database


class AIService:
    """AI service with PDF knowledge base."""
    
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.openai_api_key)
        self.embeddings_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.knowledge_base = []
        self.embeddings = None
        self._load_knowledge_base()
    
    def _load_knowledge_base(self):
        """Load and process PDF knowledge base."""
        pdf_dir = os.path.join(os.path.dirname(__file__), "../../../ai_knowledge")
        
        if not os.path.exists(pdf_dir):
            return
        
        for filename in os.listdir(pdf_dir):
            if filename.endswith('.pdf'):
                pdf_path = os.path.join(pdf_dir, filename)
                text_chunks = self._extract_pdf_text(pdf_path)
                self.knowledge_base.extend(text_chunks)
        
        if self.knowledge_base:
            self.embeddings = self.embeddings_model.encode(self.knowledge_base)
    
    def _extract_pdf_text(self, pdf_path: str) -> List[str]:
        """Extract text chunks from PDF."""
        chunks = []
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                
                # Split into chunks of ~500 words
                words = text.split()
                chunk_size = 500
                for i in range(0, len(words), chunk_size):
                    chunk = " ".join(words[i:i + chunk_size])
                    if len(chunk.strip()) > 100:  # Only keep substantial chunks
                        chunks.append(chunk.strip())
        except Exception as e:
            print(f"Error processing PDF {pdf_path}: {e}")
        
        return chunks
    
    def _get_relevant_context(self, query: str, top_k: int = 3) -> str:
        """Get relevant context from knowledge base."""
        if not self.knowledge_base or self.embeddings is None:
            return ""
        
        query_embedding = self.embeddings_model.encode([query])
        similarities = cosine_similarity(query_embedding, self.embeddings)[0]
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        relevant_chunks = [self.knowledge_base[i] for i in top_indices if similarities[i] > 0.3]
        return "\n\n".join(relevant_chunks)
    
    async def _get_cached_response(self, cache_key: str) -> Optional[str]:
        """Get cached AI response."""
        if not settings.ai_cache_enabled:
            return None
        
        db = get_database()
        cached = await db.ai_cache.find_one({"key": cache_key})
        
        if cached and cached["expires_at"] > datetime.utcnow():
            return cached["response"]
        
        return None
    
    async def _cache_response(self, cache_key: str, response: str):
        """Cache AI response."""
        if not settings.ai_cache_enabled:
            return
        
        db = get_database()
        expires_at = datetime.utcnow() + timedelta(seconds=settings.cache_ttl_seconds)
        
        await db.ai_cache.update_one(
            {"key": cache_key},
            {
                "$set": {
                    "key": cache_key,
                    "response": response,
                    "expires_at": expires_at,
                    "created_at": datetime.utcnow()
                }
            },
            upsert=True
        )
    
    def _create_cache_key(self, prompt: str, context: str = "") -> str:
        """Create cache key for AI request."""
        content = f"{prompt}:{context}"
        return hashlib.md5(content.encode()).hexdigest()
    
    async def _make_ai_request(self, prompt: str, context: str = "") -> str:
        """Make AI request with caching."""
        cache_key = self._create_cache_key(prompt, context)
        
        # Check cache first
        cached_response = await self._get_cached_response(cache_key)
        if cached_response:
            return cached_response
        
        # Get relevant knowledge
        relevant_context = self._get_relevant_context(prompt)
        
        # Construct system message
        system_message = """Eres un experto en experiencia del cliente y gestión de relaciones comerciales. 
        Proporciona sugerencias prácticas y específicas basadas en mejores prácticas del sector.
        Mantén las respuestas concisas y accionables. No menciones fuentes específicas."""
        
        if relevant_context:
            system_message += f"\n\nContexto relevante:\n{relevant_context}"
        
        if context:
            system_message += f"\n\nDatos del sistema:\n{context}"
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=settings.ai_max_tokens,
                temperature=settings.ai_temperature
            )
            
            ai_response = response.choices[0].message.content
            
            # Cache the response
            await self._cache_response(cache_key, ai_response)
            
            return ai_response
            
        except Exception as e:
            return f"Error al generar sugerencia: {str(e)}"
    
    async def get_churn_reduction_suggestions(self, client_data: Dict[str, Any]) -> str:
        """Get suggestions to reduce client churn."""
        context = f"""
        Cliente: {client_data.get('nombre', '')} {client_data.get('apellido', '')}
        Puntuación de churn: {client_data.get('churn_score', 0)}
        Total de compras: {client_data.get('total_compras', 0)}
        Valor total: ${client_data.get('valor_total', 0)}
        """
        
        prompt = f"""
        Un cliente tiene una puntuación de churn de {client_data.get('churn_score', 0):.2f}.
        ¿Qué estrategias específicas recomendarías para reducir el riesgo de que este cliente abandone?
        Proporciona 3-4 acciones concretas y personalizadas.
        """
        
        return await self._make_ai_request(prompt, context)
    
    async def get_offer_suggestions(self, purchase_data: List[Dict[str, Any]], client_data: List[Dict[str, Any]]) -> str:
        """Get offer suggestions based on purchase patterns."""
        context = f"""
        Datos de compras recientes: {json.dumps(purchase_data[:10], default=str)}
        Datos de clientes: {json.dumps(client_data[:5], default=str)}
        """
        
        prompt = """
        Basándote en los patrones de compra y el comportamiento de los clientes,
        ¿qué ofertas o promociones específicas recomendarías para aumentar las ventas?
        Proporciona 3-4 sugerencias concretas con justificación.
        """
        
        return await self._make_ai_request(prompt, context)
    
    async def get_pricing_suggestions(self, product_data: Dict[str, Any], market_context: str = "") -> str:
        """Get pricing suggestions for products."""
        context = f"""
        Producto: {product_data.get('nombre_producto', '')}
        Precio actual: ${product_data.get('precio', 0)}
        Stock actual: {product_data.get('stock_actual', 0)}
        {market_context}
        """
        
        prompt = f"""
        Para el producto "{product_data.get('nombre_producto', '')}" con precio actual de ${product_data.get('precio', 0)},
        ¿qué estrategia de precios recomendarías? Considera factores como demanda, competencia y rentabilidad.
        Proporciona recomendaciones específicas.
        """
        
        return await self._make_ai_request(prompt, context)
    
    async def get_restock_plan(self, product_data: List[Dict[str, Any]], sales_data: List[Dict[str, Any]]) -> str:
        """Get monthly restock plan suggestions."""
        context = f"""
        Productos en stock: {json.dumps(product_data, default=str)}
        Datos de ventas: {json.dumps(sales_data, default=str)}
        """
        
        prompt = """
        Basándote en los niveles de stock actuales y los patrones de venta,
        ¿qué plan de reposición mensual recomendarías? Incluye cantidades específicas
        y prioridades para cada producto.
        """
        
        return await self._make_ai_request(prompt, context)
    
    async def get_global_insights(self, dashboard_data: Dict[str, Any]) -> str:
        """Get global business insights."""
        context = f"""
        Métricas del dashboard: {json.dumps(dashboard_data, default=str)}
        """
        
        prompt = """
        Basándote en las métricas generales del negocio, ¿qué insights estratégicos
        y recomendaciones de mejora proporcionarías? Enfócate en oportunidades
        de crecimiento y optimización.
        """
        
        return await self._make_ai_request(prompt, context)


# Global AI service instance
ai_service = AIService()

