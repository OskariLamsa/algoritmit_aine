import os
import csv

def map_loader(file_name):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_dir, "maps_data")
    if not os.path.isdir(path):
        return print("maps_data not found")
    #try:
    with open(os.path.join(path, file_name), "r") as f:
        print("Found file ", file_name)
        map_data = []
        for line in f:
            parts = line.strip().split(";")
            if len(parts) != 2:
                continue
            else:
                map_data.append((float(parts[0]), float(parts[1])))
        return map_data
    #except:
        #print("Could not find file ", file_name)

if __name__ == "__main__":
    map_loader("Berlin_0_1024.csv")