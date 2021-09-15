from utilities.mongodb import MongoDBClient
# DB client is only for Mock purposes

class PortsScanner:
    def scan_ports(self, ip, type, brand, rank):
        mongo_client = MongoDBClient()
        ports = mongo_client.find_ports(brand, type)
        if rank > 35:
            return ports['common_ports'] + ports['special_ports']
        if rank > 10:
            return ports['common_ports']
        else:
            return ["9999"]

