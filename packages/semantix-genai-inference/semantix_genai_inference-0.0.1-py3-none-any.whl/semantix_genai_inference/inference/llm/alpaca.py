from typing import Optional
import aiohttp
from .. import SemantixGenClient


class AlpacaInferenceClient(SemantixGenClient):
    def __init__(self, inference_server_id: str, api_secret: str, version: Optional[str] = None):
        super().__init__(inference_server_id, api_secret, version=version)
        self._type = "alpaca"

    async def predict(self, prompt, max_tokens, top_p):
        body = {
            "prompt": [prompt],
            "max_tokens": [max_tokens],
            "top_p": [top_p]
        }
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.post(self.url, json=body) as response:
                return await response.json()