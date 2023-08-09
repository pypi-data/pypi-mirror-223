"""
    QuaO Project job_fetching_handler.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
from qiskit import QiskitError
from qiskit_ibm_provider import IBMProvider

from .handler import Handler
from ..async_tasks.post_processing_task import post_processing_task
from ..component.callback.update_job_metadata import update_job_metadata
from ..config.logging_config import logger
from ..data.callback.callback_url import CallbackUrl
from ..data.promise.post_processing_promise import PostProcessingPromise
from ..data.request.job_fetching_request import JobFetchingRequest
from ..data.response.authentication import Authentication
from ..data.response.job_response import JobResponse
from ..enum.invocation_step import InvocationStep
from ..enum.status.job_status import JobStatus
from ..util.json_parser_utils import JsonParserUtils
from ..util.response_utils import ResponseUtils
from ..config.thread_config import circuit_running_pool


class JobFetchingHandler(Handler):
    def __init__(self, request_data: dict):
        super().__init__(request_data)

    def fetch(self, post_processing):
        """
        fetch job status and result if job done fom ibm quantum

        @param post_processing: function handle job result
        @return: response for backend
        """
        # Create request
        request = JobFetchingRequest(self.request_data)

        # Get job info
        logger.info("Start get job info.")
        provider_job_id = request.provider_job_id

        # Init job response
        job_response = self.__init_job_response(request=request)

        try:
            # Fetch job from IBM
            job = self.__get_job(
                token=request.provider_authentication.get("token"),
                crn=request.provider_authentication.get("crn"),
                provider_job_id=provider_job_id,
            )
            job_status = job.status().name
            job_response.job_status = job_status

            # Check job done
            if JobStatus.DONE.value.__eq__(job_status):
                circuit_running_pool.submit(
                    self.__handle_job_result, job, request, post_processing
                )

        except Exception as exception:
            logger.debug(
                "Exception when fetch job with provider_job_id {0}: {1}".format(
                    provider_job_id, str(exception)
                )
            )

            job_response.job_result = {
                "error": "Exception when fetch job with provider_job_id {0}: {1}".format(
                    provider_job_id, str(exception)
                ),
                "exception": str(exception),
            }
            job_response.reset_job_status(JobStatus.ERROR.value)

        # Return current status
        response = ResponseUtils.generate_response(job_response)

        return response

    def __handle_job_result(self, job, request, post_processing):
        """
        Fetch job from IBM Quantum

        @return: Job status
        """
        # init job response
        job_response = self.__init_job_response(request=request)

        job_response.job_status = job.status().name
        job_result = job.result()

        self.__analyst_job_result(
            callback_url=request.analysis,
            job_response=job_response,
            job_result=job_result,
        )

        promise = PostProcessingPromise(
            callback_url=request.finalization,
            authentication=Authentication(
                user_token=request.user_token, user_identity=request.user_identity
            ),
            job_result=job_result,
        )
        post_processing_task(post_processing, promise)

    def __analyst_job_result(
        self, callback_url: CallbackUrl, job_response: JobResponse, job_result
    ):
        logger.info("Analyst result ...")
        provider_job_id = job_response.provider_job_id
        # Call to backend start analyst
        job_response.reset_invocation_step(InvocationStep.ANALYSIS)
        update_job_metadata(
            job_response=job_response, callback_url=callback_url.on_start
        )

        try:
            logger.debug("Producing histogram ....")
            job_response.job_histogram = self.__produce_histogram_data(job_result)
            logger.debug("Producing histogram completed!")

            logger.debug("Calculating execution time ....")
            job_result_parse = JsonParserUtils.parse(job_result)
            execution_time = self.__get_execution_time(job_result_parse)
            job_response.execution_time = execution_time
            logger.debug(
                "Execution time calculation was: {0} seconds".format(execution_time)
            )
            # Call to backend done analyst
            update_job_metadata(
                job_response=job_response, callback_url=callback_url.on_done
            )
        except Exception as exception:
            logger.error(
                "Exception when analyst job result with provider_job_id {0}: {1}".format(
                    provider_job_id, str(exception)
                )
            )

            job_response.job_result = {
                "error": "Exception when analyst job result with provider_job_id {0}".format(
                    provider_job_id
                ),
                "exception": str(exception),
            }
            job_response.job_status = JobStatus.ERROR.value
            # Call to backend error analyst
            update_job_metadata(
                job_response=job_response, callback_url=callback_url.on_error
            )

        logger.info("Analyst result completed!")

    @staticmethod
    def __get_job(token: str, crn: str, provider_job_id: str):

        logger.info(
            "Has IBM token: {0}".format((token is not None) and (len(token) > 0))
        )

        provider = IBMProvider(token=token, instance=crn)

        return provider.retrieve_job(job_id=provider_job_id)

    @staticmethod
    def __produce_histogram_data(job_result) -> dict:
        try:
            histogram_data = job_result.get_counts()
        except QiskitError as qiskit_error:
            logger.debug(
                "Can't produce histogram with error: {0}".format(str(qiskit_error))
            )
            histogram_data = None

        return histogram_data

    @staticmethod
    def __get_execution_time(job_result):
        if "_metadata" not in job_result:
            return None

        metadata = job_result["_metadata"]["metadata"]

        if (
            metadata is None
            or not bool(metadata)
            or "time_taken_execute" not in metadata
        ):
            return None

        return metadata["time_taken_execute"]

    @staticmethod
    def __init_job_response(request: JobFetchingRequest) -> JobResponse:
        return JobResponse(
            provider_job_id=request.provider_job_id,
            authentication=Authentication(
                user_token=request.user_token, user_identity=request.user_identity
            ),
        )
