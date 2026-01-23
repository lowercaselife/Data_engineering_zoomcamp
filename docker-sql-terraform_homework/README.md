# Docker SQL Terraform Homework

This directory contains the solution and setup for the Docker, SQL, and Terraform homework. It includes a containerized pipeline to ingest NY Taxi data into a PostgreSQL database and utilities to analyze the data.

## Project Structure

- `docker-compose.yaml`: Defines the services for the project:
  - `pgdatabase`: PostgreSQL 18 database server.
  - `pgadmin`: Web-based interface for managing PostgreSQL.
  - `ingester`: A Python-based service that runs `main_pipeline.py` to ingest data.
- `Dockerfile`: Defines the image for the `ingester` service. It installs Python 3.14, `uv` for dependency management, and necessary libraries like `pandas`, `sqlalchemy`, and `pyarrow`.
- `main_pipeline.py`: The data ingestion script. It downloads Green Taxi data (Parquet) and Taxi Zone lookup data (CSV), then loads them into the Postgres database.
- `.env`: Configuration file for environment variables (Database credentials).
- `pyproject.toml` / `uv.lock`: Dependency definitions.

## Steps to set-up environment

### 1. Environment Setup

Ensure you have Docker installed.

1.  **Configure Environment Variables**:
    Create a `.env` file in this directory (if it doesn't already exist) with the following content:
    ```env
    PG_USER=postgres
    PG_PASSWORD=postgres
    PG_HOST=pgdatabase
    PG_PORT=5432
    PG_DB=ny_taxi
    ```

### 2. Build and Run Services (Question 1)

To build the images and start the services, run:

```bash
docker-compose up --build
```

This command will:

1.  Pull the `postgres:18` and `dpage/pgadmin4` images.
2.  Build the custom `ingester` image using the `Dockerfile`.
3.  Start all three services.



### 3. Data Ingestion

Once the services are up, the `ingester` container (`taxi_ingester`) will automatically start running the `main_pipeline.py` script.

- It connects to the `pgdatabase` service.
- Downloads `green_tripdata_2025-11.parquet` and `taxi_zone_lookup.csv`.
- Ingests the data into `green_taxi_trips` and `taxi_zones` tables respectively.
- You can monitor the progress in the docker-compose logs.

### 4. Accessing the Database (pgAdmin)

You can access the database using pgAdmin to run SQL queries for the homework questions.

1.  Open your browser and navigate to `http://localhost:8085`.
2.  **Login**:
    - Email: `admin@admin.com`
    - Password: `root`
3.  **Register Server**:
    - Right-click `Servers` -> `Register` -> `Server...`
    - **General** tab: Name it `NY Taxi DB`.
    - **Connection** tab:
      - Host name/address: `pgdatabase`
      - Port: `5432`
      - Maintenance database: `ny_taxi`
      - Username: `root`
      - Password: `root`
    - Click `Save`.

### 5. Running SQL Queries

1.  In pgAdmin, expand `Servers` -> `NY Taxi DB` -> `Databases` -> `ny_taxi` -> `Schemas` -> `public` -> `Tables`.
2.  You should see `green_taxi_trips` and `taxi_zones`.
3.  Right-click `ny_taxi` (or any table) and select `Query Tool`.
4.  Write/Paste your SQL queries to analyze the data (e.g., counting trips, finding max distances, grouping by zones).

### 6. Alternative: Jupyter Notebook

You can also use the local Jupyter notebooks for analysis if you prefer Python/Pandas over direct SQL in pgAdmin. Ensure your local environment has the necessary dependencies (`pandas`, `sqlalchemy`, `psycopg2-binary`) installed.
