import numpy as np
from datetime import datetime
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import os

MINERAL_VALUE_INDEX = {
    "Lithium": 0.95,
    "Gold": 0.90,
    "Tin": 0.55,
    "Iron ore": 0.50,
    "Lead-zinc": 0.45,
    "Coal": 0.40,
    "Limestone": 0.30,
    "Bitumen": 0.35,
    "Gemstone": 0.70,
}


class RegionScorer:
    def __init__(self):
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            random_state=42,
            n_jobs=-1
        )
        self.scaler = StandardScaler()
        self.is_trained = False
        self.feature_names = [
            'avg_concentration', 'std_concentration',
            'avg_depth', 'trend_depth',
            'avg_yield', 'std_yield',
            'reading_count', 'recency_days',
            'mineral_value'
        ]

    def extract_features(self, readings: list, mineral_type: str = None) -> np.ndarray:
        if not readings:
            return np.zeros(len(self.feature_names))

        conc = [r.mineral_concentration for r in readings]
        depth = [r.depth_m for r in readings]
        yld = [r.yield_kg for r in readings]
        timestamps = [r.timestamp for r in readings if r.timestamp]

        if timestamps:
            latest = max(timestamps)
            recency = (datetime.utcnow() - latest).days
        else:
            recency = 90

        if len(depth) >= 2:
            trend = np.polyfit(range(len(depth)), depth, 1)[0]
        else:
            trend = 0.0

        mineral_value = MINERAL_VALUE_INDEX.get(mineral_type, 0.4)

        return np.array([
            np.mean(conc), np.std(conc),
            np.mean(depth), trend,
            np.mean(yld), np.std(yld),
            len(readings), recency,
            mineral_value
        ])

    def generate_training_data(self, n_samples=600):
        np.random.seed(42)
        X, y = [], []

        for _ in range(n_samples):
            avg_conc = np.random.uniform(0.1, 1.0)
            std_conc = np.random.uniform(0.0, 0.3)
            avg_depth = np.random.uniform(10, 100)
            trend = np.random.uniform(-2, 5)
            avg_yield = np.random.uniform(10, 500)
            std_yield = np.random.uniform(0, 100)
            count = np.random.randint(1, 50)
            recency = np.random.randint(0, 90)
            mineral_value = np.random.uniform(0.3, 0.95)

            score = (
                avg_conc * 30 +
                (avg_yield / 500) * 25 +
                mineral_value * 25 +
                min(count, 30) / 30 * 10 +
                max(0, trend) * 1.5 +
                (1 - recency / 90) * 8
            )
            score = np.clip(score + np.random.normal(0, 3), 0, 100)

            X.append([avg_conc, std_conc, avg_depth, trend,
                       avg_yield, std_yield, count, recency, mineral_value])
            y.append(score)

        return np.array(X), np.array(y)

    def train(self, X=None, y=None):
        if X is None or y is None:
            X, y = self.generate_training_data()

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        X_train_s = self.scaler.fit_transform(X_train)
        X_test_s = self.scaler.transform(X_test)

        self.model.fit(X_train_s, y_train)
        self.is_trained = True

        preds = self.model.predict(X_test_s)
        mae = mean_absolute_error(y_test, preds)
        r2 = r2_score(y_test, preds)

        print(f"Model trained. MAE: {mae:.2f} | R2: {r2:.3f}")
        return {'mae': mae, 'r2': r2}

    def score_region(self, readings: list, mineral_type: str = None) -> float:
        if not self.is_trained:
            self.train()

        features = self.extract_features(readings, mineral_type)
        X = features.reshape(1, -1)
        X_scaled = self.scaler.transform(X)
        raw = self.model.predict(X_scaled)[0]
        return round(float(np.clip(raw, 0, 100)), 2)

    def feature_importance(self) -> dict:
        if not self.is_trained:
            return {}
        importance = self.model.feature_importances_
        return dict(zip(self.feature_names, importance.tolist()))

    def save(self, path='model.joblib'):
        joblib.dump({'model': self.model, 'scaler': self.scaler, 'is_trained': self.is_trained}, path)

    def load(self, path='model.joblib'):
        if os.path.exists(path):
            data = joblib.load(path)
            self.model = data['model']
            self.scaler = data['scaler']
            self.is_trained = data.get('is_trained', True)
        else:
            self.train()
            self.save(path)


scorer = RegionScorer()
