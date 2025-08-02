import React, { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { Save, X, ShoppingCart, Brain } from 'lucide-react';
import { purchasesAPI, clientsAPI, aiAPI } from '../../services/api';

const PurchaseForm = ({ purchase, onSave, onCancel }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [clients, setClients] = useState([]);
  const [loadingClients, setLoadingClients] = useState(true);
  const [aiSuggestions, setAiSuggestions] = useState('');
  const [loadingSuggestions, setLoadingSuggestions] = useState(false);
  
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
    setValue,
    watch
  } = useForm();

  const watchedFields = watch();

  useEffect(() => {
    loadClients();
  }, []);

  useEffect(() => {
    if (purchase) {
      setValue('producto_comprado', purchase.producto_comprado);
      setValue('cliente_id', purchase.cliente_id);
      setValue('cantidad', purchase.cantidad);
      setValue('fecha', new Date(purchase.fecha).toISOString().split('T')[0]);
      setValue('precio_unitario', purchase.precio_unitario);
    } else {
      reset();
      setValue('fecha', new Date().toISOString().split('T')[0]);
    }
  }, [purchase, setValue, reset]);

  const loadClients = async () => {
    try {
      const response = await clientsAPI.getClients();
      setClients(response.data);
    } catch (error) {
      console.error('Error loading clients:', error);
    } finally {
      setLoadingClients(false);
    }
  };

  const handleGetOfferSuggestions = async () => {
    setLoadingSuggestions(true);
    try {
      const response = await aiAPI.getOfferSuggestions(10);
      setAiSuggestions(response.data.suggestions);
    } catch (error) {
      console.error('Error getting AI suggestions:', error);
      setAiSuggestions('Error al obtener sugerencias de IA');
    } finally {
      setLoadingSuggestions(false);
    }
  };

  const onSubmit = async (data) => {
    setLoading(true);
    setError('');

    try {
      // Convert date string to ISO format
      const formData = {
        ...data,
        fecha: new Date(data.fecha).toISOString(),
        cantidad: parseInt(data.cantidad),
        precio_unitario: parseFloat(data.precio_unitario)
      };

      if (purchase) {
        // Update existing purchase
        await purchasesAPI.updatePurchase(purchase.id, formData);
      } else {
        // Create new purchase
        await purchasesAPI.createPurchase(formData);
      }
      
      onSave();
      if (!purchase) {
        reset(); // Only reset form for new purchases
        setValue('fecha', new Date().toISOString().split('T')[0]);
      }
    } catch (error) {
      console.error('Error saving purchase:', error);
      setError(error.response?.data?.detail || 'Error al guardar la compra');
    } finally {
      setLoading(false);
    }
  };

  const calculateTotal = () => {
    const cantidad = parseInt(watchedFields.cantidad) || 0;
    const precio = parseFloat(watchedFields.precio_unitario) || 0;
    return cantidad * precio;
  };

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-white flex items-center">
          <ShoppingCart className="w-5 h-5 mr-2" />
          {purchase ? 'Editar Compra' : 'Registrar Nueva Compra'}
        </h2>
        {purchase && (
          <button
            onClick={onCancel}
            className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
          >
            <X className="w-5 h-5" />
          </button>
        )}
      </div>

      {error && (
        <div className="alert alert-error mb-6">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Producto Comprado */}
          <div>
            <label htmlFor="producto_comprado" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Producto Comprado *
            </label>
            <input
              type="text"
              id="producto_comprado"
              {...register('producto_comprado', {
                required: 'El producto es requerido',
                minLength: {
                  value: 1,
                  message: 'El producto debe tener al menos 1 carácter'
                },
                maxLength: {
                  value: 200,
                  message: 'El producto no puede exceder 200 caracteres'
                }
              })}
              className={`input-field ${errors.producto_comprado ? 'border-red-500' : ''}`}
              placeholder="Nombre del producto"
            />
            {errors.producto_comprado && (
              <p className="mt-1 text-sm text-red-600 dark:text-red-400">
                {errors.producto_comprado.message}
              </p>
            )}
          </div>

          {/* Cliente que Compra */}
          <div>
            <label htmlFor="cliente_id" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Cliente que Compra *
            </label>
            <select
              id="cliente_id"
              {...register('cliente_id', {
                required: 'El cliente es requerido'
              })}
              className={`input-field ${errors.cliente_id ? 'border-red-500' : ''}`}
              disabled={loadingClients}
            >
              <option value="">Selecciona un cliente</option>
              {clients.map((client) => (
                <option key={client.id} value={client.id}>
                  {client.nombre} {client.apellido} - {client.correo_electronico}
                </option>
              ))}
            </select>
            {errors.cliente_id && (
              <p className="mt-1 text-sm text-red-600 dark:text-red-400">
                {errors.cliente_id.message}
              </p>
            )}
          </div>

          {/* Cantidad */}
          <div>
            <label htmlFor="cantidad" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Cantidad *
            </label>
            <input
              type="number"
              id="cantidad"
              min="1"
              {...register('cantidad', {
                required: 'La cantidad es requerida',
                min: {
                  value: 1,
                  message: 'La cantidad debe ser mayor a 0'
                }
              })}
              className={`input-field ${errors.cantidad ? 'border-red-500' : ''}`}
              placeholder="1"
            />
            {errors.cantidad && (
              <p className="mt-1 text-sm text-red-600 dark:text-red-400">
                {errors.cantidad.message}
              </p>
            )}
          </div>

          {/* Fecha */}
          <div>
            <label htmlFor="fecha" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Fecha *
            </label>
            <input
              type="date"
              id="fecha"
              {...register('fecha', {
                required: 'La fecha es requerida'
              })}
              className={`input-field ${errors.fecha ? 'border-red-500' : ''}`}
            />
            {errors.fecha && (
              <p className="mt-1 text-sm text-red-600 dark:text-red-400">
                {errors.fecha.message}
              </p>
            )}
          </div>

          {/* Precio Unitario */}
          <div>
            <label htmlFor="precio_unitario" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Precio Unitario *
            </label>
            <input
              type="number"
              id="precio_unitario"
              step="0.01"
              min="0.01"
              {...register('precio_unitario', {
                required: 'El precio unitario es requerido',
                min: {
                  value: 0.01,
                  message: 'El precio debe ser mayor a 0'
                }
              })}
              className={`input-field ${errors.precio_unitario ? 'border-red-500' : ''}`}
              placeholder="0.00"
            />
            {errors.precio_unitario && (
              <p className="mt-1 text-sm text-red-600 dark:text-red-400">
                {errors.precio_unitario.message}
              </p>
            )}
          </div>

          {/* Total Calculado */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Total Calculado
            </label>
            <div className="input-field bg-gray-50 dark:bg-gray-700 text-gray-600 dark:text-gray-400">
              ${calculateTotal().toFixed(2)}
            </div>
          </div>
        </div>

        {/* AI Suggestions Section */}
        <div className="border-t border-gray-200 dark:border-gray-700 pt-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-md font-medium text-gray-900 dark:text-white">
              Sugerencias de Ofertas IA
            </h3>
            <button
              type="button"
              onClick={handleGetOfferSuggestions}
              disabled={loadingSuggestions}
              className="btn-secondary text-sm flex items-center space-x-2"
            >
              {loadingSuggestions ? (
                <div className="spinner" />
              ) : (
                <Brain className="w-4 h-4" />
              )}
              <span>Sugerir Ofertas</span>
            </button>
          </div>
          
          {aiSuggestions && (
            <div className="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg">
              <p className="text-sm text-blue-800 dark:text-blue-200 whitespace-pre-wrap">
                {aiSuggestions}
              </p>
            </div>
          )}
        </div>

        {/* Form Actions */}
        <div className="flex items-center justify-end space-x-4 pt-6 border-t border-gray-200 dark:border-gray-700">
          {purchase && (
            <button
              type="button"
              onClick={onCancel}
              className="btn-secondary"
            >
              Cancelar
            </button>
          )}
          <button
            type="submit"
            disabled={loading}
            className="btn-primary flex items-center space-x-2"
          >
            {loading ? (
              <div className="spinner" />
            ) : (
              <Save className="w-4 h-4" />
            )}
            <span>
              {loading 
                ? (purchase ? 'Actualizando...' : 'Guardando...') 
                : (purchase ? 'Actualizar Compra' : 'Guardar Compra')
              }
            </span>
          </button>
        </div>
      </form>
    </div>
  );
};

export default PurchaseForm;

