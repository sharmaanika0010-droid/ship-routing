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

LANDMARKS = [
    ( 18.9,  72.8, "Mumbai",             "🏙️", "Port",    "Major Indian port — Gateway of India"),
    ( 13.0,  80.2, "Chennai",            "🏙️", "Port",    "Major port on Coromandel Coast"),
    ( 22.5,  88.3, "Kolkata",            "🏙️", "Port",    "India's oldest major port"),
    ( 22.3,  91.8, "Chittagong",         "🏙️", "Port",    "Largest port in Bangladesh"),
    ( 15.5,  73.8, "Goa",               "🏖️", "City",    "Famous Indian coastal city"),
    (  9.9,  76.3, "Kochi",             "⚓",  "Port",    "Historic spice trade port, Kerala"),
    (  8.5,  76.9, "Thiruvananthapuram","🏙️", "City",    "Southernmost major Indian city"),
    (  6.9,  79.8, "Colombo",           "🏙️", "Port",    "Capital and main port of Sri Lanka"),
    (  9.7,  80.0, "Jaffna",            "🏛️", "City",    "Northern Sri Lanka — historic city"),
    (  7.9,  81.0, "Trincomalee",       "⚓",  "Port",    "Natural deep-water harbour, Sri Lanka"),
    ( 25.2,  55.2, "Dubai",             "🌆", "Port",    "UAE — busiest port in Middle East"),
    ( 24.5,  54.4, "Abu Dhabi",         "🌆", "City",    "Capital of the UAE"),
    ( 23.6,  58.6, "Muscat",            "🏙️", "Port",    "Capital of Oman"),
    ( 21.5,  39.2, "Jeddah",            "⚓",  "Port",    "Saudi Arabia — major Red Sea port"),
    ( 12.8,  45.0, "Aden",             "⚓",  "Port",    "Yemen — gateway to Red Sea"),
    ( 11.6,  43.1, "Djibouti",          "⚓",  "Port",    "Strategic Horn of Africa port"),
    ( -4.0,  39.6, "Mombasa",           "🏙️", "Port",    "Kenya — largest East African port"),
    ( -6.8,  39.3, "Dar es Salaam",     "🏙️", "Port",    "Tanzania — major port city"),
    (-11.7,  43.3, "Moroni",            "🏝️", "Island",  "Capital of Comoros islands"),
    (-18.9,  47.5, "Antananarivo",      "🏙️", "City",    "Capital of Madagascar"),
    (-20.2,  57.5, "Mauritius",         "🏝️", "Island",  "Volcanic island — major shipping stop"),
    (-21.1,  55.5, "Reunion",           "🏝️", "Island",  "French island in Indian Ocean"),
    (-25.9,  32.6, "Maputo",            "🏙️", "Port",    "Capital of Mozambique"),
    (-29.8,  31.0, "Durban",            "🏙️", "Port",    "South Africa — busiest African port"),
    (-33.9,  18.4, "Cape Town",         "🏙️", "City",    "South Africa — Cape of Good Hope"),
    (-37.0,  24.0, "Cape Agulhas",      "📍", "Cape",    "Southernmost tip of Africa"),
    (  1.3, 103.8, "Singapore",         "🌆", "Port",    "World 2nd busiest container port"),
    (  3.1, 101.7, "Kuala Lumpur",      "🏙️", "City",    "Capital of Malaysia"),
    (  5.4, 100.3, "Penang",            "🏙️", "Port",    "Historic Malaysian port city"),
    ( 13.8, 100.5, "Bangkok",           "🏙️", "City",    "Capital of Thailand"),
    (-31.9, 115.8, "Perth",             "🏙️", "Port",    "Australia — Indian Ocean gateway"),
    (-34.9, 138.6, "Adelaide",          "🏙️", "Port",    "South Australian port city"),
    ( -4.6,  55.5, "Seychelles",        "🏝️", "Island",  "Archipelago of 115 islands"),
    ( 12.5,  43.5, "Bab-el-Mandeb",    "🚧", "Strait",  "Narrow strait — Red Sea to Gulf of Aden"),
    (  1.2, 103.5, "Strait of Malacca", "🚧", "Strait",  "World's busiest shipping lane"),
    (  0.0,  68.0, "Equator Crossing",  "📍", "Equator", "Crossing 0 degrees latitude"),
    (  5.0,  72.0, "Chagos Archipelago","🏝️", "Island",  "British Indian Ocean Territory"),
    ( 20.0,  63.0, "Arabian Sea",       "🌊", "Sea",     "Monsoon weather zone"),
    (-15.0,  78.0, "South Indian Ocean","🌊", "Ocean",   "Roaring Forties — strong winds"),
    ( 10.0,  80.0, "Bay of Bengal",     "🌊", "Sea",     "Cyclone-prone sea — eastern India"),
    (-20.0,  80.0, "Central Indian Ocean","🌊","Ocean",  "Deep ocean — avg depth 3800m"),
    (-25.0,  55.0, "Southern Ocean Approach","🌊","Ocean","Gateway to Southern Ocean"),
    (-30.0,  80.0, "Perth Approach",    "🌊", "Ocean",   "Eastern Indian Ocean — deep waters"),
    ( -8.0,  55.0, "Mozambique Channel","🌊", "Channel", "Channel between Africa and Madagascar"),
    ( 15.0,  60.0, "Gulf of Aden",      "🌊", "Gulf",   "Connects Red Sea to Arabian Sea"),
]

def haversine_dist(lat1, lon1, lat2, lon2):
    R = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlam/2)**2
    return 2 * R * math.asin(math.sqrt(a))

def get_route_landmarks(path, radius_km=600):
    """Find landmarks within radius_km of any point on the route."""
    result = []
    seen = set()
    for lm in LANDMARKS:
        lm_lat, lm_lon, name, emoji, ltype, desc = lm
        best_idx  = -1
        best_dist = float('inf')
        for i, (lat, lon) in enumerate(path):
            d = haversine_dist(lat, lon, lm_lat, lm_lon)
            if d < best_dist:
                best_dist = d
                best_idx  = i
        if best_dist <= radius_km and name not in seen:
            seen.add(name)
            result.append({
                "wpIdx": best_idx,
                "name":  name,
                "emoji": emoji,
                "type":  ltype,
                "desc":  desc,
                "dist":  round(best_dist)
            })
    result.sort(key=lambda x: x["wpIdx"])
    return result


def create_route_map(path, start_name, end_name, eta_hours, risk_score,
                     output_file="route_map.html"):

    m = folium.Map(location=[10, 75], zoom_start=3, tiles="CartoDB positron")

    # Route line — clean map, no extra markers
    if path and len(path) > 1:
        folium.PolyLine(
            locations=path, color="#0057b8", weight=4,
            opacity=0.85, tooltip="Optimal Route"
        ).add_to(m)

    # Only start and end markers on map
    s_coord = path[0]  if path else PORTS.get(start_name, (0,0))
    e_coord = path[-1] if path else PORTS.get(end_name,   (0,0))

    folium.Marker(
        location=s_coord,
        tooltip=f"START: {start_name}",
        popup=folium.Popup(f"<b>🚢 {start_name}</b><br>Departure port", max_width=180),
        icon=folium.Icon(color="green", icon="ship", prefix="fa")
    ).add_to(m)

    folium.Marker(
        location=e_coord,
        tooltip=f"END: {end_name}",
        popup=folium.Popup(f"<b>🏁 {end_name}</b><br>ETA: {eta_hours:.1f} hrs", max_width=180),
        icon=folium.Icon(color="red", icon="flag", prefix="fa")
    ).add_to(m)

    # Get landmarks along route
    landmarks = get_route_landmarks(path, radius_km=600)
    landmarks = [l for l in landmarks
                 if l["name"] != start_name and l["name"] != end_name]

    print(f"\n  🗺️  Places along route: {len(landmarks)}")
    for l in landmarks:
        print(f"      wp {l['wpIdx']:3d} → {l['emoji']} {l['name']} (~{l['dist']} km)")

    # Build journey list HTML
    journey_items = ""
    for i, l in enumerate(landmarks, 1):
        journey_items += f"""<div id="ji_{i}" style="
            display:flex;align-items:flex-start;
            padding:8px 10px;border-radius:8px;margin-bottom:6px;
            background:#f8f9fa;border-left:3px solid #dee2e6;
            transition:all 0.4s ease;opacity:0.45;">
          <div style="font-size:20px;margin-right:10px;margin-top:1px;min-width:24px;">{l['emoji']}</div>
          <div>
            <div style="font-weight:bold;font-size:13px;color:#1a1a2e;">{l['name']}</div>
            <div style="font-size:11px;color:#888;margin-top:1px;">{l['type']} &bull; ~{l['dist']} km away</div>
            <div style="font-size:11px;color:#555;margin-top:2px;">{l['desc']}</div>
          </div>
        </div>"""

    if not journey_items:
        journey_items = '<div style="color:#999;font-size:12px;padding:8px;">No landmarks found near this route.</div>'

    # Timing
    days   = int(eta_hours // 24)
    hrs    = int(eta_hours % 24)
    t_str  = f"{days}d {hrs}h" if days else f"{hrs}h"
    r_color = "#28a745" if risk_score < 4 else "#ffc107" if risk_score < 7 else "#dc3545"
    r_label = "Low"    if risk_score < 4 else "Medium"  if risk_score < 7 else "High"

    # ── LEFT PANEL ────────────────────────────────────────────────────────────
    left_panel = f"""
    <div style="position:fixed;top:15px;left:15px;z-index:1000;
        background:white;border-radius:14px;
        box-shadow:0 4px 20px rgba(0,0,0,0.18);
        font-family:Arial,sans-serif;
        width:265px;max-height:92vh;
        display:flex;flex-direction:column;overflow:hidden;">

      <!-- Header -->
      <div style="background:#0d2b4e;color:white;
                  padding:13px 15px;border-radius:14px 14px 0 0;flex-shrink:0;">
        <div style="font-size:15px;font-weight:bold;">
          🚢 {start_name} &rarr; {end_name}
        </div>
        <div style="font-size:11px;opacity:0.85;margin-top:5px;line-height:1.8;">
          ⏱️ ETA: <b>{t_str}</b> &nbsp;|&nbsp;
          📌 <b>{len(path)}</b> waypoints<br>
          🛡️ Risk:
          <span style="background:{r_color};color:white;
            padding:1px 8px;border-radius:8px;font-weight:bold;font-size:11px;">
            {r_label} ({risk_score}/10)
          </span>
        </div>
      </div>

      <!-- Section title -->
      <div style="padding:9px 14px 5px;font-size:12px;font-weight:bold;
                  color:#0d2b4e;border-bottom:1px solid #eee;
                  flex-shrink:0;background:#f0f4f8;">
        🗺️ PLACES ALONG ROUTE &nbsp;
        <span style="background:#0d2b4e;color:white;border-radius:10px;
              padding:1px 8px;font-size:11px;">{len(landmarks)}</span>
      </div>

      <!-- Scrollable list -->
      <div id="journeyList"
           style="overflow-y:auto;padding:10px 10px;flex:1;">
        {journey_items}
      </div>

      <!-- Current place footer -->
      <div id="currentPlace" style="display:none;flex-shrink:0;
          padding:10px 14px;border-top:2px solid #ff8c00;
          background:#fff8f0;">
        <div style="font-size:10px;color:#999;margin-bottom:3px;
                    text-transform:uppercase;letter-spacing:0.5px;">
          Currently passing near
        </div>
        <div id="cpLine" style="font-size:14px;font-weight:bold;color:#1a1a2e;"></div>
        <div id="cpDesc" style="font-size:11px;color:#666;margin-top:2px;"></div>
        <div id="cpDist" style="font-size:11px;color:#0057b8;margin-top:2px;"></div>
      </div>
    </div>"""
    m.get_root().html.add_child(folium.Element(left_panel))

    # ── RIGHT PANEL — animation controls ─────────────────────────────────────
    right_panel = """
    <div style="position:fixed;bottom:25px;right:20px;z-index:1000;
        background:white;padding:15px 18px;border-radius:14px;
        border-left:5px solid #28a745;
        box-shadow:0 4px 20px rgba(0,0,0,0.18);
        font-family:Arial,sans-serif;font-size:13px;min-width:200px;">
      <div style="font-size:15px;font-weight:bold;margin-bottom:10px;color:#1a1a2e;">
        🎬 Ship Animation
      </div>
      <div style="margin-bottom:10px;display:flex;gap:8px;">
        <button onclick="startAnim()" id="startBtn"
          style="background:#28a745;color:white;border:none;
                 padding:8px 16px;border-radius:8px;cursor:pointer;
                 font-size:13px;font-weight:bold;flex:1;">▶ Start</button>
        <button onclick="resetAnim()"
          style="background:#6c757d;color:white;border:none;
                 padding:8px 14px;border-radius:8px;cursor:pointer;
                 font-size:13px;font-weight:bold;">↺</button>
      </div>
      <div style="margin-bottom:10px;font-size:12px;color:#555;">
        Speed:&nbsp;
        <select id="spd" style="padding:4px 8px;border-radius:6px;
                border:1px solid #ccc;font-size:12px;">
          <option value="1200">🐢 Slow</option>
          <option value="600" selected>🚢 Normal</option>
          <option value="250">💨 Fast</option>
          <option value="80">⚡ Very Fast</option>
        </select>
      </div>
      <div id="prog" style="color:#666;font-size:12px;min-height:16px;">
        Press ▶ Start to begin sailing
      </div>
    </div>"""
    m.get_root().html.add_child(folium.Element(right_panel))

    # ── Build JS data ─────────────────────────────────────────────────────────
    wps_js = "[" + ",".join(f"[{p[0]:.4f},{p[1]:.4f}]" for p in path) + "]"

    def esc(s):
        return (s.replace("\\", "\\\\")
                 .replace("'", "\\'")
                 .replace('"', '\\"'))

    lms_js = "[" + ",".join(
        "{i:%d,n:'%s',e:'%s',t:'%s',d:'%s',km:%d,ji:%d}" % (
            l["wpIdx"], esc(l["name"]), esc(l["emoji"]),
            esc(l["type"]),  esc(l["desc"]),
            l["dist"], idx + 1
        )
        for idx, l in enumerate(landmarks)
    ) + "]"

    end_esc = esc(end_name)

    # ── JavaScript ────────────────────────────────────────────────────────────
    js = f"""
<script>
(function() {{

  var WPS = {wps_js};
  var LMS = {lms_js};
  var N   = WPS.length;
  var idx = 0, timer = null;
  var ship = null, trail = null, pts = [];
  var shown = {{}};

  // Ship emoji icon
  var shipIcon = L.divIcon({{
    html: '<div style="font-size:26px;line-height:1;'
        + 'transform:translate(-50%,-50%);">🚢</div>',
    iconSize:[34,34], iconAnchor:[17,17], className:''
  }});

  // Find the Leaflet map instance
  function getMap() {{
    for (var k in window) {{
      try {{
        var o = window[k];
        if (o && o._leaflet_id !== undefined
            && typeof o.addLayer === 'function') return o;
      }} catch(e) {{}}
    }}
    return null;
  }}

  // Highlight a place in the left panel list
  function highlightPlace(lm) {{
    if (shown[lm.n]) return;
    shown[lm.n] = true;

    // Light up the list item
    var el = document.getElementById('ji_' + lm.ji);
    if (el) {{
      el.style.background      = '#fff3cd';
      el.style.borderLeftColor = '#ff8c00';
      el.style.opacity         = '1';
      el.style.boxShadow       = '0 2px 8px rgba(255,140,0,0.2)';
      el.scrollIntoView({{ behavior:'smooth', block:'nearest' }});
    }}

    // Update bottom footer of left panel
    document.getElementById('cpLine').textContent = lm.e + '  ' + lm.n;
    document.getElementById('cpDesc').textContent = lm.d;
    document.getElementById('cpDist').textContent = '~' + lm.km + ' km from route';
    document.getElementById('currentPlace').style.display = 'block';
  }}

  // Dim all items back to default
  function resetList() {{
    LMS.forEach(function(lm) {{
      var el = document.getElementById('ji_' + lm.ji);
      if (el) {{
        el.style.background      = '#f8f9fa';
        el.style.borderLeftColor = '#dee2e6';
        el.style.opacity         = '0.45';
        el.style.boxShadow       = 'none';
      }}
    }});
    document.getElementById('currentPlace').style.display = 'none';
  }}

  window.startAnim = function() {{
    var map = getMap();
    if (!map) {{ alert('Map is still loading — wait a moment.'); return; }}

    // Clear any previous animation
    if (timer) clearInterval(timer);
    if (ship)  try{{ map.removeLayer(ship);  }}catch(e){{}}
    if (trail) try{{ map.removeLayer(trail); }}catch(e){{}}

    idx = 0; pts = []; shown = {{}};
    resetList();

    var btn = document.getElementById('startBtn');
    btn.disabled = true;
    btn.style.background = '#adb5bd';
    document.getElementById('prog').textContent = 'Setting sail from {esc(start_name)}...';

    // Place ship at start
    ship  = L.marker(WPS[0], {{icon: shipIcon}}).addTo(map);
    pts   = [WPS[0]];
    trail = L.polyline(pts, {{
      color: '#ff6600', weight: 3,
      opacity: 0.9, dashArray: '8,5'
    }}).addTo(map);

    var spd = parseInt(document.getElementById('spd').value);

    timer = setInterval(function() {{
      idx++;

      if (idx >= N) {{
        clearInterval(timer);
        timer = null;
        document.getElementById('prog').textContent = '✅ Arrived at {end_esc}!';
        btn.disabled = false;
        btn.style.background = '#28a745';
        // Mark all remaining unvisited items as complete
        LMS.forEach(function(lm) {{
          var el = document.getElementById('ji_' + lm.ji);
          if (el && el.style.opacity !== '1') el.style.opacity = '1';
        }});
        return;
      }}

      // Move ship and trail
      var pos = WPS[idx];
      ship.setLatLng(pos);
      pts.push(pos);
      trail.setLatLngs(pts);
      map.panTo(pos, {{animate: true, duration: 0.35}});

      // Update progress
      var pct = Math.round(idx / (N - 1) * 100);
      document.getElementById('prog').textContent =
        '⛵ Sailing... ' + pct + '% (' + idx + '/' + (N-1) + ')';

      // Check if any landmark is at or near this waypoint
      LMS.forEach(function(lm) {{
        if (Math.abs(lm.i - idx) <= 1) highlightPlace(lm);
      }});

    }}, spd);
  }};

  window.resetAnim = function() {{
    var map = getMap();
    if (!map) return;
    if (timer) clearInterval(timer);
    if (ship)  try{{ map.removeLayer(ship);  }}catch(e){{}}
    if (trail) try{{ map.removeLayer(trail); }}catch(e){{}}
    timer = ship = trail = null;
    idx = 0; pts = []; shown = {{}};
    resetList();
    var btn = document.getElementById('startBtn');
    btn.disabled = false;
    btn.style.background = '#28a745';
    document.getElementById('prog').textContent = 'Press ▶ Start to begin sailing';
    map.fitBounds(L.latLngBounds(WPS));
  }};

}})();
</script>"""

    m.get_root().html.add_child(folium.Element(js))
    m.save(output_file)
    print(f"  ✅ Animated map saved → '{output_file}'")
    return output_file