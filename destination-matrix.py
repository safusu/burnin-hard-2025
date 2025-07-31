import googlemaps
import csv
import os
from dotenv import load_dotenv

def parse_time(time: str):
    parts = time.split(" ")
    if "hour" in time:
        return int(parts[0])*60 + int(parts[2])
    else:
        return int(parts[0])

load_dotenv()

gmaps = googlemaps.Client(key=os.getenv("API_KEY"))

# List of sources (campgrounds)
# List of destinations-1 (places to work)
# List of destinations-2 (plces to recreate)

# Go from source to destination-1, then from destination-1 to destination-2

# Go from source to destination-2 with destination-1 as a secondary waypoint (Hard to visualize since it's a 3D matrix)
origins = [
    {
        "name": "Belk Library & Information Commons",
        "link": 'https://maps.google.com/?cid=7922941740508531071',
        "address": '218 College St, Boone, NC 28607'
    },
    {
        "name": "Blowing Rock Community Library",
        "link": "https://maps.google.com/?cid=3123170376393942156",
        "address": '1022 Main St, Blowing Rock, NC 28605'
    },
    {
        "name": "Avery County Public Library",
        "link": "https://maps.google.com/?cid=6333430848061830071",
        "address": '150 Library Road, Newland, NC 28657'
    },
    {
        "name": "Ashe County Public Library",
        "link": "https://maps.google.com/?cid=15366723538443277807",
        "address": "148 Library Dr, West Jefferson, NC 28694"
    }
]
destinations = [
    {
        "name": "Grandfather Mountain State Park",
        "link": "https://maps.google.com/?cid=13465009727551890838",
        "address": '9872 Highway 105 South, Banner Elk, NC 28604'
    },
    {
        "name": "The Blowing Rock",
        "link": "https://maps.google.com/?cid=571609647164462331",
        "address": '432 The Rock Rd, Blowing Rock, NC 28605'
    },
    {
        "name": "Elk Knob State Park",
        "link": "https://maps.google.com/?cid=5675832616437957340",
        "address": '5564 Meat Camp Rd, Todd, NC 28684'
    },
    {
        "name": "Mount Jefferson State Natural Area",
        "link": "https://maps.google.com/?cid=3511155376946601472",
        "address": '1481 Mt Jefferson Rd, West Jefferson, NC 28694'
    },
    {
        "name": "Elk Shoals New River State Park",
        "link": "https://maps.google.com/?cid=2248739972622955810",
        "address": "349 Methodist Camp Rd, West Jefferson, NC 28694"
    },
    {
        "name": "New River State Park",
        "link": "https://maps.google.com/?cid=6560696066801570497",
        "address": "358 New River State Park Rd, Laurel Springs, NC 28644"
    },
    {
        "name": "Rendezvous Mountain State Park",
        "link": "https://maps.google.com/?cid=8203334465362831444",
        "address": "1956 Rendezvous Mountain Rd, Purlear, NC 28665"
    }
]

origin_addresses = [x["address"] for x in origins]
destination_addresses = [x["address"] for x in destinations]
destination_links = [x["link"] for x in destinations]

matrix_result = gmaps.distance_matrix(origin_addresses, destination_addresses, mode="driving", units="imperial")

with open("distance_matrix.csv", 'w') as f:
    writer = csv.writer(f)
    writer.writerow([" "]  + destination_links)
    for i, origin in enumerate(origins):
        durations = []
        dest = []
        for j, destination in enumerate(destinations):
            element = matrix_result["rows"][i]["elements"][j]
            distance = element["distance"]["text"]
            duration = parse_time(element["duration"]["text"])
            print(f"From {origin["address"]} to {destination["address"]}: Distance - {distance}, Duration - {duration} mins")
            durations.append(duration)
        writer.writerow([origin["link"]] + durations)

print("A")
