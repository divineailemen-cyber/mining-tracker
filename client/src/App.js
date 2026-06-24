import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import MiningMap from './components/MiningMap';
import RegionTable from './components/RegionTable';
import UploadForm from './components/UploadForm';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

function App() {
  const [regions, setRegions] = useState([]);
  const [stats, setStats] = useState(null);
  const [scoring, setScoring] = useState(false);
  const [scoreMsg, setScoreMsg] = useState('');

  const fetchRegions = useCallback(async () => {
    try {
      const res = await axios.get(`${API_URL}/api/regions`);
      setRegions(res.data);
    } catch (err) {
      console.error('Failed to fetch regions', err);
    }
  }, []);

  const fetchStats = useCallback(async () => {
    try {
      const res = await axios.get(`${API_URL}/api/stats`);
      setStats(res.data);
    } catch (err) {
      console.error('Failed to fetch stats', err);
    }
  }, []);

  useEffect(() => {
    fetchRegions();
    fetchStats();
  }, [fetchRegions, fetchStats]);

  const handleScoreRegions = async () => {
    setScoring(true);
    setScoreMsg('Scoring all regions with AI model...');
    try {
      const res = await axios.post(`${API_URL}/api/score-regions`);
      setScoreMsg(`Done. ${res.data.high_potential_count} region(s) now flagged as high potential.`);
      await fetchRegions();
      await fetchStats();
    } catch (err) {
      setScoreMsg('Scoring failed. Check that the backend is running.');
    } finally {
      setScoring(false);
    }
  };

  const handleUploadComplete = async () => {
    await fetchRegions();
    await fetchStats();
  };

  const highPotential = regions.filter((r) => r.ai_score >= 75);

  return (
    <div className="app-container">
      <div className="header">
        <div>
          <h1>Nigeria mining AI tracker</h1>
          <p>Track mineral-rich regions across Nigeria with AI region scoring</p>
        </div>
        <button onClick={handleScoreRegions} disabled={scoring}>
          {scoring ? 'Scoring...' : 'Run AI scoring'}
        </button>
      </div>

      {scoreMsg && <div className="alert-banner">{scoreMsg}</div>}

      {stats && (
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-label">Total regions</div>
            <div className="stat-value">{stats.total_regions}</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Sensor readings</div>
            <div className="stat-value">{stats.total_readings}</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">High potential</div>
            <div className="stat-value">{stats.high_potential_regions}</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Average score</div>
            <div className="stat-value">{stats.average_score}</div>
          </div>
        </div>
      )}

      <div className="main-grid">
        <div>
          <div className="card">
            <h2>Region map</h2>
            <MiningMap regions={regions} />
          </div>
        </div>
        <div>
          <div className="card">
            <h2>Upload sensor readings</h2>
            <UploadForm onUploadComplete={handleUploadComplete} />
          </div>
        </div>
      </div>

      <div className="card">
        <h2>Region ranking ({highPotential.length} high potential)</h2>
        <RegionTable regions={regions} />
      </div>
    </div>
  );
}

export default App;
