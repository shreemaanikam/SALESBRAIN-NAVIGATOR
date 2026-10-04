import re
file_path = "README.md"
with open(file_path, "r") as f:
    content = f.read()

vercel_instructions = """
# Vercel Deployment Instructions (Services / Monorepo)

This project uses Vercel Services to deploy both the Next.js frontend and the FastAPI backend within a single project.

## Prerequisites
1. A Vercel account with Services or Monorepo support enabled.
2. A PostgreSQL database (e.g. Supabase, Vercel Postgres, Render Postgres).
3. An S3-compatible Object Storage bucket (e.g. AWS S3, Cloudflare R2).
4. Firebase Authentication project.

## Environment Variables

### Shared / Vercel Project Level
Configure these in the Vercel Dashboard under **Settings > Environment Variables**:

**Backend Secrets (Do NOT prefix with `NEXT_PUBLIC_`):**
* `DATABASE_URL`: Your PostgreSQL connection string.
* `WORKSPACE_STORAGE_BACKEND`: `s3`
* `OBJECT_STORAGE_ENDPOINT`: e.g. `https://s3.amazonaws.com`
* `OBJECT_STORAGE_BUCKET`: The bucket name.
* `OBJECT_STORAGE_REGION`: e.g. `us-east-1`
* `OBJECT_STORAGE_ACCESS_KEY`: Your S3 Access Key.
* `OBJECT_STORAGE_SECRET_KEY`: Your S3 Secret Key.
* `FIREBASE_SERVICE_ACCOUNT`: JSON string of your Firebase Admin SDK credentials.
* `ENVIRONMENT`: `production`

**Frontend Public Variables (Must prefix with `NEXT_PUBLIC_`):**
* `NEXT_PUBLIC_API_BASE_URL`: `/api/v1`
* `NEXT_PUBLIC_FIREBASE_API_KEY`
* `NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN`
* `NEXT_PUBLIC_FIREBASE_PROJECT_ID`
* `NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET`
* `NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID`
* `NEXT_PUBLIC_FIREBASE_APP_ID`

## Deployment Steps
1. Connect your GitHub repository to Vercel.
2. Vercel will automatically detect `vercel.json` and configure the builds for `frontend/` (Next.js) and `backend/api/index.py` (FastAPI).
3. Add the environment variables listed above.
4. Deploy the project.

### Database Migration
The database tables are automatically initialized on application startup (`create_all` via FastAPI lifespan).

### Testing Steps
1. Go to your Vercel deployment URL.
2. Sign in with Firebase Auth.
3. Go to **My Data > Upload** and upload a CSV/XLSX file (Max 4.5 MB).
4. Verify the dashboard and ML insights generate successfully.
5. Check `/api/v1/health` to confirm `storage.reachable` is `true` and the database `status` is `ok`.

### Rollback Procedure
If a deployment fails:
1. Go to the **Deployments** tab in your Vercel Dashboard.
2. Locate the previous successful deployment.
3. Click the three dots (⋮) and select **Instant Rollback**.
4. To rollback database migrations, connect to your PostgreSQL database manually and restore from a backup.

---

"""

# Prepend the new instructions right after the main title
content = re.sub(r'# SalesBrain Navigator\n', f'# SalesBrain Navigator\n{vercel_instructions}', content)

with open(file_path, "w") as f:
    f.write(content)
