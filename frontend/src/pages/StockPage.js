import React, { useState } from 'react';
import { Package } from 'lucide-react';
import StockForm from '../components/stock/StockForm';
import StockList from '../components/stock/StockList';
import StockCharts from '../components/stock/StockCharts';

const StockPage = () => {
  const [editingProduct, setEditingProduct] = useState(null);
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleSave = () => {
    setEditingProduct(null);
    setRefreshTrigger(prev => prev + 1);
  };

  const handleEdit = (product) => {
    setEditingProduct(product);
  };

  const handleCancel = () => {
    setEditingProduct(null);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white flex items-center">
          <Package className="w-6 h-6 mr-3" />
          Gestión de Stock
        </h1>
      </div>

      {/* Stock Form */}
      <StockForm
        product={editingProduct}
        onSave={handleSave}
        onCancel={handleCancel}
      />

      {/* Stock Charts */}
      <StockCharts />

      {/* Stock List */}
      <div className="card">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-6">
          Inventario de Productos
        </h2>
        <StockList
          onEdit={handleEdit}
          refreshTrigger={refreshTrigger}
        />
      </div>
    </div>
  );
};

export default StockPage;

