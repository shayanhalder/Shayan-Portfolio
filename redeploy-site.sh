#!/bin/bash
cd Shayan-Portfolio
python3 -m venv python3-virtualenv
source python3-virtualenv/bin/activate
pip install -r requirements.txt
git fetch && git reset origin/main --hard 
systemctl daemon-reload
systemctl restart myportfolio
systemctl status myportfolio
