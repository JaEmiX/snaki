import json

file_path = 'data.json'


def read_data():
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
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
        json.dump(data, file)


def _update_data(key, value):
    data = read_data()
    data[key] = value
    with open(file_path, 'w') as file:
        json.dump(data, file)


def add_to_epoch(epoch: int):
    _add_to_data('epoch', epoch)


def update_record(record: int):
    _update_data('record', record)
