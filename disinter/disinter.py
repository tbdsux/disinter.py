from __future__ import annotations

import asyncio
from typing import Any, Awaitable, Callable, Dict, List, Union

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
    ApplicationCommandTypeMessage,
    ApplicationCommandTypeUser,
)
from disinter.context import (
    ComponentContext,
    MessageContext,
    ModalSubmitContext,
    SlashContext,
    UserContext,
)
from disinter.errors import CommandNameExists
from disinter.response import DiscordResponse
from disinter.types import (
    ComponentTypes,
    InteractionApplicationCommand,
    InteractionMessageComponent,
)
from disinter.types.interaction import InteractionModalSubmit
from disinter.utils import validate_name

# slash command function callback type
SLASH_CALLBACK_FUNCTION = Union[
    Callable[[SlashContext], DiscordResponse],
    Callable[[SlashContext], Awaitable[DiscordResponse]],
]

# user command function callback type
USER_CALLBACK_FUNCTION = Union[
    Callable[[UserContext], DiscordResponse],
    Callable[[UserContext], Awaitable[DiscordResponse]],
]

# message command function callback type
MESSAGE_CALLBACK_FUNCTION = Union[
    Callable[[MessageContext], DiscordResponse],
    Callable[[MessageContext], Awaitable[DiscordResponse]],
]


# component function callback type
COMPONENT_CALLBACK_FUNCTION = Union[
    Callable[[ComponentContext], DiscordResponse],
    Callable[[ComponentContext], Awaitable[DiscordResponse]],
]


# modal submit function callback type
MODALSUBMIT_CALLBACK_FUNCTION = Union[
    Callable[[ModalSubmitContext], DiscordResponse],
    Callable[[ModalSubmitContext], Awaitable[DiscordResponse]],
]


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
        def _subcommand(func: SLASH_CALLBACK_FUNCTION):
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
        callback: SLASH_CALLBACK_FUNCTION,
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
        self, command: ApplicationCommand, callback: SLASH_CALLBACK_FUNCTION
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
        def _subcommand(func: SLASH_CALLBACK_FUNCTION):
            subcmd = SlashSubcommand(name, description, func, options)

            self._subcommands[name] = subcmd
            return self._subcommands[name]

        return _subcommand


class UserCommand:
    def __init__(
        self, command: ApplicationCommand, func: USER_CALLBACK_FUNCTION
    ) -> None:
        self.command = command
        self._callback = func

    def _to_json(self):
        return {"name": self.command.name, "type": self.command.type}


class MessageCommand:
    def __init__(
        self, command: ApplicationCommand, func: MESSAGE_CALLBACK_FUNCTION
    ) -> None:
        self.command = command
        self._callback = func

    def _to_json(self):
        return {"name": self.command.name, "type": self.command.type}


class MessageComponent:
    def __init__(self, custom_id: str, func: COMPONENT_CALLBACK_FUNCTION) -> None:
        self.custom_id = custom_id
        self._callback = func


class ModalSubmit:
    def __init__(self, custom_id, func: MODALSUBMIT_CALLBACK_FUNCTION) -> None:
        self.custom_id = custom_id
        self._callback = func


class DisInter(FastAPI):
    def __init__(
        self,
        token: str,
        application_id: int | str,
        public_key: str,
        guilds: List[str] | None = None,
    ) -> None:
        super().__init__()

        self.token = token
        self.application_id = application_id
        self.public_key = public_key
        self.guilds = guilds

        self.api = DiscordAPI(token, application_id)

        self._slash_commands: Dict[str, SlashCommand] = {}
        self._user_commands: Dict[str, UserCommand] = {}
        self._message_commands: Dict[str, MessageCommand] = {}

        self._button_components: Dict[str, MessageComponent] = {}
        self._button_fallback: COMPONENT_CALLBACK_FUNCTION | None = None
        self._selectmenu_components: Dict[str, MessageComponent] = {}
        self._selectmenu_fallback: COMPONENT_CALLBACK_FUNCTION | None = None

        self._modalsubmit_handlers: Dict[str, ModalSubmit] = {}
        self._modalsubmit_fallback: MODALSUBMIT_CALLBACK_FUNCTION | None = None

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

        req = await request.json()

        # Automatically respond to pings
        if req["type"] == InteractionType.PING:
            return JSONResponse({"type": InteractionResponseType.PONG})

        if req["type"] == InteractionType.APPLICATION_COMMAND:
            data: InteractionApplicationCommand = req
            command_name = data["data"]["name"]

            # slash commands
            command = self._slash_commands.get(command_name)
            if command is not None:
                # slash command exists

                if data["data"].get("options") is not None:
                    _opt = data["data"]["options"][0]

                    # check if subcommand group
                    if _opt["type"] == ApplicationCommandOptionTypeSubCommandGroup:
                        group = command._command_groups.get(_opt["name"])
                        if group is not None:
                            if len(_opt["options"]) > 0:
                                _sub = _opt["options"][0]
                                if (
                                    _sub["type"]  # type: ignore
                                    == ApplicationCommandOptionTypeSubCommand
                                ):
                                    subcommand = group._subcommands.get(_sub["name"])  # type: ignore
                                    if subcommand is None:
                                        return JSONResponse(
                                            {"error": "Command not defined in app"},
                                            status_code=400,
                                        )

                                    ctx = SlashContext(data, _sub["options"])  # type: ignore
                                    json = await self._execute_handler(
                                        ctx, subcommand._callback
                                    )
                                    return JSONResponse(json, status_code=200)

                    # check if subcommand
                    if _opt["type"] == ApplicationCommandOptionTypeSubCommand:
                        subcommand = command._subcommands.get(_opt["name"])
                        if subcommand is None:
                            return JSONResponse(
                                {"error": "Command not defined in app"}, status_code=400
                            )

                        ctx = SlashContext(data, _opt["options"])
                        json = await self._execute_handler(ctx, subcommand._callback)
                        return JSONResponse(json, status_code=200)

                slash_ctx = SlashContext(data, data["data"].get("options"))
                json = await self._execute_handler(slash_ctx, command._callback)
                return JSONResponse(json, status_code=200)

            # user commands
            user_command = self._user_commands.get(command_name)
            if user_command is not None:
                # user command exists
                user_ctx = UserContext(data)
                json = await self._execute_handler(user_ctx, user_command._callback)
                return JSONResponse(json, status_code=200)

            # message commands
            message_command = self._message_commands.get(command_name)
            if message_command is not None:
                # message command exists
                msg_ctx = MessageContext(data)
                json = await self._execute_handler(msg_ctx, message_command._callback)
                return JSONResponse(json, status_code=200)

            # unknown command in here
            return JSONResponse({"error": "Unknown type"}, status_code=401)

        if req["type"] == InteractionType.MESSAGE_COMPONENT:
            msg_component: InteractionMessageComponent = req

            custom_id = msg_component["data"]["custom_id"]
            component_type = msg_component["data"]["component_type"]
            component_context = ComponentContext(msg_component)

            if component_type == ComponentTypes.Button:  # handle button component
                btn_component = self._button_components.get(custom_id)
                if btn_component is not None:
                    json = await self._execute_handler(
                        component_context, btn_component._callback
                    )
                    return JSONResponse(json, status_code=200)

                if self._button_fallback is not None:
                    json = await self._execute_handler(
                        component_context, self._button_fallback
                    )
                    return JSONResponse(json, status_code=200)

                # no button wrapper callback set in app
                return JSONResponse(
                    {"error": "Component wrapper callback function not set"},
                    status_code=500,
                )

            if component_type in [
                ComponentTypes.StringSelect,
                ComponentTypes.UserSelect,
                ComponentTypes.RoleSelect,
                ComponentTypes.MentionableSelect,
                ComponentTypes.ChannelSelect,
            ]:
                # handle select menu component
                menu_component = self._selectmenu_components.get(custom_id)
                if menu_component is not None:
                    json = await self._execute_handler(
                        component_context, menu_component._callback
                    )
                    return JSONResponse(json, status_code=200)

                if self._selectmenu_fallback is not None:
                    json = await self._execute_handler(
                        component_context, self._selectmenu_fallback
                    )
                    return JSONResponse(json, status_code=200)

                # no select menu wrapper callback set in app
                return JSONResponse(
                    {"error": "Component wrapper callback function not set"},
                    status_code=500,
                )

        if req["type"] == InteractionType.MODAL_SUBMIT:
            modalsubmit: InteractionModalSubmit = req

            custom_id = modalsubmit["data"]["custom_id"]
            modal_context = ModalSubmitContext(modalsubmit)

            modal_handler = self._modalsubmit_handlers.get(custom_id)
            if modal_handler is not None:
                json = await self._execute_handler(
                    modal_context, modal_handler._callback
                )
                return JSONResponse(json, status_code=200)

            if self._modalsubmit_fallback is not None:
                json = await self._execute_handler(
                    modal_context, self._modalsubmit_fallback
                )
                return JSONResponse(json, status_code=200)

            # no modalsubmit handler defined set in app
            return JSONResponse(
                {"error": "Modal submit wrapper callback function not set."},
                status_code=500,
            )

    async def _execute_handler(
        self,
        context: SlashContext
        | UserContext
        | MessageContext
        | ComponentContext
        | ModalSubmitContext,
        callback: SLASH_CALLBACK_FUNCTION
        | USER_CALLBACK_FUNCTION
        | MESSAGE_CALLBACK_FUNCTION
        | COMPONENT_CALLBACK_FUNCTION
        | MODALSUBMIT_CALLBACK_FUNCTION,
    ):
        output = None

        if asyncio.iscoroutinefunction(callback):
            output = await callback(context)
        else:
            output = callback(context)  # type: ignore

        assert isinstance(output, DiscordResponse)

        return output._to_json()  # type: ignore

    def modalsubmit_handler(self, custom_id: str | None = None):
        """Add a function handler to a modal component when submitted.

        Args:
            custom_id (str | None, optional): ID of the modal. Defaults to None.
        """

        def _modalsubmit(func: MODALSUBMIT_CALLBACK_FUNCTION):
            if custom_id is None:
                self._modalsubmit_fallback = func
                return

            modalsub = ModalSubmit(custom_id=custom_id, func=func)
            self._modalsubmit_handlers[custom_id] = modalsub
            return self._modalsubmit_handlers[custom_id]

        return _modalsubmit

    def button_component(self, custom_id: str | None = None):
        """Add a function callback to the custom_id of a button component.

        Args:
            custom_id (str): ID of the button.
        """

        def _component(func: COMPONENT_CALLBACK_FUNCTION):
            if custom_id is None:
                self._button_fallback = func
                return

            cmp = MessageComponent(custom_id=custom_id, func=func)
            self._button_components[custom_id] = cmp
            return self._button_components[custom_id]

        return _component

    def selectmenu_component(self, custom_id: str | None = None):
        """Add a function callback to the custom_id of a select menu component.

        Args:
            custom_id (str): ID of the select menu.
        """

        def _component(func: COMPONENT_CALLBACK_FUNCTION):
            if custom_id is None:
                self._selectmenu_fallback = func
                return

            cmp = MessageComponent(custom_id=custom_id, func=func)
            self._selectmenu_components[custom_id] = cmp
            return self._selectmenu_components[custom_id]

        return _component

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
        """Add a new slash command.

        Args:
            name (str): Name of the command
            description (str): Description of the slash
            name_localizations (Dict[str, str], optional): _description_. Defaults to None.
            description_localizations (Dict[str, str], optional): _description_. Defaults to None.
            options (List[ApplicationCommandOption], optional): Slash command options. Defaults to None.
            default_member_permissions (str, optional): Set of permissions for the command. Defaults to None.
            dm_permission (bool, optional): Allow command in DMs. Defaults to None.
        """

        def _command(func: SLASH_CALLBACK_FUNCTION):
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

    def user_command(self, name: str):
        """Add a new user command.

        Args:
            name (str): Name of the user command.
        """

        def _command(func: USER_CALLBACK_FUNCTION):
            cmd = ApplicationCommand(name=name, type=ApplicationCommandTypeUser)
            self._user_commands[name] = UserCommand(cmd, func)
            return self._user_commands[name]

        return _command

    def message_command(self, name: str):
        """Add a new message command.

        Args:
            name (str): Name of the message command.
        """

        def _command(func: MESSAGE_CALLBACK_FUNCTION):
            cmd = ApplicationCommand(name=name, type=ApplicationCommandTypeMessage)
            self._message_commands[name] = MessageCommand(cmd, func)
            return self._message_commands[name]

        return _command

    def _parse_commands(self):
        cmd_json: List[Dict[str, Any]] = []
        cmd_keys: List[str] = []

        for cmd in self._slash_commands.values():
            name = cmd.command.name
            if name in cmd_keys:
                raise CommandNameExists(name)

            js = cmd._to_json()
            cmd_json.append(js)
            cmd_keys.append(cmd.command.name)

        for cmd in self._user_commands.values():
            name = cmd.command.name
            if name in cmd_keys:
                raise CommandNameExists(name)

            js = cmd._to_json()
            cmd_json.append(js)
            cmd_keys.append(cmd.command.name)

        for cmd in self._message_commands.values():
            name = cmd.command.name
            if name in cmd_keys:
                raise CommandNameExists(name)

            js = cmd._to_json()
            cmd_json.append(js)
            cmd_keys.append(cmd.command.name)

        return cmd_json, cmd_keys

    def sync_commands(self):
        """
        Sync commands to the set guilds in the app.

        If `self.guilds` is `None`, it will register the defined app commands as global commands.

        Note: `None != []`
        """
        commands, cmd_keys = self._parse_commands()

        if self.guilds is None:
            # global commans
            global_commands = self.api.get_application_commands()
            for i in global_commands:
                # check if command exist in current new ones
                if i["name"] in cmd_keys:
                    continue

                # remove if it does not exist
                self.api.delete_application_command(i["id"])

            # overwrite commands
            self.api.bulk_overwrite_application_commands(commands)

        for i in self.guilds:
            guild_commands = self.api.get_application_commands(i)
            for k in guild_commands:
                # check if command exists in current new ones
                if k["name"] in cmd_keys:
                    continue

                # remove if it does not exist
                self.api.delete_application_command(k["id"], i)

            # overwrite commands
            self.api.bulk_overwrite_application_commands(commands, i)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        await super().__call__(scope, receive, send)
