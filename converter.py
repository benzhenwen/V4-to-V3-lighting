import json

input_path: str = input("input file path: ")
output_path: str = input("output file path: ")

# file read
input_f = open(input_path, "r")
input = input_f.read().replace("\n", "").replace(" ", "")
input_f.close()

structure: json = json.loads(input)

structure["version"] = "3.3.0"


# default values
def default_value(base: dict, key):
    if not key in base:
        base[key] = 0

# basic events
for event in structure["basicEvents"]:
    default_value(event, "b")
    default_value(event, "i")

for event in structure["basicEventsData"]:
    default_value(event, "t")
    default_value(event, "i")
    default_value(event, "f")

# color boost events
for event in structure["colorBoostEvents"]:
    default_value(event, "b")
    default_value(event, "i")

for event in structure["colorBoostEvents"]:
    default_value(event, "b")

# waypoints
for event in structure["waypoints"]:
    default_value(event, "b")
    default_value(event, "i")
    
for event in structure["waypointsData"]:
    default_value(event, "x")
    default_value(event, "y")
    default_value(event, "d")

# index filters
for event in structure["waypointsData"]:
    default_value(event, "c")
    default_value(event, "f")
    default_value(event, "p")
    default_value(event, "t")
    default_value(event, "r")
    default_value(event, "n")
    default_value(event, "s")
    default_value(event, "l")
    default_value(event, "d")

# event box groups
event_box_groups = structure["eventBoxGroups"]
for index in range(len(event_box_groups)):
    event_box = event_box_groups[index]
    event_box_type = event_box["t"]

    default_value(event_box, "b")
    default_value(event_box, "g")
    # do not default t because t should already be defined 1-4
    if event_box_type == 0:
        print("warning: None type event box found")
    
    for e_box in event_box["e"]:
        default_value(e_box, "f")
        default_value(e_box, "e")

        for l_box in e_box["l"]:
            default_value(l_box, "b")
            default_value(l_box, "i")

# light color events
for event in structure["lightColorEventBoxes"]:
    default_value(event, "w")
    default_value(event, "d")
    default_value(event, "s")
    default_value(event, "t")
    default_value(event, "b")
    default_value(event, "e")

for event in structure["lightColorEvents"]:
    default_value(event, "p")
    default_value(event, "e")
    default_value(event, "c")
    default_value(event, "s")
    default_value(event, "f")
    default_value(event, "sb")
    default_value(event, "sf")

# light roation events
for event in structure["lightRotationEventBoxes"]:
    default_value(event, "w")
    default_value(event, "d")
    default_value(event, "s")
    default_value(event, "t")
    default_value(event, "b")
    default_value(event, "e")
    default_value(event, "a")
    default_value(event, "r")

for event in structure["lightRotationEvents"]:
    default_value(event, "p")
    default_value(event, "e")
    default_value(event, "r")
    default_value(event, "d")
    default_value(event, "l")

# light translation events
for event in structure["lightTranslationEventBoxes"]:
    default_value(event, "w")
    default_value(event, "d")
    default_value(event, "s")
    default_value(event, "t")
    default_value(event, "b")
    default_value(event, "e")

for event in structure["lightTranslationEvents"]:
    default_value(event, "p")
    default_value(event, "e")
    default_value(event, "t")

# fx events
for event in structure["fxEventBoxes"]:
    default_value(event, "w")
    default_value(event, "d")
    default_value(event, "s")
    default_value(event, "t")
    default_value(event, "b")
    default_value(event, "e")

for event in structure["floatFxEvents"]:
    default_value(event, "p")
    default_value(event, "e")
    default_value(event, "v")


# main stuff
def revertIndexStructure(V4_name, V4_data, V3_name):
    events_data = structure[V4_data]
    for index in range(len(structure[V4_name])):
        event = structure[V4_name][index]
        event_index = int(event["i"])
        del event["i"]
        structure[V4_name][index] = event | events_data[event_index]
    del structure[V4_data]
    if V4_name != V3_name:
        structure[V3_name] = structure[V4_name]
        del structure[V4_name]


# basic events
revertIndexStructure("basicEvents", "basicEventsData", "basicBeatmapEvents")


# boost color events
boost_events_data = structure["colorBoostEventsData"]
for index in range(len(boost_events_data)):
    boost_events_data[index]["o"] = boost_events_data[index]["b"] == 1
    del boost_events_data[index]["b"]
revertIndexStructure("colorBoostEvents", "colorBoostEventsData", "colorBoostBeatmapEvents")

# waypoints
revertIndexStructure("waypoints", "waypointsData", "waypoints")


def replace(base: list, fr: str, to: str):
    for struct in base:
        struct[to] = struct[fr]
        del struct[fr]


# event box groups
index_filters: json = structure["indexFilters"] # index filters are universal for all event boxes

# for type 1 (light color)
color_event_boxes = structure["lightColorEventBoxes"]
color_events = structure["lightColorEvents"]

replace(color_event_boxes, "s", "r")
replace(color_event_boxes, "e", "i")
replace(color_events, "p", "i")
for e in color_events: del e["e"] # v3 color events dont have easing

# for type 2 (light rotation)
rotation_event_boxes = structure["lightRotationEventBoxes"]
rotation_events = structure["lightRotationEvents"]

replace(rotation_event_boxes, "e", "i")

# for type 3 (light translation)
translation_event_boxes = structure["lightTranslationEventBoxes"]
translation_events = structure["lightTranslationEvents"]

replace(translation_event_boxes, "s", "r")
replace(translation_event_boxes, "e", "i")

# for type 4 (fx)
fx_event_boxes = structure["fxEventBoxes"]
fx_events = structure["floatFxEvents"]

structure["_fxEventsCollection"] = {
    "_fl": [], 
    "_il": []
} # why must v3 fx events be so quirky uwu and use index system for only this

fxfl_collection: list = structure["_fxEventsCollection"]["_fl"] # only access to floats
fxfl_event_index_tracker: int = 0 # used to track how many fx events have been created and 

replace(fx_event_boxes, "e", "i")

def get_event_box(id):
    match id:
        case 1: return color_event_boxes
        case 2: return rotation_event_boxes
        case 3: return translation_event_boxes
        case 4: return fx_event_boxes
def get_event(id):
    match id:
        case 1: return color_events
        case 2: return rotation_events
        case 3: return translation_events
        case 4: return fx_events
def get_name(id):
    match id:
        case 1: return "lightColorEventBoxGroups"
        case 2: return "lightRotationEventBoxGroups"
        case 3: return "lightTranslationEventBoxGroups"
        case 4: return "vfxEventBoxGroups"

for i in range(1, 5):
    structure[get_name(i)] = []

# event_box_groups = structure["eventBoxGroups"]
for index in range(len(event_box_groups)):
    event_box = event_box_groups[index]
    event_box_type = event_box["t"]

    new_body: dict = {}

    new_body["b"] = event_box["b"]
    new_body["g"] = event_box["g"]

    
    new_body["e"] = []
    # for each event box
    for e_body in event_box["e"]:
        new_e_body: dict = {}

        new_e_body["f"] = index_filters[e_body["f"]]
        new_e_body = new_e_body | get_event_box(event_box_type)[e_body["e"]]

        new_e_body["l"] = []
        # for event types 1-3
        if event_box_type != 4:
            # for each event
            for l_body in e_body["l"]:
                new_l_body: dict = {}

                new_l_body["b"] = l_body["b"]
                new_l_body = new_l_body | get_event(event_box_type)[l_body["i"]]
              
                new_e_body["l"].append(new_l_body)
            new_body["e"].append(new_e_body)

        # for event type 4 (fx events)
        if event_box_type == 4:
            for l_body in e_body["l"]:
                new_fl_event: dict = {}

                new_fl_event["b"] = l_body["b"]
                new_fl_event = new_fl_event | get_event(4)[l_body["i"]]

                fxfl_collection.append(new_fl_event)
                new_e_body["l"].append(fxfl_event_index_tracker)
                fxfl_event_index_tracker += 1
            new_body["e"].append(new_e_body)

    structure[get_name(event_box_type)].append(new_body)


# cleanup to remove unneeded stuff
del structure["eventBoxGroups"]
del structure["indexFilters"]
del structure["lightColorEventBoxes"]
del structure["lightColorEvents"]
del structure["lightRotationEventBoxes"]
del structure["lightRotationEvents"]
del structure["lightTranslationEventBoxes"]
del structure["lightTranslationEvents"]
del structure["fxEventBoxes"]
del structure["floatFxEvents"]



# file write
try: 
    output_f = open(output_path, "r")
    output_contents: json = json.loads(output_f.read())
    output_f.close()

    for key in structure:
        output_contents[key] = structure[key]
except:
    output_contents:json = structure


output: str = json.dumps(output_contents, separators=(',', ':'))
output.replace("True", "true")

o = open(output_path, "w")
o.write(output)
o.close()