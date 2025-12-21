import pytest
from visualizer import Visualizer
from map_loader import map_loader
import algorithms.astar
import algorithms.jps
import csv
import main
import random
import os

#random.seed("algo")

def test_random():
    maps = main.list_maps()
    maps.remove("3x3test")
    maps.remove("mymap")
    maps.remove("test_diagonal")
    maps.remove("test_diagonal_90")
    maps.remove("test_diagonal_180")
    maps.remove("test_diagonal_270")
    maps.remove("test_cardinal")
    maps.remove("test_cardinal_90")
    maps.remove("test_cardinal_180")
    maps.remove("test_cardinal_270")
    with open("test_report", "w") as file:
        writer = csv.writer(file, delimiter=';')
        for i in maps:
            map_data = map_loader(f"{i}.csv")
            counter = 0
            while counter <= 2:
                while True:
                    # Arvotaan satunnaisesti aloitus ja lopetus nodet
                    start_pos = (random.randint(0,1068), random.randint(0,1068))
                    end_pos = (random.randint(0,1068), random.randint(0,1068))
                    #Tarkistetaan, että valitut nodet eivät ole seiniä
                    if start_pos not in map_data and end_pos not in map_data:
                        #Tarkistetaan, että on tarpeeksi pitkä matka nodejen välillä
                        if algorithms.astar.h(start_pos, end_pos) > 500:
                            break
                # Ajetaan ensiksi JPS, koska se on nopeampi
                v = Visualizer(width=1100, rows=3, caption="testing", map_data=map_data, start_pos=start_pos, end_pos=end_pos)
                jps_time, jps_distance = v.run_algorithm(algorithms.jps.algorithm)
                # Jos polkua ei ole
                if jps_distance == "":
                    pass
                # Koska polku loytyi, aja astar myos.
                else:
                    jps_time = round(jps_time, 3)
                    jps_distance = round(jps_distance, 3)
                    v = Visualizer(width=1100, rows=3, caption="testing", map_data=map_data, start_pos=start_pos, end_pos=end_pos)
                    astar_time, astar_distance = v.run_algorithm(algorithms.astar.algorithm)
                    astar_time = round(astar_time, 3)
                    astar_distance = round(astar_distance, 3)
                    writer.writerow([(i, start_pos, end_pos, astar_time, jps_time, astar_distance, jps_distance)])
                    counter += 1
    assert os.path.isfile("test_report_fix.csv") == True