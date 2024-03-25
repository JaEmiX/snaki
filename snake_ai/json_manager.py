import json

from dataclasses import asdict
from typing import List

from snake_ai.persistent_data import PersistentData
from snake_ai.record_model import RecordModel

file_path = 'data.json'


def read_data():
    try:
        with open(file_path, 'r') as file:
            data = PersistentData(**json.load(file))
        return data
    except FileNotFoundError:
        print("File not found. Creating a new file.")
        return {}
    except json.JSONDecodeError:
        print("Error decoding JSON. Starting with an empty dataset.")
        return {}


def _add_to_data(key, value):
    data = read_data()
    current_value = data[key]
    data[key] = current_value + value
    with open(file_path, 'w') as file:
        json.dump(asdict(data), file)


def add_data_record_model(record_model: RecordModel):
    data = read_data()
    data.record_models.append(record_model)
    with open(file_path, 'w') as file:
        json.dump(asdict(data), file)


def update_data_record_model(record_model: List[RecordModel]):
    data = read_data()
    data.record_models = record_model
    with open(file_path, 'w') as file:
        json.dump(asdict(data), file)


def update_data_record(record: int):
    data = read_data()
    data.record = record
    with open(file_path, 'w') as file:
        json.dump(asdict(data), file)


def add_data_epoch(epoch: int):
    data = read_data()
    data.epoch = epoch
    with open(file_path, 'w') as file:
        json.dump(asdict(data), file)
