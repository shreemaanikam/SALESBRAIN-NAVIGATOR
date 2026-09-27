export interface Product {
  id: string;
  name: string;
  category: string;
  subCategory: string;
  region: string;
  market: string;
  country: string;
  sales: number;
  profit: number;
  profitMargin: number;
  quantity: number;
  averageDiscount: number;
  shippingCost: number;
  orderCount: number;
  riskStatus: 'Low' | 'Medium' | 'High';
}

export interface Metric {
  label: string;
  value: string | number;
  trend: 'up' | 'down' | 'neutral';
  trendValue?: string;
  description?: string;
}

export interface ChartData {
  name: string;
  [key: string]: string | number;
}

export interface Insight {
  id: string;
  type: 'Analytical Insight' | 'Recommendation Preview' | 'Risk Alert';
  title: string;
  description: string;
  recommendation?: string;
  impact?: 'High' | 'Medium' | 'Low';
  affectedEntity?: string;
}

export interface Outlier {
  id: string;
  orderId: string;
  sales: number;
  profit: number;
  margin: number;
  discount: number;
  type: 'Loss Risk' | 'High Discount' | 'Sales Anomaly' | 'Shipping Anomaly';
  severity: 'Low' | 'Medium' | 'High';
}
