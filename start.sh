#!/usr/bin/env bash
cd ~/bishe/myspiders
nohup python be_man.py lin 1 >/dev/null 2>&1 &
nohup python vy_man.py lin 1 >/dev/null 2>&1 &
nohup python monitor.py lin >/dev/null 2>&1 &