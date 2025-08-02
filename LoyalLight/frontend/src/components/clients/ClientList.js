import React, { useState, useEffect } from 'react';
import { Edit, Trash2, Mail, Calendar, TrendingDown } from 'lucide-react';
import { clientsAPI } from '../../services/api';
import { useAuth } from '../../hooks/useAuth';

const ClientList = ({ onEdit, refreshTrigger }) => {
  const [clients, setClients] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { isAdmin } = useAuth();

  useEffect(() => {
    loadClients();
  }, [refreshTrigger]);

  const loadClients = async () => {
    try {
      setLoading(true);
      const response = await clientsAPI.getClients();
      setClients(response.data);
      setError('');
    } catch (error) {
      console.error('Error loading clients:', error);
      setError('Error al cargar los clientes');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (clientId) => {
    if (!window.confirm('¿Estás seguro de que quieres eliminar este cliente?')) {
      return;
    }

    try {
      await clientsAPI.deleteClient(clientId);
      setClients(clients.filter(client => client.id !== clientId));
    } catch (error) {
      console.error('Error deleting client:', error);
      setError('Error al eliminar el cliente');
    }
  };

  const getChurnRiskColor = (score) => {
    if (score >= 0.7) return 'text-red-600 bg-red-100 dark:bg-red-900/20';
    if (score >= 0.4) return 'text-orange-600 bg-orange-100 dark:bg-orange-900/20';
    return 'text-green-600 bg-green-100 dark:bg-green-900/20';
  };

  const getChurnRiskLabel = (score) => {
    if (score >= 0.7) return 'Alto';
    if (score >= 0.4) return 'Medio';
    return 'Bajo';
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="spinner w-8 h-8" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="alert alert-error">
        {error}
      </div>
    );
  }

  if (clients.length === 0) {
    return (
      <div className="text-center py-12">
        <Mail className="w-16 h-16 text-gray-400 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
          No hay clientes registrados
        </h3>
        <p className="text-gray-600 dark:text-gray-400">
          Comienza agregando tu primer cliente usando el formulario de arriba.
        </p>
      </div>
    );
  }

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
        <thead className="bg-gray-50 dark:bg-gray-800">
          <tr>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
              Cliente
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
              Correo Electrónico
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
              Fecha Registro
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
              Compras
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
              Valor Total
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
              Riesgo Churn
            </th>
            <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
              Acciones
            </th>
          </tr>
        </thead>
        <tbody className="bg-white dark:bg-gray-900 divide-y divide-gray-200 dark:divide-gray-700">
          {clients.map((client) => (
            <tr key={client.id} className="hover:bg-gray-50 dark:hover:bg-gray-800">
              <td className="px-6 py-4 whitespace-nowrap">
                <div className="flex items-center">
                  <div className="w-10 h-10 bg-primary-600 rounded-full flex items-center justify-center">
                    <span className="text-white font-medium">
                      {client.nombre.charAt(0)}{client.apellido.charAt(0)}
                    </span>
                  </div>
                  <div className="ml-4">
                    <div className="text-sm font-medium text-gray-900 dark:text-white">
                      {client.nombre} {client.apellido}
                    </div>
                  </div>
                </div>
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                <div className="flex items-center text-sm text-gray-600 dark:text-gray-400">
                  <Mail className="w-4 h-4 mr-2" />
                  {client.correo_electronico}
                </div>
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                <div className="flex items-center text-sm text-gray-600 dark:text-gray-400">
                  <Calendar className="w-4 h-4 mr-2" />
                  {new Date(client.fecha_registro).toLocaleDateString()}
                </div>
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                {client.total_compras || 0}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                ${(client.valor_total || 0).toLocaleString()}
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getChurnRiskColor(client.churn_score)}`}>
                  <TrendingDown className="w-3 h-3 mr-1" />
                  {getChurnRiskLabel(client.churn_score)} ({(client.churn_score * 100).toFixed(1)}%)
                </span>
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <div className="flex items-center justify-end space-x-2">
                  <button
                    onClick={() => onEdit(client)}
                    className="text-primary-600 hover:text-primary-900 dark:text-primary-400 dark:hover:text-primary-300"
                  >
                    <Edit className="w-4 h-4" />
                  </button>
                  {isAdmin && (
                    <button
                      onClick={() => handleDelete(client.id)}
                      className="text-red-600 hover:text-red-900 dark:text-red-400 dark:hover:text-red-300"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  )}
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ClientList;

