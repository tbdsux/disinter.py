# disinter.py

Discord bot to respond to interactions via webhook.

## Usage

- Create and manage the bot in a `main.py` or so...

```python
# main.py

import datetime
import os

from disinter import (
    ApplicationCommandOption,
    ApplicationCommandOptionTypeUser,
    ButtonStyles,
    ComponentActionRows,
    ComponentButton,
    ComponentContext,
    DisInter,
    Embed,
    EmbedField,
    MessageContext,
    SlashContext,
    UserContext,
)

TOKEN = os.environ.get("TOKEN", "")
APPLICATION_ID = os.environ.get("APPLICATION_ID", "")
GUILDS = os.environ.get("GUILD", "").split(",")
PUBLIC_KEY = os.environ.get("PUBLIC_KEY", "")

app = DisInter(
    token=TOKEN, application_id=APPLICATION_ID, public_key=PUBLIC_KEY, guilds=GUILDS
)


@app.user_command(name="List")
async def list(ctx: UserContext):
    return ctx.reply(content=f"This is a user command.. Hello <@{ctx.user['id']}>")


@app.message_command(name="Bookmark")
async def bookmark(ctx: MessageContext):
    return ctx.reply(
        content=f"This is a message command\n Content of the message: `{ctx.message['content']}`"
    )


@app.slash_command(name="ping", description="Ping command")
async def ping(ctx: SlashContext):
    return ctx.reply("pong")


@app.slash_command(name="embed", description="Sample with embed")
async def embed(ctx: SlashContext):
    em = Embed(
        title="Embed",
        description="This is a sample embed",
        fields=[EmbedField(name="field", value="value")],
        timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    )

    return ctx.reply(embeds=[em])


@app.slash_command(name="components", description="Sample with components")
def components(ctx: SlashContext):
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


@app.button_component("sample-click")
def sampleclick(ctx: ComponentContext):
    return ctx.reply("This is a response to the `Click Me` button.")


@app.slash_command(
    name="mention",
    description="Mention user",
    options=[
        ApplicationCommandOption(
            type=ApplicationCommandOptionTypeUser,
            name="user",
            description="User to mention",
            required=True,
        )
    ],
)
async def mention(ctx: SlashContext):
    return ctx.reply("hello there!")

```

- Create a separate `register.py` and call it whenever you have changes in your app commands.

```python
# register.py

from main import app

app._sync_commands()
```

## Not Implemented

- File attachments
- Autocomplete
- Modals

##

**&copy; 2022 | TheBoringDude**
