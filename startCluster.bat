@echo off
start cmd /k "python .\node.py -id 1 -cfg /config/cluster.cfg"
start cmd /k "python .\node.py -id 2 -cfg /config/cluster.cfg"
start cmd /k "python .\node.py -id 3 -cfg /config/cluster.cfg"