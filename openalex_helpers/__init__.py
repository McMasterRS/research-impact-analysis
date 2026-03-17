import os

import pyalex
from dotenv import load_dotenv


load_dotenv()

OPENALEX_API_KEY = os.getenv("OPENALEX_API_KEY")
pyalex.config.api_key = OPENALEX_API_KEY
