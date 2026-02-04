import { useState } from "react";
import UploadCSV from "./UploadCSV";
import Summary from "./Summary";
import ChartView from "./ChartView";
import History from "./History";
import DownloadPDF from "./DownloadPDF";

function Dashboard({ onLogout }) {
  const [summary, setSummary] = useState(null);

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h4 className="mb-0">Dashboard</h4>
          <small className="text-muted">Manage your equipment data</small>
        </div>
        <button className="btn btn-outline-danger btn-sm" onClick={onLogout}>
          Logout
        </button>
      </div>

      <div className="card mb-4">
        <div className="card-body">
          <h5 className="mb-3">Upload CSV</h5>
          <UploadCSV onResult={setSummary} />
        </div>
      </div>

      {summary && (
        <div className="card mb-4">
          <div className="card-body">
            <Summary data={summary} />

            <div className="mt-4">
              <ChartView
                distribution={summary.equipment_type_distribution}
              />
            </div>

            <div className="mt-4">
              <DownloadPDF />
            </div>
          </div>
        </div>
      )}

      <div className="card">
        <div className="card-body">
          <History />
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
