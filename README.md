# SalesBrain Navigator

An AI-Powered Retail Intelligence and Decision Support System.

SalesBrain Navigator is an enterprise-grade web application that leverages machine learning to predict transaction-level profit, detect risks, generate automated business recommendations, and simulate 'what-if' scenarios.

## Features

- **Executive Dashboard**: High-level KPIs and real-time business pulse.
- **Sales & Profitability Analytics**: Interactive visualizations of historical data.
- **AI Insights & Recommendations**: Rule-based engine highlighting risks and opportunities.
- **What-If Simulator**: Estimate profit outcomes of proposed pricing and shipping changes using an ensemble machine learning model.
- **Risk Center**: Detect statistical outliers and margin compression dynamically.
- **Reports**: Export capabilities for executive and operational datasets.

## Architecture

- **Backend**: FastAPI (Python 3.11), Pandas, scikit-learn (Voting Ensemble: ExtraTrees, RandomForest, GradientBoosting, etc.).
- **Frontend**: Next.js 14 (React 18), Tailwind CSS, Zustand, Recharts, React Three Fiber.
- **Integration**: Full REST API connecting the frontend with real-time data analysis and machine learning artifacts.

## Quick Start

### 1. Requirements
- Python 3.11
- Node.js 18+

### 2. Backend Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```

Set up environment variables:
```bash
cp .env.example .env
```
Ensure `dataset/Cleaned_SuperStore.csv` is present.

### 3. Machine Learning Training
Train the model artifacts before starting the backend:
```bash
python -m backend.app.ml.train
```

### 4. Start Backend
```bash
uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

### 5. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

The application will be available at `http://localhost:3000`.

## Testing

Run the comprehensive backend test suite:
```bash
pytest backend/tests/ -v
```

## Deployment

A `Dockerfile` and `docker-compose.yml` are provided for containerized deployment.
```bash
docker-compose up --build
```

---

## 🔒 Authentication & Database Configuration (Production Readiness)

SalesBrain Navigator is equipped with robust Tenant Isolation, Authentication flows, and Database pooling suited for local development and scalable production.

### Database Operations (SQLite vs PostgreSQL)
The application seamlessly toggles between SQLite (Local) and PostgreSQL (Production) based on the `DATABASE_URL` environment variable.

- **Local:** `DATABASE_URL=sqlite:///./backend/app/data/salesbrain.db`
- **Production:** `DATABASE_URL=postgresql://user:password@hostname:5432/dbname` (Configure in Render Dashboard).

**Running Migrations:**
We use `Alembic` to manage database schema updates. Before running the backend for the first time, or after pulling new code, run:
```bash
cd backend
alembic upgrade head
```

### Authentication Modes
The application supports two modes controlled by `AUTH_MODE` in your `.env`.

**1. Local Development (`AUTH_MODE=local`)**
Bypasses strict JWT validation and assigns a mock user ID for frictionless UI testing. *Note: The backend will crash intentionally if this mode is accidentally pushed to a production environment.*

**2. Production (`AUTH_MODE=firebase`)**
Enforces strict JWT token validation. To enable:
1. Set up a Firebase project and enable Email/Password Authentication.
2. Obtain the Firebase Admin SDK private key JSON.
3. Configure the frontend `AuthContext.tsx` to use the Firebase JS SDK `signInWithEmailAndPassword` method to retrieve the real JWT token.
4. Set `AUTH_MODE=firebase` in your Render environment variables.

### Troubleshooting
- **401 Unauthorized:** Ensure the frontend is correctly storing the token in `localStorage` and `api.ts` is attaching it to the `Authorization: Bearer <token>` header.
- **500 Internal Server Error (Auth):** If deployed to Render, ensure `AUTH_MODE` is explicitly set to `firebase`.
- **Database Missing Column:** You forgot to run `alembic upgrade head`.

---
