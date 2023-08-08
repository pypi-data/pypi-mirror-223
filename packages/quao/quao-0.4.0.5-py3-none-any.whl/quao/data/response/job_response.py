"""
    QuaO Project job_response.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
from .authentication import Authentication
from ...enum.invocation_step import InvocationStep
from ...enum.media_type import MediaType
from ...enum.status.job_status import JobStatus


class JobResponse(object):
    def __init__(
            self,
            provider_job_id: str = "",
            job_status: str = None,
            invocation_step: InvocationStep = None,
            job_result: dict = None,
            content_type: MediaType = MediaType.ALL_TYPE,
            authentication: Authentication = None,
            job_histogram: dict = None,
            execution_time: float = None
    ):
        self.provider_job_id = provider_job_id
        self.job_status = job_status
        self.job_result = job_result
        self.content_type = content_type
        self.job_histogram = job_histogram
        self.user_identity = authentication.user_identity
        self.user_token = authentication.user_token
        self.execution_time = execution_time
        self.invocation_step = invocation_step

    def reset_invocation_step(self, invocation_step: InvocationStep):
        self.job_status = None
        self.invocation_step = invocation_step

    def reset_job_status(self, job_status: str):
        self.invocation_step = None
        self.job_status = job_status

