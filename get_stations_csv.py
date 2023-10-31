#! /usr/bin/env python3
"""Fetch EV station data from developer.nrel.gov API and write to a csv file suitable for postgres import."""

import argparse
import csv
import logging
import json
import requests
import os

from config import get_config

stations_json_full_path = "/tmp/stations.json"
stations_csv_full_path = "/tmp/stations.csv"


def fetch_nrel_stations_to_file(config):
    url = "https://developer.nrel.gov/api/alt-fuel-stations/v1.json"
    logging.info(f"fetching ev stations from '{url}' ... ")
    params = {
        "format": "json",
        "api_key": config["nrel key"],
        "status": "E",
        "access": "public",
        "fuel_type": "ELEC",
        "limit": "all",
    }
    r = requests.get(url, params=params)
    j = json.loads(r.text)

    with open(stations_json_full_path, "w") as f:
        logging.info(f"writing ev station json to '{stations_json_full_path}'")
        f.write(json.dumps(j, indent=2))


def get_optional_list(s):
    if s:
        return " ".join(s)
    return ""


def get_optional_number(s):
    if s:
        return int(s)
    return 0


def remove_tabs(s):
    return s.replace("\t", " ")


def remove_crap(s):
    return s.replace("\n", " ").replace("\r", "").replace("\t", " ").replace("\\", "")


def write_stations_csv_file(config):
    logging.info(f"reading ev stations json from '{stations_json_full_path}'")
    with open(stations_json_full_path, "r") as f:
        j = json.load(f)

    # "(-122.3493,47.6205)",Space Needle,400 Broad St,"Seattle, WA 98109",24 hours,Space needle,https://www.spaceneedle.com/,0,1,2,J1772
    logging.info(f"writing ev stations csv to '{stations_csv_full_path}'")
    with open(stations_csv_full_path, "w") as f:
        writer = csv.writer(f, delimiter="\t")
        for s in j["fuel_stations"]:
            row = [
                f"({s['longitude']},{s['latitude']})",
                remove_crap(s["station_name"]),
                remove_crap(s["street_address"]),
                remove_crap(f"{s['city']}, {s['state']} {s['zip']}"),
                s["access_days_time"],
                s["ev_network"],
                s["ev_network_web"],
                get_optional_number(s["ev_level1_evse_num"]),
                get_optional_number(s["ev_level2_evse_num"]),
                get_optional_number(s["ev_dc_fast_num"]),
                get_optional_list(s["ev_connector_types"]),
            ]
            writer.writerow(row)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.INFO)

    config = get_config()
    if os.path.exists(stations_json_full_path):
        logging.info(f"'{stations_json_full_path}' exists, skipping json fetch")
    else:
        fetch_nrel_stations_to_file(config)

    write_stations_csv_file(config)
