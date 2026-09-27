import pandas as pd
import numpy as np

class RiskService:
    def get_risks(self, df: pd.DataFrame, category=None, region=None, limit=50):
        if df.empty:
            return []
            
        if category:
            df = df[df['category'] == category]
        if region:
            df = df[df['region'] == region]
            
        risks = []
        
        if 'profit' in df.columns:
            neg_profit = df[df['profit'] < 0].sort_values('profit').head(limit)
            for _, row in neg_profit.iterrows():
                order_id = row.get('order_id', 'unknown')
                risks.append({
                    "id": f"risk_prof_{order_id}",
                    "type": "negative_profit",
                    "severity": "High",
                    "affected_entity": str(order_id),
                    "actual_value": float(row['profit']),
                    "threshold": 0.0,
                    "detection_method": "rule_engine",
                    "evidence": {"sales": float(row.get('sales', 0)), "profit": float(row['profit'])},
                    "recommended_action": "Review pricing and cost for this order.",
                    "order_id": str(order_id)
                })

        return risks[:limit]

    def get_opportunities(self, df: pd.DataFrame, category=None, region=None, limit=50):
        if df.empty:
            return []
        
        opps = []
        if 'Profit_Margin' in df.columns:
            high_margin = df[df['Profit_Margin'] > 40].head(limit)
            for _, row in high_margin.iterrows():
                order_id = row.get('order_id', 'unknown')
                opps.append({
                    "id": f"opp_marg_{order_id}",
                    "type": "high_margin",
                    "severity": "Low",
                    "affected_entity": str(order_id),
                    "actual_value": float(row['Profit_Margin']),
                    "threshold": 40.0,
                    "detection_method": "rule_engine",
                    "evidence": {"margin": float(row['Profit_Margin'])},
                    "recommended_action": "Analyze success factors for replication.",
                    "order_id": str(order_id)
                })
                
        return opps[:limit]

risk_service = RiskService()
