import React from 'react';
import { Brain, RefreshCw } from 'lucide-react';

const AIInsights = ({ insights, loading, onRefresh }) => {
  return (
    <div className="card">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-white flex items-center">
          <Brain className="w-5 h-5 text-purple-500 mr-2" />
          Sugerencias IA Globales
        </h2>
        <button
          onClick={onRefresh}
          disabled={loading}
          className="btn-secondary text-sm flex items-center space-x-2"
        >
          {loading ? (
            <div className="spinner" />
          ) : (
            <RefreshCw className="w-4 h-4" />
          )}
          <span>Actualizar</span>
        </button>
      </div>
      
      <div className="bg-gradient-to-r from-purple-50 to-blue-50 dark:from-purple-900/20 dark:to-blue-900/20 rounded-lg p-4 border border-purple-200 dark:border-purple-800">
        {loading ? (
          <div className="flex items-center justify-center py-8">
            <div className="spinner w-6 h-6 mr-3" />
            <span className="text-gray-600 dark:text-gray-400">
              Generando insights con IA...
            </span>
          </div>
        ) : insights ? (
          <div className="prose prose-sm max-w-none">
            <p className="text-gray-800 dark:text-gray-200 leading-relaxed whitespace-pre-wrap">
              {insights}
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
      
      <div className="mt-3 text-xs text-gray-500 dark:text-gray-400 flex items-center">
        <Brain className="w-3 h-3 mr-1" />
        Insights generados por IA basados en datos del sistema y mejores prácticas del sector
      </div>
    </div>
  );
};

export default AIInsights;

