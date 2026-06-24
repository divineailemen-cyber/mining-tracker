import React from 'react';

function getScoreClass(score) {
  if (score >= 75) return 'score-high';
  if (score >= 50) return 'score-medium';
  return 'score-low';
}

function getStatusLabel(score) {
  if (score >= 75) return 'High potential';
  if (score >= 50) return 'Medium potential';
  return 'Low potential';
}

export default function RegionTable({ regions }) {
  const sorted = [...regions].sort((a, b) => b.ai_score - a.ai_score);

  return (
    <table>
      <thead>
        <tr>
          <th>Region</th>
          <th>State</th>
          <th>Mineral</th>
          <th>Score</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        {sorted.map((r) => (
          <tr key={r.id}>
            <td>{r.name}</td>
            <td>{r.state}</td>
            <td>{r.mineral_type}</td>
            <td>{r.ai_score}</td>
            <td>
              <span className={`score-badge ${getScoreClass(r.ai_score)}`}>
                {getStatusLabel(r.ai_score)}
              </span>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
