import json
import yaml
from pathlib import Path

BASE_DIR = Path(__file__).parent

with open(BASE_DIR / "openapi.json", "r", encoding="utf-8") as f:
    spec = json.load(f)

with open(BASE_DIR / "swagger.yaml", "w", encoding="utf-8") as f:
    yaml.dump(spec, f, sort_keys=False, allow_unicode=True)

print("✅ swagger.yaml generated successfully.")