FROM python:3-slim
WORKDIR /app/
ENV PYTHONUNBUFFERED=1 \
    APP_CONFIG=config.py
COPY . /app
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && rm -rf /var/lib/apt/lists/* \
    && pip install -r requirements.txt \
    && apt-get purge -y --auto-remove gcc
CMD ["gunicorn", \
     "--worker-class", "eventlet", \
     "--bind", ":5000", \
     "--log-level", "info", \
     "app:app"]
