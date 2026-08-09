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
### Step 2: Install required packages:

```
pip install -r requirements.txt
```

### Step 3: Discord Developer Portal Configuration

1. Go to the Discord Developer Portal and click New Application. Name your bot.
2. Go to the Bot tab on the left menu:
   - Click Reset Token and copy your token for your `.env` file.
   - Under Privileged Gateway Intents, enable: Presence Intent, Server Members Intent, and Message Content Intent.
3. Go to the OAuth2 > URL Generator tab:
   - Under Scopes, select `bot` and `applications.commands`.
   - Under Bot Permissions, select Read Messages/View Channels, Send Messages, Embed Links, and Read Message History.
   - Copy the generated URL, paste it into your browser, and invite the bot to your server.

### Step 4: Environment Configuration


### Project Structure & Required Files

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
├── .gitignore                  # lists files Git should ignore
├── Dockerfile                  # Container build instructions
├── .dockerignore               # securely pass .env file to Docker container
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

### Protect Your `.env` File

Create a `.dockerignore` file in the root project directory. This prevents Docker from copying sensitive files such as `.env` into the Docker image when using `COPY . .`.<br> 
Othwerwise, your credential files could potentially be exposed on the http serer used for the health status check. 

Create the file:

    .dockerignore

Add the following:
```
    .env
    .env.*
    !.env.example

    .git
    .gitignore

    __pycache__
    *.pyc
    *.pyo
    *.pyd

    local_data
```

### Step 5: Run via Docker

Open a terminal in the project root directory and run:

```
docker compose up -d --build
```

---

## Reverse Proxy & http server setup

This setup routes external traffic through a Caddy reverse proxy over HTTPS (Port 443) using DuckDNS subdomains. Caddy automatically provisions SSL certificates via Let's Encrypt / ZeroSSL, while DuckDNS keeps our subdomains mapped to our home IP address.<br>
This allows you to embed an http server into your Docker container that can be used for uptime monitoring for your bot on servies such as betteruptime.com.

---

### 1. Prerequisites: DuckDNS & Caddy Installation

#### Step A: Set Up DuckDNS Subdomains
1. Go to https://www.duckdns.org and log in.
2. Under the subdomains section, create your subdomains (e.g., for Plex, Wizarr, and Status).
3. Note down your DuckDNS Token.

#### Step B: Install Caddy on Windows
1. Download the Windows binary from https://caddyserver.com/download.
2. Create a folder at C:\caddy on your host machine.
3. Move the downloaded executable into C:\caddy and rename it to caddy.exe.
4. Add C:\caddy to your Windows System PATH environment variables.
5. Create your configuration file named Caddyfile inside C:\caddy.

---

### 2. Port Forwarding
Forward standard web ports on your router to your host machine's local IP:
* TCP Port 80 (HTTP - SSL validation)
* TCP Port 443 (HTTPS - secure traffic)

---

### 3. Caddy Reverse Proxy Setup (Caddyfile)
Create or update C:\caddy\Caddyfile:

```
# Discord Bot
[INSERT_STATUS_SUBDOMAIN].duckdns.org {
    reverse_proxy 127.0.0.1:8080
}
```
Run caddy as a service (optional)
```
sc.exe create caddy start= auto binPath= "C:\caddy\caddy.exe run --config C:\caddy\Caddyfile"
```
```
sc.exe start caddy
```

Open PowerShell or Command Prompt and reload Caddy:
```
caddy reload --config C:\caddy\Caddyfile
```

---

### 4. Dynamic DNS Maintenance (DuckDNS PowerShell Script)
Create a PowerShell script named duckdns-update.ps1 to update DuckDNS when your IP changes:

```
$Token = "[INSERT_DUCKDNS_TOKEN]"
$URL = "https://www.duckdns.org/update?domains=[INSERT_SUBDOMAIN_1],[INSERT_SUBDOMAIN_2],[INSERT_SUBDOMAIN_3]&token=$Token"
Invoke-RestMethod -Uri $URL
```

### 5. Schedule DuckDNS update Script
   Schedule the DuckDNS Update Script using task scheduler (optional)

### 6. Ptotect your .env file
   Remember to use the docker-compose.yml file above that embeds the http server and also create the .dockerignore file to protect your .env credentials from being exposed on your web server. 

---
