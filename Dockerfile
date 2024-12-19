FROM python:3.11-slim-buster

WORKDIR /app

COPY poetry.lock pyproject.toml ./
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi

COPY . .

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
