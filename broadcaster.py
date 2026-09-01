"""Collect commute and weather data and publish normalized MQTT snapshots."""

import asyncio
import json
import logging
import os
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional

import aiohttp
import paho.mqtt.client as mqtt

LOGGER = logging.getLogger(__name__)


def env_int(name: str, default: int) -> int:
    value = os.environ.get(name)
    return int(value) if value else default


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


class Publisher:
    def __init__(self) -> None:
        self.prefix = os.environ.get("MQTT_TOPIC_PREFIX", "commute/dashboard").rstrip("/")
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    def start(self) -> None:
        self.client.connect(os.environ["MQTT_HOST"], env_int("MQTT_PORT", 1883), 60)
        self.client.loop_start()
        self._publish_discovery()

    def stop(self) -> None:
        self.client.disconnect()
        self.client.loop_stop()

    def publish(self, topic: str, data: Any) -> None:
        payload = json.dumps({"updated_at": now(), "data": data}, separators=(",", ":"))
        result = self.client.publish(f"{self.prefix}/{topic}", payload, qos=1, retain=True)
        if result.rc != mqtt.MQTT_ERR_SUCCESS:
            raise RuntimeError(f"MQTT publish failed for {topic}: {result.rc}")

    def status(self, source: str, error: Optional[str] = None) -> None:
        self.publish(f"status/{source}", {"ok": error is None, "error": error})

    def _publish_discovery(self) -> None:
        base = f"{self.prefix}/transit"
        entities = {
            "next_city_bus": ("Next city bus", f"{base}/city-buses",
                              "{{ value_json.data[0].departure | default('unknown') }}"),
            "next_journey": ("Next T-Centralen journey", f"{base}/journeys",
                             "{{ value_json.data[0].train_departure_time | default('unknown') }}"),
            "next_other_bus": ("Next other bus", f"{base}/other-buses",
                               "{{ value_json.data[0].departure | default('unknown') }}"),
        }
        for object_id, (name, state_topic, value_template) in entities.items():
            config = {
                "name": name, "state_topic": state_topic,
                "value_template": value_template, "unique_id": f"commute_{object_id}",
                "device": {"identifiers": ["commute-broadcaster"], "name": "Commute broadcaster"},
            }
            self.client.publish(
                f"homeassistant/sensor/commute_broadcaster/{object_id}/config",
                json.dumps(config, separators=(",", ":")), qos=1, retain=True,
            )


class Collector:
    def __init__(self, publisher: Publisher) -> None:
        self.publisher = publisher
        self.latitude = os.environ["WEATHER_LATITUDE"]
        self.longitude = os.environ["WEATHER_LONGITUDE"]
        self.sl_headers = (
            {"Ocp-Apim-Subscription-Key": os.environ["SL_API_KEY"]}
            if os.environ.get("SL_API_KEY") else None
        )

    async def get(
        self, session: aiohttp.ClientSession, url: str, params: Dict[str, Any],
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        async with session.get(url, params=params, headers=headers) as response:
            response.raise_for_status()
            return await response.json()

    async def weather(self, session: aiohttp.ClientSession) -> None:
        params = {
            "lat": self.latitude, "lon": self.longitude, "units": "metric",
            "lang": "sv", "appid": os.environ["OWM_API_KEY"],
        }
        current, forecast = await asyncio.gather(
            self.get(session, os.environ["OWM_CURRENT_API"], params),
            self.get(session, os.environ["OWM_FORECAST_API"], {**params, "cnt": 8}),
        )
        current_weather = current["weather"][0]
        self.publisher.publish("weather/current", {
            "temperature_c": round(current["main"]["temp"]),
            "feels_like_c": round(current["main"]["feels_like"]),
            "minimum_c": round(current["main"]["temp_min"]),
            "maximum_c": round(current["main"]["temp_max"]),
            "wind_mps": round(current["wind"]["speed"], 1),
            "location": current["name"],
            "condition": current_weather["description"],
            "icon": current_weather["icon"],
        })
        self.publisher.publish("weather/forecast", [
            {
                "time": item["dt"], "temperature_c": round(item["main"]["temp"]),
                "wind_mps": round(item["wind"]["speed"], 1),
                "icon": item["weather"][0]["icon"],
            }
            for item in forecast["list"]
        ])

    async def solar(self, session: aiohttp.ClientSession) -> None:
        response = await self.get(session, os.environ["SUN_API"], {
            "lat": self.latitude, "lng": self.longitude,
            "tzid": os.environ.get("TIMEZONE", "Europe/Stockholm"), "formatted": 0,
        })
        self.publisher.publish("weather/solar", response["results"])

    async def departures(
        self, session: aiohttp.ClientSession, site_id: str, direction: str
    ) -> List[Dict[str, Any]]:
        payload = await self.get(
            session, f"{os.environ['SL_DEPARTURES_API'].rstrip('/')}/{site_id}/departures",
            {"transport": "BUS", "direction": direction, "forecast": 1200},
            self.sl_headers,
        )
        return [
            {
                "line": item["line"]["designation"], "destination": item["destination"],
                "departure": item["display"], "scheduled_at": item.get("expected"),
            }
            for item in payload.get("departures", [])
            if item.get("state") == "EXPECTED"
        ]

    async def transit(self, session: aiohttp.ClientSession) -> None:
        city, other, journeys = await asyncio.gather(
            self.departures(session, os.environ["SL_CITY_BUS_SITE_ID"], os.environ.get("SL_CITY_BUS_DIRECTION", "2")),
            self.departures(session, os.environ["SL_OTHER_BUS_SITE_ID"], os.environ.get("SL_OTHER_BUS_DIRECTION", "1")),
            self.get(session, os.environ["SL_TRIPS_API"], {
                "origin": os.environ["SL_ORIGIN"], "destination": os.environ["SL_DESTINATION"],
                "transport": "BUS,TRAIN", "limit": 3,
            }, self.sl_headers),
        )
        city_lines = set(os.environ.get("CITY_BUS_LINES", "809,809C,807").split(","))
        self.publisher.publish("transit/city-buses", [
            item for item in city if item["line"] in city_lines
        ][:3])
        self.publisher.publish("transit/other-buses", [
            item for item in other if item["line"] not in city_lines
        ][:3])
        self.publisher.publish("transit/journeys", normalize_journeys(journeys)[:3])


def normalize_journeys(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract the bus -> transfer -> train presentation model from SL responses."""
    trips = payload.get("trips", payload.get("Trip", []))
    normalized = []
    for trip in trips:
        legs = trip.get("legs", trip.get("LegList", {}).get("Leg", []))
        bus = next((leg for leg in legs if leg.get("mode") == "BUS"), None)
        train = next((leg for leg in legs if leg.get("mode") == "TRAIN"), None)
        if not bus or not train:
            continue
        normalized.append({
            "bus_departure_time": bus.get("departureTime", bus.get("Origin", {}).get("time")),
            "bus_line_number": bus.get("line", bus.get("Product", {}).get("line")),
            "bus_line_destination": bus.get("destination", bus.get("Destination", {}).get("name")),
            "transfer_minutes": bus.get("transferMinutes", trip.get("transferMinutes")),
            "train_departure_time": train.get("departureTime", train.get("Origin", {}).get("time")),
            "train_line_number": train.get("line", train.get("Product", {}).get("line")),
            "train_destination": train.get("destination", train.get("Destination", {}).get("name")),
        })
    return normalized


async def repeat(name: str, interval: int, operation, session: aiohttp.ClientSession) -> None:
    while True:
        try:
            await operation(session)
            operation.__self__.publisher.status(name)
        except Exception as error:
            LOGGER.exception("%s collection failed", name)
            operation.__self__.publisher.status(name, str(error))
        await asyncio.sleep(interval)


async def main() -> None:
    publisher = Publisher()
    publisher.start()
    collector = Collector(publisher)
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=15)) as session:
            await asyncio.gather(
                repeat("weather", env_int("WEATHER_INTERVAL_SECONDS", 900), collector.weather, session),
                repeat("solar", env_int("SOLAR_INTERVAL_SECONDS", 900), collector.solar, session),
                repeat("transit", env_int("TRANSIT_INTERVAL_SECONDS", 60), collector.transit, session),
            )
    finally:
        publisher.stop()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    asyncio.run(main())
