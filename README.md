# Optimal Ship Routing — Indian Ocean

> Graph-based ship routing system for the Indian Ocean region.  
> Optimizes voyage for **minimum time** and **maximum safety** using Dijkstra's algorithm.

---

## Project Overview

This project builds an intelligent routing system that finds the optimal route 
between any two ports in the Indian Ocean based on:

- **Minimum travel time** — fastest route considering ship speed and weather
- **Maximum weather safety** — avoids high waves and strong winds  
- **Ship-aware routing** — different results for cargo, tanker, container ships

---

## Project Structure
ship-routing/
│
├── src/
│   ├── routing/
│   │   ├── optimizer.py      # Core routing engine (Dijkstra's algorithm)
│   │   └── map_display.py    # Interactive HTML map generation (Folium)
│   ├── ships/
│   │   └── ship.py           # Ship types and speed model
│   ├── weather/
│   │   └── weather.py        # Weather data module
│   └── main.py               # Entry point
│
├── tests/
│   ├── test_routing.py       # 18 unit tests — all passing
│   └── test_optimizer.py     # Optimizer tests
│
├── docs/                     # SRS document and project reports
├── diagrams/                 # Architecture diagrams
├── notebooks/                # Demo notebooks
├── route_map.html            # Interactive output map
├── requirements.txt          # Dependencies
└── README.md
---

## Algorithm — How It Works

The system uses **Dijkstra's shortest path algorithm** on a geographic ocean grid:

1. Indian Ocean is divided into a grid of nodes (lat/lon points)
2. Nodes are connected by edges — land nodes are removed
3. Each edge weight is calculated based on:
   - **Time mode:** travel time = distance ÷ effective ship speed
   - **Safety mode:** penalty for high waves (>4.5m) and strong winds
4. Dijkstra finds the minimum-weight path from origin to destination
5. Result is displayed on an interactive Folium map

---

## Weather Model

The `WeatherData` class provides weather conditions at any ocean point:
- Significant wave height (metres)
- Wind speed (m/s)

Ship speed is reduced automatically based on weather using the drift coefficient formula:
effective_speed = max(speed - drift_coeff × (wind×0.1 + wave×0.2), speed×0.3)
---

## How to Run

### 1. Clone the repository
```bash
git clone https://github.com/sharmaanika0010-droid/ship-routing.git
cd ship-routing
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the system
```bash
python src/main.py
```

### 4. Select options when prompted
Enter Start Port: Mumbai
Enter End Port: Mombasa
Enter Ship type: cargo
Enter Mode: time
### 5. Open the map
Double-click `route_map.html` in the ship-routing folder to see the route on an interactive map.

---

## Available Ports

| Port | Country | Coordinates |
|------|---------|-------------|
| Mumbai | India | 18.9°N, 72.8°E |
| Chennai | India | 13.0°N, 80.2°E |
| Kolkata | India | 22.5°N, 88.3°E |
| Colombo | Sri Lanka | 6.9°N, 79.8°E |
| Singapore | Singapore | 1.3°N, 103.8°E |
| Dubai | UAE | 25.2°N, 55.2°E |
| Mombasa | Kenya | -4.0°N, 39.6°E |
| Perth | Australia | -31.9°N, 115.8°E |
| Durban | South Africa | -29.8°N, 31.0°E |
| Chittagong | Bangladesh | 22.3°N, 91.8°E |

---

## Ship Types

| Type | Speed | Drift Coefficient |
|------|-------|------------------|
| Cargo Vessel | 14 knots | 0.8 |
| Oil Tanker | 12 knots | 1.0 |
| Container Ship | 18 knots | 0.6 |

---

## Tests

**18 unit tests — all passing**

```bash
python -m pytest tests/test_routing.py -v
```

Tests cover: distance calculation, ship speed model, weather module, ocean/land detection, optimizer modes.

---

## Dependencies
numpy, scipy, networkx, folium, requests, flask, pandas, pytest

---

## Future Scope

- [ ] Multi-objective optimization (MOPSO) for simultaneous time + safety + fuel optimization
- [ ] Real-time ERA5 / CMEMS weather data integration
- [ ] FastAPI web service
- [ ] CO₂ emission reporting (IMO 2030 compliance)

---

## Author

**sharmaanika0010-droid**  
B.Tech Minor Project — AI with IBM  
Built with Python | Open Source
