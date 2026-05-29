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
        print("\n=== TASK TO MODEL ===\n")
        print(task[:3000])
        messages = [

            ChatCompletionSystemMessageParam(
                role="system",
                content=f"""
{self.role}

Критически важно:

- не показывай reasoning
- не объясняй ход мыслей
- не начинай с "Okay"
- не начинай с "Let's"
- не начинай с "First"
- не пиши анализ
- верни только результат
"""
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
            temperature=0.05,
            extra_body={
                "think": False,
                "options": {
                    "num_predict": 2500,
                    "temperature": 0.05
                }
            }
        )


        message = (
            response
            .choices[0]
            .message
        )


        content = (
            message.content
            or
            ""
        )
        print("\n=== MODEL RESPONSE ===\n")
        print(content[:5000])

        bad_prefixes = [

            "Okay",
            "Let's",
            "Let me",
            "First",
            "I need",
            "I'll"
        ]


        cleaned = []


        for line in content.split(
            "\n"
        ):

            if any(

                line.strip().startswith(
                    prefix
                )

                for prefix
                in bad_prefixes
            ):

                continue


            cleaned.append(
                line
            )


        return "\n".join(
            cleaned
        ).strip()