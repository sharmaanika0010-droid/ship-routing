class WeatherData:
    def fetch(self, lat, lon):
        # Fast default — API call skip karo
        return {"wave_height": 1.5, "wind_speed": 10.0}