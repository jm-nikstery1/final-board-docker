FROM python:3.11.9-slim-bookworm

ENV POETRY_VERSION=1.8.2 \
   POETRY_VIRTUALENVS_CREATE=false \
   PATH="$PATH:/root/.poetry/bin" \
   DEBIAN_FRONTEND=noninteractive \
   DEBCONF_NONINTERACTIVE_SEEN=true

RUN apt-get update && apt-get -y install \
    curl gcc default-libmysqlclient-dev \
    libpq-dev python3-pip python3-dev -y

RUN pip install --upgrade pip
RUN pip install "poetry==$POETRY_VERSION" --no-cache-dir

WORKDIR /backend-django 

COPY ./backend-django /backend-django

RUN ls -la /backend-django

RUN poetry install

# Run tests and generate coverage and JUnit XML reports
RUN poetry run pytest --cov --cov-report=xml:tests/test_output_report_cov_1.xml --junit-xml=tests/test_output_report_junit_1.xml


RUN poetry run python manage.py collectstatic --no-input

WORKDIR /backend-django
EXPOSE 8000
CMD ["gunicorn", "django_backend.asgi:application", "--workers", "4", "--threads", "3", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind","0.0.0.0:8000"]
