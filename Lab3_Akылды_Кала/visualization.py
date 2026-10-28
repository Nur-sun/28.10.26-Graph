"""NetworkX + Matplotlib граф визуализациясы."""
import matplotlib.pyplot as plt
import networkx as nx

def draw_graph(city_graph, result=None, mode="distance", save_path=None):
    G = nx.Graph()
    G.add_nodes_from(city_graph.nodes)
    for a,b,d,t in city_graph.edges:
        if city_graph.edge_key(a,b) in city_graph.closed_edges:
            continue
        G.add_edge(a,b,weight=(d if mode == "distance" else t))
    pos = nx.spring_layout(G, seed=18, k=0.9)
    route = result.get("route", []) if result else []
    route_edges = list(zip(route, route[1:]))
    route_edges_set = {frozenset(e) for e in route_edges}

    plt.figure(figsize=(12,8))
    nx.draw_networkx_nodes(G,pos,node_color="#dbeafe",edgecolors="#1d4ed8",node_size=850)
    nx.draw_networkx_labels(G,pos,font_size=10,font_weight="bold")
    regular = [e for e in G.edges if frozenset(e) not in route_edges_set]
    nx.draw_networkx_edges(G,pos,edgelist=regular,width=1.5,edge_color="#94a3b8")
    if route_edges:
        nx.draw_networkx_edges(G,pos,edgelist=route_edges,width=4,edge_color="#dc2626")
    labels = { (a,b): f'{data["weight"]:g}' for a,b,data in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G,pos,edge_labels=labels,font_size=8)
    title = "Ақылды қала — ең тиімді маршрут"
    if result and result.get("total") is not None:
        title += f' | {mode}: {result["total"]:g}'
    plt.title(title, fontsize=15)
    plt.axis("off")
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=160, bbox_inches="tight")
    plt.show()
