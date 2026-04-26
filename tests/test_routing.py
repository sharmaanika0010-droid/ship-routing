"""
test_routing.py
Unit tests for Optimal Ship Routing System
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from math import radians, cos, sin, asin, sqrt
from routing.optimizer import haversine, RouteOptimizer
from ships.ship import Ship, SHIPS
from weather.weather import WeatherData


# ── Test 1: Haversine Distance ────────────────────────────────────────────────

def test_haversine_mumbai_mombasa():
    """Mumbai to Mombasa approx 3900 km."""
    dist = haversine(19.0, 72.8, -4.0, 39.7)
    assert 4200 < dist < 4600, f"Got {dist:.1f} km"

def test_haversine_same_point():
    """Same point = zero distance."""
    dist = haversine(10.0, 60.0, 10.0, 60.0)
    assert dist < 0.01

def test_haversine_always_positive():
    """Distance is never negative."""
    dist = haversine(-30.0, 40.0, 25.0, 100.0)
    assert dist > 0

def test_haversine_chennai_dubai():
    """Chennai to Dubai approx 2800 km."""
    dist = haversine(13.08, 80.27, 25.2, 55.27)
    assert 2600 < dist < 3100, f"Got {dist:.1f} km"


# ── Test 2: Ship Class ────────────────────────────────────────────────────────

def test_ship_creation():
    """Ship object stores values correctly."""
    ship = Ship("Test Ship", "cargo", 14, 0.8)
    assert ship.name == "Test Ship"
    assert ship.speed_knots == 14
    assert ship.drift_coeff == 0.8

def test_ship_effective_speed_calm():
    """In calm weather, speed should be close to normal."""
    ship = Ship("Test", "cargo", 14, 0.8)
    speed = ship.effective_speed(wind_speed=0, wave_height=0)
    assert speed == 14.0

def test_ship_effective_speed_rough():
    """In rough weather, speed must reduce."""
    ship = Ship("Test", "cargo", 14, 0.8)
    calm_speed = ship.effective_speed(0, 0)
    rough_speed = ship.effective_speed(20, 5)
    assert rough_speed < calm_speed

def test_ship_speed_never_zero():
    """Speed must never go below 30% of normal."""
    ship = Ship("Test", "tanker", 12, 1.0)
    speed = ship.effective_speed(wind_speed=100, wave_height=50)
    assert speed >= 12 * 0.3

def test_ships_dict_has_types():
    """SHIPS dictionary must have cargo, tanker, container."""
    assert "cargo"     in SHIPS
    assert "tanker"    in SHIPS
    assert "container" in SHIPS

def test_ships_dict_speeds():
    """Default ship speeds must be positive."""
    for name, ship in SHIPS.items():
        assert ship.speed_knots > 0, f"{name} has zero speed"


# ── Test 3: WeatherData ───────────────────────────────────────────────────────

def test_weather_fetch_returns_dict():
    """WeatherData.fetch must return a dictionary."""
    wd = WeatherData()
    result = wd.fetch(10.0, 65.0)
    assert isinstance(result, dict)

def test_weather_fetch_has_wave_height():
    """Result must contain wave_height key."""
    wd = WeatherData()
    result = wd.fetch(10.0, 65.0)
    assert "wave_height" in result

def test_weather_fetch_has_wind_speed():
    """Result must contain wind_speed key."""
    wd = WeatherData()
    result = wd.fetch(10.0, 65.0)
    assert "wind_speed" in result

def test_weather_values_positive():
    """Wave height and wind speed must be non-negative."""
    wd = WeatherData()
    result = wd.fetch(10.0, 65.0)
    assert result["wave_height"] >= 0
    assert result["wind_speed"]  >= 0


# ── Test 4: RouteOptimizer ────────────────────────────────────────────────────

def test_optimizer_ocean_check_arabian_sea():
    """Arabian Sea open water must be ocean."""
    ship    = SHIPS["cargo"]
    weather = WeatherData()
    opt = RouteOptimizer((19.0, 72.8), (-4.0, 39.7), ship, weather)
    assert opt._is_ocean(10.0, 65.0) is True

def test_optimizer_ocean_check_land():
    """Indian subcontinent must NOT be ocean."""
    ship    = SHIPS["cargo"]
    weather = WeatherData()
    opt = RouteOptimizer((19.0, 72.8), (-4.0, 39.7), ship, weather)
    assert opt._is_ocean(19.0, 75.0) is False

def test_optimizer_ocean_check_arabian_peninsula():
    """Arabian Peninsula core must NOT be ocean."""
    ship    = SHIPS["cargo"]
    weather = WeatherData()
    opt = RouteOptimizer((19.0, 72.8), (-4.0, 39.7), ship, weather)
    assert opt._is_ocean(21.0, 54.0) is False

def test_optimizer_modes():
    """Optimizer must accept both time and safety modes."""
    ship    = SHIPS["cargo"]
    weather = WeatherData()
    for mode in ["time", "safety"]:
        opt = RouteOptimizer((19.0, 72.8), (-4.0, 39.7), ship, weather, mode=mode)
        assert opt.mode == mode