import os
import json
import csv

def choose_ship():
    ships = sorted(map(lambda x: x.split(".")[0]
                      ,[s for s in os.listdir('hulls') if "ship" in s]))
    return ships

def load_ship(selected):
    with open("hulls/"+selected+".ship", "r") as f:
        ship_json = json.load(f)
    with open("hulls/ship_data.csv", "r") as f:
        reader = csv.reader(f)
        fields = []
        for row in reader:
            if reader.line_num == 1:
                fields.append(row)
            if selected in row:
                fields.append(row)
        ship_csv = dict(zip(*fields))

    return ship_json, ship_csv

def load_weapon_json(wid):
    uncommented_json = ""
    with open("weapons/" + wid + ".wpn", "r") as f:
        for line in f:
            line = "".join([l for l in line if l != "\n"])
            # BEGIN JSON error fixes
            if "#" in line:
                line = line[0:line.index("#")]
            if (((len(line) > 0) and (any([c not in [" ", "	"] for c in line])))
                and ("renderHints" not in line)
                and ("pierceSet" not in line)
                and ("textureType" not in line)):
                if (line.lstrip()[0] == "}") and (uncommented_json.rstrip()[-1] == ","):
                    uncommented_json = uncommented_json.rstrip()[:-1] + "\n"
                if (line.rstrip()[-1] == ";"):
                    line = line.rstrip()[:-1] + ","
                uncommented_json += line + "\n"
            # END JSON error fixes
    return json.loads(uncommented_json)

typecomp = {
    "BALLISTIC": ["BALLISTIC", "COMPOSITE", "HYBRID", "UNIVERSAL"],
    "ENERGY": ["ENERGY", "HYBRID", "SYNERGY", "UNIVERSAL"],
    "MISSILE": ["MISSILE", "COMPOSITE", "SYNERGY", "UNIVERSAL"],
    "Empty": ["BALLISTIC", "MISSILE", "ENERGY",
              "HYBRID", "COMPOSITE", "SYNERGY",
              "UNIVERSAL"]
}

sizecomp = {
    "SMALL": 1,
    "MEDIUM": 2,
    "LARGE": 3
}

def choose_weapon(slot_size, slot_type):
    weaponids = sorted(map(lambda x: x.split(".")[0]
                      ,[s for s in os.listdir('weapons/') if "wpn" in s]))

    available_weaponids = ["Empty"]

    for i in weaponids:
        weapon = load_weapon_json(i)
        if weapon["type"] == "DECORATIVE":
            continue
        if (sizecomp[weapon["size"]] <= sizecomp[slot_size]) and (slot_type in typecomp[weapon["type"]]):
            available_weaponids.append(i)

    return available_weaponids

def load_weapon(selected):
    if selected == "Empty":
        return ({"id": "Empty", "name": "Empty", "size": "SMALL", "type": "Empty"},
                {"id": "Empty", "name": "Empty", "range": 50})

    with open("weapons/weapon_data.csv", "r") as f:
        weapon_csv = [*csv.reader(f)]
        weapon_csv = [dict(zip(weapon_csv[0],w)) for w in weapon_csv[1:]]
        for w in weapon_csv:
            if (w["id"] == selected):
                weapon_csv = w
                break

    weapon_json = load_weapon_json(selected)

    return weapon_json, weapon_csv
