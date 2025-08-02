import React, { useState } from 'react';
import { TrendingDown, Brain, Eye, ChevronRight } from 'lucide-react';
import { aiAPI } from '../../services/api';

const ChurnAnalysis = ({ churnClients = [] }) => {
  const [showAll, setShowAll] = useState(false);
  const [suggestions, setSuggestions] = useState({});
  const [loadingSuggestions, setLoadingSuggestions] = useState({});

  const getRiskColor = (risk) => {
    switch (risk) {
      case 'high':
        return 'text-red-600 dark:text-red-400 bg-red-100 dark:bg-red-900/20';
      case 'medium':
        return 'text-orange-600 dark:text-orange-400 bg-orange-100 dark:bg-orange-900/20';
      default:
        return 'text-yellow-600 dark:text-yellow-400 bg-yellow-100 dark:bg-yellow-900/20';
    }
  };

  const getRiskLabel = (risk) => {
    switch (risk) {
      case 'high':
        return 'Alto';
      case 'medium':
        return 'Medio';
      default:
        return 'Bajo';
    }
  };

  const handleGetSuggestions = async (clientId) => {
    setLoadingSuggestions(prev => ({ ...prev, [clientId]: true }));
    
    try {
      const response = await aiAPI.getChurnSuggestions(clientId);
      setSuggestions(prev => ({ 
        ...prev, 
        [clientId]: response.data.suggestions 
      }));
    } catch (error) {
      console.error('Error getting AI suggestions:', error);
      setSuggestions(prev => ({ 
        ...prev, 
        [clientId]: 'Error al obtener sugerencias de IA' 
      }));
    } finally {
      setLoadingSuggestions(prev => ({ ...prev, [clientId]: false }));
    }
  };

  const displayClients = showAll ? churnClients : churnClients.slice(0, 5);

  if (churnClients.length === 0) {
    return (
      <div className="card">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          Top 5 Riesgo de Churn
        </h2>
        <div className="text-center py-8">
          <TrendingDown className="w-12 h-12 text-green-500 mx-auto mb-4" />
          <p className="text-gray-600 dark:text-gray-400">
            ¡Excelente! No hay clientes con alto riesgo de abandono
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-white flex items-center">
          <TrendingDown className="w-5 h-5 text-red-500 mr-2" />
          Top 5 Riesgo de Churn
        </h2>
        {churnClients.length > 5 && (
          <button
            onClick={() => setShowAll(!showAll)}
            className="text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300 text-sm font-medium flex items-center"
          >
            {showAll ? 'Ver menos' : 'Ver más'}
            <ChevronRight className={`w-4 h-4 ml-1 transition-transform ${showAll ? 'rotate-90' : ''}`} />
          </button>
        )}
      </div>
      
      <div className="space-y-4">
        {displayClients.map((clientData) => {
          const client = clientData.client || clientData;
          const risk = clientData.churn_risk || 'medium';
          const churnScore = clientData.churn_score || client.churn_score || 0;
          
          return (
            <div
              key={client.id}
              className="border border-gray-200 dark:border-gray-700 rounded-lg p-4 space-y-3"
            >
              {/* Client Header */}
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="font-medium text-gray-900 dark:text-white">
                    {client.nombre} {client.apellido}
                  </h3>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    {client.correo_electronico}
                  </p>
                </div>
                <div className="text-right">
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${getRiskColor(risk)}`}>
                    Riesgo {getRiskLabel(risk)}
                  </span>
                  <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                    Score: {(churnScore * 100).toFixed(1)}%
                  </p>
                </div>
              </div>

              {/* Client Stats */}
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="text-gray-600 dark:text-gray-400">Compras:</span>
                  <span className="ml-2 font-medium text-gray-900 dark:text-white">
                    {client.total_compras || 0}
                  </span>
                </div>
                <div>
                  <span className="text-gray-600 dark:text-gray-400">Valor total:</span>
                  <span className="ml-2 font-medium text-gray-900 dark:text-white">
                    ${(client.valor_total || 0).toLocaleString()}
                  </span>
                </div>
              </div>

              {/* AI Suggestions */}
              <div className="border-t border-gray-200 dark:border-gray-700 pt-3">
                {suggestions[client.id] ? (
                  <div className="bg-blue-50 dark:bg-blue-900/20 p-3 rounded-lg">
                    <h4 className="text-sm font-medium text-blue-900 dark:text-blue-100 mb-2 flex items-center">
                      <Brain className="w-4 h-4 mr-1" />
                      Sugerencias IA para reducir churn:
                    </h4>
                    <p className="text-sm text-blue-800 dark:text-blue-200">
                      {suggestions[client.id]}
                    </p>
                  </div>
                ) : (
                  <button
                    onClick={() => handleGetSuggestions(client.id)}
                    disabled={loadingSuggestions[client.id]}
                    className="w-full btn-secondary text-sm flex items-center justify-center space-x-2"
                  >
                    {loadingSuggestions[client.id] ? (
                      <div className="spinner" />
                    ) : (
                      <Brain className="w-4 h-4" />
                    )}
                    <span>
                      {loadingSuggestions[client.id] 
                        ? 'Generando sugerencias...' 
                        : 'Sugerencia IA para reducir churn'
                      }
                    </span>
                  </button>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default ChurnAnalysis;

