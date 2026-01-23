from datetime import datetime as dt
import os 

_file = dt.now().strftime("%Y-%m-%d") + ".log"

def log(log: str):
    log = f"{dt.now().strftime('%Y-%m-%d %H:%M:%S')} - {log}\n"
    print(log)
    if os.path.exists('logs/') == False:
        os.makedirs('logs/')
    open(f'logs/{_file}', "a").write(log)