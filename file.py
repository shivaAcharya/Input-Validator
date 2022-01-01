"""
Data Structures:
get_filenames => list of filenames => Ex. ["Yaris..", "roof_crush_impactor"]
get_material_info => If MAT card has $ property, return dictionary of dictionaries
                        material_info = {mat_card_name : {mat_property : mat_value}}
                        Ex. {"PIECEWISE_LINEAR_PLASTICITY": [{"mid": 200001, "ro": 7.89E-9}, {"mid": 20002,...}]}
                    Otherwise, returns dictionary with property N/A.
                        Ex. {"RIGID": [{"N/A": 1, "N/A": 7.6E-9, "N/A" 200.00, "N/A": 0.3, "N/A": 0.0]}
"""

#TODO: #1 Look for better data structure for get_material_info method.
#TOD0: #2 Better way to exit while loop


import os

class File:
    def __init__(self, master, filename, filepath):  # master -> True for Master File
        self.master = master
        self.filename = filename
        self.filepath = filepath

    # Get File data list with each line as one element
    def get_file_data(self):
        ""
        input_file_data = []
        file_filename_path = os.path.join(self.filepath, self.filename)
        with open(file_filename_path) as input_file:
            input_file_data = input_file.readlines()
            return input_file_data

    # Get Filenames if master
    def get_filenames(self, input_file_data):
        """ Return list of filenames under INCLUDE card of master file"""
        file_list = []
        if not self.master:
            return []
        for line, data in enumerate(input_file_data):
            if data.startswith("*INCLUDE"):
                file_list.append(input_file_data[line + 1].rstrip("\n"))
        return file_list

    # Get Material Info
    def get_material_info(self, input_data):
        """ Returns dictionary of dictionaries if MAT card has property"""
        material_info = {}

        for line, data in enumerate(input_data):
            mat_property_value = {}

            # For MAT Card
            if data.startswith('*MAT'):
                # Do this until next card or section is reached
                mat_card_name = ""
                while input_data[line+1].startswith('$#'): # or input_data[line+1].startswith(" "):
                    mat_card_name = data.lstrip("*MAT_").rstrip("\n")
                    # Multi line material property
                    if input_data[line + 1].startswith('$#'):
                        mat_property = input_data[line + 1].lstrip('$#').split()
                        mat_value = input_data[line + 2].split()
                    # One line material property
                    elif input_data[line + 1].startswith('$'):
                        mat_property = input_data[line + 1].lstrip('$').split()
                        mat_value = input_data[line + 2].split()
                    # If no comment, put N/A for property
                    else:
                        mat_property = ["N/A"] * len(input_data[line+1])
                        mat_value = input_data[line + 1].split()

                    if len(mat_property) > 0:
                        # If not used present:
                        if len(mat_property) > len(mat_value):
                            mat_property[-2] = mat_property[-2] + " " + mat_property[-1]
                            mat_property.pop()

                        # Store property and value for each Mat Card
                        mat_property_value_one_line = {}
                        for i, card_property in enumerate(mat_property):
                            mat_property_value_one_line[card_property] = mat_value[i]
                        mat_property_value |= mat_property_value_one_line

                    line += 2

                material_info[mat_card_name] = material_info.get(mat_card_name, []) + [mat_property_value]


        return material_info



