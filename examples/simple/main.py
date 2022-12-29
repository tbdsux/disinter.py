import datetime
import os

from disinter import DisInter
from disinter.components import Embed, EmbedField
from disinter.context import SlashContext

GUILDS = os.environ.get("GUILD", "").split(",")

bot = DisInter(guilds=GUILDS)


@bot.on_event("startup")
def start():
    try:
        # register the commands
        bot.sync_commands()
    except Exception as e:
        print(e)


@bot.slash_command(name="ping", description="Ping command")
async def ping(ctx: SlashContext):
    return ctx.reply("pong")


@bot.slash_command(name="embeds", description="Example with an embed response")
def embeds(ctx: SlashContext):
    em = Embed(
        title="Embed",
        description="This is a sample embed",
        fields=[EmbedField(name="field", value="value")],
        timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    )

    return ctx.reply(embeds=[em])
