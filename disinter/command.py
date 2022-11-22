from __future__ import annotations

from typing import Any, Dict, List, NewType

ApplicationCommandOptionType = NewType("ApplicationCommandOptionType", int)

ApplicationCommandOptionTypeSubCommand = ApplicationCommandOptionType(1)
ApplicationCommandOptionTypeSubCommandGroup = ApplicationCommandOptionType(2)

ApplicationCommandOptionTypeString = ApplicationCommandOptionType(3)
ApplicationCommandOptionTypeInteger = ApplicationCommandOptionType(
    4
)  # Any integer between -2^53 and 2^53
ApplicationCommandOptionTypeBoolean = ApplicationCommandOptionType(5)
ApplicationCommandOptionTypeUser = ApplicationCommandOptionType(6)
ApplicationCommandOptionTypeChannel = ApplicationCommandOptionType(
    7
)  # Includes all channel types + categories
ApplicationCommandOptionTypeRole = ApplicationCommandOptionType(8)
ApplicationCommandOptionTypeMentionable = ApplicationCommandOptionType(9)
ApplicationCommandOptionTypeNumber = ApplicationCommandOptionType(
    10
)  # Any double between -2^53 and 2^53
ApplicationCommandOptionTypeAttachment = ApplicationCommandOptionType(
    11
)  # attachment object


ApplicationCommandType = NewType("ApplicationCommandType", int)
ApplicationCommandTypeSlashCommand = ApplicationCommandType(1)  # CHAT_INPUT
ApplicationCommandTypeUser = ApplicationCommandType(2)  # USER
ApplicationCommandTypeMessage = ApplicationCommandType(3)  # MESSAGE


class ApplicationCommandOptionChoice:
    def __init__(
        self,
        name: str,
        value: str | int | float,
        name_localizations: Dict[str, str] = None,
    ) -> None:
        self.name = name
        self.value = value
        self.name_localizations = name_localizations

    def _to_json(self) -> Dict[str, Any]:
        attrs = vars(self)
        json: Dict[str, Any] = {}
        for key, value in attrs.items():
            if value is not None:
                json[key] = value

        return json


class ApplicationCommandOption:
    def __init__(
        self,
        type: ApplicationCommandOptionType,
        name: str,
        description: str,
        name_localizations: Dict[str, str] = None,
        description_localizations: Dict[str, str] = None,
        required: bool = None,
        choices: List[ApplicationCommandOptionChoice] = None,
        channel_types: List[int] = None,
        min_value: int | float | None = None,
        max_value: int | float | None = None,
        min_length: int = None,
        max_length: int = None,
        autocomplete: bool = None,
    ) -> None:
        self.type = type
        self.name = name
        self.description = description
        self.name_localizations = name_localizations
        self.description_localizations = description_localizations
        self.required = required
        self.choices = choices
        self.channel_types = channel_types
        self.min_value = min_value
        self.max_value = max_value
        self.min_length = min_length
        self.max_length = max_length
        self.autocomplete = autocomplete

    def _to_json(self):
        attrs = vars(self)
        json: Dict[str, Any] = {}
        for key, value in attrs.items():
            if value is not None:
                # parsing list classes
                if isinstance(value, list):
                    list_arr: List[Dict[str, Any]] = []
                    for i in value:
                        list_arr.append(i._to_json())
                    json[key] = list_arr

                    continue

                json[key] = value

        return json


class ApplicationCommand:
    def __init__(
        self,
        name: str,
        description: str = None,
        type: ApplicationCommandType = ApplicationCommandTypeSlashCommand,
        id: str = None,
        application_id: str = None,
        name_localizations: Dict[str, str] = None,
        description_localizations: Dict[str, str] = None,
        options: List[
            ApplicationCommandOption  # NOTE: options param should not include subcommand or subcommand_group type
        ] = None,
        default_member_permissions: str = None,
        dm_permission: bool = None,
        version: str = None,
    ) -> None:
        self.name = name
        self.description = description
        self.type = type
        self.id = id
        self.application_id = application_id
        self.name_localizations = name_localizations
        self.description_localizations = description_localizations
        self.options = options
        self.default_member_permissions = default_member_permissions
        self.dm_permission = dm_permission
        self.version = version

    def _to_json(self) -> Dict[str, Any]:
        attrs = vars(self)
        json: Dict[str, Any] = {}
        for key, value in attrs.items():
            if value is not None:
                # parsing list classes
                if isinstance(value, list):
                    list_arr: List[Dict[str, Any]] = []
                    for i in value:
                        list_arr.append(i._to_json())
                    json[key] = list_arr

                    continue

                json[key] = value

        return json
