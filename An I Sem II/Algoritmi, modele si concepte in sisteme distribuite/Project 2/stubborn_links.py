from utils import send_to_network, next_msg_id


class StubbornLinks:
    """
    StubbornPointToPointLinks - sl
    Garanteaza ca fiecare mesaj este livrat cel putin o data."""

    def __init__(self, node):
        self.node = node

    def send(self, q, m):
        # Trimite mesajul m catre procesul q

        body = dict(m)
        body.setdefault("msg_id", next_msg_id())
        send_to_network(self.node.node_id, q, body)

    def on_deliver(self, p, m):
        #Cand un mesaj este primit de la procesul p, il urcam la stratul Perfect Links
        self.node.pl.on_sl_deliver(p, m)