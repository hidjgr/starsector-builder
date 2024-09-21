from tkinter import *
from graphics import *
from loader import *
import time

size_canvas = (500,500)
size_shiplist = (200,200)

root = Tk()
root.title('Starsector builder')
root.geometry(str(size_shiplist[1]+size_canvas[1])+"x"+str(size_canvas[0]))

canvas = Canvas(root, width=size_canvas[0], height=size_canvas[1], bg="black")
canvas.grid(row=0,column=0,rowspan=3)

shiplist = Listbox(root, selectmode=BROWSE,
                   height=size_shiplist[0]//20,
                   width=size_shiplist[1]//8,
                   exportselection=False)
for i in choose_ship():
    shiplist.insert(END, i)
shiplist.grid(row=0,column=1)

slotlist = Listbox(root, height=150//20, width=size_shiplist[1]//8,
                   exportselection=False)
slotlist.grid(row=1,column=1)

weaponlist = Listbox(root, height=150//20, width=size_shiplist[1]//8,
                     exportselection=False)
weaponlist.grid(row=2,column=1)

selected_ship_name = [None]
selected_ship = [None]
selected_slot = [None]
weapon_map = {}
targetcolors = {"unused": {"red", "green", "blue", "orange"},
                "used": set()}
target_map = {}

draw_current = lambda: draw(canvas, selected_ship[0][0], selected_slot[0], weapon_map, target_map)

def select_ship(*args):
    selection = shiplist.get(shiplist.curselection()[0])
    if selection == selected_ship_name[0]:
        return

    selected_ship_name[0] = selection
    selected_ship[0] = load_ship(selected_ship_name[0])

    slotlist.delete(0,END)
    weapon_map.clear()

    for w in selected_ship[0][0]["weaponSlots"]:
        if w["type"] not in ["BUILT_IN", "DECORATIVE",
                             "LAUNCH_BAY", "SYSTEM"]:
            slotlist.insert(END, w["id"])
            weapon_map[w["id"]] = "Empty"

    draw_current()

shiplist.bind('<<ListboxSelect>>', select_ship)

def select_slot(*args):
    selected_slot[0] = slotlist.get(slotlist.curselection()[0])
    for s in selected_ship[0][0]["weaponSlots"]:
        if s["id"] == selected_slot[0]:
            slot_size = s["size"]
            slot_type = s["type"]
            break
    available_weapons = choose_weapon(slot_size, slot_type)
    weaponlist.delete(0, END)
    for w in available_weapons:
        weaponlist.insert(END, w)
    weaponidx = weaponlist.get(0, END).index(weapon_map[selected_slot[0]])
    weaponlist.selection_set(weaponidx, weaponidx)
    draw_current()

slotlist.bind('<<ListboxSelect>>', select_slot)

def select_weapon(*args):
    weapon_map[selected_slot[0]] = weaponlist.get(
            weaponlist.curselection()[0])
    draw_current()

weaponlist.bind('<<ListboxSelect>>', select_weapon)

zoomupdate = lambda x: zoom(canvas, selected_ship[0][0], selected_slot[0], weapon_map, target_map, x)

def create_target(event):
    target_map[0] = {"location": rotatelist(scalelist(
        from_canvas_center(canvas, [event.x, event.y]),
        1/zoomlevel[0]), 180),
        "color": "lightgreen"}
    print(target_map)
    draw_current()

canvas.bind('<Button-1>', create_target)
canvas.bind('<Button-4>', zoomupdate)
canvas.bind('<Button-5>', zoomupdate)

root.mainloop()
