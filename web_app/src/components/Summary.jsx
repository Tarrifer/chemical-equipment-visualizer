function Summary({ data }) {
  return (
    <div>
      <h3 className="mb-3">Summary</h3>
      <div className="row g-3">
        <div className="col-md-6 col-lg-3">
          <div className="card h-100">
            <div className="card-body text-center">
              <h6 className="card-subtitle mb-2 text-muted">Total Equipment</h6>
              <h4 className="card-title text-primary mb-0">{data.total_equipment}</h4>
            </div>
          </div>
        </div>
        
        <div className="col-md-6 col-lg-3">
          <div className="card h-100">
            <div className="card-body text-center">
              <h6 className="card-subtitle mb-2 text-muted">Avg Flowrate</h6>
              <h4 className="card-title text-info mb-0">{data.average_flowrate}</h4>
            </div>
          </div>
        </div>
        
        <div className="col-md-6 col-lg-3">
          <div className="card h-100">
            <div className="card-body text-center">
              <h6 className="card-subtitle mb-2 text-muted">Avg Pressure</h6>
              <h4 className="card-title text-success mb-0">{data.average_pressure}</h4>
            </div>
          </div>
        </div>
        
        <div className="col-md-6 col-lg-3">
          <div className="card h-100">
            <div className="card-body text-center">
              <h6 className="card-subtitle mb-2 text-muted">Avg Temperature</h6>
              <h4 className="card-title text-warning mb-0">{data.average_temperature}</h4>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Summary;
