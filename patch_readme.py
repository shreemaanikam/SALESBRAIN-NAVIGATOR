with open('README.md', 'a') as f:
    f.write("""
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
""")
