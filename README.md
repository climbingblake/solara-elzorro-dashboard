# solara-watertank

> sudo apt install -y mosquitto mosquitto-clients
sudo systemctl enable mosquitto.service

> python -m venv solara-env

> source ./solara-env/bin/activate

pip install -r ./requirements.txt

solara run sol.py --host 0.0.0.0
