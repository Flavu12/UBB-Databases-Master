#!/usr/bin/env python3
"""
Reliable Broadcast (Algorithm 3.2) - Jepsen Maelstrom
Entrypoint principal.

Ruleaza cu:
    chmod +x main.py
    ./maelstrom test -w broadcast --bin main.py --node-count 3 --time-limit 20 --rate 10 --log-stderr
"""

import sys
import json
import threading

from event_queue import event_queue
from node import Node
from utils import log, next_msg_id


node = Node()


def process_event(event):
    etype = event.get("_type")

    if etype == "network_message":
        msg   = event["msg"]
        src   = msg["src"]
        body  = msg["body"]
        mtype = body.get("type", "")

        if mtype == "init":
            node.init(body["node_id"], body["node_ids"])
            node.pl.send(src, {
                "type": "init_ok",
                "in_reply_to": body.get("msg_id"),
            })
        else:
            # Toate celelalte mesaje intra prin sl -> pl -> modul potrivit
            node.sl.on_deliver(src, body)

    elif etype == "Timeout":
        if node.node_id is not None:
            node.pfd.on_timeout()


def event_processor():
    """Proceseaza evenimentele din coada serial (un singur thread)."""
    while True:
        event = event_queue.get()
        try:
            process_event(event)
        except Exception as e:
            log(f"Event processor error: {e}")
        finally:
            event_queue.task_done()


def main():
    # Pornim event processor thread
    ep = threading.Thread(target=event_processor, daemon=True)
    ep.start()

    # Main thread: citeste din STDIN si pune in event_queue
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
            event_queue.put({"_type": "network_message", "msg": msg})
        except json.JSONDecodeError as e:
            log(f"JSON error: {e}")


if __name__ == "__main__":
    main()