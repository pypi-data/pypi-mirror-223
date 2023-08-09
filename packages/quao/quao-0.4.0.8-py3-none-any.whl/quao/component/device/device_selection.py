"""
    QuaO Project device_selection.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""

from json import JSONDecodeError

import requests

from ...config.logging_config import logger
from ...data.backend.backend_information import BackendInformation
from ...util.http_utils import HttpUtils


class DeviceSelection:
    def __init__(self,
                 required_qubit_number,
                 device_id,
                 user_token,
                 url):
        self.required_qubit_number = required_qubit_number
        self.device_id = device_id
        self.user_token = user_token
        self.url = url

    def select(self) -> BackendInformation:
        """

        @return: Backend information
        """

        request, header = self._prepare()

        return self._do(request, header)

    def _prepare(self):
        """

        @return: Request and header
        """

        request = {
            "deviceId": self.device_id,
            "qubitAmount": self.required_qubit_number
        }
        header = HttpUtils.create_bearer_header(self.user_token)

        logger.debug('Device selection request: {0}'.format(request))

        return request, header

    def _do(self, request: dict, header: dict):
        """

        @param request: Request
        @param header: Header
        @return:
        """

        response = requests.get(
            self.url,
            params=request,
            headers=header
        )

        if response.status_code != 200:
            return None

        try:
            response_dict = response.json().get("data")

            return BackendInformation(
                provider_tag=response_dict.get("providerTag"),
                device_name=response_dict.get("deviceName"),
                authentication=response_dict.get("authentication"))
        except JSONDecodeError:
            return None
