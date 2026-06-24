import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd

from models import db, Region, SensorReading
from ml_model import scorer

app = Flask(__name__)

database_url = os.environ.get('DATABASE_URL', 'sqlite:///mining_tracker.db')
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)
db.init_app(app)

with app.app_context():
    db.create_all()
    scorer.load('model.joblib')


@app.route('/')
def home():
    return jsonify({"status": "ok", "message": "Nigeria Mining AI Tracker API is running"})


@app.route('/api/regions', methods=['GET'])
def get_regions():
    regions = Region.query.order_by(Region.ai_score.desc()).all()
    return jsonify([r.to_dict() for r in regions])


@app.route('/api/regions', methods=['POST'])
def add_region():
    data = request.get_json()
    region = Region(
        name=data.get('name'),
        state=data.get('state'),
        lat=data.get('lat'),
        lng=data.get('lng'),
        mineral_type=data.get('mineral_type'),
        is_asm=data.get('is_asm', True),
        has_cadastre_title=data.get('has_cadastre_title', False)
    )
    db.session.add(region)
    db.session.commit()
    return jsonify(region.to_dict()), 201


@app.route('/api/upload', methods=['POST'])
def upload_data():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    try:
        df = pd.read_csv(file)
    except Exception as e:
        return jsonify({"error": f"Could not read CSV: {str(e)}"}), 400

    required_cols = {'region_id', 'mineral_concentration', 'depth_m', 'yield_kg'}
    if not required_cols.issubset(set(df.columns)):
        return jsonify({"error": f"CSV must contain columns: {required_cols}"}), 400

    rows_added = 0
    for _, row in df.iterrows():
        region = Region.query.get(int(row['region_id']))
        if region is None:
            continue
        reading = SensorReading(
            region_id=int(row['region_id']),
            mineral_concentration=float(row['mineral_concentration']),
            depth_m=float(row['depth_m']),
            yield_kg=float(row['yield_kg'])
        )
        db.session.add(reading)
        rows_added += 1

    db.session.commit()
    return jsonify({"status": "ok", "rows_added": rows_added})


@app.route('/api/score-regions', methods=['POST'])
def score_regions():
    regions = Region.query.all()
    scores = {}

    for region in regions:
        readings = SensorReading.query.filter_by(region_id=region.id).all()
        score = scorer.score_region(readings, region.mineral_type)
        region.ai_score = score
        scores[region.id] = score

    db.session.commit()

    high_potential = [r.to_dict() for r in regions if r.ai_score >= 75]

    return jsonify({
        "status": "ok",
        "scores": scores,
        "high_potential_count": len(high_potential),
        "high_potential": high_potential
    })


@app.route('/api/feature-importance', methods=['GET'])
def feature_importance():
    importance = scorer.feature_importance()
    sorted_imp = dict(sorted(importance.items(), key=lambda x: x[1], reverse=True))
    return jsonify(sorted_imp)


@app.route('/api/region/<int:region_id>/readings', methods=['GET'])
def get_region_readings(region_id):
    readings = SensorReading.query.filter_by(region_id=region_id).order_by(SensorReading.timestamp.desc()).all()
    return jsonify([r.to_dict() for r in readings])


@app.route('/api/stats', methods=['GET'])
def get_stats():
    total_regions = Region.query.count()
    total_readings = SensorReading.query.count()
    high_potential = Region.query.filter(Region.ai_score >= 75).count()
    avg_score = db.session.query(db.func.avg(Region.ai_score)).scalar() or 0

    return jsonify({
        "total_regions": total_regions,
        "total_readings": total_readings,
        "high_potential_regions": high_potential,
        "average_score": round(avg_score, 2)
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
