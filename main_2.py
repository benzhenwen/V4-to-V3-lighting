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
except:
    print("basic events failed")


# boost color events
try:
    boost_events_data = structure["colorBoostEventsData"]
    for index in range(len(boost_events_data)):
        boost_events_data[index]["o"] = boost_events_data[index]["b"] == 1
        del boost_events_data[index]["b"]
    revertIndexStructure("colorBoostEvents", "colorBoostEventsData", "colorBoostBeatmapEvents")

except:
    print("boost events failed")

# waypoints
try:
    revertIndexStructure("waypoints", "waypointsData", "waypoints")
except:
    print("basic events failed")



# event box groups (actually fml what is this shit)
event_box_groups = structure["eventBoxGroups"]
for index in range(len(event_box_groups)):
    event_box = structure



print(structure)