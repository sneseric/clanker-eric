import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-3.6-flash"
FALLBACK_MODEL_NAME = "gemini-3.5-flash-lite"

# Load payment links dynamically
BUY_ME_COFFEE_LINK = os.getenv("BUY_ME_COFFEE_LINK", "Link not configured")
AMAZON_WISHLIST_LINK = os.getenv("AMAZON_WISHLIST_LINK", "Link not configured")
AMAZON_REGISTRY_LINK = os.getenv("AMAZON_REGISTRY_LINK", "Link not configured")
GOFUNDME_LINK = os.getenv("GOFUNDME_LINK", "Link not configured")

if not DISCORD_TOKEN or not GEMINI_API_KEY:
    raise ValueError("Missing DISCORD_TOKEN or GEMINI_API_KEY in .env file.")