import numpy as np
import networkx as nx
from math import radians, cos, sin, asin, sqrt


def haversine(lat1, lon1, lat2, lon2):
    """
    Calculates distance (in km) between two points
    Earth is round, so simple formulas won't work
    """
    R = 6371  # Earth radius in km
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return 2 * R * asin(sqrt(a))


class RouteOptimizer:
    # Indian Ocean boundaries
    LAT_MIN, LAT_MAX = -35, 28
    LON_MIN, LON_MAX = 32, 108
    GRID_STEP = 8   

    def __init__(self, start, end, ship, weather_client, mode="time"):
        self.start = start          # (lat, lon) tuple
        self.end = end              # (lat, lon) tuple
        self.ship = ship            # Ship object
        self.weather = weather_client
        self.mode = mode            # "time" or "safety"

    def _build_graph(self):
        """
        Build an ocean grid
        Each grid point is a node
        Edges connect nearby nodes
        """
        print("  📐 Building ocean grid...")
        G = nx.Graph()

        lats = np.arange(self.LAT_MIN, self.LAT_MAX, self.GRID_STEP)
        lons = np.arange(self.LON_MIN, self.LON_MAX, self.GRID_STEP)

        # Create all nodes
        nodes = []
        for lat in lats:
            for lon in lons:
                node = (round(float(lat), 1), round(float(lon), 1))
                nodes.append(node)
                G.add_node(node)

        print(f"  🔵 Total nodes: {len(nodes)}")

        # Connect nearby nodes
        edge_count = 0
        for i, n1 in enumerate(nodes):
            for n2 in nodes[i + 1:]:
                dist = haversine(n1[0], n1[1], n2[0], n2[1])
                if dist < self.GRID_STEP * 160:  # Connect only nearby nodes
                    weight = self._edge_weight(n1, n2, dist)
                    if weight < float('inf'):
                        G.add_edge(n1, n2, weight=weight)
                        edge_count += 1

        print(f"  🔗 Total edges: {edge_count}")
        return G

    def _edge_weight(self, n1, n2, dist_km):
        """
        Calculate the 'cost' between two nodes
        In time mode: how much time it will take
        In safety mode: how risky it is
        """
        mid_lat = (n1[0] + n2[0]) / 2
        mid_lon = (n1[1] + n2[1]) / 2

        # Avoid land
        if not self._is_ocean(mid_lat, mid_lon):
            return float('inf')  # This path is impossible

        # Fetch weather data
        weather = self.weather.fetch(mid_lat, mid_lon)
        wave_h = weather["wave_height"]
        wind_s = weather["wind_speed"]

        if self.mode == "safety":
            # Increase weight in rough weather
            if wave_h > 4.5:
                return float('inf')  # Very dangerous — block path
            risk_factor = 1 + (wave_h * 0.4) + (wind_s * 0.02)
            return dist_km * risk_factor

        else:  # time mode
            speed_knots = self.ship.effective_speed(wind_s, wave_h)
            speed_kmph = speed_knots * 1.852
            time_hours = dist_km / speed_kmph
            return time_hours

    def _is_ocean(self, lat, lon):
        """
        Rough land check — avoid Indian subcontinent and nearby land
        """
        # Indian subcontinent
        if lat > 8 and lat < 28 and lon > 68 and lon < 80:
            return False
        # Sri Lanka area
        if lat > 5 and lat < 10 and lon > 79 and lon < 82:
            return False
        # Arabian peninsula
        if lat > 12 and lat < 26 and lon > 44 and lon < 60:
            return False
        return True

    def _nearest_node(self, graph, point):
        """Find the nearest graph node to any given point"""
        nodes = list(graph.nodes)
        distances = [haversine(point[0], point[1], n[0], n[1]) for n in nodes]
        return nodes[int(np.argmin(distances))]

    def calculate(self):
        """Main function — calculate the route"""
        G = self._build_graph()

        start_node = self._nearest_node(G, self.start)
        end_node = self._nearest_node(G, self.end)

        print(f"  🟢 Start node: {start_node}")
        print(f"  🔴 End node:   {end_node}")
        print(f"  🧮 Running Dijkstra's algorithm...")

        try:
            path = nx.dijkstra_path(G, start_node, end_node, weight='weight')
            cost = nx.dijkstra_path_length(G, start_node, end_node, weight='weight')
            print(f"  ✅ Route found! Waypoints: {len(path)}")
            return path, cost
        except nx.NetworkXNoPath:
            print("  ❌ No path found!")
            return [], float('inf')