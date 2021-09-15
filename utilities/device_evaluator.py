from utilities.mongodb import MongoDBClient
class DeviceEvaluator:
    def evaluate_device(self, open_ports, type, brand):
        mongo_client = MongoDBClient()
        ports = mongo_client.find_ports(brand, type)
        common_ports = ports['common_ports']
        special_ports = ports['special_ports']

        open_common_ports = set(open_ports).intersection(common_ports)
        open_specific_ports = set(open_ports).intersection(special_ports)

        s = open_common_ports.union(open_specific_ports)
        not_expected_ports = [x for x in open_ports if x not in s]

        certainty_delta = 0

        if len(common_ports) == 0:
            certainty_delta += 1
        elif(len(open_common_ports) == len(common_ports)):
            certainty_delta += 5
        else:
            certainty_delta -= 5

        if len(special_ports) == 0:
            certainty_delta += 0
        elif(len(open_specific_ports) == len(special_ports)):
            certainty_delta += 10
        elif len(open_specific_ports) > 0:
            certainty_delta += 5
        else:
            certainty_delta -= 1

        if len(not_expected_ports) > 0:
            #UPDATE LEARNING CYCLE
            certainty_delta -= 2

        return certainty_delta


