import json

# Assuming your config file is named 'config.json'
config_path = 'config.json'

# Load the config file
with open(config_path, 'r') as config_file:
    config = json.load(config_file)
