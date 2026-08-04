# clanker-eric
AI-Powered Discord Bot

# Clanker Eric 🤖

Clanker Eric is a cynical, sarcastic, AI-powered Discord bot integrated with the Google Gemini API. He tracks user context, roasts newcomers, hounds the server for server-cost donations, and manages media requests.

---

## Features
* **Gemini-Powered Sarcasm:** Automatically responds when mentioned, replied to, or messaged in DMs.
* **Persistent User Context:** Maintains per-user context in local markdown files for personalized interactions.
* **Automated Chatter & Payment Reminders:** Periodically drops unprompted roasts and payment/donation requests and interactive payment UI buttons.
* **Media Requests:** Features a `/request` slash command restricted to the `#media-server` channel 
* **Dockerized Deployment:** Runs in a lightweight, containerized Python environment.

---

## Setup & Deployment Instructions

### Step 1: Discord Developer Portal Configuration
1. Go to the Discord Developer Portal and click New Application. Name your bot.
2. Go to the Bot tab on the left menu:
   - Click Reset Token and copy your token for your .env file.
   - Under Privileged Gateway Intents, enable: Presence Intent, Server Members Intent, and Message Content Intent.
3. Go to the OAuth2 > URL Generator tab:
   - Under Scopes, select bot and applications.commands.
   - Under Bot Permissions, select Read Messages/View Channels, Send Messages, Embed Links, and Read Message History.
   - Copy the generated URL, paste it into your browser, and invite the bot to your server.

### Step 2: Environment Configuration

## Project Structure & Required Files

```
clanker-eric/
│
├── local_data/
│   ├── brain.md                # Core personality and system instructions
│   └── memories/               # Per-user markdown context files
│
├── server_functions/
│   ├── __init__.py
│   ├── donate.py               # Interactive donation UI buttons and command
│   └── media_requests.py       # /request slash command handler
│
├── bot.py                      # Main Discord bot loop and event handlers
├── config.py                   # Environment variable loader
├── gemini_service.py           # Google GenAI API integration and model fallback logic
├── memory_manager.py           # Local file-based memory caching and linking handler
├── welcome_messages.py         # Dynamic welcome roasts generator
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Container build instructions
└── docker-compose.yml          # Container orchestration file
```

Create a .env file in your root project directory:

```
DISCORD_TOKEN=your_token_here
GEMINI_API_KEY=your_gemini_key_here
BUY_ME_COFFEE_LINK=https://www.buymeacoffee.com/yourlink
AMAZON_WISHLIST_LINK=https://www.amazon.com/...
AMAZON_REGISTRY_LINK=https://www.amazon.com/...
GOFUNDME_LINK=https://www.gofundme.com/...
```

### Step 3: Run via Docker
Open your terminal in the project root directory and run:
```
docker compose up -d --build
```

---



