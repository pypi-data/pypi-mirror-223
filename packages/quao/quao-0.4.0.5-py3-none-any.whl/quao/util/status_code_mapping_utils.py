from ..enum.invocation_step import InvocationStep
from ..enum.status.job_status import JobStatus
from ..enum.status.status_code import StatusCode


class StatusCodeMappingUtils:
    status_code_mapping = {
        JobStatus.ERROR: StatusCode.ERROR,
        JobStatus.DONE: StatusCode.DONE,
        JobStatus.COMPLETED: StatusCode.DONE,
        InvocationStep.PREPARATION: StatusCode.DONE,
        InvocationStep.POLLING: StatusCode.POLLING,
        InvocationStep.PROMISE: StatusCode.PROMISE,
        InvocationStep.ANALYSIS: StatusCode.DONE,
        InvocationStep.EXECUTION: StatusCode.DONE,
        InvocationStep.FINALIZATION: StatusCode.DONE
    }

    @staticmethod
    def resolve_status_code(key):
        result = StatusCodeMappingUtils.status_code_mapping.get(key)

        if result is None:
            return StatusCode.POLLING

        return result
