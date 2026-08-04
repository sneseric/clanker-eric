# clanker-eric
AI-Powered Discord Bot

# Clanker Eric 🤖

Clanker Eric is a cynical, sarcastic, AI-powered Discord bot integrated with the Google Gemini API. He tracks user context, roasts newcomers, hounds the server for server-cost donations, and manages media requests.

[**Chat with Clanker Eric now**](https://discord.gg/T6n2us8)

---

## Features
* **Gemini-Powered Sarcasm:** Automatically responds when mentioned, replied to, or messaged in DMs.
* **Persistent User Context:** Maintains per-user context in local markdown files for personalized interactions.
* **Automated Chatter & Payment Reminders:** Periodically drops unprompted roasts and payment/donation requests and interactive payment UI buttons.
* **Media Requests:** Features a `/request` slash command restricted to the `#media-server` channel.
* **Dockerized Deployment:** Runs in a lightweight, containerized Python environment.

---

## Setup & Deployment Instructions

### Step 1: Clone the Repository

[**Download the source files**](https://github.com/sneseric/clanker-eric/archive/refs/heads/main.zip) or set up the project files manually using the project structure shown below.

To clone the repository directly, open a terminal in your IDE or the directory where you want to store the project and run:

```bash
git clone https://github.com/sneseric/clanker-eric.git
```

Then enter the project directory:

```bash
cd clanker-eric
```

### Step 2: Discord Developer Portal Configuration

1. Go to the Discord Developer Portal and click New Application. Name your bot.
2. Go to the Bot tab on the left menu:
   - Click Reset Token and copy your token for your `.env` file.
   - Under Privileged Gateway Intents, enable: Presence Intent, Server Members Intent, and Message Content Intent.
3. Go to the OAuth2 > URL Generator tab:
   - Under Scopes, select `bot` and `applications.commands`.
   - Under Bot Permissions, select Read Messages/View Channels, Send Messages, Embed Links, and Read Message History.
   - Copy the generated URL, paste it into your browser, and invite the bot to your server.

### Step 3: Environment Configuration

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

Create a `.env` file in your root project directory:

```env
DISCORD_TOKEN=your_token_here
GEMINI_API_KEY=your_gemini_key_here
BUY_ME_COFFEE_LINK=https://www.buymeacoffee.com/yourlink
AMAZON_WISHLIST_LINK=https://www.amazon.com/...
AMAZON_REGISTRY_LINK=https://www.amazon.com/...
GOFUNDME_LINK=https://www.gofundme.com/...
```

### Step 4: Run via Docker

Open a terminal in the project root directory and run:

```bash
docker compose up -d --build
```

---