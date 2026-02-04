import { useState } from "react";
import { api } from "../api";

function UploadCSV({ onResult }) {
  const [file, setFile] = useState(null);
  const [error, setError] = useState("");
  const [uploading, setUploading] = useState(false);
  const [fileName, setFileName] = useState("");

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
    setFileName(selectedFile ? selectedFile.name : "");
    setError("");
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Please select a CSV file");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    setUploading(true);

    try {
      const response = await api.post(
        "/api/equipment/upload/",
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
        }
      );

      onResult(response.data);
      setError("");

      const successMsg = document.createElement('div');
      successMsg.className = 'alert alert-success mt-3';
      successMsg.textContent = '✓ File uploaded successfully!';
      successMsg.style.transition = 'opacity 0.3s';
      document.querySelector('.upload-section')?.appendChild(successMsg);
      setTimeout(() => {
        successMsg.style.opacity = '0';
        setTimeout(() => successMsg.remove(), 300);
      }, 2000);
    } catch (err) {
      setError("Upload failed. Please check your file and try again.");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="upload-section">
      <div className="mb-3">
        <label htmlFor="csvFile" className="form-label">
          Select CSV File
        </label>
        <input
          id="csvFile"
          type="file"
          className="form-control"
          accept=".csv"
          onChange={handleFileChange}
          disabled={uploading}
        />
        {fileName && (
          <div className="form-text">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="currentColor" className="bi bi-file-earmark-text me-1" viewBox="0 0 16 16">
              <path d="M5.5 7a.5.5 0 0 0 0 1h5a.5.5 0 0 0 0-1zM5 9.5a.5.5 0 0 1 .5-.5h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1-.5-.5m0 2a.5.5 0 0 1 .5-.5h2a.5.5 0 0 1 0 1h-2a.5.5 0 0 1-.5-.5"/>
              <path d="M9.5 0H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V4.5zm0 1v2A1.5 1.5 0 0 0 11 4.5h2V14a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1z"/>
            </svg>
            Selected: <strong>{fileName}</strong>
          </div>
        )}
      </div>

      <button
        className="btn btn-success"
        onClick={handleUpload}
        disabled={uploading || !file}
      >
        {uploading ? (
          <>
            <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
            Uploading...
          </>
        ) : (
          <>
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-cloud-upload me-2" viewBox="0 0 16 16">
              <path fillRule="evenodd" d="M4.406 1.342A5.53 5.53 0 0 1 8 0c2.69 0 4.923 2 5.166 4.579C14.758 4.804 16 6.137 16 7.773 16 9.569 14.502 11 12.687 11H10a.5.5 0 0 1 0-1h2.688C13.979 10 15 8.988 15 7.773c0-1.216-1.02-2.228-2.313-2.228h-.5v-.5C12.188 2.825 10.328 1 8 1a4.53 4.53 0 0 0-2.941 1.1c-.757.652-1.153 1.438-1.153 2.055v.448l-.445.049C2.064 4.805 1 5.952 1 7.318 1 8.785 2.23 10 3.781 10H6a.5.5 0 0 1 0 1H3.781C1.708 11 0 9.366 0 7.318c0-1.763 1.266-3.223 2.942-3.593.143-.863.698-1.723 1.464-2.383"/>
              <path fillRule="evenodd" d="M7.646 4.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1-.708.708L8.5 5.707V14.5a.5.5 0 0 1-1 0V5.707L5.354 7.854a.5.5 0 1 1-.708-.708z"/>
            </svg>
            Upload CSV
          </>
        )}
      </button>

      {error && (
        <div className="alert alert-danger mt-3 mb-0" role="alert">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-exclamation-circle me-2" viewBox="0 0 16 16">
            <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/>
            <path d="M7.002 11a1 1 0 1 1 2 0 1 1 0 0 1-2 0M7.1 4.995a.905.905 0 1 1 1.8 0l-.35 3.507a.552.552 0 0 1-1.1 0z"/>
          </svg>
          {error}
        </div>
      )}
    </div>
  );
}

export default UploadCSV;
