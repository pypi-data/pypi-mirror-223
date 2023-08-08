from ..enum.http_header import HttpHeader
from ..enum.media_type import MediaType
from ..enum.token_type import TokenType


class HttpUtils:
    @staticmethod
    def create_bearer_header(token):
        return {
            HttpHeader.AUTHORIZATION.value: TokenType.BEARER.value + ' ' + token
        }

    @staticmethod
    def create_application_json_header(token):
        return {
            HttpHeader.AUTHORIZATION.value: TokenType.BEARER.value + ' ' + token,
            HttpHeader.CONTENT_TYPE.value: MediaType.APPLICATION_JSON.value,
            HttpHeader.ACCEPT.value: MediaType.APPLICATION_JSON.value
        }
