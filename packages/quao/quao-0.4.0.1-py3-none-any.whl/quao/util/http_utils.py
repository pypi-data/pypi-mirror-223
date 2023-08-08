from ..enum.http_header import HttpHeader
from ..enum.token_type import TokenType


class HttpUtils:
    @staticmethod
    def create_bearer_header(token):
        return {
            HttpHeader.AUTHORIZATION.value: TokenType.BEARER.value + ' ' + token
        }
