#!/bin/bash
#
#  Run this at boot time, this is for deployment
#
apphome=/var/www/twilio-weatherman

# I need to load my secret API key
. /home/bwilson/environ.sh

if [ ! -e /run/uwsgi/ ]; then
    mkdir -p /run/uwsgi/
fi

$apphome/pyweatherman/venv/bin/uwsgi \
    --master --pidfile=/run/uwsgi/master.pid \
    --socket=127.0.0.1:29000 \
    --processes=5 \
    --uid=www-data --gid=www-data \
    --harakiri=20 \
    --max-requests=5000 \
    --vacuum \
    --daemonize=/var/log/uwsgi/uwsgi.log \
    --chdir=$apphome/pyweatherman \
    --ini pyweatherman.ini

