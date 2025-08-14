API = {
    "current": {
        "url": "https://api.openweathermap.org/data/2.5/weather",
        "params": {
            "units": "metric",
            "lat": 59.421491,
            "lon": 17.819238,
            "appid": OWM_API_KEY
        }
    },
    "hourly": {
        "url": "https://api.openweathermap.org/data/2.5/forecast",
        "params": {
            "cnt": 4,
            "units": "metric",
            "lat": 59.421491,
            "lon": 17.819238,
            "appid": OWM_API_KEY
        }
    }
}

async def _fetch(self, segment="current"):
    API_REF = WeatherData.API[segment]
    data = await fetch_json(
        url=API_REF["url"],
        params=API_REF["params"]
    )
    return data

async def fetch_current(self):
    return await self._fetch()

async def fetch_hourly(self):
    return await self._fetch("hourly")