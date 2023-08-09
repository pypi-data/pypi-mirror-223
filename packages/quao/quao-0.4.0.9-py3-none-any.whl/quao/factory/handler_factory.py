"""
    QuaO Project handler_factory.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
from ..handler.invocation_handler import InvocationHandler
from ..handler.job_fetching_handler import JobFetchingHandler


class HandlerFactory:
    @staticmethod
    def create_handler(event):
        request_data = event.json()
        provider_job_id = request_data.get("providerJobId")

        if provider_job_id is None:
            return InvocationHandler(request_data)
        return JobFetchingHandler(request_data)
