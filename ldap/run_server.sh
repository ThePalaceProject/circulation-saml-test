#!/bin/bash
#
# Register default environment
#
export HOSTNAME=${HOSTNAME:-$(hostname --fqdn)}

export LDAP_SUFFIX=${LDAP_SUFFIX:-"dc=idptestbed"}
export LDAP_ADMIN_USERNAME=${LDAP_ADMIN_USERNAME:-"admin"}
export LDAP_ADMIN_PASSWORD=${LDAP_ADMIN_PASSWORD:-${LDAP_MANAGER_PASSWORD:-"admin"}}
export LDAP_MANAGER_PASSWORD=${LDAP_MANAGER_PASSWORD:-${LDAP_ADMIN_PASSWORD:-"admin"}}

#
# housekeeping variables
#
BASEDIR="/etc/dirsrv/slapd-dir"
LOGDIR="/var/log/dirsrv/slapd-dir"
LOCKDIR="/var/lock/dirsrv/slapd-dir"
RUNDIR="/var/run/dirsrv/"
ROOT_DN="cn=Directory Manager"

#
# Setup Directory instance
#
setup_dirsrv() {
    /bin/cp -rp /etc/dirsrv-tmpl/* /etc/dirsrv

    echo 'Applying configuration'
    /sbin/setup-ds.pl -s -f /389ds-setup.inf --debug
}

#
# Load initial data and configuration
#
init_config() {
    # need slapd running to import data and load initial data and configuration
    ns-slapd -D $BASEDIR && sleep 30

    echo 'Adding users' > /tmp/log

    ldapadd -x -D"$ROOT_DN" -w${LDAP_MANAGER_PASSWORD} -f /init-users.ldif
    pkill -f ns-slapd && sleep 30
}

#
# Make sure lock and run directories are avaiable if recreating container with existing instance setup
#
if [ ! -d ${LOCKDIR} ]; then
    mkdir -p ${RUNDIR} && chown -R nobody:nobody ${RUNDIR}
    mkdir -p ${LOCKDIR} && chown -R nobody:nobody ${LOCKDIR}
fi

#
# Setup instance if not already setup
#
if [ ! -d ${BASEDIR} ]; then
    echo "Server hasn't been configured yet, starting the initialization phase"

    # generate configuration and setup instance
    /confd -onetime -backend env
    setup_dirsrv
    init_config
else
    echo "Server has already been configured, skipping the initialization phase"
fi


# remove stray lockfiles
rm -f /var/lock/dirsrv/slapd-dir/server/*

exec /usr/sbin/ns-slapd -D ${BASEDIR} -d 16384


