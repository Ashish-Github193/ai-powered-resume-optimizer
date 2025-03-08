FROM python:3.11.11-slim-bookworm

RUN apt-get update -qqy && \
    apt-get -qqy --no-install-recommends install sudo build-essential wget && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false

RUN adduser appuser
RUN echo "appuser ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

USER appuser
WORKDIR /home/appuser

COPY --chown=appuser:appuser requirements-lock.txt requirements.txt

RUN python -m venv venv
RUN venv/bin/pip install pip wheel setuptools --upgrade
RUN venv/bin/pip install -r requirements.txt && rm -rf ~/.cache/pip

COPY --chown=appuser:appuser resume_opt resume_opt
COPY --chown=appuser:appuser entrypoints/server-entrypoint.sh ./

RUN chmod +x server-entrypoint.sh

EXPOSE 5000

ENTRYPOINT ["./server-entrypoint.sh"]
