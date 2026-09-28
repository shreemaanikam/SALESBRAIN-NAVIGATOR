from fastapi import APIRouter
from backend.app.api.v1.routes import health, dashboard, sales, products, customers, geography, profitability, outliers, data_routes
from backend.app.api.v1.routes import predictions, insights, explanations, scenarios, reports
from backend.app.api.v1.routes import datasets

api_router = APIRouter()

api_router.include_router(health.router, tags=["health"])
api_router.include_router(dashboard.router, tags=["dashboard"])
api_router.include_router(sales.router, tags=["sales"])
api_router.include_router(products.router, tags=["products"])
api_router.include_router(customers.router, tags=["customers"])
api_router.include_router(geography.router, tags=["geography"])
api_router.include_router(profitability.router, tags=["profitability"])
api_router.include_router(outliers.router, tags=["outliers"])
api_router.include_router(data_routes.router, tags=["data"])

# New routes
api_router.include_router(predictions.router, tags=["predictions"])
api_router.include_router(insights.router, tags=["insights"])
api_router.include_router(explanations.router, tags=["explanations"])
api_router.include_router(scenarios.router, tags=["scenarios"])
api_router.include_router(reports.router, tags=["reports"])
api_router.include_router(datasets.router, tags=["datasets"])
