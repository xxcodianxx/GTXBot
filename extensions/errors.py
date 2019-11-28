import discord
from discord.ext import commands
import asyncio
import traceback

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, e):
        if hasattr(ctx.command, "on_error"):
            return

        elif isinstance(e, commands.MissingRequiredArgument):
            await ctx.send(f':x: **``{ctx.command.name}`` requires the ``{e.param}`` argument!**')

        elif isinstance(e, commands.MissingPermissions):
            await ctx.send(f':closed_lock_with_key: **You need ``{e.args}`` to be able to execute ``{ctx.command.name}``**')

        elif isinstance(e, commands.BotMissingPermissions):
            perm_name = e.args[0].replace('Bot requires ', '').replace(' permission(s) to run this command.', '').strip()
            await ctx.send(f":closed_lock_with_key: **I need ``{perm_name}`` to be able to execute ``{ctx.command.name}``**")

        elif isinstance(e, commands.NotOwner):
            await ctx.send(f':closed_lock_with_key: **``{ctx.command.name}`` can be executed only by bot developers.**')

        elif isinstance(e, commands.BadArgument):
            await ctx.send(f':x: **Argument {e.args[0]} is invalid.**')

        elif isinstance(e, commands.CheckFailure):
            await ctx.send(f':x: **You do not meet the execution requirements for ``{ctx.command.name}``**')

        elif isinstance(e, commands.CommandNotFound):
            await ctx.message.add_reaction("🤔")
            await asyncio.sleep(2)
            await ctx.message.remove_reaction("🤔", self.bot.user)

        else:
            await ctx.send(f':x: **An internal error has occurred.** ```py\n{e}```')
            traceback.print_exception(type(e), e, e.__traceback__)

def setup(bot):
    bot.add_cog(
        ErrorHandler(bot)
    )