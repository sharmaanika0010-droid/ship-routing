import folium
import math

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

# ── All important places near Indian Ocean shipping lanes ─────────────────────
# Format: (lat, lon, name, type, description)
LANDMARKS = [
    # Indian ports
    ( 18.9,  72.8,  "Mumbai",          "🏙️ Port", "Major Indian port — Gateway of India"),
    ( 13.0,  80.2,  "Chennai",         "🏙️ Port", "Major Indian port on Coromandel Coast"),
    ( 22.5,  88.3,  "Kolkata",         "🏙️ Port", "India's oldest major port"),
    ( 22.3,  91.8,  "Chittagong",      "🏙️ Port", "Largest port in Bangladesh"),
    ( 15.5,  73.8,  "Goa",             "🏖️ City", "Famous Indian coastal city"),
    (  9.9,  76.3,  "Kochi",           "⚓ Port",  "Historic spice trade port — Kerala"),
    (  8.5,  76.9,  "Thiruvananthapuram","🏙️ City","Southernmost major Indian city"),

    # Sri Lanka
    (  6.9,  79.8,  "Colombo",         "🏙️ Port", "Capital and main port of Sri Lanka"),
    (  9.7,  80.0,  "Jaffna",          "🏛️ City", "Northern Sri Lanka — historic city"),
    (  7.9,  81.0,  "Trincomalee",     "⚓ Port",  "Natural deep-water harbour"),

    # Arabian Sea / Gulf region
    ( 25.2,  55.2,  "Dubai",           "🌆 Port", "UAE — busiest port in Middle East"),
    ( 24.5,  54.4,  "Abu Dhabi",       "🌆 City", "Capital of UAE"),
    ( 23.6,  58.6,  "Muscat",          "🏙️ Port", "Capital of Oman"),
    ( 12.8,  45.0,  "Aden",            "⚓ Port",  "Yemen — gateway to Red Sea"),
    ( 11.6,  43.1,  "Djibouti",        "⚓ Port",  "Strategic Horn of Africa port"),
    ( 15.6,  32.5,  "Khartoum",        "🏙️ City", "Sudan capital near Red Sea"),

    # East Africa
    ( -4.0,  39.6,  "Mombasa",         "🏙️ Port", "Kenya — largest East African port"),
    ( -6.8,  39.3,  "Dar es Salaam",   "🏙️ Port", "Tanzania — major port city"),
    (-25.9,  32.6,  "Maputo",          "🏙️ Port", "Capital of Mozambique"),
    (-29.8,  31.0,  "Durban",          "🏙️ Port", "South Africa — busiest African port"),

    # Southeast Asia
    (  1.3, 103.8,  "Singapore",       "🌆 Port", "World's 2nd busiest container port"),
    (  3.1, 101.7,  "Kuala Lumpur",    "🏙️ City", "Capital of Malaysia"),
    (  5.4, 100.3,  "Penang",          "🏙️ Port", "Historic Malaysian port city"),
    ( 13.8, 100.5,  "Bangkok",         "🏙️ City", "Capital of Thailand"),

    # Australian ports
    (-31.9, 115.8,  "Perth",           "🏙️ Port", "Australia — Indian Ocean gateway"),
    (-34.9, 138.6,  "Adelaide",        "🏙️ City", "South Australian port city"),

    # Madagascar & Islands
    (-18.9,  47.5,  "Antananarivo",    "🏙️ City", "Capital of Madagascar"),
    (-20.2,  57.5,  "Mauritius",       "🏝️ Island","Volcanic island — major shipping stop"),
    (-21.1,  55.5,  "Réunion",         "🏝️ Island","French island in Indian Ocean"),
    (-4.6,   55.5,  "Seychelles",      "🏝️ Island","Archipelago — 115 islands"),
    (-12.3,  44.3,  "Mayotte",         "🏝️ Island","French territory near Mozambique"),

    # Strategic waterways
    ( 12.5,  43.5,  "Bab-el-Mandeb",  "🚧 Strait","Narrow strait — Red Sea to Gulf of Aden"),
    (  1.2, 103.5,  "Strait of Malacca","🚧 Strait","World's busiest shipping lane"),
    ( 22.5,  59.8,  "Gulf of Oman",    "🌊 Gulf",  "Connects Arabian Sea to Persian Gulf"),
    (-34.0,  26.0,  "Cape Agulhas",    "📍 Cape",  "Southernmost tip of Africa"),
    (  0.0,  73.0,  "Equator Crossing","📍 Equator","Crossing the equator — 0° latitude"),

    # Ocean features
    (  5.0,  65.0,  "Chagos Archipelago","🏝️ Islands","British Indian Ocean Territory"),
    (-10.0,  70.0,  "Mid Indian Ocean", "🌊 Ocean", "Deep ocean — avg depth 3,800m"),
    ( 20.0,  65.0,  "Arabian Sea",     "🌊 Sea",   "Known for monsoon weather patterns"),
    (-15.0,  60.0,  "South Indian Ocean","🌊 Ocean","Roaring Forties wind zone"),
]

def haversine_dist(lat1, lon1, lat2, lon2):
    """Distance in km between two coordinates."""
    R = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi  = math.radians(lat2 - lat1)
    dlam  = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlam/2)**2
    return 2 * R * math.asin(math.sqrt(a))

def get_nearby_landmarks(path, radius_km=350):
    """
    For each waypoint in path, find all landmarks within radius_km.
    Returns list of (waypoint_index, landmark_data) — no duplicates.
    """
    found = {}   # landmark name → (waypoint_index, data)
    for i, (lat, lon) in enumerate(path):
        for lm in LANDMARKS:
            lm_lat, lm_lon, name, ltype, desc = lm
            dist = haversine_dist(lat, lon, lm_lat, lm_lon)
            if dist <= radius_km and name not in found:
                found[name] = (i, lm_lat, lm_lon, name, ltype, desc, dist)
    # Sort by waypoint index so they appear in route order
    return sorted(found.values(), key=lambda x: x[0])


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
                    popup=f"Waypoint {i}"
                ).add_to(m)

    # ── Origin & destination ──────────────────────────────────────────────────
    s_coord = path[0]  if path else PORTS.get(start_name, (0,0))
    e_coord = path[-1] if path else PORTS.get(end_name,   (0,0))

    folium.Marker(
        location=s_coord, tooltip=f"START: {start_name}",
        popup=folium.Popup(f"<b>🚢 {start_name}</b><br>Departure port", max_width=180),
        icon=folium.Icon(color="green", icon="ship", prefix="fa")
    ).add_to(m)

    folium.Marker(
        location=e_coord, tooltip=f"END: {end_name}",
        popup=folium.Popup(
            f"<b>🏁 {end_name}</b><br>ETA: <b>{eta_hours:.1f} hrs</b><br>"
            f"Risk: <b>{risk_score:.1f}/10</b>", max_width=180),
        icon=folium.Icon(color="red", icon="flag", prefix="fa")
    ).add_to(m)

    # ── Nearby landmarks along route ──────────────────────────────────────────
    nearby = get_nearby_landmarks(path, radius_km=350)
    print(f"\n  🗺️  Places found along route: {len(nearby)}")

    for (wp_idx, lm_lat, lm_lon, name, ltype, desc, dist) in nearby:
        # Skip if same as start/end port
        if name == start_name or name == end_name:
            continue

        popup_html = (
            f"<b>{ltype} {name}</b><br>"
            f"<span style='color:#555;font-size:12px;'>{desc}</span><br>"
            f"<span style='color:#0057b8;font-size:11px;'>"
            f"~{dist:.0f} km from route</span>"
        )
        folium.Marker(
            location=[lm_lat, lm_lon],
            tooltip=f"{ltype} {name}",
            popup=folium.Popup(popup_html, max_width=220),
            icon=folium.Icon(
                color="orange" if "Port" in ltype or "port" in ltype
                      else "blue" if "Island" in ltype or "Strait" in ltype
                      else "purple",
                icon="anchor"  if "Port" in ltype or "port" in ltype
                      else "info-sign",
                prefix="glyphicon"
            )
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
        font-family:Arial,sans-serif;font-size:14px;min-width:220px;">
      <div style="font-size:17px;font-weight:bold;margin-bottom:10px;">🚢 Route Summary</div>
      <div>📍 <b>From:</b> {start_name}</div>
      <div>🏁 <b>To:</b>   {end_name}</div>
      <div>⏱️ <b>ETA:</b>  {t_str}</div>
      <div>📌 <b>Stops:</b> {len(path)} waypoints</div>
      <div>🗺️ <b>Places nearby:</b> {len(nearby)} locations</div>
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
        font-family:Arial,sans-serif;font-size:13px;min-width:200px;">
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
          <option value="1200">Slow</option>
          <option value="500" selected>Normal</option>
          <option value="200">Fast</option>
          <option value="80">Very Fast</option>
        </select>
      </div>
      <div id="progressText"
        style="margin-top:8px;color:#555;font-size:12px;">
        Ready to sail...
      </div>
      <div id="nearbyInfo"
        style="margin-top:6px;color:#0057b8;font-size:12px;
               font-weight:bold;min-height:16px;">
      </div>
    </div>"""
    m.get_root().html.add_child(folium.Element(anim_panel))

    # ── Build nearby landmarks as JS array ────────────────────────────────────
    nearby_js_items = []
    for (wp_idx, lm_lat, lm_lon, name, ltype, desc, dist) in nearby:
        if name == start_name or name == end_name:
            continue
        safe_name = name.replace("'","\'")
        safe_desc = desc.replace("'","\'")
        nearby_js_items.append(
            f"{{wpIdx:{wp_idx},lat:{lm_lat},lon:{lm_lon},"
            f"name:'{safe_name}',type:'{ltype}',desc:'{safe_desc}',"
            f"dist:{dist:.0f}}}"
        )
    nearby_js = "[" + ",".join(nearby_js_items) + "]"

    waypoints_js = "[" + ",".join(
        f"[{pt[0]:.4f},{pt[1]:.4f}]" for pt in path
    ) + "]"

    # ── JavaScript: animation + place popups ──────────────────────────────────
    animation_js = f"""
    <script>
    document.addEventListener('DOMContentLoaded', function() {{

        var waypoints    = {waypoints_js};
        var nearbyPlaces = {nearby_js};
        var totalPoints  = waypoints.length;
        var currentIdx   = 0;
        var animTimer    = null;
        var shipMarker   = null;
        var trailLine    = null;
        var trailPoints  = [];
        var popupMarkers = [];
        var shownPlaces  = {{}};

        // ── Ship emoji icon ──
        var shipIcon = L.divIcon({{
            html: '<div style="font-size:30px;line-height:1;'
                + 'filter:drop-shadow(2px 2px 4px rgba(0,0,0,0.6));'
                + 'transform:translate(-50%,-50%);">🚢</div>',
            iconSize:   [38,38],
            iconAnchor: [19,19],
            className:  ''
        }});

        // ── Find Leaflet map ──
        function getMap() {{
            for (var key in window) {{
                try {{
                    if (window[key] && window[key]._leaflet_id !== undefined
                        && typeof window[key].addLayer === 'function') {{
                        return window[key];
                    }}
                }} catch(e) {{}}
            }}
            return null;
        }}

        // ── Show a place popup that fades out ──
        function showPlacePopup(map, place) {{
            var icon = L.divIcon({{
                html: '<div style="'
                    + 'background:white;'
                    + 'border:2px solid #ff8c00;'
                    + 'border-radius:10px;'
                    + 'padding:6px 10px;'
                    + 'font-family:Arial,sans-serif;'
                    + 'font-size:12px;'
                    + 'font-weight:bold;'
                    + 'box-shadow:0 3px 10px rgba(0,0,0,0.25);'
                    + 'white-space:nowrap;'
                    + 'min-width:140px;'
                    + 'text-align:center;'
                    + '">'
                    + place.type + ' ' + place.name
                    + '<br><span style="font-weight:normal;color:#555;font-size:11px;">'
                    + place.desc
                    + '</span>'
                    + '<br><span style="color:#0057b8;font-size:10px;">~'
                    + place.dist + ' km from route</span>'
                    + '</div>',
                iconSize:   [160, 70],
                iconAnchor: [80, 35],
                className:  ''
            }});

            var marker = L.marker([place.lat, place.lon], {{icon:icon}}).addTo(map);
            popupMarkers.push(marker);

            // Update side panel
            document.getElementById('nearbyInfo').innerHTML =
                '📍 Passing near: <b>' + place.name + '</b>';

            // Auto-remove popup after 3 seconds
            setTimeout(function() {{
                try {{ map.removeLayer(marker); }} catch(e) {{}}
            }}, 3000);
        }}

        // ── Start animation ──
        window.startAnimation = function() {{
            var map = getMap();
            if (!map) {{
                alert('Map not ready — please wait a second and try again.');
                return;
            }}

            // Clear previous
            if (animTimer) {{ clearInterval(animTimer); }}
            popupMarkers.forEach(function(mk) {{
                try {{ map.removeLayer(mk); }} catch(e) {{}}
            }});
            popupMarkers = [];
            trailPoints  = [];
            shownPlaces  = {{}};
            if (trailLine)   {{ map.removeLayer(trailLine);   trailLine  = null; }}
            if (shipMarker)  {{ map.removeLayer(shipMarker);  shipMarker = null; }}

            currentIdx = 0;

            document.getElementById('startBtn').disabled = true;
            document.getElementById('startBtn').style.background = '#6c757d';
            document.getElementById('nearbyInfo').innerHTML = '';

            // Place ship at start
            shipMarker  = L.marker(waypoints[0], {{icon:shipIcon}}).addTo(map);
            trailPoints = [waypoints[0]];
            trailLine   = L.polyline(trailPoints, {{
                color:'#ff6600', weight:3, opacity:0.85, dashArray:'6,4'
            }}).addTo(map);

            var speed = parseInt(document.getElementById('speedSelect').value);

            animTimer = setInterval(function() {{
                currentIdx++;
                if (currentIdx >= totalPoints) {{
                    clearInterval(animTimer);
                    animTimer = null;
                    document.getElementById('progressText').innerHTML =
                        '✅ Arrived at ' + '{end_name}' + '!';
                    document.getElementById('nearbyInfo').innerHTML =
                        '🏁 Journey complete!';
                    document.getElementById('startBtn').disabled  = false;
                    document.getElementById('startBtn').style.background = '#28a745';
                    return;
                }}

                var pos = waypoints[currentIdx];

                // Move ship
                shipMarker.setLatLng(pos);

                // Extend trail
                trailPoints.push(pos);
                trailLine.setLatLngs(trailPoints);

                // Smooth pan
                map.panTo(pos, {{animate:true, duration:0.4}});

                // Progress %
                var pct = Math.round((currentIdx / (totalPoints-1)) * 100);
                document.getElementById('progressText').innerHTML =
                    '⛵ Sailing... ' + pct + '%';

                // ── Check for nearby places ──
                nearbyPlaces.forEach(function(place) {{
                    if (shownPlaces[place.name]) return;
                    if (place.wpIdx === currentIdx ||
                        Math.abs(place.wpIdx - currentIdx) <= 1) {{
                        shownPlaces[place.name] = true;
                        showPlacePopup(map, place);
                    }}
                }});

            }}, speed);
        }};

        // ── Reset animation ──
        window.resetAnimation = function() {{
            var map = getMap();
            if (!map) return;

            if (animTimer) {{ clearInterval(animTimer); animTimer = null; }}
            popupMarkers.forEach(function(mk) {{
                try {{ map.removeLayer(mk); }} catch(e) {{}}
            }});
            popupMarkers = [];
            if (shipMarker) {{ map.removeLayer(shipMarker); shipMarker = null; }}
            if (trailLine)  {{ map.removeLayer(trailLine);  trailLine  = null; }}

            trailPoints = [];
            shownPlaces = {{}};
            currentIdx  = 0;

            document.getElementById('startBtn').disabled = false;
            document.getElementById('startBtn').style.background = '#28a745';
            document.getElementById('progressText').innerHTML = 'Ready to sail...';
            document.getElementById('nearbyInfo').innerHTML   = '';

            map.fitBounds(L.latLngBounds(waypoints));
        }};

    }});
    </script>"""

    m.get_root().html.add_child(folium.Element(animation_js))
    m.save(output_file)
    print(f"  ✅ Animated map saved → '{output_file}'")
    return output_file