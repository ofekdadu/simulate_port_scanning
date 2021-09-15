import json
import os

def get_data_from_json():
    list_of_devices = []
    directory = "RawJsonFiles"
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            f = open(os.path.join(directory, filename))
            data = json.load(f)
            domain = data.get('smp-domain') if data.get('smp-domain') is not None else data.get('domain')
            gw_identifier = data.get('gw_identifier')
            for device in data['iot_stats']:
                device_destination_services = device['destination_services']
                device_info = device['device']
                mydict = {
                            "ip": "1.2.3.4",
                            "MAC": "1234",
                            "gw_identifier": gw_identifier,
                            "domain": domain,
                            "GroupName": device_info.get('GroupName'),
                            "_id": device_info.get('ID'),
                            "brand": device_info.get('brand'),
                            "hash_id": device_info.get('hash-id'),
                            "model": device_info.get('model') if device_info.get('model') is not None else "",
                            "name": device_info.get('name'),
                            "rank": device_info.get('rank'),
                            "type": device_info.get('type'),
                            "vendor": device_info.get('vendor'),
                            "destination_services": device_destination_services
                        }
                list_of_devices.append(mydict)
            f.close()
    return list_of_devices

def get_ports_from_json():
    directory = "PortsMap"
    filename = "ports.json"
    f = open(os.path.join(directory, filename))
    data = json.load(f)
    ports = data['ports']
    f.close()
    return ports


get_ports_from_json()