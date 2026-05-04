import folium
import math

PORTS = {
    "Mumbai":     (18.9, 72.8),
    "Chennai":    (13.0, 80.2),
    "Kolkata":    (22.5, 88.3),
    "Colombo":    (6.9, 79.8),
    "Singapore":  (1.3, 103.8),
    "Dubai":      (25.2, 55.2),
    "Mombasa":    (-4.0, 39.6),
    "Perth":      (-31.9, 115.8),
    "Durban":     (-29.8, 31.0),
    "Chittagong": (22.3, 91.8),
}

LANDMARKS = [
    (18.9,72.8,"Mumbai","🏙️","Port","Major Indian port — Gateway of India"),
    (13.0,80.2,"Chennai","🏙️","Port","Major port on Coromandel Coast"),
    (22.5,88.3,"Kolkata","🏙️","Port","India's oldest major port"),
    (22.3,91.8,"Chittagong","🏙️","Port","Largest port in Bangladesh"),
    (15.5,73.8,"Goa","🏖️","City","Famous Indian coastal city"),
    (9.9,76.3,"Kochi","⚓","Port","Historic spice trade port, Kerala"),
    (8.5,76.9,"Thiruvananthapuram","🏙️","City","Southernmost major Indian city"),
    (6.9,79.8,"Colombo","🏙️","Port","Capital and main port of Sri Lanka"),
    (9.7,80.0,"Jaffna","🏛️","City","Northern Sri Lanka — historic city"),
    (7.9,81.0,"Trincomalee","⚓","Port","Natural deep-water harbour, Sri Lanka"),
    (25.2,55.2,"Dubai","🌆","Port","UAE — busiest port in Middle East"),
    (24.5,54.4,"Abu Dhabi","🌆","City","Capital of the UAE"),
    (23.6,58.6,"Muscat","🏙️","Port","Capital of Oman"),
    (21.5,39.2,"Jeddah","⚓","Port","Saudi Arabia — major Red Sea port"),
    (12.8,45.0,"Aden","⚓","Port","Yemen — gateway to Red Sea"),
    (11.6,43.1,"Djibouti","⚓","Port","Strategic Horn of Africa port"),
    (-4.0,39.6,"Mombasa","🏙️","Port","Kenya — largest East African port"),
    (-6.8,39.3,"Dar es Salaam","🏙️","Port","Tanzania — major port city"),
    (-11.7,43.3,"Moroni","🏝️","Island","Capital of Comoros islands"),
    (-18.9,47.5,"Antananarivo","🏙️","City","Capital of Madagascar"),
    (-25.9,32.6,"Maputo","🏙️","Port","Capital of Mozambique"),
    (-29.8,31.0,"Durban","🏙️","Port","South Africa — busiest African port"),
    (-33.9,18.4,"Cape Town","🏙️","City","South Africa — Cape of Good Hope"),
    (1.3,103.8,"Singapore","🌆","Port","World 2nd busiest container port"),
    (3.1,101.7,"Kuala Lumpur","🏙️","City","Capital of Malaysia"),
    (5.4,100.3,"Penang","🏙️","Port","Historic Malaysian port city"),
    (13.8,100.5,"Bangkok","🏙️","City","Capital of Thailand"),
    (-31.9,115.8,"Perth","🏙️","Port","Australia — Indian Ocean gateway"),
    (-20.2,57.5,"Mauritius","🏝️","Island","Volcanic island — major shipping stop"),
    (-21.1,55.5,"Reunion","🏝️","Island","French island in Indian Ocean"),
    (-4.6,55.5,"Seychelles","🏝️","Island","Archipelago of 115 islands"),
    (12.5,43.5,"Bab-el-Mandeb","🚧","Strait","Narrow strait — Red Sea to Gulf of Aden"),
    (1.2,103.5,"Strait of Malacca","🚧","Strait","World's busiest shipping lane"),
    (0.0,68.0,"Equator Crossing","📍","Equator","Crossing 0 degrees latitude"),
    (5.0,72.0,"Chagos Archipelago","🏝️","Island","British Indian Ocean Territory"),
    (-37.0,24.0,"Cape Agulhas","📍","Cape","Southernmost tip of Africa"),
    (20.0,63.0,"Arabian Sea","🌊","Sea","Monsoon weather zone"),
    (-15.0,60.0,"South Indian Ocean","🌊","Ocean","Roaring Forties — strong winds"),
    (10.0,80.0,"Bay of Bengal","🌊","Sea","Cyclone-prone sea — eastern India"),
]

def haversine_dist(lat1, lon1, lat2, lon2):
    R = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlam/2)**2
    return 2 * R * math.asin(math.sqrt(a))

def get_route_landmarks(path, radius_km=350):
    result = []
    seen = set()
    for lm in LANDMARKS:
        lm_lat, lm_lon, name, emoji, ltype, desc = lm
        best_idx = -1
        best_dist = float('inf')
        for i, (lat, lon) in enumerate(path):
            d = haversine_dist(lat, lon, lm_lat, lm_lon)
            if d < best_dist:
                best_dist = d
                best_idx = i
        if best_dist <= radius_km and name not in seen:
            seen.add(name)
            result.append({
                "wpIdx": best_idx,
                "lat": lm_lat,
                "lon": lm_lon,
                "name": name,
                "emoji": emoji,
                "type": ltype,
                "desc": desc,
                "dist": round(best_dist)
            })
    result.sort(key=lambda x: x["wpIdx"])
    return result

def create_route_map(path, start_name, end_name, eta_hours, risk_score, output_file="route_map.html"):
    m = folium.Map(location=[10, 75], zoom_start=3, tiles="CartoDB positron")

    if path and len(path) > 1:
        folium.PolyLine(locations=path, color="#0057b8", weight=4, opacity=0.85, tooltip="Optimal Route").add_to(m)

    s_coord = path[0] if path else PORTS.get(start_name, (0,0))
    e_coord = path[-1] if path else PORTS.get(end_name, (0,0))

    folium.Marker(location=s_coord, tooltip=f"START: {start_name}",
                  popup=folium.Popup(f"<b>🚢 {start_name}</b><br>Departure port", max_width=180),
                  icon=folium.Icon(color="green", icon="ship", prefix="fa")).add_to(m)

    folium.Marker(location=e_coord, tooltip=f"END: {end_name}",
                  popup=folium.Popup(f"<b>🏁 {end_name}</b><br>ETA: {eta_hours:.1f} hrs", max_width=180),
                  icon=folium.Icon(color="red", icon="flag", prefix="fa")).add_to(m)

    landmarks = get_route_landmarks(path, radius_km=350)
    landmarks = [l for l in landmarks if l["name"] != start_name and l["name"] != end_name]

    journey_items = ""
    for i, l in enumerate(landmarks, 1):
        journey_items += f"""
        <div id="ji_{i}" style="display:flex;align-items:flex-start;padding:8px 10px;border-radius:8px;margin-bottom:6px;background:#f8f9fa;border-left:3px solid #dee2e6;transition:all 0.3s;opacity:0.5;">
          <div style="font-size:18px;margin-right:10px;margin-top:2px;">{l['emoji']}</div>
          <div>
            <div style="font-weight:bold;font-size:13px;color:#1a1a2e;">{l['name']}</div>
            <div style="font-size:11px;color:#888;">{l['type']} &bull; ~{l['dist']} km</div>
            <div style="font-size:11px;color:#555;margin-top:2px;">{l['desc']}</div>
          </div>
        </div>"""

    days = int(eta_hours // 24)
    hrs = int(eta_hours % 24)
    t_str = f"{days}d {hrs}h" if days else f"{hrs}h"
    r_color = "#28a745" if risk_score < 4 else "#ffc107" if risk_score < 7 else "#dc3545"
    r_label = "Low" if risk_score < 4 else "Medium" if risk_score < 7 else "High"

    left_panel = f"""<div style="position:fixed;top:20px;left:20px;z-index:1000;background:white;border-radius:14px;box-shadow:0 4px 20px rgba(0,0,0,0.15);font-family:Arial,sans-serif;width:270px;max-height:90vh;display:flex;flex-direction:column;">
      <div style="background:#0d2b4e;color:white;padding:14px 16px;border-radius:14px 14px 0 0;">
        <div style="font-size:16px;font-weight:bold;">🚢 {start_name} → {end_name}</div>
        <div style="font-size:12px;opacity:0.8;margin-top:4px;">⏱️ ETA: {t_str} | 📌 {len(path)} waypoints | <span style="background:{r_color};padding:1px 7px;border-radius:8px;font-size:11px;font-weight:bold;">{r_label}</span></div>
      </div>
      <div style="padding:10px 14px 4px;font-size:13px;font-weight:bold;color:#0d2b4e;border-bottom:1px solid #eee;">🗺️ Places Along Route ({len(landmarks)})</div>
      <div id="journeyList" style="overflow-y:auto;padding:10px 12px;flex:1;">{journey_items}</div>
    </div>"""

    m.get_root().html.add_child(folium.Element(left_panel))
    m.save(output_file)
    return output_file