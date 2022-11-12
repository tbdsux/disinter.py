from typing import Any, Dict, Generic, List, TypeVar

from disinter.components import Components, Embed
from disinter.response import DiscordResponse, InteractionCallback, ResponseData
from disinter.types import (
    InteractionApplicationCommand,
    InteractionDataOption,
    InteractionMessageComponent,
    InteractionModalSubmit,
    Member,
    Message,
    User,
)

T = TypeVar(
    "T",
    InteractionApplicationCommand,
    InteractionMessageComponent,
    InteractionModalSubmit,
)


class InteractionContext(Generic[T]):
    def __init__(self, interaction: T) -> None:
        self.interaction: T = interaction

        self.guild_id = interaction.get("guild_id")
        self.channel_id = interaction.get("channel_id")
        self.application_id = interaction.get("application_id")

        self.member = interaction.get(
            "member"
        )  # the one who called the command, in a guild
        self.user = interaction.get("user")  # user who called the command, in a dm

    def reply(
        self,
        content: str = None,
        components: List[Components] | None = None,
        embeds: List[Embed] | None = None,
        allowed_mentions: Dict[str, Any] | None = None,
        ephemeral: bool | None = None,
        suppress_embeds: bool | None = None,
    ):
        """Send a reply to the interaction.

        Args:
            content (str, optional): Content of the response. Defaults to None.
            components (List[Components] | None, optional): Array of message components. Defaults to None.
            embeds (List[Embed] | None, optional): Array of message embeds. Supports up to 10 embeds. Defaults to None.
            allowed_mentions (Dict[str, Any] | None, optional): Allowed mentions object. Defaults to None.
            ephemeral (bool | None, optional): Set `EPHEMERAL` message flag. Cannot be set with `suppress_embeds`. Defaults to None.
            suppress_embeds (bool | None, optional):  Set `SUPPRESS_EMBEDS` message. Cannot be set with `ephemeral`. Defaults to None.

        Returns:
            DiscordResponse: Response wrapper class.
        """

        flags: int | None = None
        if ephemeral is True:
            flags = 1 << 6

        if suppress_embeds is True:
            if flags is not None:
                flags = 1 << 2

        return DiscordResponse(
            type=InteractionCallback.ChannelMessageWithSource,
            data=ResponseData(
                content=content,
                components=components,
                embeds=embeds,
                allowed_mentions=allowed_mentions,
                flags=flags,
            ),
        )


class SlashContext(InteractionContext):
    def __init__(
        self,
        interaction: InteractionApplicationCommand,
        options: List[InteractionDataOption] | None,
    ) -> None:
        super().__init__(interaction)

        self.data = interaction.get("data")

        self.options: Dict[str, InteractionDataOption] = {
            i["name"]: i for i in options or []
        }


class UserContext(InteractionContext):
    def __init__(self, interaction: InteractionApplicationCommand) -> None:
        super().__init__(interaction)

        self.data = interaction.get("data")

        # this is the target user
        self.user: User = interaction["data"]["resolved"]["users"][
            interaction["data"]["target_id"]
        ]
        # partial member
        self.member: Member = interaction["data"]["resolved"]["members"][
            interaction["data"]["target_id"]
        ]


class MessageContext(InteractionContext):
    def __init__(self, interaction: InteractionApplicationCommand) -> None:
        super().__init__(interaction)

        self.data = interaction.get("data")

        # this is the target message
        self.message: Message = interaction["data"]["resolved"]["messages"][
            interaction["data"]["target_id"]
        ]


class ComponentContext(InteractionContext):
    def __init__(self, interaction: InteractionMessageComponent) -> None:
        super().__init__(interaction)

        self.data = interaction.get("data")
