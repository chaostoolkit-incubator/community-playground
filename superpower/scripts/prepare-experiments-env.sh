export SUPERPOWER_URL="http://127.0.0.1:30280/"

pip install -U chaostoolkit chaostoolkit-kubernetes

cd chaospower
../.venv/bin/python3 setup.py -q develop
cd -