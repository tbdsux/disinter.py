from typing import Dict, List

from disinter.response import (
    DiscordResponse,
    InteractionCallbackTypeChannelMessageWithSource,
    ResponseData,
)
from disinter.types.interaction import Interaction, InteractionDataOption


class InteractionContext:
    def __init__(self, interaction: Interaction) -> None:
        self.interaction = interaction

        self.data = interaction.get("data")
        self.guild_id = interaction.get("guild_id")
        self.channel_id = interaction.get("channel_id")
        self.application_id = interaction.get("application_id")
        self.member = interaction.get("member")
        self.user = interaction.get("user")

    def reply(self, content: str = None):
        return DiscordResponse(
            type=InteractionCallbackTypeChannelMessageWithSource,
            data=ResponseData(content=content),
        )


class SlashContext(InteractionContext):
    def __init__(
        self, interaction: Interaction, options: List[InteractionDataOption] | None
    ) -> None:
        super().__init__(interaction)

        self.options: Dict[str, InteractionDataOption] = {
            i["name"]: i for i in options or []
        }


class UserContext(InteractionContext):
    def __init__(self, interaction: Interaction) -> None:
        super().__init__(interaction)

        self.user = interaction["data"]["resolved"]["users"][
            interaction["data"]["target_id"]
        ]
        self.member = interaction["data"]["resolved"]["members"][
            interaction["data"]["target_id"]
        ]


class MessageContext(InteractionContext):
    def __init__(self, interaction: Interaction) -> None:
        super().__init__(interaction)

        self.message = interaction["data"]["resolved"]["messages"][
            interaction["data"]["target_id"]
        ]
