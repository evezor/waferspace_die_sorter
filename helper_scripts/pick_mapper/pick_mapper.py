import csv
import json
from pathlib import Path

def csv_to_dict(csv_path: str, json_path: str):
    """
    Read a CSV file and convert it to a dictionary keyed by COL|ROW.
    Each key maps to a list of [X, Y, RETICLE_SHOT].
    """

    result = {}

    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            # print(row)
            key = row["COL|ROW"]

            x = float(row["X"])
            y = float(row["Y"])
            reticle_shot = row["RETICLE_SHOT"].strip()

            if key not in result:
                result[key] = []

            result[key].append([x, y, reticle_shot])

    with open(json_path, "w", encoding="utf-8") as jsonfile:
        json.dump(result, jsonfile, indent=2)

    return result


if __name__ == "__main__":
    # TODO: somewhere we harmonize with actual run data from stitcher
    
    run = 'run1' 
    csv_file = "../die_yield_helper/waferspace_run1_test.csv"
    json_file = "waferspace_run1_test.json"

    data = csv_to_dict(csv_file, json_file)
    print(f"Processed {sum(len(v) for v in data.values())} rows")
    print(f"Unique COL|ROW entries: {len(data)}")
    print(data.keys())
