from datetime import datetime as dt
from utils.paths import LOGS_DIR

_file = dt.now().strftime("%Y-%m-%d") + ".log"

def log(log: str):
    log = f"{dt.now().strftime('%Y-%m-%d %H:%M:%S')} - {log}\n"
    print(log)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    (LOGS_DIR / _file).open("a", encoding="utf-8").write(log)