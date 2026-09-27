import pandas as pd
import numpy as np

class RecommendationService:
    def generate_recommendations(self, df: pd.DataFrame, category=None, region=None, market=None):
        if df.empty:
            return []
            
        if category:
            df = df[df['category'] == category]
        if region:
            df = df[df['region'] == region]
        if market:
            df = df[df['market'] == market]
            
        recs = []
        
        if 'product_id' in df.columns and 'sales' in df.columns and 'profit' in df.columns:
            prod_df = df.groupby('product_id').agg({'sales': 'sum', 'profit': 'sum'}).reset_index()
            prod_df['margin'] = np.where(prod_df['sales'] > 0, prod_df['profit'] / prod_df['sales'], 0)
            median_sales = prod_df['sales'].median()
            bad_prods = prod_df[(prod_df['sales'] > median_sales) & (prod_df['margin'] < 0.05)]
            for _, row in bad_prods.head(5).iterrows():
                recs.append({
                    "id": f"rec_prod_{row['product_id']}",
                    "title": "High Sales, Low Margin Product",
                    "insight": f"Product {row['product_id']} has high sales but margin is under 5%.",
                    "affected_entity": str(row['product_id']),
                    "metric_values": {"sales": float(row['sales']), "margin": float(row['margin'])},
                    "suggested_action": "Consider reviewing pricing or cost structure.",
                    "priority": "High",
                    "source": "rule_engine",
                    "limitations": "Historical data suggests this trend; validate before acting."
                })
                
        if 'sub_category' in df.columns and 'discount' in df.columns:
            sub_df = df.groupby('sub_category').agg({'discount': 'mean', 'sales': 'sum', 'profit': 'sum'}).reset_index()
            sub_df['margin'] = np.where(sub_df['sales'] > 0, sub_df['profit'] / sub_df['sales'], 0)
            bad_subs = sub_df[(sub_df['discount'] > 0.2) & (sub_df['margin'] < 0.1)]
            for _, row in bad_subs.head(5).iterrows():
                recs.append({
                    "id": f"rec_sub_{row['sub_category']}",
                    "title": "High Discount Impacts Profitability",
                    "insight": f"Sub-category {row['sub_category']} averages >20% discount with <10% margin.",
                    "affected_entity": str(row['sub_category']),
                    "metric_values": {"avg_discount": float(row['discount']), "margin": float(row['margin'])},
                    "suggested_action": "Evaluate discount strategy for these items.",
                    "priority": "Medium",
                    "source": "rule_engine",
                    "limitations": "Validate before acting."
                })

        if 'sub_category' in df.columns:
            loss_subs = df.groupby('sub_category')['profit'].sum().reset_index()
            loss_subs = loss_subs[loss_subs['profit'] < 0]
            for _, row in loss_subs.head(5).iterrows():
                recs.append({
                    "id": f"loss_{row['sub_category']}",
                    "title": "Loss-making Sub-category",
                    "insight": f"Sub-category {row['sub_category']} has a total negative profit.",
                    "affected_entity": str(row['sub_category']),
                    "metric_values": {"total_profit": float(row['profit'])},
                    "suggested_action": "Investigate root causes of losses.",
                    "priority": "High",
                    "source": "rule_engine",
                    "limitations": "Based on historical aggregate."
                })

        if 'region' in df.columns:
            reg_df = df.groupby('region').agg({'sales': 'sum', 'profit': 'sum'}).reset_index()
            reg_df['margin'] = np.where(reg_df['sales'] > 0, reg_df['profit'] / reg_df['sales'], 0)
            avg_margin = reg_df['margin'].mean()
            opp_regs = reg_df[(reg_df['sales'] > reg_df['sales'].median()) & (reg_df['margin'] < avg_margin)]
            for _, row in opp_regs.head(5).iterrows():
                recs.append({
                    "id": f"opp_reg_{row['region']}",
                    "title": "Regional Margin Opportunity",
                    "insight": f"Region {row['region']} has high sales but below-average margin.",
                    "affected_entity": str(row['region']),
                    "metric_values": {"sales": float(row['sales']), "margin": float(row['margin'])},
                    "suggested_action": "Optimize operations to improve margin.",
                    "priority": "Medium",
                    "source": "rule_engine",
                    "limitations": "Assumes potential for margin improvement."
                })

        if 'sub_category' in df.columns and 'shipping_cost' in df.columns:
            ship_df = df.groupby('sub_category').agg({'sales': 'sum', 'shipping_cost': 'sum'}).reset_index()
            ship_df['ship_ratio'] = np.where(ship_df['sales'] > 0, ship_df['shipping_cost'] / ship_df['sales'], 0)
            bad_ship = ship_df[ship_df['ship_ratio'] > 0.15]
            for _, row in bad_ship.head(5).iterrows():
                recs.append({
                    "id": f"ship_sub_{row['sub_category']}",
                    "title": "High Shipping Cost Ratio",
                    "insight": f"Shipping cost for {row['sub_category']} is >15% of sales.",
                    "affected_entity": str(row['sub_category']),
                    "metric_values": {"ship_ratio": float(row['ship_ratio'])},
                    "suggested_action": "Review shipping logistics and carrier rates.",
                    "priority": "Low",
                    "source": "rule_engine",
                    "limitations": "Check if high shipping costs are standard for this category."
                })
                
        return recs

recommendation_service = RecommendationService()
