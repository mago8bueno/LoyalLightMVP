import React from 'react';
import { Crown, Mail, DollarSign } from 'lucide-react';

const TopClients = ({ clients = [] }) => {
  if (clients.length === 0) {
    return (
      <div className="card">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          Top 5 Clientes Más Fieles
        </h2>
        <div className="text-center py-8">
          <Crown className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-600 dark:text-gray-400">
            No hay datos de clientes disponibles
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="card">
      <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
        <Crown className="w-5 h-5 text-yellow-500 mr-2" />
        Top 5 Clientes Más Fieles
      </h2>
      
      <div className="space-y-4">
        {clients.map((clientData, index) => {
          const client = clientData.client || clientData;
          const ranking = clientData.ranking || index + 1;
          const loyaltyScore = clientData.loyalty_score || (1 - client.churn_score);
          
          return (
            <div
              key={client.id}
              className="flex items-center space-x-4 p-3 rounded-lg bg-gray-50 dark:bg-gray-700/50 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
            >
              {/* Ranking Badge */}
              <div className={`w-8 h-8 rounded-full flex items-center justify-center text-white font-bold text-sm ${
                ranking === 1 ? 'bg-yellow-500' :
                ranking === 2 ? 'bg-gray-400' :
                ranking === 3 ? 'bg-orange-600' :
                'bg-primary-500'
              }`}>
                {ranking}
              </div>
              
              {/* Client Info */}
              <div className="flex-1">
                <h3 className="font-medium text-gray-900 dark:text-white">
                  {client.nombre} {client.apellido}
                </h3>
                <div className="flex items-center space-x-4 text-sm text-gray-600 dark:text-gray-400">
                  <div className="flex items-center">
                    <Mail className="w-3 h-3 mr-1" />
                    {client.correo_electronico}
                  </div>
                  <div className="flex items-center">
                    <DollarSign className="w-3 h-3 mr-1" />
                    ${(client.valor_total || 0).toLocaleString()}
                  </div>
                </div>
              </div>
              
              {/* Loyalty Score */}
              <div className="text-right">
                <div className="text-sm font-medium text-gray-900 dark:text-white">
                  {(loyaltyScore * 100).toFixed(1)}%
                </div>
                <div className="text-xs text-gray-500 dark:text-gray-400">
                  Fidelidad
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default TopClients;

