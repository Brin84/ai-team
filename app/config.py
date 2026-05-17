from dotenv import load_dotenv
import os


load_dotenv()


class Settings:

    OPENAI_API_KEY = os.getenv(
        "OPENAI_API_KEY"
    )

    BASE_URL = os.getenv(
        "BASE_URL"
    )

    MODEL_NAME = os.getenv(
        "MODEL_NAME"
    )


settings = Settings()