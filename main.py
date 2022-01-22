"""
Data Structures:
child_files_data => dictionary with keys as child file objects, and values as
                    child file data

"""
from file import File
import material
import json
import os

master_material_info_db = {}

master_file_name = "000_yaris_dynamic_roof_crush_01.k"
master_file_path = r"D:\Learning\Computer Science\Projects\Input Validator\zip-for-download"
output_file_path = r"D:\Learning\Computer Science\Projects\Input Validator\zip-for-download"

# Create master_file object
master_file = File(master=True, filename=master_file_name, filepath=master_file_path)

# List to store master_file_data
master_file_data = master_file.get_file_data()

# Dictionary to store child_files objects
child_files_with_data = {}  # key => file object, value => file_data

# List with child filenames extracted from master file
child_filenames = master_file.get_filenames(master_file_data)
print(child_filenames)

# Create child_file objects for each file in *INCLUDE card
for file in child_filenames:
    key = File(master=False, filename=file, filepath=master_file_path)
    child_files_with_data[key] = key.get_file_data()

material_info = {}
for child_file, input_data in child_files_with_data.items():
    material_info[str(child_file)] = material.get_material_info(input_data)

output_file = os.path.join(output_file_path, "Report.txt")
with open(output_file, 'w') as outputFile:
    outputFile.write(json.dumps(material_info, indent=4, sort_keys=False))

# print(master_file.get_filenames(master_file_data))
# print(child_files_with_data.keys())
