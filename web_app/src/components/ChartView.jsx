import { useEffect, useState } from "react";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Bar } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

function ChartView({ distribution }) {
  const [isDark, setIsDark] = useState(true);

  useEffect(() => {
    const updateTheme = () => {
      const theme = document.body.getAttribute('data-bs-theme');
      setIsDark(theme === 'dark' || !theme);
    };

    updateTheme();

    const observer = new MutationObserver(updateTheme);
    observer.observe(document.body, { attributes: true, attributeFilter: ['data-bs-theme'] });

    return () => observer.disconnect();
  }, []);

  const labels = Object.keys(distribution);
  const values = Object.values(distribution);

  const colors = [
    "rgba(255, 99, 132, 0.7)",
    "rgba(54, 162, 235, 0.7)",
    "rgba(255, 206, 86, 0.7)",
    "rgba(75, 192, 192, 0.7)",
    "rgba(153, 102, 255, 0.7)",
    "rgba(255, 159, 64, 0.7)",
  ];

  const data = {
    labels,
    datasets: [
      {
        label: "Equipment Count",
        data: values,
        backgroundColor: labels.map(
          (_, index) => colors[index % colors.length]
        ),
        borderColor: labels.map(
          (_, index) => colors[index % colors.length].replace('0.7', '1')
        ),
        borderWidth: 2,
      },
    ],
  };

  const textColor = isDark ? '#e9ecef' : '#2c3e50';
  const gridColor = isDark ? 'rgba(255, 255, 255, 0.08)' : 'rgba(0, 0, 0, 0.08)';

  const options = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: { 
        display: true,
        labels: {
          color: textColor,
          font: {
            size: 12
          }
        }
      },
      title: {
        display: true,
        text: "Equipment Type Distribution",
        color: textColor,
        font: {
          size: 16,
          weight: 'bold'
        }
      },
    },
    scales: {
      y: {
        ticks: {
          color: textColor
        },
        grid: {
          color: gridColor
        }
      },
      x: {
        ticks: {
          color: textColor
        },
        grid: {
          color: gridColor
        }
      }
    }
  };

  return (
    <div className="chart-container">
      <div className="row justify-content-center">
        <div className="col-12 col-lg-10">
          <Bar data={data} options={options} />
        </div>
      </div>
    </div>
  );
}

export default ChartView;
