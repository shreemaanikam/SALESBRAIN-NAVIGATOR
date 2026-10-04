with open('backend/app/services/workspace_service.py', 'r') as f:
    content = f.read()

import re

# We need to import prediction_service
content = content.replace(
    "from typing import Dict, Any, List, Optional", 
    "from typing import Dict, Any, List, Optional\nfrom backend.app.services.prediction_service import prediction_service"
)

old_kpis = r"""    result\["kpis"\] = kpis"""
new_kpis = """    result["kpis"] = kpis
    
    # ── ML Predictions ──
    ml_status = prediction_service.check_compatibility(mapping)
    result["ml_compatibility"] = ml_status
    if ml_status.get("compatible"):
        try:
            preds = prediction_service.predict_batch(df, mapping)
            total_pred_profit = float(preds.sum())
            kpis.append({"label": "Predicted Profit (ML)", "value": f"${total_pred_profit:,.2f}", "raw": total_pred_profit, "is_ml": True})
            
            # Aggregate predictions by Category if available
            if col("category"):
                df_temp = df.copy()
                df_temp["_pred_profit"] = preds
                cat_preds = df_temp.groupby(col("category"))["_pred_profit"].sum().reset_index()
                cat_preds = cat_preds.sort_values("_pred_profit", ascending=False).to_dict("records")
                result["ml_predictions_by_category"] = [
                    {"category": row[col("category")], "predicted_profit": row["_pred_profit"]} 
                    for row in cat_preds
                ]
            result["ml_predictions"] = {"total_predicted_profit": total_pred_profit, "model_info": prediction_service.get_model_info()}
        except Exception as e:
            logger.error(f"Failed to generate ML predictions for dashboard: {e}")
            result["ml_compatibility"]["error"] = str(e)
            result["ml_compatibility"]["compatible"] = False"""

content = re.sub(old_kpis, new_kpis, content)

with open('backend/app/services/workspace_service.py', 'w') as f:
    f.write(content)
