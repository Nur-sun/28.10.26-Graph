"""Графты басқару: adjacency list, тексеру және JSON сақтау."""
import json
from pathlib import Path

DEFAULT_EDGES = [
    ("A","B",4,6), ("A","C",2,3), ("B","C",1,2), ("B","D",5,7),
    ("C","E",7,8), ("C","F",4,5), ("D","E",2,3), ("D","G",6,9),
    ("E","F",1,2), ("E","H",3,4), ("F","H",5,6), ("F","I",8,10),
    ("G","H",2,3), ("G","J",7,8), ("H","I",2,3), ("H","K",6,7),
    ("I","L",4,5), ("I","M",9,11), ("J","K",1,2), ("J","N",8,10),
    ("K","L",3,4), ("K","N",5,6), ("L","M",2,3), ("L","O",7,8),
    ("M","O",3,4), ("N","O",4,5), ("B","F",9,11), ("C","H",10,12),
    ("E","K",8,9), ("G","N",6,7)
]

class CityGraph:
    def __init__(self):
        self.nodes = list("ABCDEFGHIJKLMNO")
        self.edges = []
        self.closed_edges = set()
        for a,b,d,t in DEFAULT_EDGES:
            self.add_edge(a,b,d,t)

    @staticmethod
    def edge_key(a,b):
        return tuple(sorted((a,b)))

    def add_node(self, node):
        node = str(node).strip().upper()
        if not node:
            raise ValueError("Төбе атауы бос болмауы керек.")
        if node in self.nodes:
            raise ValueError(f"{node} төбесі бұрыннан бар.")
        self.nodes.append(node)

    def remove_node(self, node):
        if node not in self.nodes:
            raise ValueError(f"{node} төбесі табылмады.")
        self.nodes.remove(node)
        self.edges = [e for e in self.edges if node not in e[:2]]
        self.closed_edges = {e for e in self.closed_edges if node not in e}

    def add_edge(self, a, b, distance, travel_time):
        a,b = str(a).strip().upper(), str(b).strip().upper()
        if a == b:
            raise ValueError("Төбе өзімен-өзі жалғанбайды.")
        if a not in self.nodes or b not in self.nodes:
            raise ValueError("Қабырға ұштары графтағы төбелер болуы керек.")
        for value, label in [(distance,"Қашықтық"),(travel_time,"Уақыт")]:
            if float(value) < 0:
                raise ValueError(f"{label} теріс болмауы керек.")
        key = self.edge_key(a,b)
        self.edges = [e for e in self.edges if self.edge_key(e[0],e[1]) != key]
        self.edges.append((a,b,float(distance),float(travel_time)))
        self.closed_edges.discard(key)

    def remove_edge(self, a, b):
        key = self.edge_key(a,b)
        before = len(self.edges)
        self.edges = [e for e in self.edges if self.edge_key(e[0],e[1]) != key]
        self.closed_edges.discard(key)
        if len(self.edges) == before:
            raise ValueError("Мұндай қабырға табылмады.")

    def set_weight(self, a, b, distance=None, travel_time=None):
        for x,y,d,t in self.edges:
            if self.edge_key(x,y) == self.edge_key(a,b):
                self.add_edge(x,y,d if distance is None else distance,
                              t if travel_time is None else travel_time)
                return
        raise ValueError("Мұндай қабырға табылмады.")

    def adjacency(self, mode="distance"):
        index = 2 if mode == "distance" else 3
        adj = {n: [] for n in self.nodes}
        for a,b,d,t in self.edges:
            if self.edge_key(a,b) in self.closed_edges:
                continue
            w = (d,t)[index-2]
            adj[a].append((b,w))
            adj[b].append((a,w))
        return adj

    def toggle_edge(self, a, b, closed=True):
        key = self.edge_key(a,b)
        if not any(self.edge_key(x,y) == key for x,y,_,_ in self.edges):
            raise ValueError("Жабылатын қабырға графта жоқ.")
        if closed:
            self.closed_edges.add(key)
        else:
            self.closed_edges.discard(key)

    def save(self, path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        data = {"nodes": self.nodes,
                "edges": [{"from":a,"to":b,"distance":d,"time":t,
                           "closed":self.edge_key(a,b) in self.closed_edges}
                          for a,b,d,t in self.edges]}
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def load(self, path):
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        self.nodes = list(data["nodes"])
        self.edges = []
        self.closed_edges = set()
        for e in data["edges"]:
            self.add_edge(e["from"],e["to"],e["distance"],e["time"])
            if e.get("closed"):
                self.closed_edges.add(self.edge_key(e["from"],e["to"]))
