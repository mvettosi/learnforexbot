from discord.ext import commands
import re


def setup(bot):
    bot.add_cog(IdeasCog(bot))


class IdeasCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ideas_channel = self.bot.get_channel(self.bot.config['ideas_channel'])
        self.pro_role = self.ideas_channel.guild.get_role(bot.config['pro_role'])

    @commands.command()
    async def newtrade(self, context, url=None, *, args=''):
        if url is None:
            await context.send(f'Looks like you forgot the idea link after the command!')
        elif not re.match(r"https://www\.tradingview\.com/x/.*", url):
            await context.send(f'Sorry, that does not look like a tradingview screenshot link! Only those are '
                               f'supported at the moment')
        else:
            await context.message.delete()
            new_message = await self.ideas_channel.send(f'New trade idea from {context.message.author.mention}\n{args}\n{url}')
            await new_message.add_reaction('\N{THUMBS UP SIGN}')
            await new_message.add_reaction('\N{THUMBS DOWN SIGN}')

    # @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.message.channel == self.ideas_channel and self.pro_role not in user.roles and self.bot.user != user:
            print(f'Removing reaction received from {user}')
            await reaction.remove(user)
            await user.send('Sorry pal, only Experienced Traders can vote on members ideas!')

