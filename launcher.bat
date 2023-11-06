@echo off
start cmd /k "mode con: cols=100 lines=100 && python main_server.py 5000"
start cmd /k "mode con: cols=100 lines=11 && python main_client.py 5001"
start cmd /k "mode con: cols=100 lines=11 && python main_client.py 5002"
start cmd /k "mode con: cols=100 lines=10 && python main_client.py 5003"
start cmd /k "mode con: cols=100 lines=11 && python main_client.py 5004"
