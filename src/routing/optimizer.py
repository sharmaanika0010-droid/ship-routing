import numpy as np
import networkx as nx
from math import radians, cos, sin, asin, sqrt


def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return 2 * R * asin(sqrt(a))


class RouteOptimizer:
    LAT_MIN, LAT_MAX = -35, 28
    LON_MIN, LON_MAX =  32, 108
    GRID_STEP = 3

    def __init__(self, start, end, ship, weather_client, mode="time"):
        self.start   = start
        self.end     = end
        self.ship    = ship
        self.weather = weather_client
        self.mode    = mode

    def _is_ocean(self, lat, lon):
        # Indian subcontinent core only
        if 15 < lat < 23 and 73 < lon < 77:
            return False
        # Arabian Peninsula core only
        if 18 < lat < 25 and 52 < lon < 57:
            return False
        return True

    def _build_graph(self):
        print("  📐 Building ocean grid...")
        G = nx.Graph()

        lats = np.arange(self.LAT_MIN, self.LAT_MAX, self.GRID_STEP)
        lons = np.arange(self.LON_MIN, self.LON_MAX, self.GRID_STEP)

        nodes = [
            (round(float(la), 1), round(float(lo), 1))
            for la in lats for lo in lons
        ]
        G.add_nodes_from(nodes)
        print(f"  🔵 Total nodes: {len(nodes)}")

        edges = 0
        for i, n1 in enumerate(nodes):
            for n2 in nodes[i + 1:]:
                dist = haversine(n1[0], n1[1], n2[0], n2[1])
                if dist < self.GRID_STEP * 160:
                    w = self._edge_weight(n1, n2, dist)
                    if w < float("inf"):
                        G.add_edge(n1, n2, weight=w)
                        edges += 1

        print(f"  🔗 Total edges: {edges}")
        return G

    def _edge_weight(self, n1, n2, dist_km):
        mid_lat = (n1[0] + n2[0]) / 2
        mid_lon = (n1[1] + n2[1]) / 2

        if not self._is_ocean(mid_lat, mid_lon):
            return float("inf")

        wx     = self.weather.fetch(mid_lat, mid_lon)
        wave_h = wx["wave_height"]
        wind_s = wx["wind_speed"]

        if self.mode == "safety":
            if wave_h > 4.5:
                return float("inf")
            return dist_km * (1 + wave_h * 0.4 + wind_s * 0.02)
        else:
            speed_kmph = self.ship.effective_speed(wind_s, wave_h) * 1.852
            return dist_km / speed_kmph

    def _nearest_node(self, graph, point):
        nodes = list(graph.nodes)
        dists = [haversine(point[0], point[1], n[0], n[1]) for n in nodes]
        return nodes[int(np.argmin(dists))]

    def calculate(self):
        G          = self._build_graph()
        start_node = self._nearest_node(G, self.start)
        end_node   = self._nearest_node(G, self.end)

        print(f"  🟢 Start node : {start_node}")
        print(f"  🔴 End node   : {end_node}")
        print("  🧮 Running Dijkstra's algorithm...")

        try:
            path = nx.dijkstra_path(G, start_node, end_node, weight="weight")
            cost = nx.dijkstra_path_length(G, start_node, end_node, weight="weight")
            print(f"  ✅ Route found — {len(path)} waypoints")
            return path, cost
        except nx.NetworkXNoPath:
            print("  ❌ No path found!")
            return [], float("inf")