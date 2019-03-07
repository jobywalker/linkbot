FROM python:3.6
ENV LOG_FILE stdout
WORKDIR /app/
ENV PYTHONUNBUFFERED 1
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN cp linkconfig_example.py linkconfig.py
CMD ["python", "linkbot.py"]