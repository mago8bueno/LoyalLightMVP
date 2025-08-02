"""
Mock AI Service for development without heavy dependencies
"""
import random
from typing import List, Dict, Any
import asyncio

class MockAIService:
    def __init__(self):
        self.mock_responses = {
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
                "Oferta especial de fin de mes: envío gratis en todas las compras.",
                "Descuento progresivo: 5% en la segunda compra, 10% en la tercera, 15% en la cuarta.",
                "Promoción flash de 24 horas con 25% de descuento en productos seleccionados.",
                "Combo familiar con descuentos especiales para compras en volumen."
            ],
            "pricing_suggestions": [
                "Basado en el análisis de mercado, considera aumentar el precio en un 8-12% para maximizar márgenes.",
                "El precio actual está alineado con la competencia. Mantén la estrategia actual.",
                "Hay oportunidad de implementar precios dinámicos según la demanda estacional.",
                "Considera ofrecer diferentes niveles de precios (básico, premium, deluxe) para segmentar el mercado.",
                "El análisis sugiere que puedes reducir el precio en 5% para aumentar el volumen de ventas."
            ],
            "restock_plan": [
                "Plan de reposición mensual:\n\n1. Productos de alta rotación: reabastecer cada 2 semanas\n2. Productos estacionales: aumentar stock 30% antes de temporada alta\n3. Productos de baja rotación: revisar cada mes y ajustar según tendencias\n4. Nuevos productos: comenzar con stock conservador y ajustar según demanda\n5. Productos promocionales: coordinar reposición con campañas de marketing",
                "Estrategia de inventario optimizada:\n\n• Implementar sistema Just-In-Time para productos perecederos\n• Mantener stock de seguridad del 20% para productos críticos\n• Negociar términos de pago extendidos con proveedores\n• Diversificar proveedores para reducir riesgos de desabastecimiento\n• Utilizar análisis predictivo para anticipar demanda futura"
            ],
            "global_insights": [
                "Análisis global del negocio:\n\n📊 Tendencias identificadas:\n• Los clientes muestran mayor preferencia por compras en línea\n• Incremento del 15% en ventas durante fines de semana\n• Los productos con mejor margen tienen menor rotación\n\n🎯 Recomendaciones estratégicas:\n• Implementar programa de fidelización para aumentar retención\n• Optimizar inventario basado en patrones estacionales\n• Desarrollar estrategia de marketing digital más agresiva\n• Considerar expansión de líneas de productos complementarios",
                "Insights de rendimiento empresarial:\n\n💡 Oportunidades detectadas:\n• Segmento de clientes premium con alto potencial de crecimiento\n• Productos con demanda insatisfecha en el mercado\n• Posibilidad de automatizar procesos para reducir costos operativos\n\n⚠️ Áreas de atención:\n• Algunos clientes muestran patrones de abandono\n• Necesidad de diversificar canales de venta\n• Optimizar cadena de suministro para mejorar márgenes\n• Implementar métricas de satisfacción del cliente"
            ]
        }
    
    async def get_churn_suggestions(self, client_id: int) -> str:
        """Generate mock churn reduction suggestions for a specific client"""
        await asyncio.sleep(0.5)  # Simulate API delay
        return random.choice(self.mock_responses["churn_suggestions"])
    
    async def get_offer_suggestions(self, limit: int = 10) -> str:
        """Generate mock offer suggestions"""
        await asyncio.sleep(0.7)  # Simulate API delay
        suggestions = random.sample(self.mock_responses["offer_suggestions"], min(limit, len(self.mock_responses["offer_suggestions"])))
        return "\n\n".join([f"{i+1}. {suggestion}" for i, suggestion in enumerate(suggestions)])
    
    async def get_pricing_suggestions(self, product_id: int) -> str:
        """Generate mock pricing suggestions for a specific product"""
        await asyncio.sleep(0.6)  # Simulate API delay
        return random.choice(self.mock_responses["pricing_suggestions"])
    
    async def get_restock_plan(self) -> str:
        """Generate mock restock plan"""
        await asyncio.sleep(0.8)  # Simulate API delay
        return random.choice(self.mock_responses["restock_plan"])
    
    async def get_global_insights(self) -> str:
        """Generate mock global business insights"""
        await asyncio.sleep(1.0)  # Simulate API delay
        return random.choice(self.mock_responses["global_insights"])

# Global instance
mock_ai_service = MockAIService()

