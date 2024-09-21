import math
import loader

def rotate(x, y, deg):
    angle = math.radians(deg-90)
    return [x * math.cos(angle) - y * math.sin(angle)
           ,x * math.sin(angle) + y * math.cos(angle)]

def rotatelist(points, deg):
    rotatedpoints = []
    for i in range(0, len(points), 2):
        rotatedpoints += rotate(points[i], points[i+1], deg)
    return rotatedpoints

def scalelist(points, fact):
    return [p * fact for p in points]

def to_canvas_center(canvas, points):
    return [i + canvas.winfo_width()/2 for i in points]

def from_canvas_center(canvas, points):
    return [i - canvas.winfo_width()/2 for i in points]

weaponsize = {"SMALL": 6, "MEDIUM": 15, "LARGE": 23}

def circle(canvas, cx, cy, r, s):
    points = []
    for i in range(s):
        x = 2*i*math.pi/s
        points.append(cx+r*math.cos(x))
        points.append(cy+r*math.sin(x))
    points.append(cx+r)
    points.append(cy)
    return points

def arc(canvas, cx, cy, radius, angle, arc, sides):
    points = []
    step = max(1,arc//10)
    start_a = math.radians(angle)+math.radians(arc)/2
    end_a = math.radians(angle)-math.radians(arc)/2

    if sides:
        points.append(cx)
        points.append(cy)
        points.append(cx+radius*1.05*math.cos(start_a))
        points.append(cy+radius*1.05*math.sin(start_a))

    for i in range(step+1):
        x = (start_a-i*(start_a-end_a)/step)
        points.append(cx+radius*math.cos(x))
        points.append(cy+radius*math.sin(x))

    if sides:
        points.append(cx+radius*1.05*math.cos(end_a))
        points.append(cy+radius*1.05*math.sin(end_a))
        points.append(cx)
        points.append(cy)

    return points

zoomlevel = [1]

def zoom(canvas, ship, slot, weapon_map, target_map, event):
    if event.num == 4:
        zoomlevel[0] *= 1.05
    if event.num == 5:
        zoomlevel[0] /= 1.05
    draw(canvas, ship, slot, weapon_map, target_map)

def draw(canvas, ship_json, slot, weapon_map, target_map):
    canvas.delete("all")
    canvas.create_line(to_canvas_center(canvas,scalelist(rotatelist(ship_json["bounds"]+ship_json["bounds"][:2], 0), zoomlevel[0])), fill="white")

    for ws in ship_json["weaponSlots"]:
        if ws["type"] not in ["BUILT_IN", "DECORATIVE",
                             "LAUNCH_BAY", "SYSTEM"]:

            canvas.create_line(
              to_canvas_center(canvas,
                  scalelist(
                      rotatelist(
                          circle(canvas,
                                 *ws["locations"],
                                 weaponsize[ws["size"]], 10) ,0),
                          zoomlevel[0])),
                  fill={slot: "red"}.get(ws["id"], "white"))

            _, weapon_csv = loader.load_weapon(weapon_map[ws["id"]])

            canvas.create_line(
              to_canvas_center(canvas,
                  scalelist(
                      rotatelist(
                          arc(canvas,
                              *ws["locations"],
                              int(weapon_csv["range"]),
                              ws["angle"],
                              ws["arc"],
                              True) ,0),
                          zoomlevel[0])),
                  fill={"Empty": "grey"}.get(weapon_map[ws["id"]], "yellow"))

    for t in target_map.values():
        points1 = (t["location"][0]-10, t["location"][1]-10,
                   t["location"][0]+10, t["location"][1]+10)
        points2 = (t["location"][0]-10, t["location"][1]+10,
                   t["location"][0]+10, t["location"][1]-10)
        canvas.create_line(
                to_canvas_center(
                    canvas, scalelist(
                        rotatelist( points1, 0),
                        zoomlevel[0])), fill=t["color"])
        canvas.create_line(
                to_canvas_center(
                    canvas, scalelist(
                        rotatelist( points2, 0),
                        zoomlevel[0])), fill=t["color"])
