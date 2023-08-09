"""
    QuaO Project invocation_handler.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""

from ..component.backend.backend import Backend
from ..config.thread_config import circuit_running_pool
from ..data.request.invocation_request import InvocationRequest
from ..data.response.job_response import JobResponse
from ..enum.invocation_step import InvocationStep
from ..handler.handler import Handler
from ..util.response_utils import ResponseUtils


class InvocationHandler(Handler):
    def __init__(self, request_data: dict):
        super().__init__(request_data)

    def invoke(self, circuit_preparation_fn, post_processing_fn):
        """

        @param post_processing_fn: post processing function
        @param circuit_preparation_fn: circuit preparation function
        @return:
        """

        invocation_request = InvocationRequest(self.request_data)

        backend = Backend(invocation_request)

        circuit_running_pool.submit(backend.submit_job,
                                    circuit_preparation_fn,
                                    post_processing_fn)

        promise_response = JobResponse(authentication=backend.authentication,
                                       invocation_step=InvocationStep.PROMISE)

        return ResponseUtils.generate_response(promise_response)
