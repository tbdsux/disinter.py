from functools import wraps
from typing import Awaitable, Callable, Dict, List
import typing
from fastapi import FastAPI
from starlette.types import Scope, Receive, Send

from .command import ApplicationCommand, ApplicationCommandOption
from .utils import validate_name
from .context import InteractionContext
from .response import DiscordResponse


if typing.TYPE_CHECKING:
    CALLBACK_FUNCTION = (
        Callable[[InteractionContext], DiscordResponse]
        | Callable[[InteractionContext], Awaitable[DiscordResponse]]
    )


class SlashCommand:
    def __init__(
        self, command: ApplicationCommand, callback: CALLBACK_FUNCTION
    ) -> None:
        self.command = command
        self.callback = callback


class DisInter(FastAPI):
    def __init__(self, token: str, application_id: str, guilds: List[str]) -> None:
        self.token = token
        self.application_id = application_id
        self.slash_commands = Dict[str, SlashCommand]

    def command(
        self,
        func: CALLBACK_FUNCTION,
    ) -> Callable:
        @wraps(func)
        def _command(
            name: str,
            description: str,
            name_localizations: Dict[str, str] = None,
            description_localizations: Dict[str, str] = None,
            options: List[ApplicationCommandOption] = None,
            default_member_permissions: str = None,
            dm_permission: bool = None,
        ):
            # validate name
            validate_name(name)

            cmd = ApplicationCommand(
                name=name,
                description=description,
                name_localizations=name_localizations,
                description_localizations=description_localizations,
                options=options,
                default_member_permissions=default_member_permissions,
                dm_permission=dm_permission,
            )

            self.slash_commands[name] = SlashCommand(cmd, func)

        return _command

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        await super().__call__(scope, receive, send)
