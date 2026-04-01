import sys, os
# Add src folder to Python path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from routing.optimizer import haversine
from ships.ship import SHIPS
from weather.weather import WeatherData


def test_haversine_mumbai_chennai():
    """Distance from Mumbai to Chennai should be ~1030 km"""
    dist = haversine(18.96, 72.82, 13.09, 80.29)
    # 1000–1100 km range rakha correct
    assert 1000 < dist < 1100, f"Expected ~1030km, got {dist:.0f}km"

def test_ship_speed_in_storm():
    """Ship should slow down in storm conditions"""
    ship = SHIPS["cargo"]
    calm_speed  = ship.effective_speed(wind_speed=0,  wave_height=0)
    storm_speed = ship.effective_speed(wind_speed=40, wave_height=6)
    assert storm_speed < calm_speed


def test_weather_returns_dict():
    """Weather module should return a dictionary with wave and wind data"""
    w = WeatherData()
    result = w.fetch(10.0, 75.0)
    assert "wave_height" in result
    assert "wind_speed" in result
    assert result["wave_height"] >= 0


def test_all_ships_exist():
    """All three ships should be defined"""
    assert "cargo"     in SHIPS
    assert "tanker"    in SHIPS
    assert "container" in SHIPS