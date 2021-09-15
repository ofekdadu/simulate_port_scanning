import pymongo
from utilities.json_parser import get_data_from_json, get_ports_from_json

class MongoDBClient:
  def __init__(self):
    self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    self.mydb = self.myclient["mydatabase"]
    self.devices = self.mydb["devices"]
    self.ports = self.mydb["ports"]

  def add_default_data_from_json(self):
    self.devices.drop()
    self.ports.drop()
    self.insert_devices_to_db(get_data_from_json())
    self.insert_ports_to_db(get_ports_from_json())

  def insert_devices_to_db(self, input):
    x = self.devices.insert_many(input)
    print("processed devices to db")

  def insert_ports_to_db(self, input):
    x = self.ports.insert_many(input)
    print("processed ports to db")

  def find_devices(self, dict_to_query=None):
    if dict_to_query == None:
      return self.devices.find()
    return self.devices.find(dict_to_query)

  def find_ports(self, brand, type):
    key = '%s&%s' % (brand, type)
    return self.ports.find_one({'key': key})

  def update_device(self, query, values):
    new_values = {"$set": values}
    self.devices.update_one(query, new_values)
