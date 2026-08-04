import asyncio
import discord
import os
import config


async def update_bot_avatar():
    client = discord.Client(intents=discord.Intents.default())

    async with client:
        # Logs in using the token already loaded from your .env by config.py
        await client.login(config.DISCORD_TOKEN)

        # The exact PNG filename from your screenshot
        image_path = "assets/clanker_profile-1961x1024.png"

        if not os.path.exists(image_path):
            print(f"Error: Could not find '{image_path}'. Ensure it is in the same directory as this script.")
            return

        with open(image_path, "rb") as image_file:
            avatar_bytes = image_file.read()

        print("Uploading PNG avatar directly to Discord API...")
        await client.user.edit(avatar=avatar_bytes)
        print("Success! Avatar updated successfully. You can delete this script now.")


if __name__ == "__main__":
    asyncio.run(update_bot_avatar())