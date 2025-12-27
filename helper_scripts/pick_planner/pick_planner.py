import json
from pathlib import Path

INPUT_JSON = "../pick_mapper/waferspace_run1_test.json"
OUTPUT_JSONL = "pick.jsonl"

feeder_names = ['C8R2', 'C8R3', 'C8R4', 'C8R5', 'C8R0', 'C8R1', 'C3R5', 'C4R4', 'C4R5', 'C5R3', 'C5R4', 'C5R5', 'C6R2', 'C6R3', 'C6R4', 'C6R5', 'C7R1', 'C7R2', 'C7R3', 'C7R4', 'C7R5', 'C1R3', 'C1R4', 'C1R5', 'C2R1', 'C2R2', 'C2R3', 'C2R4', 'C2R5', 'C3R0', 'C3R1', 'C3R2', 'C3R3', 'C3R4', 'C4R0', 'C4R1', 'C4R2', 'C4R3', 'C5R0', 'C5R1', 'C5R2', 'C6R0', 'C6R1', 'C7R0', 'C0R0', 'C0R1', 'C0R2', 'C0R3', 'C0R4', 'C0R5', 'C1R0', 'C1R1', 'C1R2', 'C2R0']

CLEAR_Z = 5.0  # mm above board for safe travel
PICK_Z = -1.0   # mm board level for pick/place

# Generate sample locations for each feeder
sample_locations = {}
num_feeders = len(feeder_names)
for i, feeder in enumerate(feeder_names):
    x = 150
    y = -200 * (i / (num_feeders - 1)) if num_feeders > 1 else 0
    sample_locations[feeder] = {'x': x, 'y': y}

def _place(component):
    yield {'cmd': 'comment', 'data': f"picking: {component}"}
    yield dict(cmd='move', x=sample_locations[component]['x'], y=sample_locations[component]['y'], f=10000)
    yield {'cmd': 'sleep', 'seconds': .1}
    yield dict(cmd='move', z=PICK_Z, f=4500)
    yield {'cmd': 'eval', 'eval': 'suck(True)'}
    yield {'cmd': 'sleep', 'seconds': .5}
    yield dict(cmd='move', z=CLEAR_Z, f=12500)
    
def _pick(x, y, reticle_shot):
    yield {'cmd': 'comment', 'data': f"picking at: X{x} Y{y} S{reticle_shot}"}
    yield dict(cmd='move', x=x, y=y-200, f=10000) # TODO: hack work offset
    yield {'cmd': 'sleep', 'seconds': .1}
    yield dict(cmd='move', z=PICK_Z, f=4500)
    yield {'cmd': 'eval', 'eval': 'suck(False)'}
    yield {'cmd': 'sleep', 'seconds': .5}
    yield dict(cmd='move', z=CLEAR_Z, f=12500)

# -----------------------------
# Load JSON
# -----------------------------
with open(INPUT_JSON, "r", encoding="utf-8") as f:
    data = json.load(f)

commands = []

for project, entries in data.items():
    for entry in entries:
        x, y, reticle_shot = entry
        for cmd in _pick(x, y, reticle_shot):
            commands.append(cmd)
        for cmd in _place(project):
            commands.append(cmd)

   
with open(OUTPUT_JSONL, "w", encoding="utf-8") as f:
    for cmd in commands:
        f.write(json.dumps(cmd) + "\n")
    
    

