FROM python:3.14-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/
WORKDIR /app
ENV PATH="/app/.venv/bin:$PATH"
COPY pyproject.toml uv.lock .python-version ./
RUN uv sync --frozen
COPY main_pipeline.py .
ENTRYPOINT ["python", "main_pipeline.py"]