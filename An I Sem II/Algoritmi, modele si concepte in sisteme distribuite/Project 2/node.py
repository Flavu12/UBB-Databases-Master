from utils import log
from stubborn_links import StubbornLinks
from perfect_links import PerfectLinks
from perfect_failure_detector import PerfectFailureDetector
from best_effort_broadcast import BestEffortBroadcast
from reliable_broadcast import ReliableBroadcast
from app import App


class Node:
    """
    Nodul Maelstrom.
    Instantiaza si conecteaza toate modulele:
        sl  -> StubbornLinks
        pl  -> PerfectLinks
        pfd -> PerfectFailureDetector
        beb -> BestEffortBroadcast
        rb  -> ReliableBroadcast
        app -> App
    """

    def __init__(self):
        self.node_id  = None
        self.node_ids = []

        self.sl  = StubbornLinks(self)
        self.pl  = PerfectLinks(self)
        self.pfd = PerfectFailureDetector(self)
        self.beb = BestEffortBroadcast(self)
        self.rb  = ReliableBroadcast(self)
        self.app = App(self)

    def init(self, node_id, node_ids):
        # Initiaza nodul cu id-ul sau si lista de noduri din cluster, apoi initializeaza toate modulele
        self.node_id  = node_id
        self.node_ids = node_ids
        log(f"Node init: id={node_id} cluster={node_ids}")
        self.rb.init()
        self.pfd.init()

    # Rutarea mesajelor PL catre modulul potrivit
    def on_pl_deliver(self, p, m):
        mtype = m.get("type", "")

        if mtype == "HEARTBEATREQUEST":
            self.pfd.on_pl_deliver_hb_request(p)

        elif mtype == "HEARTBEATREPLY":
            self.pfd.on_pl_deliver_hb_reply(p)

        elif mtype == "RB_DATA":
            self.beb.on_pl_deliver(p, m)

        elif mtype == "broadcast":
            self.app.handle_broadcast(p, m)

        elif mtype == "read":
            self.app.handle_read(p, m)

        elif mtype == "topology":
            self.app.handle_topology(p, m)

        else:
            log(f"Unhandled pl_deliver type={mtype} from={p}")