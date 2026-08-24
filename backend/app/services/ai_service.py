from ollama import Client


class AIService:

    def __init__(self):
        self.client = Client(
            host="http://localhost:11434"
        )

        self.model = "qwen3:4b"

    def generate_response(
        self,
        prompt: str,
    ) -> str:

        response = self.client.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response["message"]["content"]