# SL Train anb busses
SL_ENDPOINT = "https://transport.integration.sl.se/v1/sites/"
SL_TRAINS = "9702/departures?transport=TRAIN&forecast=60&direction=1"

# Weather sources
WEATHER_ENDPOINT = "https://api.open-meteo.com/v1/forecast"
WEATHER_CURRENT = (
    "latitude=59.414938&longitude=17.825792"
    "&current=temperature_2m,"
    "precipitation,weather_code,cloud_cover,surface_pressure,wind_speed_10m"
    ",wind_direction_10m&hourly=temperature_2m,weather_code,wind_speed_10m"
    ",wind_direction_10m&wind_speed_unit=ms&timezone=Europe%2FBerlin"
    "&forecast_days=1"
)
