import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8001/api';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: (credentials) => api.post('/auth/login', credentials),
  logout: () => api.post('/auth/logout'),
  getMe: () => api.get('/auth/me'),
};

// Clients API
export const clientsAPI = {
  getClients: (params = {}) => api.get('/clients', { params }),
  getClient: (id) => api.get(`/clients/${id}`),
  createClient: (data) => api.post('/clients', data),
  updateClient: (id, data) => api.put(`/clients/${id}`, data),
  deleteClient: (id) => api.delete(`/clients/${id}`),
  getTopLoyal: (limit = 5) => api.get(`/clients/analytics/top-loyal?limit=${limit}`),
  getChurnRisk: (limit = 5) => api.get(`/clients/analytics/churn-risk?limit=${limit}`),
};

// Purchases API
export const purchasesAPI = {
  getPurchases: (params = {}) => api.get('/purchases', { params }),
  getPurchase: (id) => api.get(`/purchases/${id}`),
  createPurchase: (data) => api.post('/purchases', data),
  updatePurchase: (id, data) => api.put(`/purchases/${id}`, data),
  deletePurchase: (id) => api.delete(`/purchases/${id}`),
  getPurchasesByClient: (clientId) => api.get(`/purchases/client/${clientId}`),
  getRecentPurchases: (days = 30) => api.get(`/purchases/analytics/recent?days=${days}`),
  getSalesAnalytics: () => api.get('/purchases/analytics/sales'),
};

// Stock API
export const stockAPI = {
  getProducts: (params = {}) => api.get('/stock', { params }),
  getProduct: (id) => api.get(`/stock/${id}`),
  createProduct: (data) => api.post('/stock', data),
  updateProduct: (id, data) => api.put(`/stock/${id}`, data),
  deleteProduct: (id) => api.delete(`/stock/${id}`),
  uploadImage: (id, file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post(`/stock/${id}/upload-image`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  getLowStock: () => api.get('/stock/analytics/low-stock'),
  getStockAlerts: () => api.get('/stock/analytics/alerts'),
  getSalesStats: (limit = 10) => api.get(`/stock/analytics/sales-stats?limit=${limit}`),
  getChartData: () => api.get('/stock/analytics/charts'),
};

// Dashboard API
export const dashboardAPI = {
  getMetrics: () => api.get('/dashboard/metrics'),
  getAlerts: () => api.get('/dashboard/alerts'),
  getSalesChart: () => api.get('/dashboard/sales-chart'),
  getCompleteData: () => api.get('/dashboard'),
};

// AI API
export const aiAPI = {
  getChurnSuggestions: (clientId) => api.post('/ai/churn-suggestions', { client_id: clientId }),
  getOfferSuggestions: (limit = 10) => api.post('/ai/offer-suggestions', { limit }),
  getPricingSuggestions: (productId) => api.post('/ai/pricing-suggestions', { product_id: productId }),
  getRestockPlan: () => api.post('/ai/restock-plan'),
  getGlobalInsights: () => api.post('/ai/global-insights'),
};

export default api;

