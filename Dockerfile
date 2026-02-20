FROM ubuntu:24.04

LABEL maintainer="Jude Tan <judetan@gmail.com>"

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -y \
  && apt-get install -y --no-install-recommends \
     python3 python3-pip python3-dev python3-venv build-essential \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN python3 -m venv /opt/venv \
  && /opt/venv/bin/pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

EXPOSE 5000
ENV PATH="/opt/venv/bin:$PATH"
CMD ["python", "app/app.py"]
