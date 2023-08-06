import logging
import os
from typing import Union, List, Dict

import time
from fastapi import FastAPI
from pydantic import BaseModel
import sentry_sdk


logging.basicConfig(level=logging.INFO)

if (sentry_dsn := os.environ.get("SENTRY_DSN")) is not None:
    sentry_sdk.init(sentry_dsn)
    logging.info("Sentry enabled")


class Measurement(BaseModel):
    mac: str
    humidity: int
    temperature: int
    pressure: int
    acceleration: int
    battery: int
    measurement_sequence_number: int
    movement_counter: int
    tx_power: int
    acceleration_x: int
    acceleration_y: int
    acceleration_z: int


class MeasurementWithTs(Measurement):
    ts: int


app = FastAPI()


MEASUREMENTS: Dict[str, MeasurementWithTs] = {}


def store_measurement(measurement: Measurement):
    measurement_with_ts = MeasurementWithTs(ts=int(time.time()), **measurement.dict())
    MEASUREMENTS[measurement.mac] = measurement_with_ts


def fetch_measurement(mac: str) -> Union[MeasurementWithTs, None]:
    return MEASUREMENTS.get(mac)


def fetch_all_measurements() -> List[MeasurementWithTs]:
    return list(MEASUREMENTS.values())


@app.post("/measurements", status_code=201, deprecated=True)
def add_measurement(measurement: Measurement):
    store_measurement(measurement)


@app.get("/measurements", deprecated=True)
def get_all_measurements() -> List[MeasurementWithTs]:
    return fetch_all_measurements()


@app.get("/measurements/{mac}", deprecated=True)
def get_measurement_by_mac(mac: str) -> Union[MeasurementWithTs, None]:
    return fetch_measurement(mac)


@app.post("/api/v0/measurements", status_code=201)
def v0_add_measurement(measurement: Measurement):
    store_measurement(measurement)


@app.get("/api/v0/measurements")
def v0_get_all_measurements() -> List[MeasurementWithTs]:
    return fetch_all_measurements()


@app.get("/api/v0/measurements/{mac}")
def v0_get_measurement_by_mac(mac: str) -> Union[MeasurementWithTs, None]:
    return fetch_measurement(mac)
