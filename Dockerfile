FROM python:3-slim
WORKDIR /app/
ENV PYTHONUNBUFFERED=1 \
    APP_CONFIG=config.py
COPY . /app
RUN pip install -r requirements.txt
CMD ["gunicorn", \
     "--worker-class", "eventlet", \
     "--bind", ":5000", \
     "--log-level", "info", \
     "app:app"]
