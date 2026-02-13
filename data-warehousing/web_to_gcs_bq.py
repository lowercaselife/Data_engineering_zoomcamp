import os
import requests
import pandas as pd
from google.cloud import storage
from google.cloud import bigquery

"""
Pre-reqs: 
1. `pip install pandas pyarrow google-cloud-storage google-cloud-bigquery`
2. Set GOOGLE_APPLICATION_CREDENTIALS to your project/service-account key
3. Set GCP_GCS_BUCKET as your bucket or change default value of BUCKET
"""

BUCKET = os.environ.get("GCP_GCS_BUCKET", "ny-taxi-data-bucket-2019-2020")
DATASET = "nytaxi"


def upload_to_gcs(bucket, object_name, local_file):
    """
    Ref: https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
    """
    client = storage.Client()
    bucket = client.bucket(bucket)
    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)


def gcs_to_bigquery(year, service):
    """
    Load data from GCS to BigQuery (assumes data is already in GCS)
    Loads each month individually
    """
    client = bigquery.Client()

    for i in range(12):
        # sets the month part of the file_name string
        month = "0" + str(i + 1)
        month = month[-2:]

        # parquet file_name in GCS
        file_name = f"{service}_tripdata_{year}-{month}.parquet"
        gcs_path = f"{service}/{file_name}"
        gcs_uri = f"gs://{BUCKET}/{gcs_path}"
        table_id = f"{DATASET}.{service}_tripdata"

        # Truncate for first month (January), append for others
        write_disposition = (
            bigquery.WriteDisposition.WRITE_TRUNCATE
            if i == 0
            else bigquery.WriteDisposition.WRITE_APPEND
        )

        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.PARQUET,
            autodetect=True,
            write_disposition=write_disposition,
        )

        if write_disposition == bigquery.WriteDisposition.WRITE_APPEND:
            job_config.schema_update_options = [
                bigquery.SchemaUpdateOption.ALLOW_FIELD_RELAXATION,
                bigquery.SchemaUpdateOption.ALLOW_FIELD_ADDITION,
            ]

        load_job = client.load_table_from_uri(
            gcs_uri,
            table_id,
            job_config=job_config,
        )

        try:
            load_job.result()  # Wait for the job to complete
            print(
                f"Loaded {load_job.output_rows} rows from {file_name} into {table_id}"
            )
        except Exception as e:
            if (
                "Schema does not match" in str(e)
                and write_disposition == bigquery.WriteDisposition.WRITE_APPEND
            ):
                # If schema mismatch on append, truncate the table and retry
                print(f"Schema mismatch on {file_name}, truncating and retrying...")
                job_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE
                job_config.schema_update_options = None
                load_job = client.load_table_from_uri(
                    gcs_uri,
                    table_id,
                    job_config=job_config,
                )
                load_job.result()
                print(
                    f"Loaded {load_job.output_rows} rows from {file_name} into {table_id}"
                )
            else:
                raise


gcs_to_bigquery("2019", "green")
gcs_to_bigquery("2020", "green")
gcs_to_bigquery("2019", "yellow")
gcs_to_bigquery("2020", "yellow")
