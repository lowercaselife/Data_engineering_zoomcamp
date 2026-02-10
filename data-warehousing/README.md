# Data Warehousing Repository

This repository contains scripts and SQL queries for setting up a data warehouse using Google Cloud Platform (GCP) services, specifically focusing on NYC yellow taxi trip data.

## Overview

The repository demonstrates data engineering workflows including:
- Downloading data from cloud sources
- Uploading data to Google Cloud Storage (GCS)
- Creating and managing BigQuery tables with various optimization strategies

## Repository Structure

### `ingestion_script.py`
A Python script that handles the complete data ingestion pipeline:
- **Downloads** yellow taxi trip data (2024 Jan-Jun) from the NYC Taxi & Limousine Commission
- **Uploads** downloaded files to Google Cloud Storage (GCS)
- **Uses threading** for concurrent downloads and uploads (max 4 workers)
- **Includes retry logic** and verification to ensure reliable uploads
- **Supports GCS bucket creation** with automatic error handling

**Key Features:**
- Concurrent file processing with `ThreadPoolExecutor`
- Chunk-based uploads (8 MB chunks) for large files
- Upload verification after each successful transfer
- Automatic bucket creation and validation

### `sql-queries-big_query/`
A collection of SQL queries for creating and optimizing BigQuery tables:

#### External Tables
- **`external_table.sql`**: Creates an external table that references CSV files stored in GCS without importing them into BigQuery

#### Table Partitioning
- **`partitioned_table.sql`**: Demonstrates creating a partitioned table for improved query performance and cost efficiency
- **`partition_impact.sql`**: Shows the performance impact of partitioning on queries

#### Table Clustering
- **`cluster_table.sql`**: Creates a clustered table to optimize query performance based on specific columns

#### Comparison Tables
- **`non_partitioned_table.sql`**: A baseline table without partitioning for comparison
- **`public.sql`**: A public version of the table or additional table definitions

## Use Cases

This repository is useful for:
- Learning data warehousing best practices with BigQuery
- Understanding the differences between external tables, partitioned tables, and clustered tables
- Automating ETL (Extract, Transform, Load) workflows with Python and GCP
- Optimizing query performance in BigQuery

## Requirements

### Python Dependencies
- `google-cloud-storage`: For GCS interactions
- `google-api-core`: For exception handling

### GCP Setup
- Active GCP project with BigQuery enabled
- GCS bucket created
- Service account credentials file (`gcs.json`)

### Data Source
- NYC yellow taxi trip data (publicly available from NYC Taxi & Limousine Commission)

## Getting Started

1. **Configure credentials**: Ensure your `gcs.json` service account file is in the project directory
2. **Update bucket name**: Modify `BUCKET_NAME` in `ingestion_script.py` to match your GCS bucket
3. **Run the ingestion script**:
   ```bash
   python ingestion_script.py
   ```
4. **Execute SQL queries**: Use the BigQuery console or CLI to run the SQL scripts to create your tables

## Notes

- The ingestion script is configured to download 6 months of yellow taxi data (January-June 2024)
- Table optimization queries demonstrate different strategies for improving BigQuery performance
- GCS bucket validation ensures proper project ownership before uploads

## Related Course

This repository is part of the **Data Engineering Zoomcamp** curriculum, focusing on data warehousing fundamentals.
