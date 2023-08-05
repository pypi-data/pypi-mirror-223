import logging
from functools import wraps

import requests
from flask import request
from keycloak import KeycloakOpenID
from keycloak.exceptions import KeycloakError
from requests import HTTPError


def flask_keycloak_authenticate(server_url, client_id, client_secret_key):
    """
    Method to be used as decorator, which accepts instance of KeycloakOpenID
    :param server_url: the URL of keycloak.
    :param client_id: The client_id of keycloak.
    :param client_secret_key: secret key of keycloak.
    :return: Error message | original function
    """

    def funct_decorator(org_function):
        @wraps(org_function)
        def authorize(*args, **kwargs):

            subdomain = request.headers.get('X-Tenant-Id')
            # subdomain = urlparse(request.url).hostname.split('.')[0]
            oidc = KeycloakOpenID(
                server_url=server_url,
                client_id=client_id,
                realm_name=subdomain,
                client_secret_key=client_secret_key,
            )
            token = request.headers.get("Authorization")
            if not token:
                logging.error("Bearer Token was not found.")
                return {
                    "statusCode": 401,
                    "message": "Token is missing"
                }, 401
            try:
                token = token.replace("Bearer ", "")
                oidc.userinfo(token)
                return org_function(*args, **kwargs)
            except KeycloakError as e:
                logging.error(f"Error: {e.__doc__} Status code: {e.response_code}")
                return {
                    "statusCode": e.response_code,
                    "message": e.__doc__
                }, e.response_code

        return authorize

    return funct_decorator


def flask_keycloak_permissions(url: str, json: dict):
    """
    Method to be used as decorator, which accepts instance of KeycloakOpenID
    :param url: the URL to which send a JSON and check permissions.
    :param json: The JSON that should be sent.
    :return: Error message | original function
    """

    def funct_decorator(org_function):
        @wraps(org_function)
        def permission_check(*args, **kwargs):
            try:
                headers = {
                    "Content-Type": "application/json",
                    "Accept": "*/*",
                    "X-Tenant-ID": request.headers.get("X-Tenant-ID"),
                    "Authorization": request.headers.get("Authorization")
                }
                response = requests.post(url=url, json=json, headers=headers)
                response.raise_for_status()
                logging.info(f"Successfully checked permissions. Response - {response.json()}")
                return org_function(*args, **kwargs)
            except HTTPError as err:
                logging.error(f"Error: {err.response.json()} Status code: {err.response.status_code}")
                return err.response.json(), err.response.status_code

        return permission_check

    return funct_decorator
