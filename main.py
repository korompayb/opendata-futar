from flask import Flask, render_template
import json
import os
import requests

app = Flask(__name__)
routeID = 'BKK_1085'
    # Load and parse JSON data
vehicles_url = f"https://futar.bkk.hu/api/query/v1/ws/otp/api/where/route-details?routeId={routeID}&date=20210707&related=false&appVersion=1.1.abc&version=2&includeReferences=true&key=7ff7c954-05d3-4dd2-93b6-cb714dcdca69"
bkk_data = requests.get(vehicles_url)

def load_json_data():
    # Load JSON data from the static folder
    json_path = os.path.join(app.static_folder, 'trains.json')
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)
    return data

@app.route("/")
def index():

    

    
    
    # Extract route information
    route_info = {
        "shortName": bkk_data.json()['data']['entry']['shortName'],
        "color": bkk_data.json()['data']['entry']['style']['color'],
        "textColor": bkk_data.json()['data']['entry']['style']['icon']['textColor']  # Added textColor if needed
    }
    
    # Extract trip information
    trip_info = bkk_data.json()['data']['entry']['variants'][0]  # Assuming we only use the first variant for simplicity
    trip_info = {
        "tripHeadsign": trip_info['headsign']
    }
    
    # Extract stops
    stop_ids = bkk_data.json()['data']['entry']['variants'][0]['stopIds']
    stop_data = bkk_data.json()['data']['references']['stops']
    
    # Create stops list and handle potential missing IDs
    stops = []
    for stop_id in stop_ids:
        stop = stop_data.get(stop_id)
        if stop:
            stops.append({
                "id": stop["id"],  # Include the ID to match current_stop_id
                "name": stop["name"],
                "arrival_time": ""  # Placeholder for arrival time
            })

    # Sort stops based on the order of stopIds
    stops = sorted(stops, key=lambda x: stop_ids.index(x['id']))

    # Extract current stop index
    current_stop_id = stop_ids[0]  # Assuming the first stop is the current one
    current_stop_index = next((i for i, stop in enumerate(stops) if stop['id'] == current_stop_id), None)
    
   
    return render_template(
        "main.html",
        stops=stops,
        current_stop_index=current_stop_index,
        route_info=route_info,
        trip_info=trip_info
    )

















@app.route("/mav")
def mav():
    # Load and parse JSON data
    
    
    # Extract route information
    route_info = {
        "shortName": bkk_data.json()['data']['entry']['shortName'],
        "color": bkk_data.json()['data']['entry']['style']['color'],
        "textColor": bkk_data.json()['data']['entry']['style']['icon']['textColor']  # Added textColor if needed
    }
    
    # Extract trip information
    trip_info = bkk_data.json()['data']['entry']['variants'][0]  # Assuming we only use the first variant for simplicity
    trip_info = {
        "tripHeadsign": trip_info['headsign']
    }
    
    # Extract stops
    stop_ids = bkk_data.json()['data']['entry']['variants'][0]['stopIds']
    stop_data = bkk_data.json()['data']['references']['stops']
    
    # Create stops list and handle potential missing IDs
    stops = []
    for stop_id in stop_ids:
        stop = stop_data.get(stop_id)
        if stop:
            stops.append({
                "id": stop["id"],  # Include the ID to match current_stop_id
                "name": stop["name"],
                "arrival_time": ""  # Placeholder for arrival time
            })

    # Sort stops based on the order of stopIds
    stops = sorted(stops, key=lambda x: stop_ids.index(x['id']))

    # Extract current stop index
    current_stop_id = stop_ids[0]  # Assuming the first stop is the current one
    current_stop_index = next((i for i, stop in enumerate(stops) if stop['id'] == current_stop_id), None)
    
   
    return render_template(
        "máv.html",
        stops=stops,
        current_stop_index=current_stop_index,
        route_info=route_info,
        trip_info=trip_info
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
