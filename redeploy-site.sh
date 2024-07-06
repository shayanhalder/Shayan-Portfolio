#!/bin/bash
tmux kill-server
cd Shayan-Portfolio
python3 -m venv python3-virtualenv
source python3-virtualenv/bin/activate
pip install -r requirements.txt
git fetch && git reset origin/main --hard 
tmux new-session -d -s portfolio
tmux send-keys -t "portfolio" "cd Shayan-Portfolio" C-m
tmux send-keys -t "portfolio" "flask run --host=0.0.0.0" C-m

