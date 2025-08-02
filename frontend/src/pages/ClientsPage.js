import React, { useState } from 'react';
import { Users } from 'lucide-react';
import ClientForm from '../components/clients/ClientForm';
import ClientList from '../components/clients/ClientList';

const ClientsPage = () => {
  const [editingClient, setEditingClient] = useState(null);
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleSave = () => {
    setEditingClient(null);
    setRefreshTrigger(prev => prev + 1);
  };

  const handleEdit = (client) => {
    setEditingClient(client);
  };

  const handleCancel = () => {
    setEditingClient(null);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white flex items-center">
          <Users className="w-6 h-6 mr-3" />
          Gestión de Clientes
        </h1>
      </div>

      {/* Client Form */}
      <ClientForm
        client={editingClient}
        onSave={handleSave}
        onCancel={handleCancel}
      />

      {/* Client List */}
      <div className="card">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-6">
          Lista de Clientes
        </h2>
        <ClientList
          onEdit={handleEdit}
          refreshTrigger={refreshTrigger}
        />
      </div>
    </div>
  );
};

export default ClientsPage;

