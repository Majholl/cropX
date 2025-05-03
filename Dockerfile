FROM python:3.12-slim AS builder 


RUN apt-get update && apt-get install --no-install-recommends -y \ 
    build-essential \
    pkg-config \
    gcc \ 
    && rm -rf /var/lib/apt/lists/*


WORKDIR /build

COPY requirements.txt .

RUN pip install --upgrade pip && pip wheel --wheel-dir=/wheel -r requirements.txt




FROM python:3.12-slim-bookworm AS runtime

WORKDIR /app

COPY --from=builder /wheel /wheels

COPY requirements.txt . 

RUN pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt

COPY . . 

RUN chmod +x entrypoint.sh

CMD ["./entrypoint.sh"]
