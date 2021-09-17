from utilities.mongodb import MongoDBClient
from utilities.ports_scanner import PortsScanner
from utilities.device_evaluator import DeviceEvaluator

clamp = lambda n, minn, maxn: max(min(maxn, n), minn)

def main():
    mongo_client = MongoDBClient()
    port_scanner = PortsScanner()
    device_evaluator = DeviceEvaluator()
    mongo_client.add_default_data_from_json()

    list_of_companies = ['AAAA','BBBB','CCCC','DDDD']
    for company in list_of_companies:
        add_module_to_company(mongo_client,port_scanner, device_evaluator, company)

    devices = mongo_client.find_devices()
    for device in devices:
        print("device id: %s , type: %s, brand: %s , rank:%s, old rank %s" % (device['_id'], device['type'], device['brand'], device['rank'], device.get('old_rank')))

def add_module_to_company(mongo_client:MongoDBClient, port_scanner:PortsScanner, device_evaluator: DeviceEvaluator, company):
    devices = mongo_client.find_devices(dict_to_query = {'domain': company})
    for device in devices:
        type = device['type']
        brand = device['brand']
        previous_rank = int(device['rank'])

        open_ports = port_scanner.scan_ports(device['ip'], type, brand, previous_rank)
        rank_diff = device_evaluator.evaluate_device(open_ports, type, brand)
        new_rank = clamp(previous_rank + rank_diff, 0, 100)
        mongo_client.update_device({'_id': device['_id']},
                                   {'rank': new_rank, 'old_rank': previous_rank, 'ports': open_ports})


def update_ports_evaluation(mongo_client:MongoDBClient, port_scanner:PortsScanner, device_evaluator: DeviceEvaluator, company):
    devices = mongo_client.find_devices(dict_to_query = {'domain': company})
    for device in devices:
        type = device['type']
        brand = device['brand']
        previous_rank = int(device['rank'])
        old_open_ports = device.get('ports') if device.get('ports') is not None else []

        open_ports = port_scanner.scan_ports(device['ip'], type, brand, previous_rank)
        difference_between_last_scan = set(open_ports).symmetric_difference(set(old_open_ports))
        if len(list(difference_between_last_scan)) > 0:
            rank_diff = device_evaluator.evaluate_device(open_ports, type, brand)
            new_rank = clamp(previous_rank + rank_diff, 0, 100)
            mongo_client.update_device({'_id': device['_id']}, {'rank': new_rank, 'old_rank': previous_rank, 'ports': open_ports})


if __name__ == "__main__":
    main()