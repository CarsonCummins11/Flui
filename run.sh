#!/bin/bash
sudo pkill python3
sudo python3 -m flask run >>log.txt 2>&1 &
