import base64
from requests import Session
from openapi.constants import *


class Client:
    """
    OpenApi Package for interacting with OpenAPI `api.qewertyy.me`
    """

    def __init__(
        self
    ):
        """
        Initialize the class
        """
        self.url = BASE_URL
        self.session = Session()
        self.models = self.getModels()
    
    def getModels(self) -> dict:
        resp = self.session.get(f'{self.url}/models')
        return resp.json()
    
    def palm(self, prompt: str) -> dict:
        """ 
        Get an answer from PaLM 2 for the given prompt
        Example:
        >>> client = Client()
        >>> response = client.palm("Hello, Who are you?")
        >>> print(response)

        Args:
            prompt (str): Input text for the query.

        Returns:
            dict: Answer from the Open API in the following format:
                {
                    "status": str,
                    "content": str
                }
        """
        params = {
            "model_id": 0,
            "prompt": prompt
        }
        try:
            self.session.headers.update({"content-type": "application/json"})
            resp = self.session.post(
                f'{self.url}/models',
                params=params,
            )
            return resp.json()
        except Exception as e:
            print(f"Request failed: {e}")

    def upscale(self, image: bytes) -> bytes:
        """ 
        Upscale an image
        Example:
        >>> client = Client()
        >>> response = client.upscale(image)
        >>> with open('upscaled.png', 'wb') as f:
                f.write(response)

        Args:
            image (bytes): Image in bytes.
        Returns:
            bytes: Upscaled image in bytes.
        """
        try:
            b = base64.b64encode(image).decode('utf-8')
            response = self.session.post(
                f'{self.url}/upscale',
                data={'image_data': b}
            )
            return response.content
        except Exception as e:
            print(f"Failed to upscale the image: {e}")
