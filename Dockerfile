FROM python:3.11-slim

WORKDIR /docs

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

EXPOSE 8000
CMD ["sh", "-c", "mkdocs serve --dev-addr=0.0.0.0:${PORT:-8000}"]
