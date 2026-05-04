import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from math import radians, cos, sin, asin, sqrt
from routing.optimizer import haversine, RouteOptimizer
from ships.ship import Ship, SHIPS
from weather.weather import WeatherData


def test_haversine_mumbai_mombasa():
    dist = haversine(19.0, 72.8, -4.0, 39.7)
    assert 4200 < dist < 4600, f"Got {dist:.1f} km"

def test_haversine_same_point():
    dist = haversine(10.0, 60.0, 10.0, 60.0)
    assert dist < 0.01

def test_haversine_always_positive():
    dist = haversine(-30.0, 40.0, 25.0, 100.0)
    assert dist > 0

def test_haversine_chennai_dubai():
    dist = haversine(13.08, 80.27, 25.2, 55.27)
    assert 2600 < dist < 3100, f"Got {dist:.1f} km"


def test_ship_creation():
    ship = Ship("Test Ship", "cargo", 14, 0.8)
    assert ship.name == "Test Ship"
    assert ship.speed_knots == 14
    assert ship.drift_coeff == 0.8

def test_ship_effective_speed_calm():
    ship = Ship("Test", "cargo", 14, 0.8)
    speed = ship.effective_speed(wind_speed=0, wave_height=0)
    assert speed == 14.0

def test_ship_effective_speed_rough():
    ship = Ship("Test", "cargo", 14, 0.8)
    calm_speed = ship.effective_speed(0, 0)
    rough_speed = ship.effective_speed(20, 5)
    assert rough_speed < calm_speed

def test_ship_speed_never_zero():
    ship = Ship("Test", "tanker", 12, 1.0)
    speed = ship.effective_speed(wind_speed=100, wave_height=50)
    assert speed >= 12 * 0.3

def test_ships_dict_has_types():
    assert "cargo" in SHIPS
    assert "tanker" in SHIPS
    assert "container" in SHIPS

def test_ships_dict_speeds():
    for name, ship in SHIPS.items():
        assert ship.speed_knots > 0


def test_weather_fetch_returns_dict():
    wd = WeatherData()
    result = wd.fetch(10.0, 65.0)
    assert isinstance(result, dict)

def test_weather_fetch_has_wave_height():
    wd = WeatherData()
    result = wd.fetch(10.0, 65.0)
    assert "wave_height" in result

def test_weather_fetch_has_wind_speed():
    wd = WeatherData()
    result = wd.fetch(10.0, 65.0)
    assert "wind_speed" in result

def test_weather_values_positive():
    wd = WeatherData()
    result = wd.fetch(10.0, 65.0)
    assert result["wave_height"] >= 0
    assert result["wind_speed"] >= 0


def test_optimizer_ocean_check_arabian_sea():
    ship = SHIPS["cargo"]
    weather = WeatherData()
    opt = RouteOptimizer((19.0, 72.8), (-4.0, 39.7), ship, weather)
    assert opt._is_ocean(10.0, 65.0) is True

def test_optimizer_ocean_check_land():
    ship = SHIPS["cargo"]
    weather = WeatherData()
    opt = RouteOptimizer((19.0, 72.8), (-4.0, 39.7), ship, weather)
    assert opt._is_ocean(19.0, 75.0) is False

def test_optimizer_ocean_check_arabian_peninsula():
    ship = SHIPS["cargo"]
    weather = WeatherData()
    opt = RouteOptimizer((19.0, 72.8), (-4.0, 39.7), ship, weather)
    assert opt._is_ocean(21.0, 54.0) is False

def test_optimizer_modes():
    ship = SHIPS["cargo"]
    weather = WeatherData()
    for mode in ["time", "safety"]:
        opt = RouteOptimizer((19.0, 72.8), (-4.0, 39.7), ship, weather, mode=mode)
        assert opt.mode == mode