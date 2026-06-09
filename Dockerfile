FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    make \
    gcc \
    nauty \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

COPY requirements.txt .
RUN pip install --no-cache-dir -r ./requirements.txt

COPY . .
RUN pip install --no-cache-dir --editable "./python[dev]"

CMD ["tail", "-f", "/dev/null"]
