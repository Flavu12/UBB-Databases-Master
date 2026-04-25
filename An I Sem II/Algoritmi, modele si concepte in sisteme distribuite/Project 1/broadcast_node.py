import socket
import threading
import time
import hashlib
import os
import sys


MSG_SIZE = 1024  # mesaje de 1024 bytes
FIRST_END = 1004 # [0-1003] - 1004 bytes
SHA_OFFSET = 1004 # hash-ul incepe de la 1004 
SHA_LEN = 20 # [1004-2023] - 20 de bytes

TIMEOUT = 5
START_WAIT = 15  

# citirea fisierului de configurare 
def parse_config(path):
    nodes = {}
    with open(path, "r") as f:
        lines = f.readlines()

    N = int(lines[0].strip()) # prima linie contine numarul de broadcast-uri pe care fiecare nod le trimite 

    implicit_id = 0 # nodurile primesc automat indecsi pornind de la 0
    for line in lines[1:]:
        line = line.split("#")[0].strip()
        if not line:
            continue

        parts = line.split()
        ip = parts[0]
        port = int(parts[1])

        if len(parts) >= 3:
            node_id = int(parts[2])
        else:
            node_id = implicit_id

        implicit_id += 1
        nodes[node_id] = (ip, port)

    return N, nodes

# contruim mesajele
def build_message(my_index):
    msg = bytearray(MSG_SIZE) # creem un vector de 1024 bytes, initial 0

    # byte 0
    msg[0] = my_index

    # bytes 1..1003
    msg[1:1004] = os.urandom(1003)

    # SHA1 over 0..1003
    sha = hashlib.sha1(msg[:FIRST_END]).digest()

    # bytes 1004..1023
    msg[SHA_OFFSET:SHA_OFFSET + SHA_LEN] = sha

    return msg

# primeste un mesaj si calculeaza SHA1 pentru bytes 0..1003
def compute_sha(msg):
    return hashlib.sha1(msg[:FIRST_END]).digest()

""" 
Primeste mesaje 
sock — socketul UDP
my_index — indexul nodului curent
expected — cate mesaje trebuie sa primeasca in total
log_file — fisierul pentru mesaje OK/FAIL
err_file — fisierul pentru erori """
def receiver(sock, my_index, expected, log_file, err_file):
    received = 0
    consecutive_timeouts = 0

    while received < expected:  # primim mesaje pana la numarul asteptat(n*m)
        try:
            data, addr = sock.recvfrom(MSG_SIZE)

            if len(data) != MSG_SIZE: # verificam daca mesajul primit are 1024 bytes
                with open(err_file, "a") as ef:
                    ef.write(f"Invalid size {len(data)} from {addr}\n")
                continue

            src = data[0]
            sent_sha = data[SHA_OFFSET:SHA_OFFSET + SHA_LEN] # hash-ul trimis in mesaj, adica bytes 1004..1023
            calc_sha = compute_sha(data) # hash-ul recalculat de noi peste bytes 0..1003

            ok = sent_sha == calc_sha # daca sunt egale, mesajul este valid

            line = f"{'OK' if ok else 'FAIL'} {src} {sent_sha.hex()} {calc_sha.hex()}\n"

            with open(log_file, "a") as lf:
                lf.write(line)

            received += 1
            consecutive_timeouts = 0

        except socket.timeout: # daca timp de 5 secunde nu vine niciun mesaj, recvfrom arunca exceptie
            consecutive_timeouts += 1

            with open(err_file, "a") as ef:
                ef.write(f"Timeout... received={received}/{expected}\n")

            if consecutive_timeouts >= 5: # daca avem peste 5 timeout-uri presupunem ca nu mai vin mesaje
                with open(err_file, "a") as ef:
                    ef.write("Too many timeouts → stopping receiver\n")
                break

        except Exception as e: # daca apare orice alta eroare, o logam si oprim receiver-ul.
            with open(err_file, "a") as ef:
                ef.write(f"Receiver error: {e}\n")
            break


# trimitem mesaje 
def sender(sock, my_index, nodes, N):
    print(f"[Node {my_index}] Waiting {START_WAIT}s before sending...")
    time.sleep(START_WAIT) # asteapta 15 secunde inainte sa inceapa trimiterea

    for i in range(N):
        msg = build_message(my_index) # construim mesajul

        for nid, (ip, port) in nodes.items(): # parcurgem toate nodurile din config
            try:
                sock.sendto(msg, (ip, port)) #trimitem mesajul
                time.sleep(0.003) 
            except Exception as e:
                print(f"Send error to {nid}: {e}")

    print(f"[Node {my_index}] Done sending.")


def main():
    if len(sys.argv) != 3: 
        print("Usage: python broadcast_node.py config.txt <nodeIndex>")
        return

    config_path = sys.argv[1] 
    my_index = int(sys.argv[2]) 

    N, nodes = parse_config(config_path)

    if my_index not in nodes: # verificam daca exista nodul
        print("Invalid node index")
        return

    my_ip, my_port = nodes[my_index]

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # creem socket 
    sock.bind((my_ip, my_port)) # legam socketul de nodul curent 
    sock.settimeout(TIMEOUT)

    M = len(nodes)
    expected = N * M

    log_file = f"log_{my_index}.txt" # log pt noduri 
    err_file = f"error_{my_index}.txt" # log de erori 

    print(f"[Node {my_index}] Started on {my_ip}:{my_port}")
    print(f"Expecting {expected} messages")
    # thread pt primire 
    t_recv = threading.Thread(target=receiver, args=(sock, my_index, expected, log_file, err_file))
    # thread pt trimitere 
    t_send = threading.Thread(target=sender, args=(sock, my_index, nodes, N))
    # pornire thread-uri 
    t_recv.start()
    t_send.start()
    
    t_send.join()
    t_recv.join()

    sock.close()

    print(f"[Node {my_index}] Finished")

if __name__ == "__main__":
    main()

