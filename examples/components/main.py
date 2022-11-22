import os

from disinter import DisInter
from disinter.components import ButtonStyles, ComponentActionRows, ComponentButton
from disinter.context import ComponentContext, SlashContext

TOKEN = os.environ.get("TOKEN", "")
APPLICATION_ID = os.environ.get("APPLICATION_ID", "")
GUILDS = os.environ.get("GUILD", "").split(",")
PUBLIC_KEY = os.environ.get("PUBLIC_KEY", "")

bot = DisInter(
    token=TOKEN, application_id=APPLICATION_ID, public_key=PUBLIC_KEY, guilds=GUILDS
)


@bot.on_event("startup")
def start():
    try:
        # register the commands
        bot.sync_commands()
    except Exception as e:
        print(e)


@bot.button_component("sample-click")
def click_me(ctx: ComponentContext):
    return ctx.reply("You have clicked the **`Click Me`** button")


@bot.slash_command(name="button", description="Show a button component")
async def button(ctx: SlashContext):
    cp = ComponentActionRows(
        components=[
            ComponentButton(
                style=ButtonStyles.Primary, label="Click Me", custom_id="sample-click"
            )
        ]
    )

    return ctx.reply(
        content="This is a sample response with components", components=[cp]
    )
