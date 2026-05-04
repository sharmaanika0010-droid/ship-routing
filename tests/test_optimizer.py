import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from routing.optimizer import haversine
from ships.ship import SHIPS
from weather.weather import WeatherData


def test_haversine_mumbai_chennai():
    dist = haversine(18.96, 72.82, 13.09, 80.29)
    assert 1000 < dist < 1100, f"Expected ~1030km, got {dist:.0f}km"

def test_ship_speed_in_storm():
    ship = SHIPS["cargo"]
    calm_speed = ship.effective_speed(wind_speed=0, wave_height=0)
    storm_speed = ship.effective_speed(wind_speed=40, wave_height=6)
    assert storm_speed < calm_speed

def test_weather_returns_dict():
    w = WeatherData()
    result = w.fetch(10.0, 75.0)
    assert "wave_height" in result
    assert "wind_speed" in result
    assert result["wave_height"] >= 0

def test_all_ships_exist():
    assert "cargo" in SHIPS
    assert "tanker" in SHIPS
    assert "container" in SHIPS