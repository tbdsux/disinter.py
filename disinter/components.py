from __future__ import annotations

from typing import Any, Dict, List, NewType, Union

from typing_extensions import Self


class BaseJSON:
    def _to_json(self):
        attrs = vars(self)
        json: Dict[str, Any] = {}
        for key, value in attrs.items():
            if value is not None:
                json[key] = value

        return json


class EmbedFooter(BaseJSON):
    def __init__(
        self, text: str, icon_url: str = None, proxy_icon_url: str = None
    ) -> None:
        self.text = text
        self.icon_url = icon_url
        self.proxy_icon_url = proxy_icon_url


class EmbedImage(BaseJSON):
    def __init__(
        self, url: str, proxy_url: str = None, height: int = None, width: int = None
    ) -> None:
        self.url = url
        self.proxy_url = proxy_url
        self.height = height
        self.width = width


class EmbedThumbnail(BaseJSON):
    def __init__(
        self, url: str, proxy_url: str = None, height: int = None, width: int = None
    ) -> None:
        self.url = url
        self.proxy_url = proxy_url
        self.height = height
        self.width = width


class EmbedVideo(BaseJSON):
    def __init__(
        self, url: str, proxy_url: str = None, height: int = None, width: int = None
    ) -> None:
        self.url = url
        self.proxy_url = proxy_url
        self.height = height
        self.width = width


class EmbedProvider(BaseJSON):
    def __init__(self, name: str = None, url: str = None) -> None:
        self.name = name
        self.url = url


class EmbedAuthor(BaseJSON):
    def __init__(
        self,
        name: str,
        url: str = None,
        icon_url: str = None,
        proxy_icon_url: str = None,
    ) -> None:
        self.name = name
        self.url = url
        self.icon_url = icon_url
        self.proxy_icon_url = proxy_icon_url


class EmbedField(BaseJSON):
    def __init__(self, name: str, value: str, inline: bool = None) -> None:
        self.name = name
        self.value = value
        self.inline = inline


class Embed:
    def __init__(
        self,
        title: str = None,
        type: str = None,
        description: str = None,
        url: str = None,
        timestamp: str = None,
        color: int = None,
        footer: EmbedFooter = None,
        image: EmbedImage = None,
        thumbnail: EmbedThumbnail = None,
        video: EmbedVideo = None,
        provider: EmbedProvider = None,
        author: EmbedAuthor = None,
        fields: List[EmbedField] = None,
    ):
        self.title = title
        self.type = type
        self.description = description
        self.url = url
        self.timestamp = timestamp
        self.color = color
        self.footer = footer
        self.image = image
        self.thumbnail = thumbnail
        self.video = video
        self.provider = provider
        self.author = author
        self.fields = fields

    def _to_json(self):
        attrs = vars(self)
        json: Dict[str, Any] = {}
        for key, value in attrs.items():
            if value is not None:
                # custom class
                if key in [
                    "footer",
                    "image",
                    "thumbnail",
                    "video",
                    "provider",
                    "author",
                ]:
                    json[key] = value._to_json()
                    continue

                # list class
                if key == "fields":
                    fields = [i._to_json() for i in self.fields]
                    json[key] = fields
                    continue

                json[key] = value

        return json


class Emoji(BaseJSON):
    def __init__(self, id: str = None, name: str = None, animated: bool = None) -> None:
        self.id = id
        self.name = name
        self.animated = animated


class ButtonStyles:
    Primary = 1
    Secondary = 2
    Success = 3
    Danger = 4
    Link = 5


class ComponentButton:
    def __init__(
        self,
        style: int,
        label: str = None,
        emoji: Emoji = None,
        custom_id: str = None,
        url: str = None,
        disabled: bool = None,
    ) -> None:
        self.type = 2
        self.style = style
        self.label = label
        self.emoji = emoji
        self.custom_id = custom_id
        self.url = url
        self.disabled = disabled

    def _to_json(self):
        attrs = vars(self)
        json: Dict[str, Any] = {}
        for key, value in attrs.items():
            if value is not None:
                if key == "emoji":
                    json[key] = value._to_json()
                    continue

                json[key] = value

        return json


ComponentSelectMenuType = NewType("ComponentSelectMenuType", int)
ComponentSelectMenuTypeText = ComponentSelectMenuType(3)
ComponentSelectMenuTypeUser = ComponentSelectMenuType(5)
ComponentSelectMenuTypeRole = ComponentSelectMenuType(6)
ComponentSelectMenuTypeMentionable = ComponentSelectMenuType(7)
ComponentSelectMenuTypeChannels = ComponentSelectMenuType(8)


class ComponentSelectMenuOption:
    def __init__(
        self,
        label: str,
        value: str,
        description: str = None,
        emoji: Emoji = None,
        default: bool = None,
    ) -> None:
        self.label = label
        self.value = value
        self.description = description
        self.emoji = emoji
        self.default = default

    def _to_json(self):
        attrs = vars(self)
        json: Dict[str, Any] = {}
        for key, value in attrs.items():
            if value is not None:
                if key == "emoji":
                    json[key] = value._to_json()
                    continue

                json[key] = value

        return json


class ComponentSelectMenu:
    def __init__(
        self,
        type: ComponentSelectMenuType,
        custom_id: str,
        options: List[ComponentSelectMenuOption] = None,
        channel_types: List[int] = None,
        placeholder: str = None,
        min_values: int = None,
        max_vales: int = None,
        disabled: bool = None,
    ) -> None:
        self.type = type
        self.custom_id = custom_id
        self.options = options
        self.channel_types = channel_types
        self.placeholder = placeholder
        self.min_values = min_values
        self.max_vales = max_vales
        self.disabled = disabled

    def _to_json(self):
        attrs = vars(self)
        json: Dict[str, Any] = {}
        for key, value in attrs.items():
            if value is not None:
                if key == "options":
                    json[key] = [i._to_json() for i in self.options]
                    continue

                json[key] = value

        return json


ComponentTextInputStyle = NewType("ComponentTextInputStyle", int)
ComponentTextInputStyleShort = ComponentTextInputStyle(1)
ComponentTextInputStyleParagraph = ComponentTextInputStyle(2)


class ComponentTextInput(BaseJSON):
    def __init__(
        self,
        custom_id: str,
        style: ComponentTextInputStyle,
        label: str,
        min_length: int = None,
        max_length: int = None,
        required: bool = None,
        value: str = None,
        placeholder: str = None,
    ) -> None:
        self.type = 4
        self.custom_id = custom_id
        self.style = style
        self.label = label
        self.min_length = min_length
        self.max_length = max_length
        self.required = required
        self.value = value
        self.placeholder = placeholder


class ComponentActionRows:
    def __init__(
        self, components: List[ComponentButton | ComponentSelectMenu | ComponentTextInput | Self]  # type: ignore
    ) -> None:
        self.type = 1
        self.components = components

    def _to_json(self):
        return {
            "type": self.type,
            "components": [i._to_json() for i in self.components],
        }


Components = Union[ComponentButton, ComponentSelectMenu, ComponentActionRows]


# class ComponentAttachment:
#     def __init__(self,
#         id: str,
#         filename: str,


#     ) -> None:
#         pass
