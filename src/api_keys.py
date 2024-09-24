import os
from dotenv import load_dotenv
from pathlib import Path

env_file = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_file)


class Neo4jDBConfig:
    NEO4J_URI = os.getenv("NEO4J_URI")
    NEO4J_USER = os.getenv("NEO4J_USER")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
    NEO4J_DATABASE = os.getenv("NEO4J_DATABASE")


class OpenAPIConfig:
    OPEN_API_KEY = os.getenv("OPEN_API_KEY")


class GeminiAPIConfig:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
