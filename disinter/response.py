from typing import Any, Dict, List, NewType

from disinter.components import Components, Embed

InteractionCallbackType = NewType("InteractionCallbackType", int)
InteractionCallbackTypePong = InteractionCallbackType(1)
InteractionCallbackTypeChannelMessageWithSource = InteractionCallbackType(4)
InteractionCallbackTypeDeferredChannelMessageWithSource = InteractionCallbackType(5)
InteractionCallbackTypeDefferedUpdateMessage = InteractionCallbackType(6)
InteractionCallbackTypeUpdateMessage = InteractionCallbackType(7)
InteractionCallbackTypeApplicationCommandAutocompleteResult = InteractionCallbackType(8)
InteractionCallbackTypeModal = InteractionCallbackType(9)


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
        self, type: InteractionCallbackType, data: ResponseData = None
    ) -> None:
        self.type = type
        self.data = data

    def _to_json(self):
        json: Dict[str, Any] = {"type": self.type}

        if self.data:
            json["data"] = self.data._to_json()

        return json
