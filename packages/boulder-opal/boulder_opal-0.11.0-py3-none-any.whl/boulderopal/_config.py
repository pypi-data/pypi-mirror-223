# Copyright 2023 Q-CTRL. All rights reserved.
#
# Licensed under the Q-CTRL Terms of service (the "License"). Unauthorized
# copying or use of this file, via any medium, is strictly prohibited.
# Proprietary and confidential. You may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#    https://q-ctrl.com/terms
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS. See the
# License for the specific language.


from qctrlclient import (
    CliAuth,
    GraphQLClient,
    get_default_api_url,
    get_default_cli_auth,
)
from qctrlclient.core import (
    ApiRouter,
    CoreClientSettings,
    LocalRouter,
    Product,
)
from qctrlclient.core.utils import show_error_message
from qctrlclient.exceptions import GraphQLClientError
from qctrlclient.globals import global_value

from ._constants import INVALID_SUBSCRIPTION_ERROR


def _get_graphql_client(api_url: str, auth: CliAuth) -> GraphQLClient:
    """
    Return a `GraphQLClient` and checks the user
    has the required access for CLI usage.
    """
    client = GraphQLClient(api_url, auth=auth)

    try:
        client.check_user_role("boulder-opal-cli-access")
    except GraphQLClientError:
        show_error_message(INVALID_SUBSCRIPTION_ERROR)

    return client


def get_default_router() -> ApiRouter:
    """
    Return the default router that the Boulder Opal client uses.
    """
    client = _get_graphql_client(get_default_api_url(), auth=get_default_cli_auth())
    settings = get_config()

    return ApiRouter(client, settings)


@global_value("BOULDER_OPAL_CONFIG")
def get_config() -> CoreClientSettings:
    """
    Return the global Boulder Opal settings.
    """
    return CoreClientSettings(router=get_default_router, product=Product.BOULDER_OPAL)


def configure(**kwargs):
    """
    Update the global Boulder Opal settings. See :class:`CoreClientSettings`
    for details on which fields can be updated.
    """
    config = get_config()
    config.update(**kwargs)


def configure_api(api_url: str, oidc_url: str):
    """
    Convenience function to configure Boulder Opal for API routing.

    Parameters
    ----------
    api_url : str
        URL of the GraphQL schema.
    oidc_url : str
        Base URL of the OIDC provider, e.g. Keycloak.
    """
    client = _get_graphql_client(api_url, CliAuth(oidc_url))
    settings = get_config()

    configure(router=ApiRouter(client, settings))


def configure_local(resolver: "BaseResolver"):  # type: ignore
    """
    Convenience function to configure Boulder Opal for local routing.

    Parameters
    ----------
    resolver : BaseResolver
        A local implementation of a workflow resolver which uses
        a registry that implements all of the available Boulder Opal
        workflows.
    """
    configure(router=LocalRouter(resolver))


def configure_organization(organization_slug: str):
    """
    Convenience function to configure the organization.

    Parameters
    ----------
    organization_slug : str
        Unique slug for the organization.
    """
    configure(organization=organization_slug)
