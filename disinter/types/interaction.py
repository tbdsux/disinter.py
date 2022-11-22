from __future__ import annotations

from typing import Any, Dict, List, TypedDict

from typing_extensions import Self

from disinter.types.custom import SnowFlake


class BaseObject(TypedDict, total=False):
    pass


class User(BaseObject):
    id: str
    username: str
    discriminator: str
    avatar: str | None
    bot: bool
    system: bool
    mfa_enabled: bool
    banner: str | None
    accent_color: int | None
    locale: str
    verified: bool
    email: str | None
    flags: int
    premium_type: int
    public_flags: int


class Member(BaseObject):
    user: User | None
    nick: str | None
    avatar: str | None
    roles: List[str]
    joined_at: str
    premium_since: str | None
    deaf: str
    mute: bool
    pending: bool | None
    permissions: str
    communication_disabled_until: str | None


class RoleTags(BaseObject):
    bot_id: str | None
    integration_id: str | None
    premium_subscriber: None


class Role(BaseObject):
    id: str
    name: str
    color: int
    hoist: bool
    icon: str | None
    unicode_emoji: str | None
    position: int
    permissions: str
    managed: bool
    mentionable: bool
    tags: RoleTags | None


class Overwrite(BaseObject):
    id: SnowFlake
    type: int
    allow: str
    deny: str


class DefaultReaction(BaseObject):
    emoji_id: SnowFlake | None
    emoji_name: str | None


class ForumTag(BaseObject):
    id: SnowFlake
    name: str
    moderated: bool
    emoji_id: SnowFlake
    emoji_name: str | None


class ThreadMember(BaseObject):
    id: SnowFlake
    user_id: SnowFlake
    join_timestamp: str
    flags: int


class ThreadMetadata(BaseObject):
    archived: bool
    auto_archive_duration: int
    archive_timestamp: str
    locked: bool
    invitable: bool
    create_timestamp: str | None


class Channel(BaseObject):
    id: SnowFlake
    type: int
    guild_id: SnowFlake
    position: int
    permission_overwrites: List[Overwrite] | None
    name: str | None
    topic: str | None
    nsfw: bool
    last_message_id: SnowFlake | None
    bitrate: int
    user_limit: int
    rate_limit_per_user: int
    recipients: List[User]
    icon: str | None
    owner_id: SnowFlake
    application_id: SnowFlake
    parent_id: SnowFlake | None
    last_pin_timestamp: str | None
    rtc_region: str | None
    video_quality_mode: int
    message_count: int
    member_count: int
    thread_metadata: ThreadMetadata
    member: ThreadMember
    default_auto_archive_duration: int
    permissions: str
    flags: int
    total_message_sent: int
    available_tags: List[ForumTag]
    applied_tags: List[SnowFlake]
    default_reaction_emoji: DefaultReaction | None
    default_thread_rate_limit_per_user: int
    default_sort_order: int | None


class ChannelMention(BaseObject):
    id: SnowFlake
    guild_id: SnowFlake
    type: int
    name: str


class Attachment(BaseObject):
    id: SnowFlake
    filename: str
    description: str
    content_type: str
    size: int
    url: str
    proxy_url: str
    height: int | None
    width: int | None
    ephemeral: bool


class EmbedFooter(BaseObject):
    text: str
    icon_url: str
    proxy_icon_url: str


class EmbedImage(BaseObject):
    url: str
    proxy_url: str
    height: int
    width: int


class EmbedVideo(EmbedImage):
    pass


class EmbedThumbnail(EmbedImage):
    pass


class EmbedProvider(BaseObject):
    name: str
    url: str


class EmbedAuthor(BaseObject):
    name: str
    url: str
    icon_url: str
    proxy_icon_url: str


class EmbedField(BaseObject):
    name: str
    value: str
    inline: bool


class Embed(BaseObject):
    title: str
    type: str
    description: str
    url: str
    timestamp: str
    color: int
    footer: EmbedFooter
    image: EmbedImage
    thumbnail: EmbedThumbnail
    video: EmbedVideo
    provider: EmbedVideo
    author: EmbedAuthor
    fields: List[EmbedField]


class Emoji(BaseObject):
    id: SnowFlake | None
    name: str | None
    roles: List[str]
    user: User
    require_colons: bool
    managed: bool
    animated: bool
    available: bool


class Reaction(BaseObject):
    count: int
    me: bool
    emoji: Emoji


class MessageActivity(BaseObject):
    type: int
    party_id: str


class MessageInteraction(BaseObject):
    id: SnowFlake
    type: int
    name: str
    user: User
    member: Member


class ComponentButton(BaseObject):
    type: int
    style: int
    label: str
    emoji: Emoji
    custom_id: str
    url: str
    disabled: bool


class ComponentSelectMenuOption(BaseObject):
    label: str
    value: str
    description: str
    emoji: Emoji
    default: bool


class ComponentSelectMenu(BaseObject):
    type: int
    custom_id: str
    options: List[ComponentSelectMenuOption]
    channel_types: List[int]
    placeholder: str
    min_values: int
    max_valueS: int
    disabled: bool


class ComponentTextInput(BaseObject):
    type: int
    custom_id: str
    style: int
    label: str
    min_length: int
    max_length: int
    required: bool
    value: str
    placeholder: str


class ComponentActionRows(BaseObject):
    type: int
    components: List[ComponentButton | ComponentSelectMenu | ComponentTextInput]


class StickerItem(BaseObject):
    id: SnowFlake
    name: str
    format_type: int


class Message(BaseObject):
    id: SnowFlake
    channel_id: SnowFlake
    author: User
    content: str
    timestamp: str
    edited_timestamp: str | None
    tts: bool
    mention_everyone: bool
    mentions: List[User]
    mention_roles: List[Role]
    mention_channels: List[ChannelMention]
    attachments: List[Attachment]
    embeds: List[Embed]
    reactions: List[Reaction]
    nonce: int | str
    pinned: bool
    webhook_id: SnowFlake
    type: int
    activity: MessageActivity
    application: Dict[str, Any]
    application_id: SnowFlake
    message_reference: Dict[str, Any]
    flags: int
    referenced_message: Dict[str, Any] | None
    interaction: MessageInteraction
    thread: Channel
    components: List[ComponentActionRows | ComponentButton | ComponentSelectMenu]
    sticker_items: List[StickerItem]
    position: int


class InteractionDataResolved(BaseObject):
    users: Dict[SnowFlake, User]
    members: Dict[SnowFlake, Member]
    roles: Dict[SnowFlake, Role]
    channels: Dict[SnowFlake, Channel]
    messages: Dict[SnowFlake, Message]
    attachments: Dict[SnowFlake, Attachment]


class InteractionDataOption(BaseObject):
    name: str
    type: int
    value: str | int | float
    options: List[Self]  # type: ignore
    focused: bool


class ApplicationCommandData(BaseObject):
    id: SnowFlake
    name: str
    type: int
    resolved: InteractionDataResolved
    options: List[InteractionDataOption]
    guild_id: SnowFlake
    target_id: SnowFlake


class MessageComponentData(BaseObject):
    custom_id: str
    component_type: int
    values: List[str] | None


class ModalSubmitData(BaseObject):
    custom_id: str
    components: List[
        ComponentActionRows | ComponentButton | ComponentSelectMenu | ComponentTextInput
    ]


class Interaction(BaseObject):
    id: SnowFlake
    application_id: SnowFlake
    type: int
    guild_id: SnowFlake
    channel_id: SnowFlake
    member: Member
    user: User
    token: str
    version: int
    message: Message
    app_permisions: str
    locale: str
    guild_locale: str


class InteractionApplicationCommand(Interaction):
    data: ApplicationCommandData


class InteractionMessageComponent(Interaction):
    data: MessageComponentData


class InteractionModalSubmit(Interaction):
    data: ModalSubmitData
