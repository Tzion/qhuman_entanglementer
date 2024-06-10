#!/bin/bash

while true
do
    sleep 10
    echo "connect 04:FE:A1:8B:4C:14" | bluetoothctl
    cd /home/zion/quanthuman-entangler 
    source /home/zion/quanthuman-entangler/venv_pi/bin/activate 
    python /home/zion/quanthuman-entangler/src/qhuman_entangler/quantum_tunnel.py &
    pid=$!
    sleep 9220
    kill -9 $pid
done
