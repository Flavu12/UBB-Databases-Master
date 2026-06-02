from utils import log


class App:
    """
    Aplicatia - nivelul cel mai de sus.
    Gestioneaza mesajele de la clientii Maelstrom si apeleaza rb.broadcast.
    """

    def __init__(self, node):
        self.node   = node
        self.values = set()  # valorile livrate de RB (pentru read)

    # Cand RB livreaza un mesaj, il adaugam in setul de valori livrate
    def on_rb_deliver(self, s, value):
        log(f"APP rb-deliver from={s} value={value}")
        self.values.add(value)

    # Cand primim un mesaj de tip broadcast, raspundem cu broadcast_ok si apoi apelam rb.broadcast pentru a incepe algoritmul de Reliable Broadcast
    def handle_broadcast(self, src, body):
        value = body["message"]
        self.node.pl.send(src, {
            "type": "broadcast_ok",
            "in_reply_to": body.get("msg_id"),
        })
        self.node.rb.broadcast(value)
    
    # Returneaza toate valorile livrate până acum
    def handle_read(self, src, body):
        # Cand primim un mesaj de tip read, raspundem cu read_ok si lista de valori livrate pana in acel moment

        self.node.pl.send(src, {
            "type": "read_ok",
            "in_reply_to": body.get("msg_id"),
            "messages": list(self.values),
        })

    # Cand primim un mesaj de tip topology
    def handle_topology(self, src, body):
        self.node.pl.send(src, {
            "type": "topology_ok",
            "in_reply_to": body.get("msg_id"),
        })