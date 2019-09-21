FROM python:3.6

# Install base dependencies
RUN apt-get update && apt-get install -y -q --no-install-recommends \
        apt-transport-https \
        build-essential \
        ca-certificates \
        curl \
        git \
        libssl-dev \
        wget \
        binutils \
        libproj-dev \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN pip install --no-cache-dir -r requirements.txt

COPY docker-entrypoint.sh /usr/src/app

COPY . /usr/src/app

EXPOSE 8000

ENTRYPOINT ["sh", "docker-entrypoint.sh"]
