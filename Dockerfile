FROM python:3.8

ARG TWCOLLECT_VERSION

RUN pip install --upgrade pip && pip install twcollect==${TWCOLLECT_VERSION}

STOPSIGNAL SIGINT
ENTRYPOINT ["python", "-m", "twcollect"]
