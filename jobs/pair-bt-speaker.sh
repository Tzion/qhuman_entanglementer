#!/bin/bash
bluetoothctl
[bluetooth]# power on
[bluetooth]# agent on
[bluetooth]# default-agent
[bluetooth]# scan on
[bluetooth]# trust 04:FE:A1:8B:4C:14 
[bluetooth]# pair 04:FE:A1:8B:4C:14
[bluetooth]# connect 04:FE:A1:8B:4C:14 
[bluetooth]# exit