import psycopg2

from config import get_config
import model

from fastapi import FastAPI, HTTPException, status, Security
from fastapi.security import (
    APIKeyHeader,
)

config = get_config()

app = FastAPI()

conn = psycopg2.connect(f"dbname={config['db_name']} user={config['db_user']}")

api_key_header = APIKeyHeader(name="X-API-Key")

api_keys = [config["my key"]]


def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    if api_key_header in api_keys:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )


@app.get("/stations/nearest")
async def stations_nearest(
    api_key: str = Security(get_api_key),
    longitude: float = -122.3493,
    latitude: float = 47.6205,
):
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM stations ORDER BY POINT(%s,%s) <-> coordinates LIMIT 20",
            (longitude, latitude),
        )
        station_tuples = cur.fetchall()

    except (Exception, psychopg2.DatabaseError) as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error
        )

    stations = []
    for s in station_tuples:
        longitude, latitude = eval(s[0])
        stations.append(
            model.Station(
                longitude=longitude,
                latitude=latitude,
                name=s[1],
                address=s[2],
                city_state_zip=s[3],
                access_days_time=s[4],
                ev_network=s[5],
                ev_network_web=s[6],
                dc_fast_chargers=s[7],
                ev_level_1_chargers=s[8],
                ev_level_2_chargers=s[9],
                ev_connector_types=s[10],
            )
        )
    return stations
