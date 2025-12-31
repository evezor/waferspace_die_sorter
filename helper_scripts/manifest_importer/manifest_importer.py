import csv
from collections import defaultdict
from pprint import pprint
MANIFEST = "manifest.csv"
TILEMAP = "tilemap.csv"


def load_slot_map(MANIFEST):
    """Return dict: CODE -> SLOT_SIZE"""
    slot_map = {}
    with open(MANIFEST, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            slot_map[row["CODE"]] = {"SLOT_SIZE": row["SLOT_SIZE"], "PROJECT": row["PROJECT"]}
    return slot_map


def load_grid(TILEMAP):
    """Return grid as list[list[str]]"""
    with open(TILEMAP, newline="") as f:
        reader = csv.reader(f)
        return [row for row in reader]


def build_layout(grid, slot_map):
    """Return layout as list[list[str]] with SLOT_SIZE values"""
    layout = []
    visited = set()
    tall = False
    for row in grid:
        if tall:
            tall = False
            continue
        layout_row = []
        double_wide = False
        for code in row:
            
            if double_wide:
                double_wide = False
                continue
            slot_size = slot_map.get(code, "UNKNOWN")["SLOT_SIZE"]
            if slot_size[0] == "1":
                double_wide = True
            name = f'{code}(2)' if code in visited else code
            data = dict(
                code=code, 
                slot_size=slot_size,
                project=slot_map.get(code, "UNKNOWN")["PROJECT"]
            )
            layout_row.append(data)
            visited.add(name)
            if slot_size[-1] == "1":
                tall = True
        layout.append(layout_row)
    return layout


def main():
    slot_map = load_slot_map(MANIFEST)
    grid = load_grid(TILEMAP)
    layout = build_layout(grid, slot_map)

    for row in layout:
        print(row)


if __name__ == "__main__":
    main()
