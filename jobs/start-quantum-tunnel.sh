#!/bin/bash
sleep 40
source ~/.bashrc
cd /home/zion/quanthuman-entangler && source /home/zion/quanthuman-entangler/venv_pi/bin/activate && python /home/zion/quanthuman-entangler/src/qhuman_entangler/quantum_tunnel.py > /home/zion/quantum_tunnel.log 2>&1
