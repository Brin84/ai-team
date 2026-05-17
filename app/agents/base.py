from openai import OpenAI
from openai.types.chat import (
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam
)

from app.config import settings


class BaseAgent:

    def __init__(
        self,
        role: str
    ):

        self.role = role

        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY,
            base_url=settings.BASE_URL
        )


    def run(
        self,
        task: str
    ) -> str:

        messages = [
            ChatCompletionSystemMessageParam(
                role="system",
                content=str(self.role)
            ),
            ChatCompletionUserMessageParam(
                role="user",
                content=str(task)
            )
        ]

        response = self.client.chat.completions.create(
            model=settings.MODEL_NAME,
            messages=messages,
            max_tokens=2500,
            temperature=0.1,
            extra_body={
                "think": False,
                "num_predict": 2500
            }
        )

        message = response.choices[0].message

        content = message.content or ""

        # если модель вернула пустой content —
        # берём reasoning как запасной вариант
        if not content:

            reasoning = getattr(
                message,
                "reasoning",
                ""
            )

            if reasoning:
                content = reasoning

        return str(content)