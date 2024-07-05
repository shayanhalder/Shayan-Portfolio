#!/bin/bash
tmux kill-server
cd Shayan-Portfolio
git fetch && git reset origin/main --hard
source python3-virtualenv/bin/activate
pip install -r requirements.txt
tmux new
flask run --host=0.0.0.0 -p 80