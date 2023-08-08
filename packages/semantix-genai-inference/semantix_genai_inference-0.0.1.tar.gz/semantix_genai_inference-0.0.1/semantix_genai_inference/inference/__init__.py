from typing import Optional
from abc import ABC, abstractmethod

class SemantixGenClient(ABC):
    def __init__(self, inference_server_id: str, api_secret: str, 
                 version: Optional[str]="v0", server: Optional[str]="app.elemeno.ai"):
        self.inference_server_id = inference_server_id
        self.url = f"https://infserv-{inference_server_id}.{server}/{version}/inference"
        # set the Authorization header on aiohttp.ClientSession
        self.headers = {
            "Authorization": f"Bearer {api_secret}",
        }

    def add_header(self, key, value):
        self.headers[key] = value

    @abstractmethod
    def predict(self, **kwargs):
        pass

    
