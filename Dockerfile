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

# install dependencies before copying project so docker cache can be utilized
COPY python/pyproject.toml ./python/pyproject.toml
COPY scripts/install_python_deps.py ./scripts/install_python_deps.py
RUN python ./scripts/install_python_deps.py

# copy and install python project
COPY python ./python
RUN python -m pip install --no-deps -e ./python

RUN ln -s /usr/bin/nauty-geng /usr/local/bin/geng
RUN ln -s /usr/bin/nauty-multig /usr/local/bin/multig

CMD ["tail", "-f", "/dev/null"]
