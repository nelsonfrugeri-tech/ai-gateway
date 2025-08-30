FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

COPY src/ src/

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DD_CALL_BASIC_CONFIG False

EXPOSE 8080

CMD ["ddtrace-run", "python", "src/api/app.py"]