from app.core.config import settings
from app.services.gemini_provider import GeminiProvider
from app.services.llm_provider import LLMProvider


def get_llm_provider() -> LLMProvider:
    provider = settings.llm_provider.lower().strip()
    if provider == "gemini":
        return GeminiProvider()
    raise ValueError(f"Unsupported LLM provider: {settings.llm_provider}")
