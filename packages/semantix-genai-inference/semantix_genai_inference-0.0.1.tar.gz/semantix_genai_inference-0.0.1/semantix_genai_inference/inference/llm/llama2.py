from typing import Optional
import aiohttp
from .. import SemantixGenClient


class Llama2InferenceClient(SemantixGenClient):
    def __init__(self, inference_server_id: str, api_secret: str, version: Optional[str] = None):
        super().__init__(inference_server_id, api_secret, version=version)
        self._type = "llama2"

    async def predict(self, prompt, temperature, top_p):
        body = {
            "prompt": [prompt],
            "temperature": [temperature],
            "top_p": [top_p]
        }
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.post(self.url, json=body) as response:
                return await response.json()