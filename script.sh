#!/bin/bash
sudo apt-get update && install python3
sudo apt install python3.8-venv
python3 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
python3 main.py
