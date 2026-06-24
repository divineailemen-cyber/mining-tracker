import React from 'react';
import { MapContainer, TileLayer, CircleMarker, Popup } from 'react-leaflet';

function getColor(score) {
  if (score >= 75) return '#639922';
  if (score >= 50) return '#ba7517';
  return '#a32d2d';
}

export default function MiningMap({ regions }) {
  return (
    <MapContainer center={[9.0820, 8.6753]} zoom={6} scrollWheelZoom={true}>
      <TileLayer
        attribution='&copy; OpenStreetMap contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {regions.map((region) => (
        <CircleMarker
          key={region.id}
          center={[region.lat, region.lng]}
          radius={10}
          pathOptions={{
            color: getColor(region.ai_score),
            fillColor: getColor(region.ai_score),
            fillOpacity: 0.7
          }}
        >
          <Popup>
            <strong>{region.name}</strong><br />
            State: {region.state}<br />
            Mineral: {region.mineral_type}<br />
            AI score: {region.ai_score}<br />
            {region.is_asm ? 'Artisanal / small-scale' : 'Formal mining title'}
          </Popup>
        </CircleMarker>
      ))}
    </MapContainer>
  );
}
