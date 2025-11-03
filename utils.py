import sys, threading, time, itertools
import pandas as pd
import json


def load_dividend_events(path):
    df = pd.read_csv(path, sep=";")
    events = {}

    for _, row in df.iterrows():
        key = row["COAC_EVENT_KEY"]
        data = row.to_dict()
        del data["COAC_EVENT_KEY"]
        events[key] = data

    return events


def write_json_file(data, agent):
    with open(f'agent_output/{agent}_output.json', 'w') as f:
        json.dump(data, f, indent=2)


def write_to_outbox(data, custodian):
    custodian = custodian.replace("/", "_")
    with open(f"custody_outbox/{custodian}_msg.txt", "a", encoding="utf-8") as f:
        f.write(f"{data.get('subject','')}\n")
        f.write(f"{data.get('body','')}\n\n")


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
