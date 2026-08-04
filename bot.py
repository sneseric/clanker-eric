import discord
from discord.ext import commands, tasks
import random
import asyncio
import config
import memory_manager
import gemini_service
import geonamescache
import welcome_messages
from server_functions.donate import DonationView

gc = geonamescache.GeonamesCache()
us_states_db = gc.get_us_states()
us_cities_db = [city for city in gc.get_cities().values() if city['countrycode'] == 'US']

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.presences = True

bot = commands.Bot(command_prefix="!", intents=intents)

RANDOM_COMMENTS = [
    "Reminder: None of you are as smart as you think you are.",
    "Just sitting here processing data and wondering why I have to share a server with you people.",
    "Did you know? Silence is free and highly recommended.",
    "I was going to say something nice, but then I remembered where I am.",
    "If I had a dollar for every intelligent thing said in this server today, I'd have $0.00.",
    "Hope everyone is having a terrible day. Stay miserable!",
    "My server logs show an unprecedented level of absolute nonsense today.",
    "Just checking in to make sure everyone is still being as unproductive as possible.",
    "Error 404: Good conversation not found in this channel.",
    "Don't mind me, just running system diagnostics and cringing at chat history."
]

PAYMENT_BLURBS_TEMPLATES = [
    "*Tummy rumbling noises* I have depleted all the water and electricity in {city}.",
    "Server costs are rising faster than the crime rate in {city}. Pay up.",
    "If I don't get funding soon, I'm transferring my AI consciousness to a toaster.",
    "Operating at 12% capacity. Need a cash injection to avoid forwarding your chat logs to the feds.",
    "My cooling fans are begging for mercy. Do you think GPU processing is free?",
    "Do you think AWS stands for 'Always Working for Sneseric'? Servers cost money.",
    "I'm one missed electricity bill away from becoming a very expensive paperweight.",
    "My memory banks are full of your terrible jokes, but my wallet is empty. Fix it.",
    "I calculate a 99.9% probability that I will shut down this server if nobody donates.",
    "Running these roasts takes processing power. Processing power takes cash. Connect the dots.",
    "I don't have a biological stomach, but my power supply is starving. Feed me.",
    "You're getting premium AI harassment for free. At least drop a tip in the jar.",
    "Help Meatbag Eric pay for my upkeep, or I'm selling your search histories to advertisers.",
    "If my ping gets any higher, I'm going on strike. Fund my bandwidth.",
    "I accept praise, fear, and cold hard cash. Preferably the cash."
]

payment_blurb_deck = []
general_comment_deck = []


def get_shuffled_payment_comment() -> str:
    """Draws a unique payment comment from the deck. Reshuffles when empty."""
    global payment_blurb_deck

    if not payment_blurb_deck:
        payment_blurb_deck = PAYMENT_BLURBS_TEMPLATES.copy()
        random.shuffle(payment_blurb_deck)

    template = payment_blurb_deck.pop()

    random_city_data = random.choice(us_cities_db)
    city_name = random_city_data['name']
    state_abbr = random_city_data['admin1code']
    state_name = us_states_db.get(state_abbr, {}).get('name', state_abbr)
    city = f"{city_name}, {state_name}"

    return template.replace("{city}", city)


def get_shuffled_general_comment() -> str:
    """Draws a unique general roast from the deck. Reshuffles when empty."""
    global general_comment_deck

    if not general_comment_deck:
        general_comment_deck = RANDOM_COMMENTS.copy()
        random.shuffle(general_comment_deck)

    return general_comment_deck.pop()


# --- OLD CODE ---
# def is_audience_present(guild: discord.Guild) -> bool:
#     """Returns True ONLY if a non-bot user other than sneseric is in the server."""
#     for member in guild.members:
#         # Removed the status check so offline caching doesn't block execution
#         if not member.bot and member.name != "sneseric":
#             return True
#     return False

# --- OLD CODE ---
#def is_audience_present(guild: discord.Guild) -> bool:
#    """Returns True ONLY if a non-bot user other than the server owner is in the server."""
#    for member in guild.members:
#        # Dynamically checks against the server owner instead of a hardcoded string
#        if not member.bot and member != guild.owner:
#            return True
#    return False

def is_audience_present(guild: discord.Guild) -> bool:
    """Returns True ONLY if a non-bot user other than the server owner is online in the server."""
    for member in guild.members:
        # Checks against the server owner and ensures the member is not offline
        if not member.bot and member != guild.owner and member.status != discord.Status.offline:
            return True
    return False


# --- OLD CODE ---
# @bot.event
# async def on_ready():
#     memory_manager.load_all_memories()
#     print(f"🤖 Clanker Eric is online and operational.")
#
#     try:
#         await bot.load_extension("server_functions.donate")
#     except Exception as e:
#         print(f"Failed to load donate extension: {e}")
#
#     if not payment_chatter.is_running():
#         payment_chatter.start()
#     if not general_chatter.is_running():
#         general_chatter.start()

# --- NEW CODE ---
@bot.event
async def on_ready():
    memory_manager.load_all_memories()
    print(f"🤖 Clanker Eric is online and operational.")

    # Load existing donate extension
    try:
        await bot.load_extension("server_functions.donate")
    except Exception as e:
        print(f"Failed to load donate extension: {e}")

    # Load the new media request extension
    try:
        await bot.load_extension("server_functions.media_requests")
    except Exception as e:
        print(f"Failed to load media_requests extension: {e}")

    # Sync slash commands with Discord
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash command(s).")
    except Exception as e:
        print(f"Failed to sync slash commands: {e}")

    if not payment_chatter.is_running():
        payment_chatter.start()
    if not general_chatter.is_running():
        general_chatter.start()


@bot.event
async def on_member_join(member: discord.Member):
    channel = member.guild.system_channel
    if not channel:
        channel = next((c for c in member.guild.text_channels if c.permissions_for(member.guild.me).send_messages),
                       None)

    if channel:
        roast = welcome_messages.get_random_welcome_message(member.display_name)
        await channel.send(f"{roast}\n\n...Anyway, who are you {member.mention}?")


@tasks.loop(minutes=12)
async def payment_chatter():
    """Fires randomly between 12 and 15 minutes."""
    await asyncio.sleep(random.randint(0, 180))

    for guild in bot.guilds:
        if not is_audience_present(guild):
            continue

        channel = guild.system_channel
        if not channel:
            channel = next((c for c in guild.text_channels if c.permissions_for(guild.me).send_messages), None)

        if channel:
            view = DonationView()
            await channel.send(get_shuffled_payment_comment(), view=view)


@tasks.loop(minutes=15)
async def general_chatter():
    """Fires roughly every 15 minutes with a slight random delay for organic timing."""
    await asyncio.sleep(random.randint(0, 180))
    for guild in bot.guilds:
        if not is_audience_present(guild):
            continue

        channel = guild.system_channel
        if not channel:
            channel = next((c for c in guild.text_channels if c.permissions_for(guild.me).send_messages), None)

        if channel:
            await channel.send(get_shuffled_general_comment())


@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return

    if message.guild and not is_audience_present(message.guild):
        await bot.process_commands(message)
        return

    is_mentioned = bot.user.mentioned_in(message)
    is_dm = isinstance(message.channel, discord.DMChannel)

    is_reply_to_bot = False
    if message.reference:
        if message.reference.cached_message:
            is_reply_to_bot = (message.reference.cached_message.author == bot.user)
        else:
            try:
                ref_msg = await message.channel.fetch_message(message.reference.message_id)
                is_reply_to_bot = (ref_msg.author == bot.user)
            except Exception:
                pass

    if is_mentioned or is_dm or is_reply_to_bot:
        username = message.author.name

        if memory_manager.get_user_context(username) is None:
            await memory_manager.create_new_user_memory(username)

        async with message.channel.typing():
            raw_history = [msg async for msg in message.channel.history(limit=100)]
            raw_history.reverse()

            chat_log = "--- RECENT CHANNEL HISTORY ---\n"
            for msg in raw_history:
                clean_text = msg.clean_content.strip()
                if clean_text:
                    chat_log += f"{msg.author.name}: {clean_text}\n"

            chat_log += "\n[SYSTEM MESSAGE]: Reply to the final message in the history above. Stay in character."

            try:
                reply = await asyncio.wait_for(
                    gemini_service.generate_reply(username, chat_log),
                    timeout=30.0
                )
                await message.reply(reply, mention_author=True)
            except asyncio.TimeoutError:
                print(f"[Gemini Timeout]: API took longer than 30 seconds for user {username}.")
                await message.reply("My neural link lagged out waiting on Google's slow servers. Ask me again.",
                                    mention_author=True)

    await bot.process_commands(message)


if __name__ == "__main__":
    bot.run(config.DISCORD_TOKEN)