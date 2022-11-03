from typing import List

from disinter.interaction import Interaction, InteractionDataOption
from disinter.response import (
    DiscordResponse,
    InteractionCallbackTypeChannelMessageWithSource,
    ResponseData,
)


class InteractionContext:
    def __init__(
        self, interaction: Interaction, options: List[InteractionDataOption]
    ) -> None:
        self.interaction = interaction

        self.data = interaction.get("data")
        self.guild_id = interaction.get("guild_id")
        self.channel_id = interaction.get("channel_id")
        self.application_id = interaction.get("application_id")
        self.member = interaction.get("member")
        self.user = interaction.get("user")

        self.options = {i["name"]: i for i in options}

    def reply(self, content: str = None):
        return DiscordResponse(
            type=InteractionCallbackTypeChannelMessageWithSource,
            data=ResponseData(content=content),
        )
