import logging
from functools import lru_cache

from google import genai

from app.core.config import settings
from app.services.llm_provider import LLMProvider

logger = logging.getLogger(__name__)


class GeminiProvider(LLMProvider):
    def __init__(self, api_key: str | None = None, model: str = "gemini-2.5-flash") -> None:
        self.api_key = api_key or settings.gemini_api_key
        self.model = model
        self.client = get_gemini_client(self.api_key) if self.api_key else None

    def generate(self, prompt: str) -> str:
        if self.client is None:
            logger.warning("GEMINI_API_KEY is not configured; using deterministic local fallback.")
            return self._fallback_response(prompt)
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
            )
            return response.text or self._fallback_response(prompt)
        except Exception as exc:
            logger.warning("Gemini generation failed; using local fallback. Error: %s", exc)
            return self._fallback_response(prompt)

    def _fallback_response(self, prompt: str) -> str:
        return (
            "I understand the customer request. Based on the available policy context, "
            "acknowledge the concern, summarize the next step, and escalate if legal, "
            "compliance, refund, or SLA risk is present."
        )


@lru_cache(maxsize=4)
def get_gemini_client(api_key: str) -> genai.Client:
    return genai.Client(api_key=api_key)
