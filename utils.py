import sys, threading, time, itertools
import pandas as pd
import json
import math








def load_dividend_events(path):
    df = pd.read_csv(path, sep=";")
    events = {}

    for _, row in df.iterrows():
        key = row["COAC_EVENT_KEY"]
        data = row.to_dict()
        del data["COAC_EVENT_KEY"]
        events[key] = data

    return events











def parse_json_output(x):
    if isinstance(x, dict):
        return x
    if not isinstance(x, str):
        try: x = str(x)
        except: return {"error": "bad_format", "raw": x}

    try: return json.loads(x)
    except: pass

    start, end = x.find("{"), x.rfind("}")
    if start != -1 and end > start:
        try: return json.loads(x[start:end+1])
        except: pass

    return {"error":"no_json", "raw":x}




def summarize_agent_output(raw):
    data = parse_json_output(raw)

    # If agent returned a "breaks" list (our use-case)
    if isinstance(data, dict) and "breaks" in data:
        if not data["breaks"]:
            return "✅ No issues detected"
        b = data["breaks"][0]  # just first break for simplicity
        kind = b.get("kind", "Unknown")
        reason = b.get("reason", b.get("why", "No reason given"))
        return f"⚠️ {kind}: {reason}"

    # If agent uses {status, kind}
    if isinstance(data, dict):
        status = data.get("status")
        kind = data.get("kind")
        reason = data.get("reason") or data.get("why")

        if status == "ok" or kind == "NONE":
            return "✅ No issues detected"
        if status == "break" or kind:
            return f"⚠️ {kind}: {reason if reason else ''}".strip()

    # Otherwise fallback
    return f"ℹ️ Raw agent output: {raw}"








def spinner(message="Working..."):
    spin = itertools.cycle(["|","/","-","\\"])
    running = True

    def animate():
        while running:
            sys.stdout.write(f"\r{message} {next(spin)}")
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write(f"\r{message}\n")
        sys.stdout.flush()

    t = threading.Thread(target=animate)
    t.start()

    def stop():
        nonlocal running
        running = False
        t.join()

    return stop











