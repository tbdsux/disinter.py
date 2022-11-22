# disinter.py

Discord bot to respond to interactions via webhook.

## Usage

(Still trying to update...)

- Required environment variables or presets

```python
import os

TOKEN = os.environ.get("TOKEN", "") # your bot token
APPLICATION_ID = os.environ.get("APPLICATION_ID", "") # application id of the bot app
GUILDS = os.environ.get("GUILD", "").split(",") # guilds you want the bot to register to,\
                                                # if None it will register as global command
PUBLIC_KEY = os.environ.get("PUBLIC_KEY", "") # the bot's public key
```

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

- Run the server. `disinter.py` wraps over `FastAPI` so you can run it asgi server like `uvicorn`

```sh
uvicorn main:app --reload
```

### Development

If you have your app running with `uvicorn`, you can use `ngrok` (install it first) to reverse proxy and use it to test your bot.

```sh
ngrok http 8000 # replace with the port your asgi server is running in
```

- Copy your forwarding url
  ![](./ngrok-proxy-url.png)

- Update your `Interactions Endpoint Url` in your discord app dashboard
  ![](./endpoint.png)

You can now enjoy developing your bot :tada: !

## Not implemented features

- File attachments
- Autocomplete
- ~~Modals~~
- Deferred response
- etc...

##

**&copy; 2022 | TheBoringDude**
