from utils import next_msg_id, log


class ReliableBroadcast:
    """
    ReliableBroadcast - rb
    Algorithm 3.2: Lazy Reliable Broadcast
    Garanteaza ca daca un mesaj este broadcast de un proces corect, atunci
    fiecare proces corect va livra acel mesaj cel putin o data.
    
    """

    def __init__(self, node):
        self.node = node

    def init(self):
        self.delivered = set()        # set de rb_msg_id
        self.forward   = set()        # set de (s, rb_msg_id, value)
        self.correct   = set(self.node.node_ids)

    # Aplicatia apeleaza aceasta functie pentru a face RB Broadcast
    def broadcast(self, value):
        # Generam un id unic pentru mesajul RB 
        rb_msg_id = f"{self.node.node_id}:{next_msg_id()}"
        log(f"RB Broadcast value={value} id={rb_msg_id}")

        # trimitem mesajul catre toate nodurile folosind BEB
        self.node.beb.broadcast({
            "type": "RB_DATA",
            "s": self.node.node_id,
            "rb_msg_id": rb_msg_id,
            "value": value,
            "_pl_seq": f"rbdata:{rb_msg_id}",
        })

    # Primim un mesaj de la BEB, trebuie sa verificam daca l-am mai livrat
    def on_beb_deliver(self, p, m):
        s         = m["s"]
        rb_msg_id = m["rb_msg_id"]
        value     = m["value"]

        # Daca mesajul a fost deja livrat, il ignoram
        if rb_msg_id in self.delivered:
            return

        self.delivered.add(rb_msg_id)
        self.node.app.on_rb_deliver(s, value)

        # Daca mesajul a venit de la un nod care nu e in setul de corecti, il re-broadcastam
        if p not in self.correct:
            self.node.beb.broadcast({
                "type": "RB_DATA",
                "s": s,
                "rb_msg_id": rb_msg_id,
                "value": value,
                "_pl_seq": f"rbdata:fwd:{rb_msg_id}:{next_msg_id()}",
            })
        else:
            # Daca mesajul a venit de la un nod corect, il adaugam in setul de forward pentru cazul in care acel nod va fi detectat ca fiind crash
            self.forward.add((s, rb_msg_id, value))

    # Daca un nod este detectat ca fiind crash, trebuie sa re-broadcastam toate mesajele pe care le-am primit de la acel nod
    def on_pfd_crash(self, p):
        self.correct.discard(p)
        log(f"PFD Crash: {p}, re-broadcasting forward set")

        # Pentru fiecare mesaj din setul de forward, daca sursa mesajului este nodul care a fost detectat ca fiind crash, atunci re-broadcastam mesajul folosind BEB
        for (s, rb_msg_id, value) in list(self.forward):
            if s == p:
                self.node.beb.broadcast({
                    "type": "RB_DATA",
                    "s": s,
                    "rb_msg_id": rb_msg_id,
                    "value": value,
                    "_pl_seq": f"rbdata:crash:{rb_msg_id}:{next_msg_id()}",
                })