import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from routing.optimizer import RouteOptimizer
from routing.map_display import create_route_map, PORTS
from ships.ship import SHIPS
from weather.weather import WeatherData


def print_banner():
    print("\n" + "="*55)
    print("    🚢  OPTIMAL SHIP ROUTING SYSTEM  🌊")
    print("        Indian Ocean Region — v1.0")
    print("="*55 + "\n")


def main():
    print_banner()

    # --- Port Selection ---
    print("📍 AVAILABLE PORTS:")
    port_list = list(PORTS.keys())
    for i, port in enumerate(port_list, 1):
        coords = PORTS[port]
        print(f"   {i:2}. {port:<15} ({coords[0]:6.2f}°, {coords[1]:7.2f}°)")

    print()
    start_name = input("➡️  Enter Start Port name: ").strip().title()
    end_name   = input("🏁  Enter End Port name:   ").strip().title()

    if start_name not in PORTS:
        print(f"\n❌ '{start_name}' port not found! Choose from the above list.")
        return
    if end_name not in PORTS:
        print(f"\n❌ '{end_name}' port not found! Choose from the above list.")
        return
    if start_name == end_name:
        print("\n❌ Start and end port must be different!")
        return

    # --- Ship Selection ---
    print("\n🛳️  SHIP TYPES:")
    print("   cargo     — Cargo Vessel      (14 knots)")
    print("   tanker    — Oil Tanker         (12 knots)")
    print("   container — Container Ship     (18 knots)")
    ship_type = input("\n➡️  Enter Ship type: ").strip().lower()
    ship = SHIPS.get(ship_type, SHIPS["cargo"])
    if ship_type not in SHIPS:
        print(f"  ⚠️  '{ship_type}' not found — Cargo ship will be used")

    # --- Mode Selection ---
    print("\n⚙️  OPTIMIZATION MODE:")
    print("   time   — Fastest route (minimum time)")
    print("   safety — Safest route  (minimum risk)")
    mode = input("\n➡️  Enter Mode (time/safety): ").strip().lower()
    if mode not in ["time", "safety"]:
        mode = "time"
        print("  ⚠️  Default mode: time")

    # --- Calculation ---
    print(f"\n{'='*55}")
    print(f"  Calculating: {start_name} → {end_name}")
    print(f"  Ship: {ship.name}  |  Mode: {mode.upper()}")
    print(f"{'='*55}")

    weather = WeatherData()
    optimizer = RouteOptimizer(
        start=PORTS[start_name],
        end=PORTS[end_name],
        ship=ship,
        weather_client=weather,
        mode=mode
    )

    path, total_cost = optimizer.calculate()

    # --- Results ---
    if path:
        if mode == "time":
            eta = total_cost
            risk_score = min(round(len(path) * 0.15, 1), 9.9)
        else:
            eta = total_cost * 0.08
            risk_score = min(round(total_cost * 0.001, 1), 9.9)

        print(f"\n{'='*55}")
        print(f"  ✅ ROUTE FOUND!")
        print(f"  📍 Waypoints : {len(path)}")
        print(f"  ⏱️  ETA       : {eta:.1f} hours")
        print(f"  🛡️  Risk Score: {risk_score}/10")
        print(f"{'='*55}")

        create_route_map(path, start_name, end_name, eta, risk_score)

        print(f"\n  🗺️  Open 'route_map.html' in your browser!")
        print(f"  (File Explorer → ship-routing folder → route_map.html → double click)\n")
    else:
        print("\n❌ Route could not be calculated. Check ports.\n")


if __name__ == "__main__":
    main()