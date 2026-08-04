import discord
from discord.ext import commands
from discord import app_commands
import asyncio
from google import genai
from google.genai import types
import config
import memory_manager

client = genai.Client(api_key=config.GEMINI_API_KEY)


class MediaRequests(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="request", description="Request a movie or TV show to be added to the server.")
    @app_commands.describe(media="The name of the movie or TV show you want")
    async def request_media(self, interaction: discord.Interaction, media: str):

        # 1. Verify the command is used in the correct channel
        if interaction.channel.name != "media-server":
            await interaction.response.send_message(
                "This command can only be used in the #media-server channel.",
                ephemeral=True
            )
            return

        # 2. Dynamically grab the server owner
        owner = interaction.guild.owner
        if not owner:
            await interaction.response.send_message(
                "Error: Could not locate the server owner.",
                ephemeral=True
            )
            return

        # 3. Send the DM to the server owner first
        username = interaction.user.name
        dm_message = f"**🎬 New Media Request**\n**From:** {interaction.user.mention} ({username})\n**Requested:** `{media}`"

        try:
            await owner.send(dm_message)
        except discord.Forbidden:
            await interaction.response.send_message(
                "The server owner currently has Direct Messages disabled. Request failed.",
                ephemeral=True
            )
            return

        # 4. Generate Clanker Eric's sarcastic response using Gemini
        await interaction.response.defer()  # Defer while Gemini generates the roast

        system_prompt = memory_manager.brain_context + "\n\n"
        system_prompt += f"""
CRITICAL MEDIA REQUEST DIRECTIVE:
The user {username} just requested a movie or TV show named '{media}'.
You must stay entirely in your sarcastic, cynical Clanker Eric persona. 
Acknowledge their request mockingly, incorporating the media name directly into a sarcastic dismissal or backhanded comment (similar to: '{media}, really? I'll see what I can do.' or '{media} received. I'll get to it when my cooling fans stop melting').
Keep the response relatively short and punchy. Do not include any brackets or tags.
"""

        def _call_api():
            response = client.models.generate_content(
                model=config.MODEL_NAME,
                contents=f"User requested media: {media}",
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=0.9,
                )
            )
            return response.text

        try:
            reply = await asyncio.wait_for(asyncio.to_thread(_call_api), timeout=20.0)
            if not reply:
                reply = f"{media}, really? I'll see what I can do."
        except Exception:
            reply = f"{media}? Are your optical sensors malfunctioning, or do you genuinely expect me to source that trash?"

        # 5. Send the sarcastic reply into the channel
        await interaction.followup.send(reply.strip())


async def setup(bot):
    await bot.add_cog(MediaRequests(bot))