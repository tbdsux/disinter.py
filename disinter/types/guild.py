from __future__ import annotations

from typing import List

from disinter.types.custom import SnowFlake
from disinter.types.interaction import BaseObject, Emoji, Role, User


class WelcomeScreenChannel(BaseObject):
    channel_id: SnowFlake
    description: str
    emoji_id: SnowFlake | None
    emoji_name: str | None


class WelcomeScreen(BaseObject):
    description: str | None
    welcome_channels: List[WelcomeScreenChannel]


class Sticker(BaseObject):
    id: SnowFlake
    pack_id: SnowFlake | None
    name: str
    description: str | None
    tags: str
    asset: str | None
    type: int
    format_type: int
    available: bool | None
    guild_id: SnowFlake | None
    user: User | None
    sort_value: int | None


class Guild(BaseObject):
    id: SnowFlake
    name: str
    icon: str | None
    icon_hash: str | None
    splash: str | None
    discovery_splash: str | None
    owner: bool | None
    owner_id: SnowFlake
    permissions: str | None
    afk_channel_id: SnowFlake | None
    afk_timeout: int
    widget_enabled: bool | None
    widget_channel_id: SnowFlake | None
    verification_level: int
    default_message_notifications: int
    explicit_content_filter: int
    roles: List[Role]
    emojis: List[Emoji]
    features: List[str]
    mfa_level: int
    application_id: SnowFlake | None
    system_channel_id: SnowFlake | None
    system_channel_flags: int
    rules_channel_id: SnowFlake | None
    max_presences: int | None
    max_members: int | None
    vanity_url_code: str | None
    description: str | None
    banner: str | None
    premium_tier: int
    premium_subscription_count: int | None
    preferred_locale: str
    public_updates_channel_id: SnowFlake | None
    max_video_channel_users: int | None
    approximate_member_count: int | None
    approximate_presence_count: int | None
    welcome_screen: WelcomeScreen | None
    nsfw_level: int
    stickers: List[Sticker] | None
    premium_progress_bar_enabled: bool
