# SalesBrain Navigator

SalesBrain Navigator is a full-stack, AI-driven retail analytics dashboard built with Next.js, FastAPI, and Pandas. It provides dynamic profiling, visualization, and strategic recommendations for CSV and Excel datasets.

## Architecture

- **Frontend:** Next.js (React 18), Tailwind CSS, Lucide Icons, Recharts, Zustand.
- **Backend:** FastAPI, Pandas, NumPy, Scikit-learn, Shap, Python 3.11.
- **Database:** PostgreSQL (Production) / SQLite (Local dev), SQLAlchemy, Alembic.
- **Authentication:** Firebase Client SDK (Frontend) & Firebase Admin SDK (Backend JWT Verification).
- **Storage:** Local Parquet files (Durable disk in Production).

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

## Production Deployment (Render + Firebase + PostgreSQL)

To deploy securely to production, follow these steps to configure real services.

### 1. Provision a PostgreSQL Database
The app explicitly blocks SQLite in production (`RENDER=true` or `ENVIRONMENT=production`). 
- In your Render Dashboard, create a **PostgreSQL** database.
- Copy the **Internal Database URL**.

### 2. Configure Firebase Authentication
- Create a project in the [Firebase Console](https://console.firebase.google.com/).
- Navigate to **Authentication** > **Sign-in method** and enable **Email/Password**.
- Navigate to **Project Settings** > **Service Accounts** and click **Generate new private key**. Copy the raw JSON file contents.
- In **Project Settings** > **General**, register a Web App and copy the `firebaseConfig` object values.
- Navigate to **Authentication** > **Settings** > **Authorized domains** and ensure your production frontend domain (e.g., `your-app.onrender.com`) is listed.

### 3. Deploy via Render Blueprint
Connect this repository to Render using the provided `render.yaml` Blueprint.

#### Backend Required Environment Variables (Render Dashboard):
* `DATABASE_URL`: Your PostgreSQL Internal Database URL (e.g., `postgresql://user:password@host:5432/dbname`)
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

### 4. Data Persistence & Migrations
The Render Blueprint automatically mounts a 1GB persistent disk at `/opt/render/project/src/backend/app/data` to retain uploaded Parquet files.
Alembic schema migrations automatically run during the build step (`alembic upgrade head`) ensuring PostgreSQL is up to date before traffic is routed.

### 5. Smoke Testing the Live Application
1. Navigate to your deployed Frontend URL (HTTPS).
2. Create a test account or sign in with an existing Firebase identity.
3. Open **My Data** and upload a synthetic CSV file.
4. Verify the dashboard, insights, and recommendations generate successfully.
5. Attempt to access the same workspace via another user account or incognito window to verify strict Tenant Isolation.

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
- **Upload Safety:** Datasets are converted to Parquet natively. Arbitrary filesystem access is blocked; identifiers enforce UUID boundaries.
- **Database Backup:** Render automatically backs up managed PostgreSQL instances. You must separately backup the `salesbrain-data` disk if Parquet files are critical for long-term storage.
