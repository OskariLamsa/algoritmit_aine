from queue import PriorityQueue
from time import sleep

def h(p1, p2):
    #Eucdlidian distance heuristiikka
    x1, y1 = p1
    x2, y2 = p2
    x_distance = abs(x1 - x2)
    y_distance = abs(y1 - y2)
    return max(x_distance,y_distance) + (0.414)*min(x_distance, y_distance)


def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current][0]
        current.make_path()
        draw()
def get_pruned_directions(parent_dir):
    drow, dcol = parent_dir
    
    if drow == 0 and dcol != 0:  # Horizontal (left/right)
        return [(drow-1, dcol), (drow, dcol), (drow+1, dcol)]
        # e.g., (0,1) → [(-1,1), (0,1), (1,1)] ✓
    elif dcol == 0 and drow != 0:  # Vertical (up/down)
        return [(drow, dcol-1), (drow, dcol), (drow, dcol+1)]
    else:  # Diagonal
        return [(drow, 0), (0, dcol), (drow, dcol)]
    
def jump(current, direction, grid, draw):
    draw()
    drow, dcol = direction
    next_row = current.row + drow
    next_col = current.col + dcol
    distance = 0

    # Palauta none, jos olet reunan ulkopuolella
    if not (0 <= next_row < current.total_rows and 0 <= next_col < current.total_rows):
        return None, 0, []
    next_node = grid[next_row][next_col]
    if next_node.is_barrier():
        return None, 0, []
    # Tarkista jos next_node on seinä
    while not next_node.is_barrier():
        distance += 1.414 if (drow != 0 and dcol != 0) else 1.0
        # Palauta maali, jos on
        if next_node.is_end():
            return next_node, distance, []
        
        if next_node.is_empty():
            next_node.make_jump()

        # Palauta, jos löytyy pakotettu naapuri 
        #if next_node.detect_forced_neighbors(grid, drow, dcol):
        #        return next_node, distance
        forced_dirs = next_node.get_forced_neighbor_directions(grid, drow, dcol)
        if forced_dirs:
            return next_node, distance, forced_dirs
        # Jos liike on diagonaali, niin lähetä vertikaali, ja horisontaali hypyt.
        if drow != 0 and dcol != 0:    
            if jump(next_node, (drow, 0), grid, draw)[0] is not None or \
            jump(next_node, (0, dcol), grid, draw)[0] is not None:
                return next_node, distance, []
            
        next_row = next_node.row + drow
        next_col = next_node.col + dcol

        if not (0 <= next_row < current.total_rows and 0 <= next_col < current.total_rows):
            return None, 0, []
            
            # Jatka hyppyä samaan suuntaan.
        next_node = grid[next_row][next_col]
    
    return None, 0, []


def algorithm(draw, grid, start, end):
    # jps algoritmi
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
        if current in came_from:
            parent, parent_dir = came_from[current]
            valid_directions = get_pruned_directions(parent_dir)
            if hasattr(current, 'forced_neighbors') and current.forced_neighbors:
                for i in current.forced_neighbors:
                    if i not in valid_directions:
                        valid_directions.append(i)
        else:
            # Kaikki suunnat, jos olet aloitus-spotissa
            valid_directions = [(1,1), (1,-1), (1,0), (0,1), (0,-1), (-1,1), (-1,0), (-1,-1),]
        for direction in valid_directions:
            jump_point, jump_distance, forced_list = jump(current, direction, grid, draw)
            if jump_point is not None:
                if forced_list:
                    print(f"I saw forced neigbors! {jump_point.get_pos()}: {forced_list}")
                    jump_point.forced_neighbors = list(forced_list)
                else:
                    jump_point.forced_neighbors = []

                temp_g_score = g_score[current] + jump_distance
                if temp_g_score < g_score[jump_point]:
                    came_from[jump_point] = (current, direction)
                    g_score[jump_point] = temp_g_score
                    f_score[jump_point] = temp_g_score + h(jump_point.get_pos(), end.get_pos())
                    if jump_point not in open_set_hash:
                        count += 1
                        open_set.put((f_score[jump_point], count, jump_point))
                        open_set_hash.add(jump_point)
                        jump_point.make_open()
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
        print("Called jps without a map file. Defaulting to empty map.")
        custom_rows = int(input("How big would you like the grid to be? "))
        v = Visualizer(width=1100, rows=custom_rows, caption="JPS", map_data=map_data)
        v.run(algorithm)
    else:
        print("Called jps with map_data" \
        "")
        map_data = sys.argv[1]
        map_data = map_loader(map_data)
        v = Visualizer(width=1100, rows=250, caption="JPS", map_data=map_data)
        v.run(algorithm)