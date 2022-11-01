from typing import Any, Dict, List

from requests import Session

from disinter import DISCORD_API
from disinter.errors import APIError


class DiscordAPI:
    def __init__(self, token: str, application_id: int | str) -> None:
        self.token = token
        self.application_id = application_id

        self._session = Session()
        self._session.headers.update({"Authorization": f"Bot {token}"})

    def _request(
        self,
        endpoint: str,
        method: str,
        params: Dict[str, Any] = None,
        body: Dict[str, Any] = None,
    ):
        """Default internal base request function for all of methods in the class.

        Args:
            endpoint (str): endpoint tot send request to
            method (str): method of request
            params (Dict[str, Any], optional): url params if available. Defaults to None.
            body (Dict[str, Any], optional): json body if available. Defaults to None.

        Raises:
            APIError: APIError with error response in dictionary

        Returns:
            Dict[str, Any]: JSON response returned by the api.
        """

        r = self._session.request(
            method=method, url=DISCORD_API + endpoint, params=params, json=body
        )

        data = r.json()

        if not r.ok:
            raise APIError(data)

        return data

    # =============== GUILD APPLICATION COMMANDS

    def get_guild_application_commands(self, guild: int | str, **kwargs):
        """Get Guild Application Commands"""

        return self._request(
            f"/applications/{self.application_id}/guilds/{guild}/commands",
            "GET",
            params=kwargs,
        )

    def create_guild_application_command(
        self, guild: int | str, command: Dict[str, Any]
    ):
        """Get Guild Application Commands"""

        return self._request(
            f"/applications/{self.application_id}/guilds/{guild}/commands",
            "POST",
            body=command,
        )

    def get_guild_application_command(self, guild: int | str, command_id: int | str):
        """Get Guild Application Command"""

        return self._request(
            f"/applications/{self.application_id}/guilds/{guild}/commands/{command_id}",
            "GET",
        )

    def edit_guild_application_command(
        self, guild: int | str, command_id: int | str, command: Dict[str, Any]
    ):
        """Edit Guild Application Command"""

        return self._request(
            f"/applications/{self.application_id}/guilds/{guild}/commands/{command_id}",
            "PATCH",
            body=command,
        )

    def delete_guild_application_command(self, guild: int | str, command_id: int | str):
        """Delete Guild Application Command"""

        return self._request(
            f"/applications/{self.application_id}/guilds/{guild}/commands/{command_id}",
            "GET",
        )

    def bulk_overwrite_guild_application_commands(
        self, guild: int | str, commands: List[Dict[str, Any]]
    ):
        """Bulk Overwrite Global Application Commands"""

        return self._request(
            f"/applications/{self.application_id}/guilds/{guild}/commands",
            "PUT",
            body=commands,
        )

    # =============== GLOBAL APPLICATION COMMANDS

    def get_global_application_commands(self, **kwargs):
        """Get Global Application Commands"""

        return self._request(
            f"/applications/{self.application_id}/commands", "GET", params=kwargs
        )

    def create_global_application_command(self, command: Dict[str, Any]):
        """Create Global Application Command"""

        return self._request(
            f"/applications/{self.application_id}/commands", "POST", body=command
        )

    def get_global_application_command(self, command_id: int | str):
        """Get Global Application Command"""

        return self._request(
            f"/applications/{self.application_id}/commands/{command_id}", "GET"
        )

    def edit_global_application_command(
        self, command_id: int | str, command: Dict[str, Any]
    ):
        """Edit Global Application Command"""

        return self._request(
            f"/applications/{self.application_id}/commands/{command_id}",
            "PATCH",
            body=command,
        )

    def delete_global_application_command(self, command_id: int | str):
        """Delete Global Application Command"""

        return self._request(
            f"/applications/{self.application_id}/commands/{command_id}", "DELETE"
        )

    def bulk_overwrite_global_application_commands(
        self, commands: List[Dict[str, Any]]
    ):
        """Bulk Overwrite Global Application Commands"""

        return self._request(
            f"/applications/{self.application_id}/commands", "PUT", body=commands
        )
