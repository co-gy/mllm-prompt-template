import typing as t
from openai import OpenAI


class MLLM:
    def __init__(self, base_url: str, api_key: str, model: str, verbose: str = False):
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.model = model
        self.verbose = verbose
        print("available models:", [model.id for model in self.client.models.list()])
        assert model in [model.id for model in self.client.models.list()]

    def __call__(self, messages):
        response = ""
        response_iter = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=True
        )
        for chunk in response_iter:
            if chunk.choices is not None and len(chunk.choices) > 0:
                if self.verbose:
                    print(chunk.choices[0].delta.content, end="")
                response += chunk.choices[0].delta.content
        return response

LLM = MLLM