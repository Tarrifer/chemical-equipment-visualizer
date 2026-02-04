import { useEffect, useState } from "react";
import { api } from "../api";

function History() {
  const [history, setHistory] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const response = await api.get("/api/equipment/history/");
        setHistory(response.data);
      } catch (err) {
        setError("Failed to load history");
      }
    };

    fetchHistory();
  }, []);

  return (
    <div>
      <h3 className="mb-3">Upload History (Last 5)</h3>

      {error && (
        <div className="alert alert-danger" role="alert">
          {error}
        </div>
      )}

      {history.length === 0 ? (
        <div className="alert alert-info" role="alert">
          No history available
        </div>
      ) : (
        <div className="table-responsive">
          <table className="table table-hover">
            <thead>
              <tr>
                <th scope="col">Uploaded At</th>
                <th scope="col" className="text-center">Total</th>
                <th scope="col" className="text-center">Avg Flowrate</th>
                <th scope="col" className="text-center">Avg Pressure</th>
                <th scope="col" className="text-center">Avg Temperature</th>
              </tr>
            </thead>
            <tbody>
              {history.map((item, index) => (
                <tr key={index}>
                  <td>{item.uploaded_at}</td>
                  <td className="text-center">{item.total_equipment}</td>
                  <td className="text-center">{item.average_flowrate}</td>
                  <td className="text-center">{item.average_pressure}</td>
                  <td className="text-center">{item.average_temperature}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default History;
