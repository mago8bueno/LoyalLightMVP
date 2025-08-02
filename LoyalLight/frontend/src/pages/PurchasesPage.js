import React, { useState } from 'react';
import { ShoppingCart } from 'lucide-react';
import PurchaseForm from '../components/purchases/PurchaseForm';
import PurchaseList from '../components/purchases/PurchaseList';

const PurchasesPage = () => {
  const [editingPurchase, setEditingPurchase] = useState(null);
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleSave = () => {
    setEditingPurchase(null);
    setRefreshTrigger(prev => prev + 1);
  };

  const handleEdit = (purchase) => {
    setEditingPurchase(purchase);
  };

  const handleCancel = () => {
    setEditingPurchase(null);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white flex items-center">
          <ShoppingCart className="w-6 h-6 mr-3" />
          Gestión de Compras
        </h1>
      </div>

      {/* Purchase Form */}
      <PurchaseForm
        purchase={editingPurchase}
        onSave={handleSave}
        onCancel={handleCancel}
      />

      {/* Purchase List */}
      <div className="card">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-6">
          Historial de Compras
        </h2>
        <PurchaseList
          onEdit={handleEdit}
          refreshTrigger={refreshTrigger}
        />
      </div>
    </div>
  );
};

export default PurchasesPage;

