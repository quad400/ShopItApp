FROM python:3.11.1-slim

COPY . /app
WORKDIR /app


RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install pip --upgrade && \
    /opt/venv/bin/pip install -r /app/requirements.txt

RUN chmod +x entrypoint.sh

CMD [ "/app/entrypoint.sh" ]