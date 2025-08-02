import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import { TrendingUp } from 'lucide-react';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

const SalesChart = ({ chartData }) => {
  if (!chartData) {
    return (
      <div className="card">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
          <TrendingUp className="w-5 h-5 text-green-500 mr-2" />
          Ventas de los Últimos 7 Días
        </h2>
        <div className="text-center py-8">
          <div className="spinner w-8 h-8 mx-auto" />
          <p className="text-gray-600 dark:text-gray-400 mt-4">
            Cargando datos de ventas...
          </p>
        </div>
      </div>
    );
  }

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          usePointStyle: true,
          color: 'rgb(107, 114, 128)', // gray-500
        },
      },
      tooltip: {
        mode: 'index',
        intersect: false,
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
    elements: {
      line: {
        tension: 0.4,
      },
      point: {
        radius: 4,
        hoverRadius: 6,
      },
    },
    interaction: {
      mode: 'nearest',
      axis: 'x',
      intersect: false,
    },
  };

  const data = {
    labels: chartData?.labels || [],
    datasets: (chartData?.datasets || []).map((dataset, index) => ({
      ...dataset,
      fill: true,
      backgroundColor: index === 0 
        ? 'rgba(59, 130, 246, 0.1)' 
        : 'rgba(16, 185, 129, 0.1)',
      borderColor: index === 0 
        ? 'rgb(59, 130, 246)' 
        : 'rgb(16, 185, 129)',
      pointBackgroundColor: index === 0 
        ? 'rgb(59, 130, 246)' 
        : 'rgb(16, 185, 129)',
      pointBorderColor: '#fff',
      pointBorderWidth: 2,
    })),
  };

  return (
    <div className="card">
      <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
        <TrendingUp className="w-5 h-5 text-green-500 mr-2" />
        Ventas de los Últimos 7 Días
      </h2>
      
      <div className="h-80">
        <Line data={data} options={options} />
      </div>
      
      {/* Summary Stats */}
      <div className="mt-4 grid grid-cols-2 gap-4 pt-4 border-t border-gray-200 dark:border-gray-700">
        <div className="text-center">
          <p className="text-sm text-gray-600 dark:text-gray-400">Total Ventas</p>
          <p className="text-lg font-semibold text-gray-900 dark:text-white">
            {chartData.datasets[0]?.data?.reduce((a, b) => a + b, 0) || 0}
          </p>
        </div>
        <div className="text-center">
          <p className="text-sm text-gray-600 dark:text-gray-400">Ingresos Totales</p>
          <p className="text-lg font-semibold text-gray-900 dark:text-white">
            ${(chartData.datasets[1]?.data?.reduce((a, b) => a + b, 0) || 0).toLocaleString()}
          </p>
        </div>
      </div>
    </div>
  );
};

export default SalesChart;

