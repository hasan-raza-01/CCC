FROM python:3.11-slim-bullseye
RUN apt-get update \
 && apt-get install -y --no-install-recommends gcc build-essential curl \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip uv \
 && uv pip install --system -e .
# port 8080 ---> localhost/AWS | 80 ---> AZURE
EXPOSE 8080 
CMD ["uv", "run", "app.py"]