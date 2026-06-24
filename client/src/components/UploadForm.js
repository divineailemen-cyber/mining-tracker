import React, { useState } from 'react';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

export default function UploadForm({ onUploadComplete }) {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState('');
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) {
      setStatus('Please choose a CSV file first.');
      return;
    }
    setLoading(true);
    setStatus('Uploading...');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await axios.post(`${API_URL}/api/upload`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setStatus(`Uploaded ${res.data.rows_added} readings successfully.`);
      onUploadComplete();
    } catch (err) {
      setStatus('Upload failed. Check your CSV format and try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-section">
      <input
        type="file"
        accept=".csv"
        onChange={(e) => setFile(e.target.files[0])}
      />
      <button onClick={handleUpload} disabled={loading}>
        {loading ? 'Uploading...' : 'Upload sensor readings'}
      </button>
      {status && <p className="status-msg">{status}</p>}
    </div>
  );
}
