import React, { useState, useEffect } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';
import { 
  BarChart3, 
  ChevronLeft, 
  ChevronRight, 
  Maximize2,
  X
} from 'lucide-react';
import { stockAPI } from '../../services/api';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const StockCharts = () => {
  const [chartData, setChartData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [currentChart, setCurrentChart] = useState(0);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const chartTypes = [
    {
      key: 'most_sold_products',
      title: 'Productos Más Comprados',
      color: 'rgba(59, 130, 246, 0.8)',
      borderColor: 'rgb(59, 130, 246)',
    },
    {
      key: 'stock_levels',
      title: 'Cantidad de Stock por Producto',
      color: 'rgba(16, 185, 129, 0.8)',
      borderColor: 'rgb(16, 185, 129)',
    }
  ];

  useEffect(() => {
    loadChartData();
  }, []);

  const loadChartData = async () => {
    try {
      const response = await stockAPI.getChartData();
      setChartData(response.data);
    } catch (error) {
      console.error('Error loading chart data:', error);
    } finally {
      setLoading(false);
    }
  };

  const getCurrentChartData = () => {
    if (!chartData) return null;

    const currentType = chartTypes[currentChart];
    const data = chartData[currentType.key];

    if (!data || !data.labels || !data.data) return null;

    return {
      labels: data.labels.slice(0, 10), // Show top 10
      datasets: [
        {
          label: currentType.title,
          data: data.data.slice(0, 10),
          backgroundColor: currentType.color,
          borderColor: currentType.borderColor,
          borderWidth: 1,
        },
      ],
    };
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          color: 'rgb(107, 114, 128)',
        },
      },
      tooltip: {
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        titleColor: 'white',
        bodyColor: 'white',
        borderColor: 'rgba(59, 130, 246, 0.5)',
        borderWidth: 1,
      },
    },
    scales: {
      x: {
        grid: {
          color: 'rgba(107, 114, 128, 0.1)',
        },
        ticks: {
          color: 'rgb(107, 114, 128)',
          maxRotation: 45,
        },
      },
      y: {
        grid: {
          color: 'rgba(107, 114, 128, 0.1)',
        },
        ticks: {
          color: 'rgb(107, 114, 128)',
        },
        beginAtZero: true,
      },
    },
  };

  const nextChart = () => {
    setCurrentChart((prev) => (prev + 1) % chartTypes.length);
  };

  const prevChart = () => {
    setCurrentChart((prev) => (prev - 1 + chartTypes.length) % chartTypes.length);
  };

  const openModal = () => {
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
  };

  if (loading) {
    return (
      <div className="card">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
          <BarChart3 className="w-5 h-5 text-blue-500 mr-2" />
          Gráficos de Stock
        </h2>
        <div className="flex items-center justify-center h-64">
          <div className="spinner w-8 h-8" />
        </div>
      </div>
    );
  }

  const currentData = getCurrentChartData();

  if (!currentData) {
    return (
      <div className="card">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
          <BarChart3 className="w-5 h-5 text-blue-500 mr-2" />
          Gráficos de Stock
        </h2>
        <div className="text-center py-8">
          <BarChart3 className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-600 dark:text-gray-400">
            No hay datos suficientes para mostrar gráficos
          </p>
        </div>
      </div>
    );
  }

  const ChartComponent = ({ isModal = false }) => (
    <div className={`${isModal ? 'h-96' : 'h-64'}`}>
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-md font-medium text-gray-900 dark:text-white">
          {chartTypes[currentChart].title}
        </h3>
        <div className="flex items-center space-x-2">
          <button
            onClick={prevChart}
            className="p-1 rounded hover:bg-gray-100 dark:hover:bg-gray-700"
          >
            <ChevronLeft className="w-4 h-4 text-gray-600 dark:text-gray-400" />
          </button>
          <span className="text-sm text-gray-500 dark:text-gray-400">
            {currentChart + 1} / {chartTypes.length}
          </span>
          <button
            onClick={nextChart}
            className="p-1 rounded hover:bg-gray-100 dark:hover:bg-gray-700"
          >
            <ChevronRight className="w-4 h-4 text-gray-600 dark:text-gray-400" />
          </button>
          {!isModal && (
            <button
              onClick={openModal}
              className="p-1 rounded hover:bg-gray-100 dark:hover:bg-gray-700"
            >
              <Maximize2 className="w-4 h-4 text-gray-600 dark:text-gray-400" />
            </button>
          )}
        </div>
      </div>
      <Bar data={currentData} options={chartOptions} />
    </div>
  );

  return (
    <>
      <div className="card">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
          <BarChart3 className="w-5 h-5 text-blue-500 mr-2" />
          Gráficos de Stock
        </h2>
        <ChartComponent />
      </div>

      {/* Modal for enlarged chart */}
      {isModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white dark:bg-gray-800 rounded-lg p-6 w-full max-w-4xl max-h-full overflow-auto">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
                {chartTypes[currentChart].title}
              </h2>
              <button
                onClick={closeModal}
                className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
              >
                <X className="w-6 h-6" />
              </button>
            </div>
            <ChartComponent isModal={true} />
          </div>
        </div>
      )}
    </>
  );
};

export default StockCharts;

