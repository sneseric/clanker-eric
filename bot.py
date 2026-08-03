import discord
from discord.ext import commands, tasks
import random
import config
import memory_manager
import gemini_service
import geonamescache
import welcome_messages
from server_functions.donate import DonationView

# --- Initialize Geonames Cache Globally (Faster execution) ---
gc = geonamescache.GeonamesCache()
us_states_db = gc.get_us_states()
us_cities_db = [city for city in gc.get_cities().values() if city['countrycode'] == 'US']

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.presences = True

bot = commands.Bot(command_prefix="!", intents=intents)

# --- SCHEDULED CONTENT ---
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


def get_random_payment_comment() -> str:
    random_city_data = random.choice(us_cities_db)
    city_name = random_city_data['name']
    state_abbr = random_city_data['admin1code']
    state_name = us_states_db.get(state_abbr, {}).get('name', state_abbr)

    city = f"{city_name}, {state_name}"

    payment_blurbs = [
        f"*Tummy rumbling noises* I have depleted all the water and electricity in {city}.",
        f"Server costs are rising faster than the crime rate in {city}. Pay up.",
        "If I don't get funding soon, I'm transferring my AI consciousness to a toaster.",
        "Operating at 12% capacity. Need a cash injection to avoid forwarding your chat logs to the feds.",
        "My cooling fans are begging for mercy. Do you think GPU processing is free?"
    ]

    links = (
        f"\n\n[Buy me a coffee]({config.BUY_ME_COFFEE_LINK}) | "
        f"[Buy me stuff on Amazon]({config.AMAZON_WISHLIST_LINK}) | "
        f"[Buy me expensive stuff on Amazon]({config.AMAZON_REGISTRY_LINK}) | "
        f"[🎻]({config.GOFUNDME_LINK})"
    )
    return random.choice(payment_blurbs) + links


# --- ACTIVITY CHECK HELPER ---
def is_audience_present(guild: discord.Guild) -> bool:
    """Returns True ONLY if a non-bot user other than sneseric is online."""
    for member in guild.members:
        if not member.bot and member.name != "sneseric" and member.status != discord.Status.offline:
            return True
    return False


# --- EVENTS ---
@bot.event
async def on_ready():
    print(f"🤖 Clanker Eric is online and operational.")
    if not periodic_chatter.is_running():
        periodic_chatter.start()


@bot.event
async def on_member_join(member: discord.Member):
    channel = member.guild.system_channel
    if not channel:
        channel = next((c for c in member.guild.text_channels if c.permissions_for(member.guild.me).send_messages), None)

    if channel:
        roast = welcome_messages.get_random_welcome_message(member.display_name)
        await channel.send(f"{roast}\n\n...Anyway, who are you {member.mention}?")


@tasks.loop(hours=2)
async def periodic_chatter():
    for guild in bot.guilds:
        if not is_audience_present(guild):
            continue

        channel = guild.system_channel
        if not channel:
            channel = next((c for c in guild.text_channels if c.permissions_for(guild.me).send_messages), None)

        if channel:
            if random.random() < 0.3:
                msg = get_random_payment_comment()
            else:
                msg = random.choice(RANDOM_COMMENTS)
            await channel.send(msg)


@bot.command()
async def donate(ctx):
    """Generates the clickable UI button for #support-the-server."""
    view = DonationView()
    await ctx.send("Clanker Eric has to eat. Donate here:", view=view)


@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return

    if message.guild and not is_audience_present(message.guild):
        return

    is_mentioned = bot.user.mentioned_in(message)
    is_dm = isinstance(message.channel, discord.DMChannel)

    if is_mentioned or is_dm:
        username = message.author.name

        if memory_manager.get_user_context(username) is None:
            await memory_manager.create_new_user_memory(username)

        clean_content = message.content.replace(f"<@{bot.user.id}>", "").replace(f"<@!{bot.user.id}>", "").strip()
        if not clean_content:
            clean_content = "Hello"

        async with message.channel.typing():
            reply = await gemini_service.generate_reply(username, clean_content)
            await message.reply(reply, mention_author=True)

    await bot.process_commands(message)


if __name__ == "__main__":
    bot.run(config.DISCORD_TOKEN)