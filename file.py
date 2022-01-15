import os


class File:
    def __init__(self, master, filename, filepath):  # master -> True for Master File
        self.master = master
        self.filename = filename
        self.filepath = filepath

    def __str__(self):
        return self.filename

    # Get File data list with each line as one element
    def get_file_data(self):
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
