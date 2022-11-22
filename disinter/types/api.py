from __future__ import annotations

from typing import Any, Dict, List

from typing_extensions import Self

from disinter.types.custom import SnowFlake
from disinter.types.interaction import BaseObject


class APIApplicationCommandOptionChoice(BaseObject):
    name: str
    name_localizations: Dict[str, Any] | None
    value: str | int | float


class APIApplicationCommandOption(BaseObject):
    type: int
    name: str
    name_localizations: Dict[str, Any] | None
    description: str
    description_localizations: Dict[str, Any] | None
    required: bool
    choices: List[APIApplicationCommandOptionChoice]
    options: List[Self]  # type: ignore
    channel_types: List[int]
    min_value: int | float
    max_value: int | float
    autocomplete: bool


class APIApplicationCommand(BaseObject):
    id: SnowFlake
    type: int
    application_id: SnowFlake
    guild_id: SnowFlake
    name: str
    name_localizations: Dict[str, Any] | None
    description: str
    description_localizations: Dict[str, Any] | None
    options: List[APIApplicationCommandOption]
    default_member_permissions: str | None
    dm_permission: bool | None
    default_permission: bool | None
    version: SnowFlake
