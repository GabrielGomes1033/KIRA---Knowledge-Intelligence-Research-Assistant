import os
from dotenv import load_dotenv

load_dotenv()

LANGUAGE = os.getenv("KIRA_LANGUAGE", "pt")
RESULTS_LIMIT = int(os.getenv("KIRA_RESULTS_LIMIT", "6"))
TIMEOUT = int(os.getenv("KIRA_TIMEOUT", "12"))
