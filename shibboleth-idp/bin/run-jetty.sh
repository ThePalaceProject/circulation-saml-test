#!/bin/sh

#set -x

export JAVA_HOME=/opt/jre-home
export PATH=$PATH:$JAVA_HOME/bin

# Wait until metadata is built
sleep 30

cp -R /opt/shibboleth-idp/confd /etc/confd
/confd -onetime -backend env

sed -i "s/^-Xmx.*$/-Xmx$JETTY_MAX_HEAP/g" /opt/shib-jetty-base/start.ini

exec /opt/jetty-home/bin/jetty.sh run
