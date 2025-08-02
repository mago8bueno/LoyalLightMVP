import React, { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { Save, X, UserPlus } from 'lucide-react';
import { clientsAPI } from '../../services/api';

const ClientForm = ({ client, onSave, onCancel }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
    setValue
  } = useForm();

  useEffect(() => {
    if (client) {
      setValue('nombre', client.nombre);
      setValue('apellido', client.apellido);
      setValue('correo_electronico', client.correo_electronico);
    } else {
      reset();
    }
  }, [client, setValue, reset]);

  const onSubmit = async (data) => {
    setLoading(true);
    setError('');

    try {
      if (client) {
        // Update existing client
        await clientsAPI.updateClient(client.id, data);
      } else {
        // Create new client
        await clientsAPI.createClient(data);
      }
      
      onSave();
      if (!client) {
        reset(); // Only reset form for new clients
      }
    } catch (error) {
      console.error('Error saving client:', error);
      setError(error.response?.data?.detail || 'Error al guardar el cliente');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-white flex items-center">
          <UserPlus className="w-5 h-5 mr-2" />
          {client ? 'Editar Cliente' : 'Añadir Cliente'}
        </h2>
        {client && (
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
          {/* Nombre */}
          <div>
            <label htmlFor="nombre" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Nombre *
            </label>
            <input
              type="text"
              id="nombre"
              {...register('nombre', {
                required: 'El nombre es requerido',
                minLength: {
                  value: 1,
                  message: 'El nombre debe tener al menos 1 carácter'
                },
                maxLength: {
                  value: 100,
                  message: 'El nombre no puede exceder 100 caracteres'
                }
              })}
              className={`input-field ${errors.nombre ? 'border-red-500' : ''}`}
              placeholder="Ingresa el nombre"
            />
            {errors.nombre && (
              <p className="mt-1 text-sm text-red-600 dark:text-red-400">
                {errors.nombre.message}
              </p>
            )}
          </div>

          {/* Apellido */}
          <div>
            <label htmlFor="apellido" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Apellido *
            </label>
            <input
              type="text"
              id="apellido"
              {...register('apellido', {
                required: 'El apellido es requerido',
                minLength: {
                  value: 1,
                  message: 'El apellido debe tener al menos 1 carácter'
                },
                maxLength: {
                  value: 100,
                  message: 'El apellido no puede exceder 100 caracteres'
                }
              })}
              className={`input-field ${errors.apellido ? 'border-red-500' : ''}`}
              placeholder="Ingresa el apellido"
            />
            {errors.apellido && (
              <p className="mt-1 text-sm text-red-600 dark:text-red-400">
                {errors.apellido.message}
              </p>
            )}
          </div>
        </div>

        {/* Correo Electrónico */}
        <div>
          <label htmlFor="correo_electronico" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Correo Electrónico *
          </label>
          <input
            type="email"
            id="correo_electronico"
            {...register('correo_electronico', {
              required: 'El correo electrónico es requerido',
              pattern: {
                value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                message: 'Ingresa un correo electrónico válido'
              }
            })}
            className={`input-field ${errors.correo_electronico ? 'border-red-500' : ''}`}
            placeholder="ejemplo@correo.com"
          />
          {errors.correo_electronico && (
            <p className="mt-1 text-sm text-red-600 dark:text-red-400">
              {errors.correo_electronico.message}
            </p>
          )}
        </div>

        {/* Form Actions */}
        <div className="flex items-center justify-end space-x-4 pt-6 border-t border-gray-200 dark:border-gray-700">
          {client && (
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
                ? (client ? 'Actualizando...' : 'Guardando...') 
                : (client ? 'Actualizar Cliente' : 'Guardar Cliente')
              }
            </span>
          </button>
        </div>
      </form>
    </div>
  );
};

export default ClientForm;

