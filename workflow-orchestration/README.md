# Workflow Orchestration with Kestra

This repository contains Kestra workflows designed to demonstrate workflow orchestration concepts, focusing on ETL (Extract, Transform, Load) and ELT (Extract, Load, Transform) patterns using both Postgres and Google Cloud Platform (GCP).

## Overview

- **ETL vs ELT**: The included flows illustrate the difference between ETL (where data is transformed before loading into the destination) and ELT (where data is loaded first, then transformed within the destination system).
- **Postgres & GCP**: Workflows are provided for both Postgres and Google Cloud Platform, showing how orchestration can be adapted to different data platforms.

## Repository Structure

- `02-workflow-orchestration/flows/` - Contains Kestra YAML workflow definitions for various ETL/ELT pipelines.
- `output_metrics.py` - Example Python script for metrics or data processing.
- `docker-compose.yaml` - For local orchestration and service setup.
- `gcp_scheduled.yaml`, `gcp_taxi.yaml`, `03-scheduled-orchestration.yaml` - Example Kestra workflow files for GCP and scheduling.

## Setup Instructions

### 1. Prerequisites

- [Docker](https://www.docker.com/) installed (for local orchestration)
- [Kestra](https://kestra.io/) (can be run via Docker Compose)
- Access to a Postgres instance (local or cloud)
- Google Cloud Platform project and service account (for GCP workflows)

### 2. Running Kestra Locally

1. Clone this repository:
   ```sh
   git clone <repo-url>
   cd workflow-orchestration
   ```
2. Start Kestra and dependencies:
   ```sh
   docker-compose up -d
   ```
3. Access the Kestra UI at [http://localhost:8080](http://localhost:8080)

### 3. Setting Up Postgres Workflows

- Ensure your Postgres instance is running and accessible.
- Update the connection details in the relevant workflow YAML files under `02-workflow-orchestration/flows/`.

### 4. Setting Up GCP Workflows

- Create a Google Cloud service account with the necessary permissions.
- Download the service account key JSON file.
- **Kestra KV Setup:**
  - In the Kestra UI, navigate to the Key/Value (KV) store.
  - Add your GCP service account key as a secret (e.g., `gcp_service_account`).
  - Reference this key in your workflow YAMLs using Kestra's secret syntax.

## Notes

- All sensitive credentials (such as GCP service keys) should be managed via Kestra's KV store and never hardcoded in workflow files.
- See individual workflow YAML files for specific configuration details and parameters.

## References

- [Kestra Documentation](https://kestra.io/docs/)
- [Google Cloud Platform](https://cloud.google.com/)
- [PostgreSQL](https://www.postgresql.org/)
