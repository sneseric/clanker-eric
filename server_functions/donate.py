import discord
from discord.ext import commands
import config


class DonationView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        if config.GOFUNDME_LINK and config.GOFUNDME_LINK != "Link not configured":
            self.add_item(discord.ui.Button(
                label="Donate",
                style=discord.ButtonStyle.link,
                url=config.GOFUNDME_LINK,
                emoji="🎻"
            ))

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