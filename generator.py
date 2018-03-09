import json

from sheet import Sheet

if __name__ == "__main__":
    config = json.load(open("resources/powerup_config.json"))
    gen = Sheet(config)
    fields = json.load(open("resources/powerup_test_2.json"))
    gen.create_from_json(fields)
