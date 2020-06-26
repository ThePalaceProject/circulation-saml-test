#!/bin/sh

# generate configs
/bin/confd -onetime -backend env

# start proxy foreground
exec /usr/sbin/nginx -g 'daemon off;'