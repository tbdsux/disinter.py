import asyncio
from typing import Any, Awaitable, Callable, Dict, List

from discord_interactions import InteractionResponseType, InteractionType, verify_key
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response
from starlette.types import Receive, Scope, Send

from disinter.api import DiscordAPI
from disinter.command import (
    ApplicationCommand,
    ApplicationCommandOption,
    ApplicationCommandOptionTypeSubCommand,
    ApplicationCommandOptionTypeSubCommandGroup,
)
from disinter.context import InteractionContext
from disinter.interaction import Interaction
from disinter.response import DiscordResponse
from disinter.utils import validate_name

CALLBACK_FUNCTION = (
    Callable[[InteractionContext], DiscordResponse]
    | Callable[[InteractionContext], Awaitable[DiscordResponse]]
)


class SlashSubgroup:
    def __init__(self, name: str, description: str) -> None:
        self.name = name
        self.description = description

        self._subcommands: Dict[str, SlashSubcommand] = {}

    def subcommand(
        self,
        name: str,
        description: str,
        options: List[ApplicationCommandOption] = None,
    ):
        def _subcommand(func: CALLBACK_FUNCTION):
            subcmd = SlashSubcommand(name, description, func, options)

            self._subcommands[name] = subcmd
            return self._subcommands[name]

        return _subcommand

    def _to_json(self):

        return {
            "name": self.name,
            "type": ApplicationCommandOptionTypeSubCommandGroup,
            "description": self.description,
            "options": [i._to_json() for _, i in self._subcommands.items()],
        }


class SlashSubcommand:
    def __init__(
        self,
        name: str,
        description: str,
        callback: CALLBACK_FUNCTION,
        options: List[ApplicationCommandOption] = None,
    ) -> None:
        self.name = name
        self.description = description
        self.options = options

        self._callback = callback

    def _to_json(self):
        json: Dict[str, Any] = {
            "name": self.name,
            "description": self.description,
            "type": ApplicationCommandOptionTypeSubCommand,
        }

        if self.options is not None:
            json["options"] = [i._to_json() for i in self.options]

        return json


class SlashCommand:
    def __init__(
        self, command: ApplicationCommand, callback: CALLBACK_FUNCTION
    ) -> None:
        self.command = command

        self._callback = callback
        self._command_groups: Dict[str, SlashSubgroup] = {}
        self._subcommands: Dict[str, SlashSubcommand] = {}

    def _to_json(self):
        command_groups = [i._to_json() for _, i in self._command_groups.items()]
        subcommands = [i._to_json() for _, i in self._subcommands.items()]

        # TODO: check if command_groups or subcommand name is similar with the one in options

        json = self.command._to_json()
        if len(command_groups) > 0 or len(subcommands) > 0:
            if "options" not in json:
                json["options"] = []

            for i in command_groups:
                json["options"].append(i)
            for i in subcommands:
                json["options"].append(i)

        return json

    def command_group(self, name: str, description: str):
        group = SlashSubgroup(name, description)

        self._command_groups[name] = group
        return self._command_groups[name]

    def subcommand(
        self,
        name: str,
        description: str,
        options: List[ApplicationCommandOption] = None,
    ):
        def _subcommand(func: CALLBACK_FUNCTION):
            subcmd = SlashSubcommand(name, description, func, options)

            self._subcommands[name] = subcmd
            return self._subcommands[name]

        return _subcommand


class DisInter(FastAPI):
    def __init__(
        self,
        token: str,
        application_id: int | str,
        public_key: str,
        guilds: List[str] = None,
    ) -> None:
        super().__init__()

        self.token = token
        self.application_id = application_id
        self.public_key = public_key
        self.guilds = guilds

        self.api = DiscordAPI(token, application_id)

        self._slash_commands: Dict[str, SlashCommand] = {}

        # add custom api router for interactions
        self.add_route(
            "/", self.__route_handler, methods=["POST"], include_in_schema=False
        )

    async def __route_handler(self, request: Request):
        body = await request.body()

        # Verify request
        signature = request.headers.get("X-Signature-Ed25519")
        timestamp = request.headers.get("X-Signature-Timestamp")
        if (
            signature is None
            or timestamp is None
            or not verify_key(body, signature, timestamp, self.public_key)
        ):
            return Response(content="Bad request signature", status_code=401)

        data: Interaction = await request.json()

        # Automatically respond to pings
        if data["type"] == InteractionType.PING:
            return JSONResponse({"type": InteractionResponseType.PONG})

        if data["type"] == InteractionType.APPLICATION_COMMAND:
            # slash / user / message commands
            command = self._slash_commands.get(data["data"]["name"])
            if command is not None:
                # slash command exists

                if len(data["data"]["options"]) > 0:
                    _opt = data["data"]["options"][0]

                    # check if subcommand group
                    if _opt["type"] == ApplicationCommandOptionTypeSubCommandGroup:
                        print("group command")
                        group = command._command_groups.get(_opt["name"])
                        if group is not None:
                            if len(_opt["options"]) > 0:
                                _sub = _opt["options"][0]
                                if (
                                    _sub["type"]
                                    == ApplicationCommandOptionTypeSubCommand
                                ):
                                    subcommand = group._subcommands.get(_sub["name"])
                                    if subcommand is None:
                                        return JSONResponse(
                                            {"error": "Command not defined in app"},
                                            status_code=400,
                                        )

                                    ctx = InteractionContext(data, _sub["options"])
                                    json = await self._execute_command_handler(
                                        ctx, subcommand._callback
                                    )
                                    return JSONResponse(json, status_code=200)

                    # check if subcommand
                    if _opt["type"] == ApplicationCommandOptionTypeSubCommand:
                        print("subcommand")
                        subcommand = command._subcommands.get(_opt["name"])
                        if subcommand is None:
                            return JSONResponse(
                                {"error": "Command not defined in app"}, status_code=400
                            )

                        ctx = InteractionContext(data, _opt["options"])
                        json = await self._execute_command_handler(
                            ctx, subcommand._callback
                        )
                        return JSONResponse(json, status_code=200)

                context = InteractionContext(data, data["options"])
                json = await self._execute_command_handler(context, command._callback)
                return JSONResponse(json, status_code=200)

    async def _execute_command_handler(
        self, context: InteractionContext, callback: CALLBACK_FUNCTION
    ):
        if asyncio.iscoroutinefunction(callback):
            output = await callback(context)
            return output._to_json()

        return callback(context)._to_json()

    def slash_command(
        self,
        name: str,
        description: str,
        name_localizations: Dict[str, str] = None,
        description_localizations: Dict[str, str] = None,
        options: List[ApplicationCommandOption] = None,
        default_member_permissions: str = None,
        dm_permission: bool = None,
    ):
        def _command(func: CALLBACK_FUNCTION):
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

            self._slash_commands[name] = SlashCommand(cmd, func)

            return self._slash_commands[name]

        return _command

    def _parse_commands(self):
        cmd_json: List[Dict[str, Any]] = []

        for _, cmd in self._slash_commands.items():
            js = cmd._to_json()

            cmd_json.append(js)

        return cmd_json

    def _sync_commands(self):
        commands = self._parse_commands()

        if self.guilds is None:
            self.api.bulk_overwrite_global_application_commands(commands)

            return

        for i in self.guilds:
            self.api.bulk_overwrite_guild_application_commands(i, commands)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        await super().__call__(scope, receive, send)
