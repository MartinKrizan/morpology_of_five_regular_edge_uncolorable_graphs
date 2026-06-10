FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    cmake \
    g++ \
    git \
    make \
    gcc \
    nauty \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

COPY requirements.txt .
RUN pip install --no-cache-dir -r ./requirements.txt
RUN pip install -e ./python
RUN alias geng=nauty-geng

CMD ["tail", "-f", "/dev/null"]
