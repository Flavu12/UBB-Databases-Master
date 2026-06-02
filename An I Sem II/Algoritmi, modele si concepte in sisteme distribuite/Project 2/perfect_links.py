class PerfectLinks:
    """
    PerfectPointToPointLinks - pl
    Garanteaza ca fiecare mesaj este livrat exact o data.
    """
 
    def __init__(self, node):
        self.node = node
        # Pentru a implementa Perfect Links, avem nevoie de Stubborn Links pentru a trimite mesajele,
        # si de o structura de date pentru a detecta mesajele duplicate.
        self.sl = node.sl
        self.delivered = set()
 
    # PerfectLinks trimite mesajul mai jos, catre StubbornLinks
    def send(self, q, m):
        self.sl.send(q, m)
 
    # Cand un mesaj este primit de la StubbornLinks, verificam daca e duplicat si apoi il urcam la stratul superior
    def on_sl_deliver(self, p, m):
        # Cream o cheie unica pentru mesaj (src + msg_id intern)
        key = (p, m.get("_pl_seq"))
        if key[1] is not None and key in self.delivered:
            return  # mesaj duplicat, ignoram
 
        if key[1] is not None:
            self.delivered.add(key)
 
        # Urmam traseul normal de livrare a mesajului catre stratul superior (Node)
        self.node.on_pl_deliver(p, m)
 