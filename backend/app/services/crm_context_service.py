import json
from functools import lru_cache
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[3]
CRM_DATA_PATH = PROJECT_ROOT / "data" / "supporting_crm_data.json"


class CRMContextService:
    def __init__(self, data_path: Path = CRM_DATA_PATH) -> None:
        self.data_path = data_path
        self.data = _load_supporting_data(str(data_path))

    def get_contact_profile(self, email: str) -> dict[str, Any]:
        normalized = email.lower()
        profiles = self.data.get("contact_profiles", {})
        domain = normalized.split("@")[-1] if "@" in normalized else normalized
        return profiles.get(normalized) or profiles.get(domain) or profiles.get("default", {})

    def check_account_status(self, email: str) -> dict[str, Any]:
        normalized = email.lower()
        accounts = self.data.get("account_status", {})
        domain = normalized.split("@")[-1] if "@" in normalized else normalized
        return accounts.get(normalized) or accounts.get(domain) or accounts.get("default", {})


@lru_cache(maxsize=1)
def _load_supporting_data(path: str) -> dict[str, Any]:
    data_path = Path(path)
    if not data_path.exists():
        return {"contact_profiles": {"default": {}}, "account_status": {"default": {}}}
    return json.loads(data_path.read_text(encoding="utf-8"))
