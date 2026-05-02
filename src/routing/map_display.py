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

    # ── Route polyline ────────────────────────────────────────────────────────
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

    # ── Origin & destination markers ──────────────────────────────────────────
    s_coord = path[0]  if path else PORTS.get(start_name, (0,0))
    e_coord = path[-1] if path else PORTS.get(end_name,   (0,0))

    folium.Marker(
        location=s_coord, tooltip=f"START: {start_name}",
        popup=folium.Popup(f"<b>🚢 {start_name}</b>", max_width=180),
        icon=folium.Icon(color="green", icon="ship", prefix="fa")
    ).add_to(m)

    folium.Marker(
        location=e_coord, tooltip=f"END: {end_name}",
        popup=folium.Popup(
            f"<b>🏁 {end_name}</b><br>ETA: <b>{eta_hours:.1f} hrs</b><br>"
            f"Risk: <b>{risk_score:.1f}/10</b>", max_width=180),
        icon=folium.Icon(color="red", icon="flag", prefix="fa")
    ).add_to(m)

    # ── Route summary panel ───────────────────────────────────────────────────
    days   = int(eta_hours // 24)
    hours  = int(eta_hours % 24)
    t_str  = f"{days}d {hours}h" if days else f"{hours}h"
    r_color = "#28a745" if risk_score < 4 else "#ffc107" if risk_score < 7 else "#dc3545"
    r_label = "Low"    if risk_score < 4 else "Medium"  if risk_score < 7 else "High"

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

    # ── Animation control panel ───────────────────────────────────────────────
    anim_panel = """
    <div style="position:fixed;bottom:30px;right:30px;z-index:1000;
        background:white;padding:14px 18px;border-radius:12px;
        border-left:5px solid #28a745;
        box-shadow:0 4px 15px rgba(0,0,0,0.18);
        font-family:Arial,sans-serif;font-size:13px;min-width:180px;">
      <div style="font-size:15px;font-weight:bold;margin-bottom:10px;">
        🎬 Ship Animation
      </div>
      <button onclick="startAnimation()" id="startBtn"
        style="background:#28a745;color:white;border:none;
               padding:7px 16px;border-radius:8px;cursor:pointer;
               font-size:13px;margin-right:6px;font-weight:bold;">
        ▶ Start
      </button>
      <button onclick="resetAnimation()" id="resetBtn"
        style="background:#6c757d;color:white;border:none;
               padding:7px 16px;border-radius:8px;cursor:pointer;
               font-size:13px;font-weight:bold;">
        ↺ Reset
      </button>
      <div style="margin-top:10px;">
        Speed:
        <select id="speedSelect"
          style="padding:3px 6px;border-radius:5px;border:1px solid #ccc;">
          <option value="800">Slow</option>
          <option value="400" selected>Normal</option>
          <option value="150">Fast</option>
          <option value="50">Very Fast</option>
        </select>
      </div>
      <div id="progressText"
        style="margin-top:8px;color:#555;font-size:12px;">
        Ready to sail...
      </div>
    </div>"""
    m.get_root().html.add_child(folium.Element(anim_panel))

    # ── JavaScript animation ──────────────────────────────────────────────────
    # Build waypoints list as JS array
    waypoints_js = "[" + ",".join(
        f"[{pt[0]:.4f},{pt[1]:.4f}]" for pt in path
    ) + "]"

    animation_js = f"""
    <script>
    // Wait for Leaflet map to be ready
    document.addEventListener('DOMContentLoaded', function() {{

        var waypoints   = {waypoints_js};
        var totalPoints = waypoints.length;
        var currentIdx  = 0;
        var animTimer   = null;
        var shipMarker  = null;
        var trailLine   = null;
        var trailPoints = [];

        // Ship icon using a boat emoji rendered as a div icon
        var shipIcon = L.divIcon({{
            html: '<div style="font-size:28px;line-height:1;'
                + 'filter:drop-shadow(2px 2px 3px rgba(0,0,0,0.5));'
                + 'transform:translate(-50%,-50%);">🚢</div>',
            iconSize:   [36, 36],
            iconAnchor: [18, 18],
            className:  ''
        }});

        // Find the Leaflet map object
        function getMap() {{
            var maps = document.querySelectorAll('.folium-map');
            if (maps.length > 0) {{
                var mapId = maps[0].id;
                return window[mapId] || null;
            }}
            // Try to find map from leaflet internal registry
            for (var key in window) {{
                if (window[key] && window[key]._leaflet_id !== undefined
                    && typeof window[key].addLayer === 'function') {{
                    return window[key];
                }}
            }}
            return null;
        }}

        window.startAnimation = function() {{
            var map = getMap();
            if (!map) {{ alert('Map not ready yet — please wait a moment and try again.'); return; }}

            // Clear any existing animation
            if (animTimer) {{ clearInterval(animTimer); }}

            // Reset trail
            trailPoints = [];
            if (trailLine) {{ map.removeLayer(trailLine); trailLine = null; }}
            if (shipMarker) {{ map.removeLayer(shipMarker); shipMarker = null; }}

            currentIdx = 0;
            document.getElementById('startBtn').disabled = true;
            document.getElementById('startBtn').style.background = '#6c757d';

            // Place ship at start
            shipMarker = L.marker(waypoints[0], {{icon: shipIcon}}).addTo(map);
            trailPoints = [waypoints[0]];
            trailLine = L.polyline(trailPoints, {{
                color: '#ff6600', weight: 3,
                opacity: 0.8, dashArray: '6,4'
            }}).addTo(map);

            var speed = parseInt(document.getElementById('speedSelect').value);

            animTimer = setInterval(function() {{
                currentIdx++;
                if (currentIdx >= totalPoints) {{
                    clearInterval(animTimer);
                    animTimer = null;
                    document.getElementById('progressText').innerHTML =
                        '✅ Arrived at destination!';
                    document.getElementById('startBtn').disabled = false;
                    document.getElementById('startBtn').style.background = '#28a745';
                    return;
                }}

                var pos = waypoints[currentIdx];

                // Move ship marker
                shipMarker.setLatLng(pos);

                // Extend orange trail
                trailPoints.push(pos);
                trailLine.setLatLngs(trailPoints);

                // Pan map to follow ship
                map.panTo(pos, {{animate: true, duration: 0.5}});

                // Update progress text
                var pct = Math.round((currentIdx / (totalPoints-1)) * 100);
                document.getElementById('progressText').innerHTML =
                    '⛵ Sailing... ' + pct + '% complete';

            }}, speed);
        }};

        window.resetAnimation = function() {{
            var map = getMap();
            if (!map) return;

            if (animTimer) {{ clearInterval(animTimer); animTimer = null; }}
            if (shipMarker) {{ map.removeLayer(shipMarker); shipMarker = null; }}
            if (trailLine)  {{ map.removeLayer(trailLine);  trailLine  = null; }}

            trailPoints = [];
            currentIdx  = 0;

            document.getElementById('startBtn').disabled = false;
            document.getElementById('startBtn').style.background = '#28a745';
            document.getElementById('progressText').innerHTML = 'Ready to sail...';

            // Zoom back to full route view
            map.fitBounds(L.latLngBounds(waypoints));
        }};

    }});
    </script>"""

    m.get_root().html.add_child(folium.Element(animation_js))
    m.save(output_file)
    print(f"\n  ✅ Map with ship animation saved → '{output_file}'")
    return output_file