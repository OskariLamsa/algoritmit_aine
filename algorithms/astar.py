from queue import PriorityQueue
from time import sleep
from math import sqrt

def h(p1, p2):
    #Manhattan distance -tyylinen heuristiikka
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)
"""
def h(p1, p2):
    #Eucdlidian distance -kokeilu
    x1, y1 = p1
    x2, y2 = p2
    x_distance = abs(x1 - x2)
    y_distance = abs(y1 - y2)
    return max(x_distance,y_distance) + (0.5)*min(x_distance, y_distance)
"""

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


def algorithm(draw, grid, start, end):
    # a* algoritmi
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}

    # algoritmin alussa asetetaan jokaisen pikselin g- ja f-arvoksi loputon.
    g_score = {pixel: float("inf") for row in grid for pixel in row}
    g_score[start] = 0
    f_score = {pixel: float("inf") for row in grid for pixel in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        #sleep(0.03)
        draw()

        if current != start:
            current.make_closed()

    return False


if __name__ == "__main__":
    import sys
    from visualizer import Visualizer
    from map_loader import map_loader
    map_data = None
    if len(sys.argv) < 2:
        print("Called astar without a map file. Defaulting to empty map.")
        custom_rows = int(input("How big would you like the grid to be? "))
        v = Visualizer(width=1100, rows=custom_rows, caption="a*", map_data=map_data)
        v.run(algorithm)
    else:
        print("Called astar with map_data" \
        "")
        map_data = sys.argv[1]
        map_data = map_loader(map_data)
<<<<<<< HEAD
        v = Visualizer(width=1100, rows=250, caption="a*", map_data=map_data)
        v.run(algorithm)
=======
    v = Visualizer(width=1100, rows=250, caption="a*", map_data=map_data)
    v.run(algorithm)
>>>>>>> 1116691dfa7601048a09c74f96241b856129d049
