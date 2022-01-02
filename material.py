"""
Data Structures:
get_filenames => list of filenames => Ex. ["Yaris..", "roof_crush_impactor"]
get_material_info => Ignore property of Material and just extract material value for now
                        material_info = {mat_card_name : [mat_value]}
                        Ex. {"PIECEWISE_LINEAR_PLASTICITY": [[200001, 7.89E-9], [20002,...]]}

"""

# TODO: #1 Look for better data structure for get_material_info method.
# TOD0: #2 Better way to exit while loop


# Get Material Info
def get_material_info(input_data):
    """ Returns dictionary of dictionaries if MAT card has property"""
    material_info = {}

    for line, data in enumerate(input_data):
        mat_property_value = {}

        # For MAT Card
        if data.startswith('*MAT'):
            # Do this until next card or section is reached
            mat_card_name = ""
            while input_data[line + 1].startswith('$#'):  # or input_data[line+1].startswith(" "):
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
                    mat_property = ["N/A"] * len(input_data[line + 1])
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
