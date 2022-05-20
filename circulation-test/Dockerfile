FROM python:3.10

COPY requirements.txt /tmp
RUN pip install pip --upgrade \
  && pip install setuptools --upgrade \
  && pip install -r /tmp/requirements.txt \
  && rm /tmp/requirements.txt

ENV FLASK_APP=circulation_test/__init__.py
ENV FLASK_ENV=production
ENV FLASK_DEBUG=0

WORKDIR /app
COPY circulation_test /app/circulation_test

EXPOSE 80

CMD ["flask", "run", "--host", "0.0.0.0", "--port", "80"]