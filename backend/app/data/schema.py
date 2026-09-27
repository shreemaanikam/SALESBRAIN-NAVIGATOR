EXPECTED_COLUMNS = [
    'order_id', 'order_date', 'ship_date', 'ship_mode', 'customer_name', 
    'segment', 'state', 'country', 'market', 'region', 'product_id', 
    'category', 'sub_category', 'product_name', 'sales', 'quantity', 
    'discount', 'profit', 'shipping_cost', 'order_priority', 'year', 
    'Month', 'Month_Name', 'Quarter', 'Day', 'Day_Name', 'Shipping_Days', 
    'Profit_Margin'
]

NUMERIC_COLUMNS = ['sales', 'quantity', 'discount', 'profit', 'shipping_cost', 'Shipping_Days', 'Profit_Margin', 'year', 'Month', 'Quarter', 'Day']
CATEGORICAL_COLUMNS = ['ship_mode', 'segment', 'state', 'country', 'market', 'region', 'category', 'sub_category', 'order_priority', 'Month_Name', 'Day_Name']
DATE_COLUMNS = ['order_date', 'ship_date']
ID_COLUMNS = ['order_id', 'product_id', 'customer_name', 'product_name']
DERIVED_COLUMNS = ['year', 'Month', 'Month_Name', 'Quarter', 'Day', 'Day_Name', 'Shipping_Days', 'Profit_Margin']
