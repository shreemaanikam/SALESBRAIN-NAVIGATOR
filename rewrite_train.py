import re

with open("backend/app/ml/train.py", "r") as f:
    code = f.read()

# Replace get_model_candidates
code = re.sub(
    r'def get_model_candidates\(\) -> Dict\[str, Any\]:.*?(?=def train_and_evaluate_all)',
    '''def get_model_candidates() -> Dict[str, Any]:
    from sklearn.linear_model import Ridge
    return {
        "Ridge Regression (Lightweight)": Ridge(alpha=1.0)
    }

''',
    code,
    flags=re.DOTALL
)

# Replace select_best_model
code = re.sub(
    r'def select_best_model\(results: Dict\[str, Dict\]\) -> Tuple\[str, Dict\]:.*?(?=def save_artifacts)',
    '''def select_best_model(results: Dict[str, Dict]) -> Tuple[str, Dict]:
    best_name = list(results.keys())[0]
    return best_name, results[best_name]

''',
    code,
    flags=re.DOTALL
)

# Remove the VotingRegressor import block if it exists
with open("backend/app/ml/train.py", "w") as f:
    f.write(code)

