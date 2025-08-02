import React, { useState, useEffect } from 'react';
import { 
  Users, 
  Package, 
  ShoppingCart, 
  DollarSign,
  TrendingUp,
  AlertTriangle,
  Brain
} from 'lucide-react';
import { dashboardAPI, aiAPI } from '../../services/api';

const Dashboard = () => {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [aiInsights, setAiInsights] = useState('');
  const [loadingInsights, setLoadingInsights] = useState(false);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      const response = await dashboardAPI.getCompleteData();
      setDashboardData(response.data);
    } catch (error) {
      console.error('Error loading dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadAIInsights = async () => {
    setLoadingInsights(true);
    try {
      const response = await aiAPI.getGlobalInsights();
      setAiInsights(response.data.insights);
    } catch (error) {
      console.error('Error loading AI insights:', error);
      setAiInsights('Error al cargar insights de IA');
    } finally {
      setLoadingInsights(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600" />
      </div>
    );
  }

  const metrics = dashboardData?.metrics || {};
  const alerts = dashboardData?.alerts || {};
  const topClients = dashboardData?.top_clients || [];
  const churnAnalysis = dashboardData?.churn_analysis || [];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
          Dashboard
        </h1>
        <button
          onClick={loadAIInsights}
          disabled={loadingInsights}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center space-x-2"
        >
          {loadingInsights ? (
            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white" />
          ) : (
            <Brain className="w-4 h-4" />
          )}
          <span>Actualizar Insights IA</span>
        </button>
      </div>

      {/* Metrics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-400">Total Clientes</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">
                {metrics.total_clients || 0}
              </p>
            </div>
            <div className="p-3 bg-blue-100 dark:bg-blue-900/20 rounded-lg">
              <Users className="w-6 h-6 text-blue-600 dark:text-blue-400" />
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-400">Total Ventas</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">
                ${(metrics.total_sales || 0).toLocaleString()}
              </p>
            </div>
            <div className="p-3 bg-green-100 dark:bg-green-900/20 rounded-lg">
              <DollarSign className="w-6 h-6 text-green-600 dark:text-green-400" />
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-400">Productos Activos</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">
                {metrics.active_products || 0}
              </p>
            </div>
            <div className="p-3 bg-purple-100 dark:bg-purple-900/20 rounded-lg">
              <Package className="w-6 h-6 text-purple-600 dark:text-purple-400" />
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-400">Valor Promedio</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">
                ${(metrics.avg_order_value || 0).toLocaleString()}
              </p>
            </div>
            <div className="p-3 bg-yellow-100 dark:bg-yellow-900/20 rounded-lg">
              <ShoppingCart className="w-6 h-6 text-yellow-600 dark:text-yellow-400" />
            </div>
          </div>
        </div>
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column */}
        <div className="lg:col-span-2 space-y-6">
          {/* Alerts */}
          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Alertas del Sistema
            </h2>
            <div className="space-y-3">
              <div className="p-4 bg-orange-50 dark:bg-orange-900/20 border border-orange-200 dark:border-orange-800 rounded-lg">
                <div className="flex items-center space-x-3">
                  <AlertTriangle className="w-5 h-5 text-orange-500" />
                  <div>
                    <h3 className="font-medium text-gray-900 dark:text-white">Stock Bajo</h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      {alerts.low_stock || 0} productos con stock bajo
                    </p>
                  </div>
                </div>
              </div>
              <div className="p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
                <div className="flex items-center space-x-3">
                  <AlertTriangle className="w-5 h-5 text-red-500" />
                  <div>
                    <h3 className="font-medium text-gray-900 dark:text-white">Riesgo de Churn</h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      {alerts.high_churn || 0} clientes con alto riesgo de abandono
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* AI Insights */}
          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
              <Brain className="w-5 h-5 text-purple-500 mr-2" />
              Insights de IA
            </h2>
            {aiInsights ? (
              <div className="prose dark:prose-invert max-w-none">
                <p className="text-gray-700 dark:text-gray-300 whitespace-pre-line">
                  {aiInsights}
                </p>
              </div>
            ) : (
              <div className="text-center py-8">
                <Brain className="w-12 h-12 text-purple-400 mx-auto mb-4" />
                <p className="text-gray-600 dark:text-gray-400">
                  Haz clic en &quot;Actualizar&quot; para obtener insights de IA
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Right Column */}
        <div className="space-y-6">
          {/* Top Clients */}
          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Top 5 Clientes Fieles
            </h2>
            <div className="space-y-3">
              {topClients.length > 0 ? (
                topClients.slice(0, 5).map((client, index) => (
                  <div key={client.id || index} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                    <div>
                      <p className="font-medium text-gray-900 dark:text-white">
                        {client.nombre} {client.apellido}
                      </p>
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        {client.total_compras} compras
                      </p>
                    </div>
                    <div className="text-right">
                      <p className="font-semibold text-green-600 dark:text-green-400">
                        ${(client.valor_total || 0).toLocaleString()}
                      </p>
                    </div>
                  </div>
                ))
              ) : (
                <p className="text-gray-600 dark:text-gray-400 text-center py-4">
                  No hay datos de clientes disponibles
                </p>
              )}
            </div>
          </div>

          {/* Churn Analysis */}
          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Análisis de Churn
            </h2>
            <div className="space-y-3">
              {churnAnalysis.length > 0 ? (
                churnAnalysis.slice(0, 3).map((client, index) => (
                  <div key={client.id || index} className="p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="font-medium text-gray-900 dark:text-white">
                          {client.nombre} {client.apellido}
                        </p>
                        <p className="text-sm text-red-600 dark:text-red-400">
                          Riesgo: {Math.round((client.churn_score || 0) * 100)}%
                        </p>
                      </div>
                    </div>
                  </div>
                ))
              ) : (
                <p className="text-gray-600 dark:text-gray-400 text-center py-4">
                  No hay clientes en riesgo
                </p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

