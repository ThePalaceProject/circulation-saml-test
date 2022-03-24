FROM python:3.9

RUN apt-get update && \
  apt-get install -y wget libxmlsec1-dev libxml2-dev && \
  apt-get clean

RUN wget https://github.com/kelseyhightower/confd/releases/download/v0.11.0/confd-0.11.0-linux-amd64 -O /confd \
  && chmod +x /confd

COPY requirements.txt /tmp/
RUN pip install pip --upgrade && \
  pip install setuptools --upgrade && \
  pip install -r /tmp/requirements.txt && \
  rm /tmp/requirements.txt

WORKDIR /app
COPY run.sh /app/
COPY flask_sp /app/flask_sp

EXPOSE 80

CMD ["/bin/sh", "run.sh"]
