from pydantic import BaseModel


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
