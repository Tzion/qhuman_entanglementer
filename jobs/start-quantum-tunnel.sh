#!/bin/bash
sleep 7
cd /home/zion/quanthuman-entangler && source venv_pi/bin/activate && python src/qhuman_entangler/quantum_tunnel.py >> /home/zion/quantum_tunnel.log 2>&1
