import folium

# Major ports in the Indian Ocean
PORTS = {
    "Mumbai":     (18.96,  72.82),
    "Chennai":    (13.09,  80.29),
    "Kolkata":    (22.57,  88.36),
    "Colombo":    (6.93,   79.84),
    "Singapore":  (1.26,  103.82),
    "Dubai":      (25.27,  55.30),
    "Mombasa":    (-4.05,  39.66),
    "Perth":      (-31.95,115.86),
    "Durban":     (-29.86, 31.02),
    "Chittagong": (22.33,  91.83),
}

def create_route_map(path, start_name, end_name, eta_hours, risk_score):
    """
    Creates a beautiful interactive map
    path = list of (lat, lon) points
    """

    # Map center — Indian Ocean
    m = folium.Map(
        location=[10, 75],
        zoom_start=4,
        tiles='CartoDB positron'
    )

    # --- Draw Route Line ---
    if path and len(path) > 1:
        folium.PolyLine(
            locations=path,
            color='#0057b8',
            weight=4,
            opacity=0.85,
            tooltip="Optimal Route"
        ).add_to(m)

        # Small dots for intermediate waypoints
        for i, point in enumerate(path):
            if i % 4 == 0 and 0 < i < len(path)-1:
                folium.CircleMarker(
                    location=point,
                    radius=4,
                    color='#0057b8',
                    fill=True,
                    fill_color='white',
                    fill_opacity=0.8,
                    popup=f"Waypoint {i}: {point[0]:.1f}°, {point[1]:.1f}°"
                ).add_to(m)

    # --- Start Port Marker (Green) ---
    start_coords = path[0] if path else PORTS.get(start_name, (0, 0))
    folium.Marker(
        location=start_coords,
        popup=folium.Popup(f"<b>🚢 START</b><br>{start_name}", max_width=200),
        tooltip=f"Start: {start_name}",
        icon=folium.Icon(color='green', icon='ship', prefix='fa')
    ).add_to(m)

    # --- End Port Marker (Red) ---
    end_coords = path[-1] if path else PORTS.get(end_name, (0, 0))
    folium.Marker(
        location=end_coords,
        popup=folium.Popup(
            f"<b>🏁 DESTINATION</b><br>{end_name}<br>"
            f"ETA: <b>{eta_hours:.1f} hrs</b><br>"
            f"Risk: <b>{risk_score:.1f}/10</b>",
            max_width=200
        ),
        tooltip=f"End: {end_name}",
        icon=folium.Icon(color='red', icon='flag', prefix='fa')
    ).add_to(m)

    # --- Info Box (Bottom Left) ---
    days = int(eta_hours // 24)
    hours = int(eta_hours % 24)
    time_str = f"{days}d {hours}h" if days > 0 else f"{hours}h"

    risk_color = "#28a745" if risk_score < 4 else "#ffc107" if risk_score < 7 else "#dc3545"
    risk_label = "Low" if risk_score < 4 else "Medium" if risk_score < 7 else "High"

    legend_html = f"""
    <div style="
        position: fixed; bottom: 30px; left: 30px; z-index: 1000;
        background: white; padding: 18px 22px;
        border-radius: 12px;
        border-left: 5px solid #0057b8;
        box-shadow: 0 4px 15px rgba(0,0,0,0.15);
        font-family: Arial, sans-serif; font-size: 14px;
        min-width: 200px;">
        <div style="font-size:18px; font-weight:bold; margin-bottom:10px;">
            🚢 Route Summary
        </div>
        <div>📍 <b>From:</b> {start_name}</div>
        <div>🏁 <b>To:</b> {end_name}</div>
        <div>⏱️ <b>ETA:</b> {time_str}</div>
        <div>📍 <b>Waypoints:</b> {len(path)}</div>
        <div style="margin-top:8px;">
            🛡️ <b>Risk:</b>
            <span style="
                background:{risk_color}; color:white;
                padding: 2px 10px; border-radius:10px;
                font-weight:bold;">
                {risk_label} ({risk_score:.1f}/10)
            </span>
        </div>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    # --- Save Map ---
    output_file = "route_map.html"
    m.save(output_file)
    print(f"\n  ✅ Map saved: '{output_file}'")
    return output_file