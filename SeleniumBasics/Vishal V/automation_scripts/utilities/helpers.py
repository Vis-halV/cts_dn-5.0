from pathlib import Path
import csv
import json


def read_csv_data(file_name):
    path = Path(__file__).resolve().parents[1] / 'test_data' / file_name
    with path.open(newline='', encoding='utf-8') as handle:
        return list(csv.DictReader(handle))


def read_json_data(file_name):
    path = Path(__file__).resolve().parents[1] / 'test_data' / file_name
    with path.open(encoding='utf-8') as handle:
        return json.load(handle)
