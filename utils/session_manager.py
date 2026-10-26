import json
from pathlib import Path

def save_session(path, data):
    Path(path).write_text(json.dumps(data,indent=2,default=str),encoding="utf-8")
def load_session(uploaded): return json.loads(uploaded.getvalue().decode("utf-8"))
