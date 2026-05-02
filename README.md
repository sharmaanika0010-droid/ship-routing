# Optimal Ship Routing Algorithm — Indian Ocean

A Multi-Objective Particle Swarm Optimization (MOPSO) based ship routing system  
developed for the Indian Ocean region. Optimizes voyage for **time**, **safety**, and **fuel efficiency** simultaneously.

## Project Overview

Most goods worldwide are transported by ships which rely heavily on fossil fuels.  
This project builds an intelligent routing algorithm that suggests the **optimal route** between any two ports in the Indian Ocean based on:

- **Minimum travel time**
- **Maximum weather safety** (avoids storms, high waves, strong winds)
- **Minimum fuel consumption**

The algorithm returns a **Pareto front** — a set of best possible trade-off routes — so the ship captain or company can choose based on their priority.

## Project Structure
ship-routing/
│
├── src/
│   ├── mopso_router.py       # Core MOPSO optimization engine
│   ├── objectives.py         # Objective functions (time, safety, fuel) + weather model
│   ├── constraints.py        # Land avoidance + depth constraints
│   └── visualise.py          # Map plots, Pareto front charts, GeoJSON export
│
├── tests/                    # Unit tests
│
├── main.py                   # ▶️ Entry point — run this to get optimal routes
├── requirements.txt          # Python dependencies
├── route_map.html            # Interactive HTML map of results
└── README.md                 # This file
---

## Algorithm — How It Works

We use **MOPSO (Multi-Objective Particle Swarm Optimization)**:

1. A "swarm" of particles (candidate routes) is initialized between origin and destination
2. Each particle is evaluated on 3 objectives: travel time, safety, fuel
3. Non-dominated solutions are stored in a **Pareto archive**
4. Particles move toward better solutions guided by personal best + global best
5. After 200 iterations, the archive contains the best possible routes

## Weather Model

The system uses a **WeatherGrid** that models:
- Significant wave height (metres)
- Wind speed (m/s)
- Surface ocean currents (speed + direction)
- Storm cells (Arabian Sea cyclone simulation)

> **For real deployment:** Replace synthetic grid with ERA5 (ECMWF) or CMEMS data via `WeatherGrid.from_netcdf("your_file.nc")`

---

## How to Run

### 1. Clone the repository
git clone https://github.com/sharmaanika0010-droid/ship-routing.git
cd ship-routing
### 2. Install dependencies
pip install -r requirements.txt
### 3. Run the optimizer
python main.py
### 4. Output files generated
| File | Description |
|------|-------------|
| `routes_map.png` | All Pareto routes plotted on Indian Ocean map |
| `pareto_front.png` | Trade-off scatter plots (time vs safety vs fuel) |
| `optimal_routes.geojson` | All routes in GeoJSON (open in QGIS / Google Earth) |
| `route_report.txt` | Top 5 recommended routes with stats |

---

## Sample Result (Mumbai → Mombasa)

| Rank | Travel Time | Safety Penalty | Fuel (tonnes) |
|------|-------------|----------------|---------------|
| #1 | 208 hours (8.7 days) | 0.0000 (safest) | 253 tonnes |
| #2 | 213 hours (8.9 days) | 105.56 | 243 tonnes |
| #3 | 210 hours (8.8 days) | 1.95 | 250 tonnes |

> Route #1 is the **balanced recommended route** — safest with reasonable time and fuel.

---

## Customize for Any Ship

Edit `ShipParams` in `main.py`:
ship = ShipParams(
name="Your Ship Name",
max_speed_kn=15.0,
service_speed_kn=12.0,
fuel_rate_t_per_day=28.0,
beam_m=32.0,
draft_m=10.5,
max_wave_height_m=5.0,
max_wind_speed_ms=18.0,
)
---

## Change Origin / Destination
run_optimisation(
origin=(19.0, 72.8),        # Mumbai, India
destination=(-4.0, 39.7),   # Mombasa, Kenya
)
---

## Dependencies
numpy
scipy
matplotlib
---

## Future Scope

- [ ] Real-time ERA5 / CMEMS weather data integration
- [ ] High-resolution coastline (Natural Earth 10m shapefile)
- [ ] Bathymetry constraint via GEBCO 2023
- [ ] FastAPI web service + Leaflet.js interactive map
- [ ] CO₂ emission reporting (IMO 2030 compliance)
- [ ] AIS historical voyage backtesting

---

## Author

**sharmaanika0010-droid**  
B.Tech Project — Indian Ocean Ship Routing  
Built with Python | Open Source

---

## 📄 License

This project is open source and available for academic and research use.
