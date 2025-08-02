import React, { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { Save, X, Package, Upload, Brain } from 'lucide-react';
import { stockAPI, aiAPI } from '../../services/api';

const StockForm = ({ product, onSave, onCancel }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [imageFile, setImageFile] = useState(null);
  const [uploadingImage, setUploadingImage] = useState(false);
  const [pricingSuggestions, setPricingSuggestions] = useState('');
  const [restockPlan, setRestockPlan] = useState('');
  const [loadingPricing, setLoadingPricing] = useState(false);
  const [loadingRestock, setLoadingRestock] = useState(false);
  
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
    setValue
  } = useForm();

  useEffect(() => {
    if (product) {
      setValue('nombre_producto', product.nombre_producto);
      setValue('precio', product.precio);
      setValue('stock_actual', product.stock_actual);
      setValue('stock_minimo', product.stock_minimo);
    } else {
      reset();
      setValue('stock_minimo', 5); // Default minimum stock
    }
  }, [product, setValue, reset]);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (file.type.startsWith('image/')) {
        setImageFile(file);
      } else {
        setError('Por favor selecciona un archivo de imagen válido');
      }
    }
  };

  const handleGetPricingSuggestions = async () => {
    if (!product?.id) {
      setError('Guarda el producto primero para obtener sugerencias de precios');
      return;
    }

    setLoadingPricing(true);
    try {
      const response = await aiAPI.getPricingSuggestions(product.id);
      setPricingSuggestions(response.data.suggestions);
    } catch (error) {
      console.error('Error getting pricing suggestions:', error);
      setPricingSuggestions('Error al obtener sugerencias de precios');
    } finally {
      setLoadingPricing(false);
    }
  };

  const handleGetRestockPlan = async () => {
    setLoadingRestock(true);
    try {
      const response = await aiAPI.getRestockPlan();
      setRestockPlan(response.data.suggestions);
    } catch (error) {
      console.error('Error getting restock plan:', error);
      setRestockPlan('Error al obtener plan de reposición');
    } finally {
      setLoadingRestock(false);
    }
  };

  const onSubmit = async (data) => {
    setLoading(true);
    setError('');

    try {
      const formData = {
        ...data,
        precio: parseFloat(data.precio),
        stock_actual: parseInt(data.stock_actual || 0),
        stock_minimo: parseInt(data.stock_minimo || 5)
      };

      let savedProduct;
      if (product) {
        // Update existing product
        const response = await stockAPI.updateProduct(product.id, formData);
        savedProduct = response.data;
      } else {
        // Create new product
        const createData = {
          nombre_producto: formData.nombre_producto,
          precio: formData.precio,
          stock_inicial: formData.stock_actual,
          stock_minimo: formData.stock_minimo
        };
        const response = await stockAPI.createProduct(createData);
        savedProduct = response.data;
      }

      // Upload image if selected
      if (imageFile && savedProduct.id) {
        setUploadingImage(true);
        try {
          await stockAPI.uploadImage(savedProduct.id, imageFile);
        } catch (imageError) {
          console.error('Error uploading image:', imageError);
          // Don't fail the whole operation for image upload errors
        } finally {
          setUploadingImage(false);
        }
      }
      
      onSave();
      if (!product) {
        reset(); // Only reset form for new products
        setValue('stock_minimo', 5);
        setImageFile(null);
        setPricingSuggestions('');
        setRestockPlan('');
      }
    } catch (error) {
      console.error('Error saving product:', error);
      setError(error.response?.data?.detail || 'Error al guardar el producto');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-white flex items-center">
          <Package className="w-5 h-5 mr-2" />
          {product ? 'Editar Producto' : 'Añadir Producto'}
        </h2>
        {product && (
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
          {/* Nombre del Producto */}
          <div className="md:col-span-2">
            <label htmlFor="nombre_producto" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Nombre del Producto *
            </label>
            <input
              type="text"
              id="nombre_producto"
              {...register('nombre_producto', {
                required: 'El nombre del producto es requerido',
                minLength: {
                  value: 1,
                  message: 'El nombre debe tener al menos 1 carácter'
                },
                maxLength: {
                  value: 200,
                  message: 'El nombre no puede exceder 200 caracteres'
                }
              })}
              className={`input-field ${errors.nombre_producto ? 'border-red-500' : ''}`}
              placeholder="Ingresa el nombre del producto"
            />
            {errors.nombre_producto && (
              <p className="mt-1 text-sm text-red-600 dark:text-red-400">
                {errors.nombre_producto.message}
              </p>
            )}
          </div>

          {/* Precio */}
          <div>
            <label htmlFor="precio" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Precio *
            </label>
            <input
              type="number"
              id="precio"
              step="0.01"
              min="0.01"
              {...register('precio', {
                required: 'El precio es requerido',
                min: {
                  value: 0.01,
                  message: 'El precio debe ser mayor a 0'
                }
              })}
              className={`input-field ${errors.precio ? 'border-red-500' : ''}`}
              placeholder="0.00"
            />
            {errors.precio && (
              <p className="mt-1 text-sm text-red-600 dark:text-red-400">
                {errors.precio.message}
              </p>
            )}
          </div>

          {/* Stock Actual */}
          <div>
            <label htmlFor="stock_actual" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Stock Actual
            </label>
            <input
              type="number"
              id="stock_actual"
              min="0"
              {...register('stock_actual', {
                min: {
                  value: 0,
                  message: 'El stock no puede ser negativo'
                }
              })}
              className={`input-field ${errors.stock_actual ? 'border-red-500' : ''}`}
              placeholder="0"
            />
            {errors.stock_actual && (
              <p className="mt-1 text-sm text-red-600 dark:text-red-400">
                {errors.stock_actual.message}
              </p>
            )}
          </div>

          {/* Stock Mínimo */}
          <div>
            <label htmlFor="stock_minimo" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Stock Mínimo
            </label>
            <input
              type="number"
              id="stock_minimo"
              min="0"
              {...register('stock_minimo', {
                min: {
                  value: 0,
                  message: 'El stock mínimo no puede ser negativo'
                }
              })}
              className={`input-field ${errors.stock_minimo ? 'border-red-500' : ''}`}
              placeholder="5"
            />
            {errors.stock_minimo && (
              <p className="mt-1 text-sm text-red-600 dark:text-red-400">
                {errors.stock_minimo.message}
              </p>
            )}
          </div>

          {/* Subida de Imagen */}
          <div className="md:col-span-2">
            <label htmlFor="imagen" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Imagen del Producto
            </label>
            <div className="flex items-center space-x-4">
              <input
                type="file"
                id="imagen"
                accept="image/*"
                onChange={handleImageChange}
                className="input-field"
              />
              {imageFile && (
                <div className="flex items-center text-sm text-green-600 dark:text-green-400">
                  <Upload className="w-4 h-4 mr-1" />
                  {imageFile.name}
                </div>
              )}
            </div>
            {product?.imagen_url && (
              <p className="mt-1 text-sm text-gray-600 dark:text-gray-400">
                Imagen actual: {product.imagen_url}
              </p>
            )}
          </div>
        </div>

        {/* AI Suggestions Section */}
        <div className="border-t border-gray-200 dark:border-gray-700 pt-6 space-y-4">
          <h3 className="text-md font-medium text-gray-900 dark:text-white">
            Sugerencias IA
          </h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Pricing Suggestions */}
            <div>
              <button
                type="button"
                onClick={handleGetPricingSuggestions}
                disabled={loadingPricing}
                className="w-full btn-secondary text-sm flex items-center justify-center space-x-2 mb-3"
              >
                {loadingPricing ? (
                  <div className="spinner" />
                ) : (
                  <Brain className="w-4 h-4" />
                )}
                <span>Sugerencias de Precios</span>
              </button>
              
              {pricingSuggestions && (
                <div className="bg-blue-50 dark:bg-blue-900/20 p-3 rounded-lg">
                  <p className="text-sm text-blue-800 dark:text-blue-200 whitespace-pre-wrap">
                    {pricingSuggestions}
                  </p>
                </div>
              )}
            </div>

            {/* Restock Plan */}
            <div>
              <button
                type="button"
                onClick={handleGetRestockPlan}
                disabled={loadingRestock}
                className="w-full btn-secondary text-sm flex items-center justify-center space-x-2 mb-3"
              >
                {loadingRestock ? (
                  <div className="spinner" />
                ) : (
                  <Brain className="w-4 h-4" />
                )}
                <span>Plan Mensual de Reposición</span>
              </button>
              
              {restockPlan && (
                <div className="bg-green-50 dark:bg-green-900/20 p-3 rounded-lg">
                  <p className="text-sm text-green-800 dark:text-green-200 whitespace-pre-wrap">
                    {restockPlan}
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Form Actions */}
        <div className="flex items-center justify-end space-x-4 pt-6 border-t border-gray-200 dark:border-gray-700">
          {product && (
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
            disabled={loading || uploadingImage}
            className="btn-primary flex items-center space-x-2"
          >
            {(loading || uploadingImage) ? (
              <div className="spinner" />
            ) : (
              <Save className="w-4 h-4" />
            )}
            <span>
              {loading 
                ? (product ? 'Actualizando...' : 'Guardando...') 
                : uploadingImage
                ? 'Subiendo imagen...'
                : (product ? 'Actualizar Producto' : 'Guardar Producto')
              }
            </span>
          </button>
        </div>
      </form>
    </div>
  );
};

export default StockForm;

