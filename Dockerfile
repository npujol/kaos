FROM python:3.11

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

EXPOSE 8000
ENV PIP_NO_CACHE_DIR off

RUN apt-get update && apt-get install -y postgresql-client postgresql-contrib

RUN pip install poetry

# Install python dependencies in /.venv
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-cache

# # Create and switch to a new user
# RUN useradd --create-home appuser
# WORKDIR /home/appuser
# USER appuser

COPY . .

# Run the application
RUN ls -la
RUN mkdir static

RUN python manage.py collectstatic
# For docker-compose
# CMD [ "gunicorn", "kaos.wsgi:application", "--bind", "0.0.0.0:8000", "--reload" ]

# For minikube

COPY ./scripts /scripts
RUN chmod -R +x /scripts
ENV PATH="/scripts:/py/bin:$PATH"

EXPOSE 80

CMD ["/scripts/run.sh"]