from backend.app.services.prediction_service import prediction_service

class ScenarioService:
    def simulate(self, baseline: dict, scenario: dict):
        discount = baseline.get('discount', 0)
        quantity = baseline.get('quantity', 1)
        shipping_cost = baseline.get('shipping_cost', 0)
        sales = baseline.get('sales', 0)

        new_discount = max(0.0, min(0.8, discount + scenario.get('discount_delta', 0)))
        new_quantity = int(quantity * (1 + scenario.get('quantity_change_pct', 0) / 100))
        new_quantity = max(1, min(new_quantity, quantity * 6))
        
        new_shipping_cost = shipping_cost * (1 + scenario.get('shipping_cost_change_pct', 0) / 100)
        new_sales = sales * (1 + scenario.get('sales_change_pct', 0) / 100)

        scenario_input = baseline.copy()
        scenario_input.update({
            'discount': new_discount,
            'quantity': new_quantity,
            'shipping_cost': new_shipping_cost,
            'sales': new_sales
        })

        warnings = []
        assumptions = ["Ceteris paribus (all other factors remain constant)"]

        if prediction_service.is_ready():
            base_res = prediction_service.predict(baseline)
            scen_res = prediction_service.predict(scenario_input)
            base_profit = base_res.get('predicted_profit', 0)
            scen_profit = scen_res.get('predicted_profit', 0)
            mode = 'model'
            model_version = base_res.get('model_version', '1.0')
        else:
            margin_rate = 0.15 - (baseline.get('discount', 0) * 0.2)
            base_profit = (sales * margin_rate) - shipping_cost
            
            scen_margin = 0.15 - (new_discount * 0.2)
            scen_profit = (new_sales * scen_margin) - new_shipping_cost
            mode = 'rule_based'
            model_version = 'n/a'
            warnings.append("Using rule-based estimation as ML model is unavailable.")

        abs_delta = scen_profit - base_profit
        pct_delta = (abs_delta / abs(base_profit) * 100) if base_profit != 0 else 0

        risk_level = "Low"
        if scen_profit < 0:
            risk_level = "High"
        elif pct_delta < -10:
            risk_level = "Medium"

        if new_discount > 0.5:
            warnings.append("Discount exceeds 50%, high risk of negative margin.")

        return {
            "baseline_profit": float(base_profit),
            "scenario_profit": float(scen_profit),
            "absolute_delta": float(abs_delta),
            "pct_delta": float(pct_delta),
            "risk_level": risk_level,
            "assumptions": assumptions,
            "warnings": warnings,
            "model_version": model_version,
            "mode": mode
        }

scenario_service = ScenarioService()
