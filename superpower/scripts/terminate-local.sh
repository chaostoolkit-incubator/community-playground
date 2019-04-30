source .venv/bin/activate

uwsgi --stop /tmp/superpower-http-router.pid
uwsgi --stop /tmp/superpower.pid
uwsgi --stop /tmp/powersource.pid
pkill --signal SIGTERM jaeger
pkill --signal SIGTERM prometheus