import folium

PORTS = {
    "Mumbai":     ( 18.9,   72.8),
    "Chennai":    ( 13.0,   80.2),
    "Kolkata":    ( 22.5,   88.3),
    "Colombo":    (  6.9,   79.8),
    "Singapore":  (  1.3,  103.8),
    "Dubai":      ( 25.2,   55.2),
    "Mombasa":    ( -4.0,   39.6),
    "Perth":      (-31.9,  115.8),
    "Durban":     (-29.8,   31.0),
    "Chittagong": ( 22.3,   91.8),
}

def create_route_map(path, start_name, end_name, eta_hours, risk_score,
                     output_file="route_map.html"):
    m = folium.Map(location=[10, 75], zoom_start=3, tiles="CartoDB positron")

    if path and len(path) > 1:
        folium.PolyLine(
            locations=path, color="#0057b8", weight=4,
            opacity=0.85, tooltip="Optimal Route"
        ).add_to(m)
        for i, pt in enumerate(path):
            if 0 < i < len(path) - 1 and i % 3 == 0:
                folium.CircleMarker(
                    location=pt, radius=4, color="#0057b8",
                    fill=True, fill_color="white", fill_opacity=0.9,
                    popup=f"Waypoint {i}: {pt[0]:.1f}°, {pt[1]:.1f}°"
                ).add_to(m)

    s_coord = path[0] if path else PORTS.get(start_name, (0, 0))
    folium.Marker(
        location=s_coord, tooltip=f"START: {start_name}",
        popup=folium.Popup(f"<b>🚢 {start_name}</b>", max_width=180),
        icon=folium.Icon(color="green", icon="ship", prefix="fa")
    ).add_to(m)

    e_coord = path[-1] if path else PORTS.get(end_name, (0, 0))
    folium.Marker(
        location=e_coord, tooltip=f"END: {end_name}",
        popup=folium.Popup(
            f"<b>🏁 {end_name}</b><br>ETA: <b>{eta_hours:.1f} hrs</b><br>"
            f"Risk: <b>{risk_score:.1f}/10</b>", max_width=180),
        icon=folium.Icon(color="red", icon="flag", prefix="fa")
    ).add_to(m)

    days  = int(eta_hours // 24)
    hours = int(eta_hours % 24)
    t_str = f"{days}d {hours}h" if days else f"{hours}h"
    r_color = "#28a745" if risk_score < 4 else "#ffc107" if risk_score < 7 else "#dc3545"
    r_label = "Low" if risk_score < 4 else "Medium" if risk_score < 7 else "High"

    panel = f"""
    <div style="position:fixed;bottom:30px;left:30px;z-index:1000;
        background:white;padding:18px 22px;border-radius:12px;
        border-left:5px solid #0057b8;
        box-shadow:0 4px 15px rgba(0,0,0,0.18);
        font-family:Arial,sans-serif;font-size:14px;min-width:210px;">
      <div style="font-size:17px;font-weight:bold;margin-bottom:10px;">🚢 Route Summary</div>
      <div>📍 <b>From:</b> {start_name}</div>
      <div>🏁 <b>To:</b> {end_name}</div>
      <div>⏱️ <b>ETA:</b> {t_str}</div>
      <div>📌 <b>Stops:</b> {len(path)} waypoints</div>
      <div style="margin-top:8px;">🛡️ <b>Risk:</b>
        <span style="background:{r_color};color:white;
          padding:2px 10px;border-radius:10px;font-weight:bold;">
          {r_label} ({risk_score:.1f}/10)</span>
      </div>
    </div>"""

    m.get_root().html.add_child(folium.Element(panel))
    m.save(output_file)
    print(f"\n  ✅ Map saved → '{output_file}'")
    return output_file