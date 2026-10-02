# SalesBrain Navigator

SalesBrain Navigator is a full-stack, AI-driven retail analytics dashboard built with Next.js, FastAPI, and Pandas. It provides dynamic profiling, visualization, and strategic recommendations for CSV and Excel datasets.

## Architecture

- **Frontend:** Next.js (React 18), Tailwind CSS, Lucide Icons, Recharts, Zustand.
- **Backend:** FastAPI, Pandas, NumPy, Scikit-learn, Shap, Python 3.11.
- **Database:** SQLite (Local dev & Free Tier Ephemeral) / PostgreSQL (Paid Production), SQLAlchemy, Alembic.
- **Authentication:** Firebase Client SDK (Frontend) & Firebase Admin SDK (Backend JWT Verification).
- **Storage:** Local Parquet files (Ephemeral on Free Tier).

---

## Local Development (Mock Authentication)

The default configuration enables a mocked authentication flow and a local SQLite database, so you don't need Firebase credentials to build or test.

1. **Install Backend Dependencies:**
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   alembic upgrade head
   ```

2. **Run Backend:**
   ```bash
   AUTH_MODE=local uvicorn app.main:app --reload
   ```

3. **Install Frontend Dependencies:**
   ```bash
   cd frontend
   npm install
   ```

4. **Run Frontend:**
   ```bash
   NEXT_PUBLIC_AUTH_MODE=local npm run dev
   ```

*(In local mode, the `/login` page allows you to bypass Firebase by typing any email to generate a dummy session).*

---

## Production Deployment (Render Free Tier)

To deploy to Render for free without adding payment methods, this project has been optimized to use Render Free Web Services. 

**Important Free Tier Caveat:** Render Free Web Services do not support persistent disks. This means your SQLite database and any uploaded Parquet datasets will be wiped whenever the instance spins down due to inactivity or when a new deployment is triggered.

### 1. Configure Firebase Authentication
- Create a project in the [Firebase Console](https://console.firebase.google.com/).
- Navigate to **Authentication** > **Sign-in method** and enable **Email/Password**.
- Navigate to **Project Settings** > **Service Accounts** and click **Generate new private key**. Copy the raw JSON file contents.
- In **Project Settings** > **General**, register a Web App and copy the `firebaseConfig` object values.
- Navigate to **Authentication** > **Settings** > **Authorized domains** and ensure your production frontend domain (e.g., `your-app.onrender.com`) is listed.

### 2. Deploy via Render Blueprint
Connect this repository to Render using the provided `render.yaml` Blueprint. The Blueprint automatically configures the **Free** instance types.

#### Backend Required Environment Variables (Render Dashboard):
* `DATABASE_URL`: `sqlite:///./backend/app/data/salesbrain.db`
* `ALLOW_EPHEMERAL_SQLITE`: `true`
* `AUTH_MODE`: `firebase`
* `FIREBASE_SERVICE_ACCOUNT`: The complete raw JSON string you copied from Firebase Service Accounts.

#### Frontend Required Environment Variables (Render Dashboard):
* `NEXT_PUBLIC_AUTH_MODE`: `firebase`
* `NEXT_PUBLIC_FIREBASE_API_KEY`: Your Firebase Web API Key.
* `NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN`: `your-project.firebaseapp.com`
* `NEXT_PUBLIC_FIREBASE_PROJECT_ID`: `your-project-id`
* `NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET`: `your-project.firebasestorage.app`
* `NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID`: `your-sender-id`
* `NEXT_PUBLIC_FIREBASE_APP_ID`: `your-app-id`
*(Note: `NEXT_PUBLIC_API_BASE_URL` is automatically configured via `RENDER_EXTERNAL_URL` in the Blueprint).*

### 3. Deploying Independently (Without Blueprint)
If you prefer not to use the Blueprint, you can create two separate "Web Services" via the Render Dashboard:

**Backend Service:**
1. Choose **New Web Service** > connect repository.
2. Select **Free** instance type.
3. Build Command: `pip install -r backend/requirements.txt && mkdir -p backend/app/data/uploads && alembic upgrade head`
4. Start Command: `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
5. Add the Backend Environment Variables from Step 2 above.

**Frontend Service:**
1. Choose **New Web Service** > connect repository.
2. Select **Free** instance type.
3. Build Command: `cd frontend && npm install && npm run build`
4. Start Command: `cd frontend && npm start`
5. Add the Frontend Environment Variables from Step 2 above. Also add `NEXT_PUBLIC_API_BASE_URL` pointing to the actual deployed backend URL (e.g., `https://your-backend.onrender.com/api/v1`).

---

## Testing & Quality Assurance

### Run Backend Tests (Pytest)
Includes rigorous testing for token verification, tenant data-isolation, and legacy workspace segregation.
```bash
cd backend
python -m pytest tests/ -v
```

### Run Frontend Build
```bash
cd frontend
npm run build
```

## Security & Known Risks
- **Tenant Isolation:** Active on all data operations. Endpoints are strictly protected by Firebase JWT validation.
- **Secret Management:** Production credentials must be exclusively stored in the hosting provider's Secrets Manager, NEVER in `.env` files or Git.
- **Storage Volatility:** Because this project uses the Render Free Tier without persistent disks or paid databases, user uploads and the SQLite database are ephemeral. They will reset to an empty state periodically.

## 🚀 Production Deployment (Render)

This application is designed to be deployed on Render.

### Ephemeral Storage Warning
**IMPORTANT:** The Render Free Web Service uses ephemeral local storage. Any SQLite databases (`salesbrain.db`) and uploaded datasets (`.parquet` files) stored on the local disk **WILL BE DELETED** when the service spins down due to inactivity or when a new deployment occurs.

To ensure your data is durable:
1. **Provision a PostgreSQL database** on Render and set `DATABASE_URL`.
2. **Provision an S3-compatible Object Storage Bucket** (e.g., AWS S3, Cloudflare R2) and configure the external storage environment variables.

### Environment Variables

Configure the following environment variables in your Render Dashboard:

```env
# Storage (Required for durable uploads)
WORKSPACE_STORAGE_BACKEND=s3
OBJECT_STORAGE_ENDPOINT=https://your-s3-endpoint.example.com
OBJECT_STORAGE_BUCKET=your-bucket-name
OBJECT_STORAGE_REGION=us-east-1
OBJECT_STORAGE_ACCESS_KEY=your-access-key
OBJECT_STORAGE_SECRET_KEY=your-secret-key

# Database
DATABASE_URL=postgresql://user:password@host:port/dbname

# Frontend CORS
CORS_ORIGINS=https://salesbrain-frontend-xxxx.onrender.com
```

### ML Model Artifacts

The pretrained Profit Prediction model (trained on the Superstore dataset) requires `profit_model.joblib` and `model_metadata.json`.

Because these artifacts can be large, they should either be:
1. Trained locally (`python -m backend.app.ml.train`) and committed if under 100MB.
2. Hosted on a private S3 bucket and downloaded at backend startup.

The current application will fallback gracefully. If the model is not found, the rule-based analytics and dashboards will remain fully functional, and a "Model Unavailable" warning will be shown for the ML features.

### Supported ML Features

The pre-trained model supports predicting `profit`. Datasets uploaded by users MUST contain the exact compatible features (e.g., `sales`, `quantity`, `discount`, `shipping_cost`, `category`, etc.) to use the ML prediction module. If the dataset does not have the required mapped features, the dashboard will safely disable ML predictions and show only rule-based insights.
