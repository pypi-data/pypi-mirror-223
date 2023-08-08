import base64
from typing import Optional

from urllib3 import Retry

from invision_client import ApiClient, Configuration
from invision_client.api.forums_api import ForumsApi
from invision_client.api.members_api import MembersApi
from invision_client.api.topics_api import TopicsApi

__all__ = ["get_api_client", "InvisionApi"]


def get_api_client(api_key, server_url=None, retries=None, verify_ssl=True, ssl_ca_cert=None):
    if api_key is None or api_key == "":
        raise KeyError('Please provide the api_key parameter')
    config = Configuration().get_default_copy()
    if server_url:
        config.host = server_url
    if retries:
        config.retries = retries
    token_bytes = base64.b64encode(api_key.encode('ascii'))
    token = token_bytes.decode()
    config.verify_ssl = verify_ssl
    if verify_ssl and ssl_ca_cert is not None:
        config.ssl_ca_cert = ssl_ca_cert
    return ApiClient(config, header_name="Authorization", header_value=f"Basic {token}")


class InvisionApi:
    """
    InvisionApi is a wrapper class around the invision library that provides access to all Rest API end points.
    """

    def __init__(
            self,
            api_key: str,
            server_url: Optional[str] = None,
            verify_ssl: Optional[bool] = True,
            retries: Optional[Retry] = None,
    ):
        self.client = get_api_client(api_key, server_url, retries, verify_ssl)
        self.apis = {MembersApi.__name__: MembersApi(self.client),
                     ForumsApi.__name__: ForumsApi(self.client),
                     TopicsApi.__name__: TopicsApi(self.client)}

    @property
    def members_api(self) -> MembersApi:
        return self.apis.get(MembersApi.__name__)

    @property
    def forums_api(self) -> ForumsApi:
        return self.apis.get(ForumsApi.__name__)

    @property
    def topics_api(self) -> TopicsApi:
        return self.apis.get(TopicsApi.__name__)
