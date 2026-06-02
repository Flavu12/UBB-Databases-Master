import threading
from utils import next_msg_id, log

DELTA = 2.0  # La fiecare DELTA secunde, detectorul verifică cine a răspuns.


class PerfectFailureDetector:
    """
    PerfectFailureDetector - P
    Detecteaza crash-urile nodurilor (model crash-stop).
    Implementare bazata pe heartbeat-uri periodice.
    """

    def __init__(self, node):
        self.node = node

    def init(self):
        # La început presupunem că toate celelalte noduri sunt alive
        self.alive    = set(self.node.node_ids) - {self.node.node_id}
        self.detected = set()
        self._start_timer()

    def _start_timer(self):
        # Porneste un timer care la expirare va pune un eveniment Timeout in coada de evenimente
        from event_queue import event_queue
        t = threading.Timer(DELTA, lambda: event_queue.put({"_type": "Timeout"}))
        t.daemon = True
        t.start()

    # La fiecare Timeout, verificam cine a raspuns la heartbeat-uri si cine nu
    def on_timeout(self):
        for p in self.node.node_ids:
            if p == self.node.node_id:
                continue
            
            # Daca un nod nu a raspuns si nu a fost deja detectat il consideram crash
            if p not in self.alive and p not in self.detected:
                self.detected.add(p)
                self.node.rb.on_pfd_crash(p)

            # Trimitem un heartbeat request catre fiecare nod
            self.node.pl.send(p, {
                "type": "HEARTBEATREQUEST",
                "_pl_seq": f"hbreq:{self.node.node_id}:{next_msg_id()}",
            })

        # Resetam lista de alive pentru urmatorul interval
        self.alive = set()
        # Pornim din nou timer-ul pentru urmatorul interval
        self._start_timer()

    # Cand primim un heartbeat request, raspundem cu un heartbeat reply
    def on_pl_deliver_hb_request(self, q):
        self.node.pl.send(q, {
            "type": "HEARTBEATREPLY",
            "_pl_seq": f"hbrep:{self.node.node_id}:{next_msg_id()}",
        })

    # Cand primim un heartbeat reply, il adaugam in lista de noduri alive
    def on_pl_deliver_hb_reply(self, p):
        self.alive.add(p)
        log(f"PFD: heartbeat reply from {p}, alive={self.alive}")