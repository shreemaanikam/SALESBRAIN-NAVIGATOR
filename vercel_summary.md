# Vercel Deployment Summary

## Files Changed:
1. `vercel.json` (Created) - Defines the Vercel Services setup mapping `/api/(.*)` to the backend and the rest to Next.js.
2. `backend/api/index.py` (Created) - The serverless entrypoint for FastAPI that automatically fixes `sys.path` so the `backend.app.main:app` can be imported properly within Vercel's root execution context.
3. `.vercelignore` (Created) - Excludes caches, tests, and heavy unused artifacts to keep the bundle size small.
4. `frontend/src/services/api.ts` - Updated `API_BASE` to automatically default to `/api/v1` in production to support the same-domain unified deployment.
5. `backend/requirements.txt` - Removed `shap` (a ~100MB+ dependency) which is not used in production inference.
6. `backend/app/services/explanation_service.py` - Made `shap` imports optional so it gracefully falls back without crashing the app.
7. `backend/app/api/v1/routes/datasets.py` & `frontend/src/app/dashboard/my-data/upload/page.tsx` - Safely clamped upload limits to 4.5 MB in both the frontend and backend to comply with Vercel's Serverless Function payload limits.
8. `backend/app/main.py` - Added programmatic database schema initialization (`Base.metadata.create_all`) to the startup lifespan for serverless cold-start safety.
9. `backend/app/services/workspace_service.py` - Removed the dangerous `df.to_parquet()` local disk write and replaced it with `storage_service.save_dataframe()` to ensure resilient saves to S3/Postgres in serverless mode.
10. `backend/app/core/config.py` & `backend/app/services/prediction_service.py` - Refactored relative path loading for ML artifacts and seed datasets using absolute module path resolution (`__file__`) so they load accurately regardless of the Vercel working directory.
11. `backend/app/api/deps.py` - Ensured `AUTH_MODE` correctly defaults to `firebase` during production deployments on Vercel.
12. `backend/tests/test_vercel.py` & `backend/tests/test_deployment.py` (Created) - Wrote tests for entrypoints, auth, tenant isolation, and upload limits.
13. `README.md` - Added detailed Vercel deployment prerequisites, environmental variables, and rollback steps.

## Final Vercel Configuration (`vercel.json`)
```json
{
  "services": {
    "frontend": {
      "root": "frontend",
      "framework": "nextjs"
    },
    "backend": {
      "root": "backend",
      "entrypoint": "api/index:app"
    }
  },
  "rewrites": [
    { "source": "/api/(.*)", "destination": { "service": "backend" } },
    { "source": "/(.*)", "destination": { "service": "frontend" } }
  ]
}
```

## Environment Variables

### Backend
* `DATABASE_URL` (Postgres connection string)
* `WORKSPACE_STORAGE_BACKEND` (Set to `s3`)
* `OBJECT_STORAGE_ENDPOINT`
* `OBJECT_STORAGE_BUCKET`
* `OBJECT_STORAGE_REGION`
* `OBJECT_STORAGE_ACCESS_KEY`
* `OBJECT_STORAGE_SECRET_KEY`
* `FIREBASE_SERVICE_ACCOUNT` (JSON payload)
* `ENVIRONMENT` (Set to `production`)

### Frontend (Must have `NEXT_PUBLIC_`)
* `NEXT_PUBLIC_API_BASE_URL` (Set to `/api/v1`)
* `NEXT_PUBLIC_FIREBASE_API_KEY`
* `NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN`
* `NEXT_PUBLIC_FIREBASE_PROJECT_ID`
* `NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET`
* `NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID`
* `NEXT_PUBLIC_FIREBASE_APP_ID`

## Test Results
* **Frontend:** `npm run build` completed an optimized production build.
* **Backend:** Ran `pytest backend/tests/test_deployment.py` and `test_vercel.py`. Passed tests validating health endpoints, tenant isolation, storage adapters, and the Vercel entrypoint.

## Remaining Blockers / Manual Actions
* You must configure an actual PostgreSQL database (e.g., Supabase or Vercel Postgres) and supply the connection string.
* You must provision an S3-compatible bucket and supply credentials.
* File uploads are capped at 4.5 MB. If files larger than this are needed, you will need to implement a full S3 Pre-Signed URL flow (this would require extensive frontend/backend modifications beyond this task's safe scope, so the limit is enforced securely instead).

## Safe Deployment Checklist
1. Connect repo to Vercel.
2. Vercel will automatically detect `vercel.json` and configure `frontend/` and `backend/api/index.py`.
3. Add the precise environment variables listed above.
4. Deploy!
