from queue import PriorityQueue
import time
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
    
    if drow == 0 and dcol != 0:  # Horisontaali liike
        return [(drow-1, dcol), (drow, dcol), (drow+1, dcol)]
    elif dcol == 0 and drow != 0:  # Vertikaali liike
        return [(drow, dcol-1), (drow, dcol), (drow, dcol+1)]
    else:  # Diagonaaali liike
        return [(drow, 0), (0, dcol), (drow, dcol)]
def jump_cardinal(current, direction, grid, draw):
    """
    Algoritmi funktio ei saa noden tutkimisen alussa lisätä nodea uudelleen listaan ennen liikettä,
    koska muuten se lisäisi tutkimiaan nodeja loputtomasti takaisin listaan. Toisaalta, kun hypitään
    viistoon, niin node pitää tarkastaa ennen horisontaalia tai vertikaalia liikettä, koska
    on tärkeää, että sama node voi olla useamman kerran open-setissä, eri suunnilla. Siksi tämä funktio,
    joka tarkistaa pakotetut naapurit ennen liikettä, ja sitten jatkaa normaalisti.
    """
    draw()
    drow, dcol = direction
    next_row = current.row + drow
    next_col = current.col + dcol
    if current.detect_forced_neighbors(grid, drow, dcol):
            return current, 0, None
    # Palauta none, jos olet reunan ulkopuolella
    if not (0 <= next_row < current.total_rows and 0 <= next_col < current.total_rows):
        return None, 0, None
    next_node = grid[next_row][next_col]
    if next_node.is_barrier():
        return None, 0, None
    # Tarkista jos next_node on seinä
    while not next_node.is_barrier():
        draw()
        # Palauta maali, jos on
        if next_node.is_end():
            return next_node, 0, None
        
        if next_node.is_empty():
            next_node.make_jump()

        # Palauta, jos löytyy pakotettu naapuri 
        if (next_node.detect_forced_neighbors(grid, drow, dcol) and dcol == 0) or (next_node.detect_forced_neighbors(grid, drow, dcol) and drow == 0):
                return next_node, 0, None
        next_row = next_node.row + drow
        next_col = next_node.col + dcol

        if not (0 <= next_row < current.total_rows and 0 <= next_col < current.total_rows):
            return None, 0, None
            
            # Jatka hyppyä samaan suuntaan.
        next_node = grid[next_row][next_col]
    
    return None, 0, None
    
def jump(current, direction, grid, draw):
    draw()
    drow, dcol = direction
    next_row = current.row + drow
    next_col = current.col + dcol
    distance = 0.0

    # Palauta none, jos olet reunan ulkopuolella
    if not (0 <= next_row < current.total_rows and 0 <= next_col < current.total_rows):
        return None, 0, None, None
    # Palauta none, jos olet seinässä
    next_node = grid[next_row][next_col]
    if next_node.is_barrier():
        return None, 0, None, None

    # cardinaali-suunta, jota pidetään yllä palautusta varten
    came_direction = None

    # Recursiivinen hyppy loop
    while not next_node.is_barrier():
        # Liikkeen "pituus" (viisto ~ sqrt2)
        distance += 1.414 if (drow != 0 and dcol != 0) else 1.0

        # Palauta maali, jos on
        if next_node.is_end():
            return next_node, distance, None, None
        
        # Maalaa hyppyruutu harmaaksi
        if next_node.is_empty():
            next_node.make_jump()

        # Jos löydetään pakotettu naapuri -> tämä on jump point.
        if next_node.detect_forced_neighbors(grid, drow, dcol):
            if drow == 0 or dcol == 0:
                came_direction = (drow, dcol)  # kardinaal liike
            return next_node, distance, None, came_direction

        # Jos liike on viisto, niin lähetä vertikaali, ja horisontaali hyppytarkistukset.
        # Tarkista ensin pystysuora ja vaakasuora hyppy erikseen.
        if drow != 0 and dcol != 0:
            # vertikaali hyppy
            vertical_result = jump_cardinal(next_node, (drow, 0), grid, draw)
            if vertical_result is not None and vertical_result[0] is not None:
                # Kirjataan, että jump point löydettiin vertikaaliliikkeen aikana
                came_direction = (drow, 0)
                # Koska horisontaali liike jäi tekemättä, palautetaan kolmantena elementtinä
                # additional_cardinal
                return next_node, distance, (0, dcol), came_direction

            # Horisontaali hyppy
            horizontal_result = jump_cardinal(next_node, (0, dcol), grid, draw)
            if horizontal_result is not None and horizontal_result[0] is not None:
                came_direction = (0, dcol)
                #Koska ei suuntia jäljellä, palauta 3. elementtinä None
                return next_node, distance, None, came_direction

        # Jatketaan samaan suuntaan.
        next_row = next_node.row + drow
        next_col = next_node.col + dcol
        # Poistu jos hyppy on reunan ulkopuolella
        if not (0 <= next_row < current.total_rows and 0 <= next_col < current.total_rows):
            return None, 0, None, None

        next_node = grid[next_row][next_col]

    return None, 0, None, None



def algorithm(draw, grid, start, end):
    start_time = time.time()
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
    additional_cardinal = None
    open_set_hash = {start}

    while not open_set.empty():
        current = open_set.get()[2]
        open_set_hash.remove(current)
        #time.sleep(2)
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            end_time = time.time()
            print(f"Resolved in {end_time - start_time} seconds")
            return True
        if current in came_from:
            parent_dir = came_from[current][1]
            valid_directions = get_pruned_directions(parent_dir)
        else:
            # Kaikki suunnat, jos olet aloitus-spotissa
            valid_directions = [(1,1), (1,-1), (1,0), (0,1), (0,-1), (-1,1), (-1,0), (-1,-1),]
        for direction in valid_directions:
            # Jos suunta on kardinaali, niin käytä sitä
            if abs(direction[0]) + abs(direction[1]) < 2:
                default_cardinal_direction = direction
            else:
                default_cardinal_direction = None

            jump_point, jump_distance, additional_cardinal, came_dir = jump(current, direction, grid, draw)

            if jump_point is not None:
                use_came_dir = came_dir if came_dir is not None else default_cardinal_direction

                temp_g_score = g_score[current] + jump_distance
                if temp_g_score < g_score[jump_point]:
                    came_from[jump_point] = (current, use_came_dir)
                    g_score[jump_point] = temp_g_score
                    f_score[jump_point] = temp_g_score + h(jump_point.get_pos(), end.get_pos())
                    if jump_point not in open_set_hash:
                        count += 1
                        open_set.put((f_score[jump_point], count, jump_point))
                        open_set_hash.add(jump_point)
                        jump_point.make_open()

                # Ehkä tarpeellinen
                """
                if additional_cardinal is not None:
                    ap, adist, dont_use, came_dir2 = jump(current, additional_cardinal, grid, draw)
                    if ap is not None:
                        temp_g_score = g_score[current] + adist
                        # when adding this additional JP, we want came_dir to be the additional_cardinal itself
                        came_from[ap] = (current, additional_cardinal)
                        g_score[ap] = temp_g_score
                        f_score[ap] = temp_g_score + h(ap.get_pos(), end.get_pos())
                        if ap not in open_set_hash:
                            count += 1
                            open_set.put((f_score[ap], count, ap))
                            open_set_hash.add(ap)
                            ap.make_open()
                """
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