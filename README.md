# Nigeria Mining AI Tracker

AI-powered MVP that helps miners track mineral-rich regions across Nigeria.

## What it does

Miners or field officers upload sensor readings (mineral concentration, depth, yield) for named Nigerian mining regions. A Random Forest AI model scores each region 0-100 based on the accumulated data. A map centered on Nigeria shows regions colour-coded green, amber, or red so a miner can quickly see where to focus.

## Project structure

```
mining-tracker/
├── app.py                  Flask API
├── models.py                Database models
├── ml_model.py               AI scoring engine
├── seed.py                  Loads 15 real Nigerian mining regions
├── sample_readings.csv      Test data for the upload feature
├── requirements.txt
├── Procfile                  for Render deployment
├── .gitignore
└── client/                  React frontend
    ├── src/
    │   ├── App.js
    │   ├── index.js
    │   ├── index.css
    │   └── components/
    │       ├── MiningMap.js
    │       ├── RegionTable.js
    │       └── UploadForm.js
    └── package.json
```

## Step 1 — Run the backend locally

```bash
cd mining-tracker
python3 -m venv venv
source venv/bin/activate          # on Windows: venv\Scripts\activate
pip install -r requirements.txt
python seed.py                    # loads 15 Nigerian mining regions
python app.py
```

Your API now runs at `http://localhost:5000`. Test it:

```bash
curl http://localhost:5000/api/regions
```

You should see 15 Nigerian regions as JSON.

## Step 2 — Run the frontend locally

Open a new terminal tab.

```bash
cd mining-tracker/client
npm install
npm start
```

Your app opens at `http://localhost:3000`. You should see a map of Nigeria with 15 markers.

## Step 3 — Test the full loop locally

1. Click "Upload sensor readings" and choose `sample_readings.csv` from the project root.
2. Wait for the success message.
3. Click "Run AI scoring".
4. Watch the map markers change colour and the table re-sort by score.

If this works locally, your MVP logic is correct end to end.

## Step 4 — Deploy the backend to Render

1. Push this whole folder to a GitHub repo.
2. Go to render.com, sign up with GitHub.
3. New → PostgreSQL → name it `mining-tracker-db` → free tier → copy the Internal Database URL.
4. New → Web Service → connect your repo.
5. Build command: `pip install -r requirements.txt`
6. Start command: `gunicorn app:app`
7. Add environment variable `DATABASE_URL` = the Postgres URL from step 3.
8. Deploy. You get a live URL like `https://mining-tracker-api.onrender.com`.
9. Run the seed script once against the live database:
   ```bash
   DATABASE_URL="your-render-postgres-url" python seed.py
   ```

## Step 5 — Deploy the frontend to Vercel

```bash
cd client
npm install -g vercel
vercel
```

Set the environment variable in Vercel dashboard:
```
REACT_APP_API_URL = https://mining-tracker-api.onrender.com
```

Redeploy after setting the env variable so it takes effect.

## Step 6 — Final end-to-end test on the live URLs

Go through this checklist on your live links, not localhost:

- [ ] Frontend loads, map shows Nigeria with 15 regions
- [ ] Upload `sample_readings.csv` successfully
- [ ] Run AI scoring, scores update
- [ ] Map colours update to match new scores
- [ ] Table sorts correctly by score
- [ ] Refresh page, confirm data did not reset
- [ ] Test on a mobile phone browser

## Notes on the AI model

The model is a Random Forest Regressor trained on synthetic data that encodes domain knowledge: higher mineral concentration, higher yield, more reading confirmations, and higher-value minerals (lithium, gold) push the score up. Replace `generate_training_data()` in `ml_model.py` with real historical outcomes once you have them, and call `scorer.train(X, y)` with your real data.

## Team

Built by Divine Omoefe Ailemen 
