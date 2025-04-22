FROM python:3.11-slim

WORKDIR /app


RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    libpq-dev \
    libffi-dev \
    curl \
    git \
    python3-dev \
    libatlas-base-dev \
    libopenblas-dev \
    liblapack-dev \
    bash \
    && rm -rf /var/lib/apt/lists/*


RUN pip install --upgrade pip setuptools wheel


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .


EXPOSE 80
CMD ["uvicorn", "main:app","--host", "0.0.0.0", "--port", "80"]