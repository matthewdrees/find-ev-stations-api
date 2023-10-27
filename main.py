import psycopg2

from fastapi import FastAPI, HTTPException, status, Security
from fastapi.security import (
    APIKeyHeader,
)

from pydantic import BaseModel

conn = psycopg2.connect("dbname=postgres user=postgres")

app = FastAPI()

api_key_header = APIKeyHeader(name="X-API-Key")


api_keys = ["dude"]


def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    if api_key_header in api_keys:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )


@app.get("/protected")
def protected_route(api_key: str = Security(get_api_key)):
    # Process the request for authenticated users
    return {"message": "Access granted!"}


class Station(BaseModel):
    longitude: float
    latitude: float
    name: str
    address: str
    city_state_zip: str
    access_days_time: str
    ev_network: str
    ev_network_web: str
    dc_fast_chargers: int
    ev_level_1_chargers: int
    ev_level_2_chargers: int
    ev_connector_types: str


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
            Station(
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
