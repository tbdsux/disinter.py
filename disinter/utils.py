# ref: https://github.com/Rapptz/discord.py/blob/master/discord/app_commands/commands.py

import re

# The re module doesn't support \p{} so we have to list characters from Thai and Devanagari manually.
THAI_COMBINING = r"\u0e31-\u0e3a\u0e47-\u0e4e"
DEVANAGARI_COMBINING = r"\u0900-\u0903\u093a\u093b\u093c\u093e\u093f\u0940-\u094f\u0955\u0956\u0957\u0962\u0963"
VALID_SLASH_COMMAND_NAME = re.compile(
    r"^[-_\w" + THAI_COMBINING + DEVANAGARI_COMBINING + r"]{1,32}$"
)


def validate_name(name: str) -> str:
    match = VALID_SLASH_COMMAND_NAME.match(name)
    if match is None:
        raise ValueError(
            f"{name!r} must be between 1-32 characters and contain only lower-case letters, numbers, hyphens, or underscores."
        )

    # Ideally, name.islower() would work instead but since certain characters
    # are Lo (e.g. CJK) those don't pass the test. I'd use `casefold` instead as
    # well, but chances are the server-side check is probably something similar to
    # this code anyway.
    if name.lower() != name:
        raise ValueError(f"{name!r} must be all lower-case")

    return name
