import logging

from kumoai.client import KumoClient
from kumoai.datamodel.jobs import (BatchPredictionOptions, JobStatus,
                                   MetadataField, PredictionArtifactType,
                                   PredictionStorageType, S3PredictionOutput)

logger = logging.getLogger(__name__)

kumo_client = KumoClient.from_env()


def run_training_job(pquery_name: str, poll_interval_seconds: float = 10.0):
    """
    This example demonstrates how to start a query (re)training job, and wait
    until it finishes by polling the job status every `poll_interval_seconds`.
    """
    # Kick off a training job.
    training_job = kumo_client.create_training_job(pquery_id=pquery_name)
    training_job = kumo_client.wait_training_job(
        training_job.job_id, poll_interval_seconds=poll_interval_seconds)
    if training_job.job_status_report.status != JobStatus.DONE:
        raise RuntimeError(f'Training job {training_job.job_id} failed for '
                           f'query {pquery_name}')
    return training_job


def run_prediction_job(
        pquery_name: str,
        s3_prediction_file_path: str,
        options: BatchPredictionOptions = BatchPredictionOptions(),
        poll_interval_seconds: float = 10.0):
    """
    This example demonstrates how to start a batch prediction job, and wait
    until it finishes by polling the job status every `poll_interval_seconds`.
    """
    # Kick off a batch prediction job.
    prediction_job = kumo_client.create_batch_prediction_job(
        pquery_id=pquery_name,
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
    prediction_job = kumo_client.wait_batch_prediction_job(
        prediction_job.job_id, poll_interval_seconds=poll_interval_seconds)
    if prediction_job.job_status_report.status != JobStatus.DONE:
        raise RuntimeError(
            f'Batch prediction job {prediction_job.job_id} failed for '
            f'query {pquery_name}')
    return prediction_job
