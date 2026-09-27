from fastapi import APIRouter
from backend.app.services.data_service import data_service
from backend.app.data.schema import EXPECTED_COLUMNS
from backend.app.schemas.analytics import DataQuality, ColumnInfo

router = APIRouter()

@router.get("/data/schema")
def get_data_schema():
    return {"columns": EXPECTED_COLUMNS}

@router.get("/data/quality", response_model=DataQuality)
def get_data_quality():
    q_info = data_service.get_quality_info()
    df = data_service.get_df()
    
    cols = []
    for col in df.columns:
        cols.append(ColumnInfo(
            name=col,
            dtype=str(df[col].dtype),
            description="",
            non_null_count=int(df[col].notna().sum()),
            sample_values=df[col].dropna().head(3).tolist()
        ))
        
    return DataQuality(
        row_count=q_info.get("row_count", 0),
        column_count=q_info.get("column_count", 0),
        missing_values=q_info.get("missing_counts", {}),
        date_range=q_info.get("date_range", {}),
        duplicates=q_info.get("duplicate_count", 0),
        columns=cols
    )
