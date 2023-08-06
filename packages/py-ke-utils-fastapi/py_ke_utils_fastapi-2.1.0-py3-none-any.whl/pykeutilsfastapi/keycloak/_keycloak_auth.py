import logging
from typing import Annotated

import requests
from fastapi import Header, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from keycloak import KeycloakOpenID, KeycloakError
from requests import HTTPError

security = HTTPBearer()


class KeycloakAuthentication:
    """
    Dependency class for FastAPI. It validates token using keycloak.
    :param server_url: The url of the keycloak.
    :param client_id: The ID of the keycloak client.
    :param client_secret_key: The secret key of the Keycloak client.
    """

    def __init__(
        self,
        server_url: str,
        client_id: str,
        client_secret_key: str,
    ):
        self.server_url = server_url
        self.client_id = client_id
        self.client_secret_key = client_secret_key

    def __call__(
        self,
        x_tenant_id: Annotated[str | None, Header()],
        credentials: HTTPAuthorizationCredentials = Depends(security),
    ):
        token = credentials.credentials
        if not token:
            logging.error("Bearer Token was not found.")
            raise HTTPException(status_code=401, detail="Unauthorized")
        try:
            oidc = KeycloakOpenID(
                server_url=self.server_url,
                client_id=self.client_id,
                realm_name=x_tenant_id,
                client_secret_key=self.client_secret_key,
            )
            token = token.replace("Bearer ", "")
            oidc.userinfo(token)
            logging.info("Successfully authorized")
        except KeycloakError as e:
            logging.error(f"Error: {e.__doc__} Status code: {e.response_code}")
            raise HTTPException(status_code=e.response_code, detail=e.__doc__)


class KeycloakPermissionCheck:
    """
    Dependency class for FastAPI. It checks the permissions of the user using keycloak.
    :param server_url: The url of the keycloak.
    :param json: The JSON to send to Keycloak
    """

    def __init__(
        self,
        server_url: str,
        json: dict,
    ):
        self.server_url = server_url
        self.json = json

    def __call__(
        self,
        x_tenant_id: Annotated[str | None, Header()],
        credentials: HTTPAuthorizationCredentials = Depends(security),
    ):
        try:
            headers = {
                "Content-Type": "application/json",
                "Accept": "*/*",
                "X-Tenant-ID": x_tenant_id,
                "Authorization": credentials.credentials,
            }
            response = requests.post(
                url=self.server_url, json=self.json, headers=headers
            )
            response.raise_for_status()
            logging.info(
                f"Successfully checked permissions. Response - {response.json()}"
            )
        except HTTPError as err:
            logging.error(
                f"Error: {err.response.json()} Status code: {err.response.status_code}"
            )
            raise HTTPException(
                status_code=err.response.status_code, detail=err.response.json()
            )
