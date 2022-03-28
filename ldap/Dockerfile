FROM centos:7
MAINTAINER michel4j@gmail.com

RUN yum -y install 389-ds-base.x86_64 openldap-clients \
  curl hostname procps-ng openssl nss-tools coreutils && \
  yum clean all

RUN curl -qL https://github.com/kelseyhightower/confd/releases/download/v0.11.0/confd-0.11.0-linux-amd64 -o /confd && \
  chmod +x /confd

COPY confd /etc/confd

VOLUME ["/etc/dirsrv", "/var/lib/dirsrv", "/var/log/dirsrv", "/certs"]

# The 389-ds setup will fail because the hostname can't reliable be determined,
# so we'll bypass it and then install.
RUN sed -i 's/checkHostname {/checkHostname {\nreturn();/g' /usr/lib64/dirsrv/perl/DSUtil.pm

# Disable SELINUX
RUN rm -fr /usr/lib/systemd/system && \
  sed -i 's/updateSelinuxPolicy($inf);//g' /usr/lib64/dirsrv/perl/* && \
  sed -i '/if (@errs = startServer($inf))/,/}/d' /usr/lib64/dirsrv/perl/*

# Move config to temporary location until volume is ready
RUN mkdir /etc/dirsrv-tmpl && mv /etc/dirsrv/* /etc/dirsrv-tmpl

EXPOSE 389 636

# supervisord
RUN yum install -y python python-setuptools && \
  curl -o "get-pip.py" https://bootstrap.pypa.io/pip/2.7/get-pip.py && python get-pip.py && \
  pip install supervisor
RUN mkdir -p /etc/supervisor
COPY supervisord.conf /etc/supervisor/supervisord.conf

COPY run_server.sh /run_server.sh
COPY start.sh /start.sh
COPY dirsrv-dir /etc/systemctl/dirsrv-dir

CMD ["/start.sh"]
