"""
Data Structures:
get_filenames => list of filenames => Ex. ["Yaris..", "roof_crush_impactor"]
get_material_info => Ignore property of Material and just extract material value for now
                        material_info = {"filename": {mat_card_name : [(TITLE,) mat_value]}
                        Ex. {"filename": {"PIECEWISE_LINEAR_PLASTICITY": [[200001, 7.89E-9], [20002,...]]}}

"""

long_format = False


# Get Material Info
def get_material_info(input_data):
    """ Returns dictionary with MAT Card name as keys and List of material values as values"""
    global long_format
    material_info = {}
    step = 10
    for line, data in enumerate(input_data):
        if data.rstrip("\n").lower() == "*KEYWORD LONG=Y":
            long_format = True
            step = 20

        # For MAT Card
        if data.startswith('*MAT'):
            # Do this until next card or section is reached
            mat_card_name = data.rstrip("\n")

            mat_value = []
            # Skip the line if TEST
            if input_data[line].endswith("TITLE"):
                mat_value.append([input_data[line+1].rstrip("\n")])
                line += 1

            # Populate mat_value
            while input_data[line + 1].startswith('$') and input_data[line+2].startswith(" "):
                for i in range(0, len(input_data[line+2].rstrip("\n")), step):
                    mat_value.append(input_data[line+2][i:i+step])

                line += 2

            # # If no comments
            while input_data[line + 1].startswith(' '):
                for i in range(0, len(input_data[line + 1].rstrip("\n")), step):
                    mat_value.append(input_data[line + 1][i:i + step])
                line += 1

            # Store mat name and value for each Mat Card
            if mat_card_name not in material_info:
                material_info[mat_card_name] = [mat_value]
            else:
                material_info[mat_card_name].append(mat_value)

    return material_info
