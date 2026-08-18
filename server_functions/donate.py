import discord
from discord.ext import commands
import config


class DonationView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        # 1. Buy Me a Coffee
        if config.BUY_ME_COFFEE_LINK and config.BUY_ME_COFFEE_LINK != "Link not configured":
            self.add_item(discord.ui.Button(label="Buy me a coffee", style=discord.ButtonStyle.link,
                                            url=config.BUY_ME_COFFEE_LINK))
        # 2. Kofi
        if config.KOFI_LINK:
            self.add_item(discord.ui.Button(label="Buy me a coffee from some other place", style=discord.ButtonStyle.link,
                                            url=config.KOFI_LINK))
        # 3. Patreon
        if config.PATREON_LINK:
            self.add_item(discord.ui.Button(label="Buy me a coffee every month", style=discord.ButtonStyle.link,
                                            url=config.PATREON_LINK))

        # 4. Amazon Wishlist
        if config.AMAZON_WISHLIST_LINK and config.AMAZON_WISHLIST_LINK != "Link not configured":
            self.add_item(discord.ui.Button(label="Buy me something on Amazon", style=discord.ButtonStyle.link,
                                            url=config.AMAZON_WISHLIST_LINK))

        # 5. Amazon Registry
        if config.AMAZON_REGISTRY_LINK and config.AMAZON_REGISTRY_LINK != "Link not configured":
            self.add_item(discord.ui.Button(label="Buy me something expensive on Amazon", style=discord.ButtonStyle.link,
                                            url=config.AMAZON_REGISTRY_LINK))

        # 6. GoFundMe (Last)
        if config.GOFUNDME_LINK and config.GOFUNDME_LINK != "Link not configured":
            self.add_item(
                discord.ui.Button(label="Donate", style=discord.ButtonStyle.link, url=config.GOFUNDME_LINK, emoji="🎻"))


class Donate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="donate")
    async def donate(self, ctx):
        """Generates the clickable UI button for #support-the-server."""
        view = DonationView()
        await ctx.send("Clanker Eric has to eat. Donate here:", view=view)


async def setup(bot):
    await bot.add_cog(Donate(bot))