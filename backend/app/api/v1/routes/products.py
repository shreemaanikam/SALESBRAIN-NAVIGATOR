from fastapi import APIRouter, Query, HTTPException, Depends
from typing import Optional
from backend.app.services.data_service import data_service
from backend.app.schemas.product import ProductListResponse, ProductSummary, ProductDetail
from backend.app.schemas.common import FilterParams
from backend.app.data.validation import clean_for_json
from backend.app.api.v1.routes.sales import apply_filters

router = APIRouter()

def get_risk_status(margin: float) -> str:
    if margin < -10:
        return "High"
    elif margin < 5:
        return "Medium"
    return "Low"

@router.get("/products", response_model=ProductListResponse)
def list_products(
    q: Optional[str] = None,
    filters: FilterParams = Depends(),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    sort_by: str = Query('total_sales'),
    sort_order: str = Query('desc')
):
    df = apply_filters(data_service.get_df(), filters)
    if q:
        df = df[df['product_name'].str.contains(q, case=False, na=False) | df['product_id'].str.contains(q, case=False, na=False)]
        
    grouped = df.groupby(['product_id', 'product_name', 'category', 'sub_category']).agg({
        'sales': 'sum',
        'profit': 'sum',
        'quantity': 'sum',
        'discount': 'mean',
        'shipping_cost': 'sum',
        'order_id': 'nunique'
    }).reset_index()
    
    # sorting
    if sort_by in ['total_sales', 'total_profit', 'total_quantity', 'avg_discount', 'order_count']:
        map_col = {
            'total_sales': 'sales', 'total_profit': 'profit', 'total_quantity': 'quantity',
            'avg_discount': 'discount', 'order_count': 'order_id'
        }
        grouped = grouped.sort_values(by=map_col.get(sort_by, 'sales'), ascending=(sort_order == 'asc'))
        
    total = len(grouped)
    start = (page - 1) * page_size
    end = start + page_size
    paged = grouped.iloc[start:end]
    
    products = []
    for _, row in paged.iterrows():
        sales = clean_for_json(row['sales'])
        profit = clean_for_json(row['profit'])
        margin = (profit / sales * 100) if sales else 0
        products.append(ProductSummary(
            product_id=clean_for_json(row['product_id']),
            name=clean_for_json(row['product_name']),
            category=clean_for_json(row['category']),
            sub_category=clean_for_json(row['sub_category']),
            total_sales=sales,
            total_profit=profit,
            profit_margin=margin,
            total_quantity=clean_for_json(row['quantity']),
            avg_discount=clean_for_json(row['discount']),
            total_shipping_cost=clean_for_json(row['shipping_cost']),
            order_count=clean_for_json(row['order_id']),
            risk_status=get_risk_status(margin)
        ))
        
    return ProductListResponse(products=products, total=total, page=page, page_size=page_size)

@router.get("/products/{product_id}", response_model=ProductDetail)
def get_product(product_id: str):
    df = data_service.get_df()
    prod_df = df[df['product_id'] == product_id]
    
    if prod_df.empty:
        raise HTTPException(status_code=404, detail="Product not found")
        
    row = prod_df.iloc[0]
    sales = clean_for_json(prod_df['sales'].sum())
    profit = clean_for_json(prod_df['profit'].sum())
    margin = (profit / sales * 100) if sales else 0
    
    monthly_trend = prod_df.groupby(['year', 'Month', 'Month_Name']).agg({'sales': 'sum', 'profit': 'sum'}).reset_index().sort_values(['year', 'Month'])
    
    return ProductDetail(
        product_id=clean_for_json(row['product_id']),
        name=clean_for_json(row['product_name']),
        category=clean_for_json(row['category']),
        sub_category=clean_for_json(row['sub_category']),
        total_sales=sales,
        total_profit=profit,
        profit_margin=margin,
        total_quantity=clean_for_json(prod_df['quantity'].sum()),
        avg_discount=clean_for_json(prod_df['discount'].mean()),
        total_shipping_cost=clean_for_json(prod_df['shipping_cost'].sum()),
        order_count=clean_for_json(prod_df['order_id'].nunique()),
        risk_status=get_risk_status(margin),
        markets=prod_df['market'].dropna().unique().tolist(),
        regions=prod_df['region'].dropna().unique().tolist(),
        countries=prod_df['country'].dropna().unique().tolist(),
        monthly_trend=[{
            "year": clean_for_json(r['year']),
            "month_name": clean_for_json(r['Month_Name']),
            "sales": clean_for_json(r['sales']),
            "profit": clean_for_json(r['profit'])
        } for _, r in monthly_trend.iterrows()]
    )
