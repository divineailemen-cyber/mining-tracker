from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Region(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    mineral_type = db.Column(db.String(50))
    is_asm = db.Column(db.Boolean, default=True)
    has_cadastre_title = db.Column(db.Boolean, default=False)
    ai_score = db.Column(db.Float, default=0)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "state": self.state,
            "lat": self.lat,
            "lng": self.lng,
            "mineral_type": self.mineral_type,
            "is_asm": self.is_asm,
            "has_cadastre_title": self.has_cadastre_title,
            "ai_score": round(self.ai_score, 2) if self.ai_score else 0
        }


class SensorReading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'), nullable=False)
    mineral_concentration = db.Column(db.Float, nullable=False)
    depth_m = db.Column(db.Float, nullable=False)
    yield_kg = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "region_id": self.region_id,
            "mineral_concentration": self.mineral_concentration,
            "depth_m": self.depth_m,
            "yield_kg": self.yield_kg,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None
        }
