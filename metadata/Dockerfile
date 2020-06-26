FROM busybox

ENV CONFD_VERSION="0.11.0" \
    CONFD_URL="https://github.com/kelseyhightower/confd/releases/download"

RUN wget -T 5 ${CONFD_URL}/v${CONFD_VERSION}/confd-${CONFD_VERSION}-linux-amd64 -O /bin/confd \
  && chmod +x /bin/confd

COPY confd /etc/confd
COPY run.sh /run.sh

CMD ["/bin/sh", "/run.sh"]