
from ..enum.status.job_status import JobStatus


class JobStatusMappingUtils:
    job_status_mapping = {
        JobStatus.ERROR.value: JobStatus.ERROR,
        JobStatus.COMPLETED.value: JobStatus.COMPLETED,
        JobStatus.DONE.value: JobStatus.DONE.value
    }

    @staticmethod
    def resolve_job_status(job_status: str):
        return JobStatusMappingUtils.job_status_mapping.get(job_status)
