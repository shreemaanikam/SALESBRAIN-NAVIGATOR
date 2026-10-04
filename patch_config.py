import re
import os

file_path = "backend/app/core/config.py"
with open(file_path, "r") as f:
    content = f.read()

replacement = """
    @property
    def DATASET_PATH(self) -> str:
        path = os.getenv('DATASET_PATH', 'dataset/Cleaned_SuperStore.csv')
        if not os.path.isabs(path):
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            return os.path.join(base_dir, path)
        return path
"""

# Let's just do a simpler replacement
# Replace DATASET_PATH: str = os.getenv...
replacement_simple = """    _DATASET_PATH_RAW: str = os.getenv('DATASET_PATH', 'dataset/Cleaned_SuperStore.csv')

    @property
    def DATASET_PATH(self) -> str:
        if os.path.isabs(self._DATASET_PATH_RAW): return self._DATASET_PATH_RAW
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        return os.path.join(base_dir, self._DATASET_PATH_RAW)
"""

content = re.sub(r'    DATASET_PATH: str = os\.getenv\(\'DATASET_PATH\', \'dataset/Cleaned_SuperStore\.csv\'\)', replacement_simple, content)

with open(file_path, "w") as f:
    f.write(content)
