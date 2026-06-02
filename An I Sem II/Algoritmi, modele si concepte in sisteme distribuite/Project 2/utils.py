import sys
import json
import threading

# Lock pentru stdout, pentru a evita amestecarea mesajelor in output
stdout_lock = threading.Lock()
# Contor global pentru generarea de msg_id unice
_msg_counter = 0
# Lock pentru contorul de msg_id, pentru a asigura thread-safety
_msg_counter_lock = threading.Lock()


def log(msg):
    # Scrie mesaje de debug pe stderr
    print(f"[DBG] {msg}", file=sys.stderr, flush=True)


def next_msg_id():
    # Generează un id unic pentru fiecare mesaj trimis
    global _msg_counter
    with _msg_counter_lock:
        _msg_counter += 1
        return _msg_counter


def send_to_network(src_id, dest, body):
    # Trimite un mesaj către Maelstrom (stdout) într-un format JSON
    msg = {"src": src_id, "dest": dest, "body": body}
    with stdout_lock:
        print(json.dumps(msg), flush=True)