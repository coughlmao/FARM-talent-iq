import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Server Configuration
    PORT = os.getenv("PORT")
    ENV_TYPE = os.getenv("ENV_TYPE")

    # Database Configuration
    MONGO_URI = os.getenv("MONGO_URI")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

    # Clerk Authentication
    CLERK_FRONTEND_API = os.getenv("CLERK_FRONTEND_API")

    # Frontend URL
    CLIENT_URL = os.getenv("CLIENT_URL")

    # Inngest Configuration
    INNGEST_SIGNING_KEY = os.getenv("INNGEST_SIGNING_KEY")
    INNGEST_EVENT_KEY = os.getenv("INNGEST_EVENT_KEY")

settings = Settings()