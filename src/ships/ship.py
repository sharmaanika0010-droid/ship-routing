class Ship:
    def __init__(self, name, ship_type, speed_knots, drift_coeff):
        self.name = name
        self.ship_type = ship_type
        self.speed_knots = speed_knots      # Normal speed
        self.drift_coeff = drift_coeff      # Effect of wind/waves on ship

    def effective_speed(self, wind_speed, wave_height):
        """
        Calculates the actual speed of the ship under rough weather
        """
        reduction = self.drift_coeff * (wind_speed * 0.1 + wave_height * 0.2)
        actual_speed = max(self.speed_knots - reduction, self.speed_knots * 0.3)
        return actual_speed


# Dictionary of ready-made ships
SHIPS = {
    "cargo":     Ship("Cargo Vessel",    "cargo",     14, 0.8),
    "tanker":    Ship("Oil Tanker",      "tanker",    12, 1.0),
    "container": Ship("Container Ship",  "container", 18, 0.6),
}