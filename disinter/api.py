from typing import Any, Dict, List

from requests import Session

from disinter import DISCORD_API
from disinter.errors import APIError
from disinter.types import APIApplicationCommand


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
        body: Any = None,
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

    def get_application_commands(
        self, guild: int | str | None = None, **kwargs
    ) -> List[APIApplicationCommand]:
        """Get application commands.

        Args:
            guild (int | str | None, optional): Guild to get the application commands. If None, gets the global commands. Defaults to None.

        Returns:
            List[APIApplicationCommand]
        """
        if guild is not None:
            return self._request(
                f"/applications/{self.application_id}/guilds/{guild}/commands",
                "GET",
                params=kwargs,
            )

        return self._request(
            f"/applications/{self.application_id}/commands", "GET", params=kwargs
        )

    def create_application_command(
        self, command: Dict[str, Any], guild: int | str | None = None
    ):
        """Create an application command.

        Args:
            command (Dict[str, Any]): Application command object.
            guild (int | str | None, optional): Guild to create the command. If None, creates a global command. Defaults to None.

        Returns:
            _type_: _description_
        """
        if guild is not None:
            return self._request(
                f"/applications/{self.application_id}/guilds/{guild}/commands",
                "POST",
                body=command,
            )

        return self._request(
            f"/applications/{self.application_id}/commands", "POST", body=command
        )

    def get_application_command(
        self, command_id: int | str, guild: int | str | None = None
    ) -> APIApplicationCommand:
        """Get an application command.

        Args:
            command_id (int | str): ID of the command to fetch.
            guild (int | str | None, optional): Guild to fetch the command_id. If None, fetches from the global commands. Defaults to None.

        Returns:
            APIApplicationCommand
        """
        if guild is not None:
            return self._request(
                f"/applications/{self.application_id}/guilds/{guild}/commands/{command_id}",
                "GET",
            )

        return self._request(
            f"/applications/{self.application_id}/commands/{command_id}", "GET"
        )

    def edit_application_command(
        self,
        command_id: int | str,
        command: Dict[str, Any],
        guild: int | str | None = None,
    ):
        """Edit an application command.

        Args:
            command_id (int | str): ID of the command to edit.
            command (Dict[str, Any]): Application command object.
            guild (int | str | None, optional): Guild to update the command. If None, updates the command in the global commands. Defaults to None.

        Returns:
            _type_: _description_
        """
        if guild is not None:
            return self._request(
                f"/applications/{self.application_id}/guilds/{guild}/commands/{command_id}",
                "PATCH",
                body=command,
            )

        return self._request(
            f"/applications/{self.application_id}/commands/{command_id}",
            "PATCH",
            body=command,
        )

    def delete_application_command(
        self, command_id: int | str, guild: int | str | None = None
    ):
        """Delete an application command.

        Args:
            command_id (int | str): ID of the command to delete.
            guild (int | str | None, optional): Guild to remove the command. If None, removes the command in the global commands. Defaults to None.

        Returns:
            _type_: _description_
        """
        if guild is not None:
            return self._request(
                f"/applications/{self.application_id}/guilds/{guild}/commands/{command_id}",
                "GET",
            )

        return self._request(
            f"/applications/{self.application_id}/commands/{command_id}", "DELETE"
        )

    def bulk_overwrite_application_commands(
        self, commands: List[Dict[str, Any]], guild: int | str | None = None
    ):
        """Bulk overwrite commands.

        Args:
            commands (List[Dict[str, Any]]): List of commands to create and overwrite.
            guild (int | str | None, optional): Guild to overwrite the commands. If None, it will overwrite to the global commands. Defaults to None.

        Returns:
            _type_: _description_
        """
        if guild is not None:
            return self._request(
                f"/applications/{self.application_id}/guilds/{guild}/commands",
                "PUT",
                body=commands,
            )

        return self._request(
            f"/applications/{self.application_id}/commands", "PUT", body=commands
        )
