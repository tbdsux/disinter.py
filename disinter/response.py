from __future__ import annotations

from typing import Any, Dict, List

from disinter.components import Components, Embed


class InteractionCallback:
    Pong = 1
    ChannelMessageWithSource = 4
    DeferredChannelMessageWithSource = 5
    DefferedUpdateMessage = 6
    UpdateMessage = 7
    ApplicationCommandAutocompleteResult = 8
    Modal = 9


class ModalResponseData:
    def __init__(
        self, custom_id: str, title: str, components: List[Components]
    ) -> None:
        self.custom_id = custom_id
        self.title = title
        self.components = components

    def _to_json(self):
        return {
            "custom_id": self.custom_id,
            "title": self.title,
            "components": [i._to_json() for i in self.components],
        }


class ResponseData:
    def __init__(
        self,
        tts: bool | None = None,
        content: str | None = None,
        embeds: List[Embed] | None = None,
        allowed_mentions: Dict[str, Any] | None = None,
        flags: int | None = None,
        components: List[Components] | None = None,
        # attachments: List = None
    ):
        self.tts = tts
        self.content = content
        self.embeds = embeds
        self.allowed_mentions = allowed_mentions
        self.flags = flags
        self.components = components
        # self.attachments = attachments // TODO:: implement adding attachment

    def _to_json(self):
        json: Dict[str, Any] = {}

        if self.tts is not None:
            json["tts"] = self.tts

        if self.content is not None:
            json["content"] = self.content

        if self.embeds is not None:
            json["embeds"] = [i._to_json() for i in self.embeds]

        if self.allowed_mentions is not None:
            json["allowed_mentions"] = self.allowed_mentions

        if self.flags is not None:
            json["flags"] = self.flags

        if self.components is not None:
            json["components"] = [i._to_json() for i in self.components]

        return json


class DiscordResponse:
    def __init__(
        self, type: int, data: ResponseData | ModalResponseData | None = None
    ) -> None:
        self.type = type
        self.data = data

    def _to_json(self):
        json: Dict[str, Any] = {"type": self.type}

        if self.data:
            json["data"] = self.data._to_json()

        return json
