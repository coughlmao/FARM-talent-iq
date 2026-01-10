import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Server Port Number
    PORT = os.getenv("PORT")

    # Database Connection String
    MONGO_URI = os.getenv("MONGO_URI")

    # Clerk Authentication
    CLERK_FRONTEND_API = os.getenv("CLERK_FRONTEND_API")

    # Frontend Url
    CLIENT_URL = os.getenv("CLIENT_URL")


settings = Settings()
