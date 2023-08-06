import logging
import sys
from time import sleep
from typing import TypeVar

from kumoai.client import KumoClient
from kumoai.datamodel.jobs import (BatchPredictionJobResource,
                                   BatchPredictionOptions, JobStatus,
                                   MetadataField, PredictionArtifactType,
                                   PredictionStorageType, S3PredictionOutput,
                                   TrainingJobResource)

logging.basicConfig(format='%(asctime)s | %(levelname)s : %(message)s',
                    level=logging.INFO,
                    stream=sys.stdout)

logger = logging.getLogger(__name__)

kumo_client = KumoClient.from_env()

JobResource = TypeVar('JobResource', TrainingJobResource,
                      BatchPredictionJobResource)


def wait_job_to_complete(
    job: JobResource,
    *,
    poll_interval_seconds: float = 10.0,
    raise_if_failed: bool = True,
) -> JobResource:
    # Poll job status every 10 seconds and log job status/progress.
    while job.job_status_report.status == JobStatus.RUNNING:
        logger.info('Job status: %s', job.job_status_report)
        sleep(poll_interval_seconds)
        if isinstance(job, TrainingJobResource):
            job = kumo_client.get_training_job(job.job_id)
        elif isinstance(job, BatchPredictionJobResource):
            job = kumo_client.get_batch_prediction_job(job.job_id)

    # Check if job is successful.
    if job.job_status_report.status != JobStatus.DONE:
        if raise_if_failed:
            raise RuntimeError(f'Job did not complete successfully: {job}')
        else:
            logger.error('Job did not complete successfully: %s', job)

    return job


def run_training_job(pquery_name: str, poll_interval_seconds: float = 10.0):
    """
    This example demonstrates how to start a query (re)training job, and wait
    until it finishes by polling the job status every `poll_interval_seconds`.
    """
    # Kick off a training job.
    training_job = kumo_client.create_training_job(pquery_id=pquery_name)
    wait_job_to_complete(training_job,
                         poll_interval_seconds=poll_interval_seconds,
                         raise_if_failed=True)


def run_prediction_job(
        s3_prediction_file_path: str,
        options: BatchPredictionOptions = BatchPredictionOptions(),
        poll_interval_seconds: float = 10.0):
    """
    This example demonstrates how to start a batch prediction job, and wait
    until it finishes by polling the job status every `poll_interval_seconds`.
    """
    # Kick off a batch prediction job.
    prediction_job = kumo_client.create_batch_prediction_job(
        pquery_id='my_predictive_query',
        outputs=[
            S3PredictionOutput(
                storage_type=PredictionStorageType.S3,
                artifact_type=PredictionArtifactType.PREDICTIONS,
                file_path=s3_prediction_file_path,
                extra_fields=[
                    MetadataField.JOB_TIMESTAMP, MetadataField.ANCHOR_TIMESTAMP
                ])
        ],
        options=options,
    )

    wait_job_to_complete(prediction_job,
                         poll_interval_seconds=poll_interval_seconds,
                         raise_if_failed=True)
