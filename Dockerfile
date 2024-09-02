FROM python:3.8

ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install -y python3-dev
RUN apt-get update && apt-get install -y \
    pulseaudio \
    libpulse-dev \
    && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y alsa-utils

WORKDIR /home/projects/serenity
ADD . /home/projects/

RUN pip install -U pip
RUN pip install -r requirements.txt --default-timeout=1000

RUN getent group audio || groupadd -r audio
RUN usermod -a -G audio root

EXPOSE 8000
