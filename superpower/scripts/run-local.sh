source .venv/bin/activate

uwsgi --chdir superpower \
    --socket /tmp/superpower.sock \
    --processes 2 \
    --master \
    --module app:app \
    --pidfile /tmp/superpower.pid \
    --static-map /public=../superpower-static \
    --daemonize /tmp/superpower.log

uwsgi --chdir superpower \
    --master \
    --http 0.0.0.0:30280 \
    --http-to /tmp/superpower.sock \
    --pidfile /tmp/superpower-http-router.pid \
    --daemonize /tmp/superpower-http-router.log

uwsgi --chdir powersource \
    --http 0.0.0.0:6061 \
    --processes 2 \
    --master \
    --module app:app \
    --pidfile /tmp/powersource.pid \
    --daemonize /tmp/powersource.log

jaeger-all-in-one --collector.zipkin.http-port=9411 > /tmp/jaeger.log 2>&1  &
prometheus --config.file=./scripts/prometheus.yml > /tmp/prometheus.log 2>&1 &
