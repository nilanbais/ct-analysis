"""
Script voor het bekijken van het verschil in grootte memory size van een JSON vs een BSON (Binary JSON)

Conclusie
Het maakt voor onderstaand script niet uit of het als json of binary wordt opgeslagen.
JSON File Size is : 553859 bytes
BSON File Size is : 553859 bytes
"""
import os
import json
import bson
from cta_classes.base_classes.json_handling_class import JsonHandler

json_handler = JsonHandler()

folder_name = './res'
test_file_name = 'known_crypto_symbols'
json_file_name = test_file_name + '.json'
bson_file_name = test_file_name + '.bson'

# Create a BSON file of the JSON file
data = json_handler.read_json(file_name=json_file_name, folder_name=folder_name)

encoded_data = json.dumps(data).encode('utf_8')
print(type(encoded_data))

for i in range(20):
    print(encoded_data[i])

json_handler.store_bson(bson_data=encoded_data, file_name=bson_file_name, folder_name=folder_name)

json_file_size = os.path.getsize(os.path.join(folder_name, json_file_name))
bson_file_size = os.path.getsize(os.path.join(folder_name, bson_file_name))

print("JSON File Size is :", json_file_size, "bytes")
print("BSON File Size is :", bson_file_size, "bytes")