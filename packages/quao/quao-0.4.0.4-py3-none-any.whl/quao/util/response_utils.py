"""
    QuaO Project response_utils.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
from .job_status_mapping_utils import JobStatusMappingUtils
from .status_code_mapping_utils import StatusCodeMappingUtils
from ..data.response.job_response import JobResponse


class ResponseUtils:

    @staticmethod
    def generate_response(job_response: JobResponse) -> dict:
        if job_response:

            job_dict = {
                "providerJobId": job_response.provider_job_id,
                "jobStatus": job_response.job_status,
                "jobResult": job_response.job_result,
                "contentType": job_response.content_type.value,
                "histogram": job_response.job_histogram,
                "executionTime": job_response.execution_time
            }

            mapping_key = job_response.invocation_step \
                if JobStatusMappingUtils.resolve_job_status(job_response.job_status) is None \
                else job_response.job_status

            response = {
                "statusCode": StatusCodeMappingUtils.resolve_status_code(mapping_key).value,
                "body": job_dict,
                "userIdentity": job_response.user_identity,
                "userToken": job_response.user_token
            }

        else:
            response = {
                "statusCode": 500,
                "body": "Error in function code. Please contact the developer.",
                "userIdentity": job_response.user_identity,
                "userToken": job_response.user_token
            }

        return response
