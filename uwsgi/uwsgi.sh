#!/bin/bash
#
#  Run this at boot time
#
apphome=/var/lib/twilio-weatherman
uwsgihome=$home/uwsgi

. $apphome/pyweatherman/venv/bin/activate
. /home/bwilson/environ.sh

if [ ! -e /run/uwsgi/ ]; then
    mkdir -p /run/uwsgi/
fi

uwsgi \
    --vhost=true \
    --master --pidfile=/run/uwsgi/master.pid \
    --socket=127.0.0.1:29000 \
    --processes=5 \
    --uid=www-data --gid=www-data \
    --harakiri=20 \
    --max-requests=5000 \
    --vacuum \
    --init $apphome/pyweatherman.ini \

    #--daemonize=/var/log/uwsgi/uwsgi.log

