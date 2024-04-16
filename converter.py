import json


# input_path: str = input("input file path: ")
# output_path: str = input("output file path: ")

input_path: str = "test.txt"

# file read
input_f = open(input_path, "r")
input = input_f.read().replace("\n", "").replace(" ", "")
input_f.close()

structure: json = json.loads(input)


def revertIndexStructure(V4_name, V4_data, V3_name):
    events_data = structure[V4_data]
    for index in range(len(structure[V4_name])):
        event = structure[V4_name][index]
        event_index = int(event["i"])
        del event["i"]
        structure[V4_name][index] = event | events_data[event_index]
    del structure[V4_data]
    if V4_name != V3_name:
        structure[V3_name] = structure[V4_name].pop()
        del structure[V4_name]


# basic events
try:
    revertIndexStructure("basicEvents", "basicEventsData", "basicBeatmapEvents")
except Exception as e: print(e)


# boost color events
try:
    boost_events_data = structure["colorBoostEventsData"]
    for index in range(len(boost_events_data)):
        boost_events_data[index]["o"] = boost_events_data[index]["b"] == 1
        del boost_events_data[index]["b"]
    revertIndexStructure("colorBoostEvents", "colorBoostEventsData", "colorBoostBeatmapEvents")
except Exception as e: print(e)

# waypoints
try:
    revertIndexStructure("waypoints", "waypointsData", "waypoints")
except Exception as e: print(e)



# event box groups
index_filters: json = structure["indexFilters"] # index filters are universal for all event boxes

# for type 1 (light color)
color_event_boxes = structure["lightColorEventBoxes"]
color_events = structure["lightColorEvents"]

# for type 2 (light rotation)
rotation_event_boxes = structure["lightRotationEventBoxes"]
rotation_events = structure["lightRotationEvents"]

# for type 3 (light translation)
translation_event_boxes = structure["lightTranslationEventBoxes"]
translation_events = structure["lightTranslationEvents"]

# for type 4 (fx)
fx_event_boxes = structure["fxEventBoxes"]
fx_events = structure["floatFxEvents"]

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

event_box_groups = structure["eventBoxGroups"]
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
        if event_box_type == 1 or event_box_type == 3: # type 1 and 3 replace "s" with "r"
            new_e_body["r"] = new_e_body["s"]
            del new_e_body["s"]
        new_e_body["i"] = new_e_body["e"] # rename easing e -> i
        del new_e_body["e"]

        new_e_body["l"] = []
        # for each event
        for l_body in e_body["l"]:
            new_l_body: dict = {}

            new_l_body["b"] = l_body["b"]
            new_l_body = new_l_body | get_event(event_box_type)[l_body["i"]]
            

        new_body["e"].append(new_e_body)
        
print(structure)