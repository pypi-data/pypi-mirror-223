import ast
import json
import logging
import os
import pathlib

import requests

logger = logging.getLogger(__name__)


class LLMFunction:
    openai_endpoint = "https://api.openai.com/v1/chat/completions"

    def __init__(
        self,
        model: str,
        temperature: float,
        function_name: str,
        description: str,
        properties: dict,
        template: str,
        openai_api_key: str = None,
    ):
        self.model = model
        self.temperature = temperature
        self.function_name = function_name
        self.description = description
        self.properties = properties
        self.template = template

        if openai_api_key:
            self.openai_api_key = openai_api_key
        else:
            self.openai_api_key = os.environ.get("OPENAI_API_KEY", None)

        if not self.openai_api_key:
            raise ValueError(
                "No OpenAI API key provided and none found in environment variables."
            )

    @classmethod
    def from_dir(cls, dir_path: str, openai_api_key: str = None):
        path = pathlib.Path(dir_path)
        template = open(path / "template.txt", "r").read()
        args = json.loads(open(path / "args.json", "r").read())
        args["template"] = template
        return cls(openai_api_key=openai_api_key, **args)

    def __call__(self, text: str):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.openai_api_key}",
        }
        payload = self._get_payload(text)
        response_json = self._fetch_openai_completion(payload=payload, headers=headers)
        prediction = self._parse_completion(response_json=response_json)
        return prediction

    def _get_payload(self, text: str) -> dict:
        function_schema = {
            "name": self.function_name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": self.properties,
                "required": list(self.properties.keys()),
            },
        }
        prompt = self.template.format(text=text)
        return {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "functions": [function_schema],
            "function_call": {
                "name": self.function_name,
            },
            "temperature": self.temperature,
        }

    def _fetch_openai_completion(self, payload: dict, headers: dict) -> dict:
        try:
            response = requests.post(
                self.openai_endpoint, headers=headers, json=payload
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error from OpenAI request: {e}")
            return {}

    def _parse_completion(self, response_json: dict) -> dict:
        choices = response_json.get("choices")
        if choices:
            values = choices[0]["message"]["function_call"].pop("arguments")

            try:
                prediction = ast.literal_eval(values)
            except:
                try:
                    prediction = json.loads(values)
                except Exception as e:
                    logger.error(f"Error evaluating OpenAI JSON output: {e}")
                    return None

        return prediction
