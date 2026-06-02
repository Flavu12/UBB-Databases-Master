class BestEffortBroadcast:
    """
    BestEffortBroadcast - beb

    BEB -> PL -> SL -> Maelstrom
    Garanteaza ca fiecare mesaj este livrat cel putin o data tuturor nodurilor din cluster.
    """

    def __init__(self, node):
        self.node = node

    # Trimite mesajul m catre toate nodurile din cluster
    def broadcast(self, m):
        for q in self.node.node_ids:
            # Pentru fiecare nod q, trimitem mesajul prin PerfectLinks
            self.node.pl.send(q, m)

    # Cand un mesaj este primit de la PerfectLinks, il urcam la stratul superior (ReliableBroadcast)
    def on_pl_deliver(self, p, m):
        # p este nodul de la care a venit mesajul, m este mesajul primit
        self.node.rb.on_beb_deliver(p, m)