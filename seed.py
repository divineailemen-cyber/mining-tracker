from app import app, db
from models import Region

NIGERIA_REGIONS = [
    {"name": "Kogi - Itakpe", "state": "Kogi", "lat": 7.5249, "lng": 6.3350, "mineral_type": "Iron ore", "has_cadastre_title": True, "is_asm": False},
    {"name": "Nasarawa Central", "state": "Nasarawa", "lat": 8.5378, "lng": 8.3206, "mineral_type": "Lithium", "has_cadastre_title": True, "is_asm": False},
    {"name": "Plateau - Jos", "state": "Plateau", "lat": 9.8965, "lng": 8.8583, "mineral_type": "Tin", "has_cadastre_title": False, "is_asm": True},
    {"name": "Zamfara - Anka", "state": "Zamfara", "lat": 12.1000, "lng": 6.2500, "mineral_type": "Gold", "has_cadastre_title": False, "is_asm": True},
    {"name": "Ebonyi - Abakaliki", "state": "Ebonyi", "lat": 6.3249, "lng": 8.1137, "mineral_type": "Lead-zinc", "has_cadastre_title": False, "is_asm": True},
    {"name": "Edo - Igarra", "state": "Edo", "lat": 7.2900, "lng": 6.1100, "mineral_type": "Limestone", "has_cadastre_title": True, "is_asm": False},
    {"name": "Enugu - Udi", "state": "Enugu", "lat": 6.4500, "lng": 7.3300, "mineral_type": "Coal", "has_cadastre_title": True, "is_asm": False},
    {"name": "Cross River - Mfamosing", "state": "Cross River", "lat": 5.9631, "lng": 8.3270, "mineral_type": "Lithium", "has_cadastre_title": False, "is_asm": True},
    {"name": "Kaduna - Birnin Gwari", "state": "Kaduna", "lat": 10.5167, "lng": 6.4833, "mineral_type": "Gold", "has_cadastre_title": False, "is_asm": True},
    {"name": "Ogun - Sagamu", "state": "Ogun", "lat": 6.8500, "lng": 3.6500, "mineral_type": "Limestone", "has_cadastre_title": True, "is_asm": False},
    {"name": "Bauchi - Gombe Road", "state": "Bauchi", "lat": 10.3158, "lng": 9.8442, "mineral_type": "Tin", "has_cadastre_title": False, "is_asm": True},
    {"name": "Niger - Kagara", "state": "Niger", "lat": 10.0500, "lng": 6.6500, "mineral_type": "Gold", "has_cadastre_title": False, "is_asm": True},
    {"name": "Kebbi - Gwandu", "state": "Kebbi", "lat": 12.5500, "lng": 4.6300, "mineral_type": "Gold", "has_cadastre_title": False, "is_asm": True},
    {"name": "Benue - Wannune", "state": "Benue", "lat": 7.4500, "lng": 8.9000, "mineral_type": "Lead-zinc", "has_cadastre_title": False, "is_asm": True},
    {"name": "Lagos - Lekki", "state": "Lagos", "lat": 6.4350, "lng": 3.9500, "mineral_type": "Bitumen", "has_cadastre_title": True, "is_asm": False},
]

with app.app_context():
    db.create_all()
    added = 0
    for r in NIGERIA_REGIONS:
        if not Region.query.filter_by(name=r["name"]).first():
            db.session.add(Region(**r))
            added += 1
    db.session.commit()
    print(f"Seeded {added} Nigerian mining regions. Total regions now: {Region.query.count()}")
