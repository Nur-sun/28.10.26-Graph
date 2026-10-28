"""Дейкстра алгоритмі: shortest_path/dijkstra дайын функцияларын қолданбаймыз."""
import heapq
from time import perf_counter

def dijkstra(graph, start, finish=None, mode="distance"):
    if mode not in ("distance", "time"):
        raise ValueError("Режим distance немесе time болуы керек.")
    if start not in graph.nodes:
        raise ValueError(f"Бастапқы төбе табылмады: {start}")
    if finish is not None and finish not in graph.nodes:
        raise ValueError(f"Соңғы төбе табылмады: {finish}")

    started = perf_counter()
    adj = graph.adjacency(mode)
    dist = {node: float("inf") for node in graph.nodes}
    previous = {node: None for node in graph.nodes}
    dist[start] = 0
    queue = [(0, start)]
    visited_order = []
    visited = set()

    while queue:
        current_dist, u = heapq.heappop(queue)
        if u in visited:
            continue
        visited.add(u)
        visited_order.append(u)
        if finish is not None and u == finish:
            break
        for v, weight in adj[u]:
            candidate = current_dist + weight
            if candidate < dist[v]:
                dist[v] = candidate
                previous[v] = u
                heapq.heappush(queue, (candidate, v))

    route = []
    if finish is not None and dist[finish] != float("inf"):
        node = finish
        while node is not None:
            route.append(node)
            node = previous[node]
        route.reverse()
    elapsed = (perf_counter() - started) * 1000
    return {"distances": dist, "previous": previous, "route": route,
            "total": None if finish is None or dist[finish] == float("inf") else dist[finish],
            "visited_order": visited_order, "visited_count": len(visited_order),
            "elapsed_ms": elapsed}
