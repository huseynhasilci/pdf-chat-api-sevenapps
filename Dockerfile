FROM python:3.11-alpine3.20

COPY ./requirements.txt /tmp/requirements.txt
COPY . /fastApiProject
WORKDIR /fastApiProject

RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    build-base \
    python3-dev \
    py3-pip

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install --no-cache-dir -r /tmp/requirements.txt && \
    rm -rf /tmp

ENV PATH="/py/bin:$PATH"

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]