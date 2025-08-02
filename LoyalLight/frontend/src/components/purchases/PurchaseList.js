import React, { useState, useEffect } from 'react';
import { Edit, Trash2, Package, Calendar, DollarSign } from 'lucide-react';
import { purchasesAPI } from '../../services/api';
import { useAuth } from '../../hooks/useAuth';

const PurchaseList = ({ onEdit, refreshTrigger }) => {
  const [purchases, setPurchases] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { isAdmin } = useAuth();

  useEffect(() => {
    loadPurchases();
  }, [refreshTrigger]);

  const loadPurchases = async () => {
    try {
      setLoading(true);
      const response = await purchasesAPI.getPurchases();
      setPurchases(response.data);
      setError('');
    } catch (error) {
      console.error('Error loading purchases:', error);
      setError('Error al cargar las compras');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (purchaseId) => {
    if (!window.confirm('¿Estás seguro de que quieres eliminar esta compra?')) {
      return;
    }

    try {
      await purchasesAPI.deletePurchase(purchaseId);
      setPurchases(purchases.filter(purchase => purchase.id !== purchaseId));
    } catch (error) {
      console.error('Error deleting purchase:', error);
      setError('Error al eliminar la compra');
    }
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

  if (purchases.length === 0) {
    return (
      <div className="text-center py-12">
        <Package className="w-16 h-16 text-gray-400 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
          No hay compras registradas
        </h3>
        <p className="text-gray-600 dark:text-gray-400">
          Comienza registrando la primera compra usando el formulario de arriba.
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
              Producto
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
              Cliente
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
              Cantidad
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
              Precio Unitario
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
              Total
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
              Fecha
            </th>
            <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
              Acciones
            </th>
          </tr>
        </thead>
        <tbody className="bg-white dark:bg-gray-900 divide-y divide-gray-200 dark:divide-gray-700">
          {purchases.map((purchase) => (
            <tr key={purchase.id} className="hover:bg-gray-50 dark:hover:bg-gray-800">
              <td className="px-6 py-4 whitespace-nowrap">
                <div className="flex items-center">
                  <div className="w-10 h-10 bg-green-600 rounded-lg flex items-center justify-center">
                    <Package className="w-5 h-5 text-white" />
                  </div>
                  <div className="ml-4">
                    <div className="text-sm font-medium text-gray-900 dark:text-white">
                      {purchase.producto_comprado}
                    </div>
                  </div>
                </div>
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                <div className="text-sm text-gray-900 dark:text-white">
                  {purchase.cliente_nombre && purchase.cliente_apellido 
                    ? `${purchase.cliente_nombre} ${purchase.cliente_apellido}`
                    : 'Cliente no encontrado'
                  }
                </div>
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                {purchase.cantidad}
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                <div className="flex items-center text-sm text-gray-600 dark:text-gray-400">
                  <DollarSign className="w-4 h-4 mr-1" />
                  {purchase.precio_unitario.toFixed(2)}
                </div>
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                <div className="flex items-center text-sm font-medium text-gray-900 dark:text-white">
                  <DollarSign className="w-4 h-4 mr-1" />
                  {purchase.total.toFixed(2)}
                </div>
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                <div className="flex items-center text-sm text-gray-600 dark:text-gray-400">
                  <Calendar className="w-4 h-4 mr-2" />
                  {new Date(purchase.fecha).toLocaleDateString()}
                </div>
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <div className="flex items-center justify-end space-x-2">
                  <button
                    onClick={() => onEdit(purchase)}
                    className="text-primary-600 hover:text-primary-900 dark:text-primary-400 dark:hover:text-primary-300"
                  >
                    <Edit className="w-4 h-4" />
                  </button>
                  {isAdmin && (
                    <button
                      onClick={() => handleDelete(purchase.id)}
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

export default PurchaseList;

