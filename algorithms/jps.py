from queue import PriorityQueue
import time
def h(p1, p2):
    #Eucdlidian distance heuristiikka
    x1, y1 = p1
    x2, y2 = p2
    x_distance = abs(x1 - x2)
    y_distance = abs(y1 - y2)
    return max(x_distance,y_distance) + (0.414)*min(x_distance, y_distance)

def is_walkable(grid, r, c):
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    return 0 <= r < rows and 0 <= c < cols and not grid[r][c].is_barrier()

def has_forced_neighbor(node, drow, dcol, grid):
    r, c = node.row, node.col
    # Vertikaali liike
    if drow != 0 and dcol == 0:
        # Vasen puoli on seinä, sen takana tyhjä tila JA oman liikkeen suunnassa tyhjä tila myös
        if (not is_walkable(grid, r, c - 1)
            and is_walkable(grid, r + drow, c - 1)
            and is_walkable(grid, r + drow, c)):
            return True
        # Sama oikealle puolelle
        if (not is_walkable(grid, r, c + 1)
            and is_walkable(grid, r + drow, c + 1)
            and is_walkable(grid, r + drow, c)):
            return True
        return False

    # Horisontaali liike
    if dcol != 0 and drow == 0:
        # Ylhäällä seinä, sen takana tyhjä tila JA oman liikkeen suunnassa tyhjä tila myös
        if (not is_walkable(grid, r - 1, c)
            and is_walkable(grid, r - 1, c + dcol)
            and is_walkable(grid, r, c + dcol)):
            return True
        # Sama alas
        if (not is_walkable(grid, r + 1, c)
            and is_walkable(grid, r + 1, c + dcol)
            and is_walkable(grid, r, c + dcol)):
            return True
        return False

    # Viisto
    if drow != 0 and dcol != 0:
        if (not is_walkable(grid, r - drow, c)
            and is_walkable(grid, r - drow, c + dcol)
            and is_walkable(grid, r, c + dcol)):
            return True

        if (not is_walkable(grid, r, c - dcol)
            and is_walkable(grid, r + drow, c - dcol)
            and is_walkable(grid, r + drow, c)):
            return True

        return False

    return False

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        parent_entry = came_from[current]
        parent = parent_entry[0]
        current = parent
        current.make_path()
        draw()
def get_pruned_directions(parent_dir):
    drow, dcol = parent_dir
    
    if drow == 0 and dcol != 0:  # Horisontaali liike
        return [(drow, dcol)]
    elif dcol == 0 and drow != 0:  # Vertikaali liike
        return [(drow, dcol)]
    else:  # Viisto liike
        return [(drow, 0), (0, dcol), (drow, dcol)]
    
def jump(current, direction, grid, draw):
    """
    Palauttaa (jump_point, distance, forced_dirs)
    - forced_dirs on lista suuntia, jotka on tulevaisuudessa tutkittava pakotettujen naapurien takia
      Ne lisätään pää-algoritmissa kyseisen noden forced-listaan.
    """
    draw()
    drow, dcol = direction
    rows = len(grid)
    cols = len(grid[0]) if rows else 0

    next_row = current.row + drow
    next_col = current.col + dcol

    # Jos olet reunan ulkopolella tai seinässä, lähde heti
    if not (0 <= next_row < rows and 0 <= next_col < cols):
        return None, 0, []
    next_node = grid[next_row][next_col]
    if next_node.is_barrier():
        return None, 0, []
    distance = 0.0

    while True:
        # Nosta liikkeen maksua. +1 kardinaalista ja +1.414... viistosta
        distance += 1.41421356237 if (drow != 0 and dcol != 0) else 1.0

        draw()
        # Viistoliike päättyy tähän jos molemmat sen suunnan edessä olevat on barrier
        # Tämä siksi, että JP:t pitää olla saavutettavissa kardinaaliliikkein, ei siis
        # Viistohyppyjä seinien läpi
        if drow != 0 and dcol != 0:
            vertical_clear = is_walkable(grid, next_row + drow, next_row)
            horizontal_clear = is_walkable(grid, next_col, next_col + dcol)
            if not vertical_clear and not horizontal_clear:
                return None, 0, []
        # Jos olet maalissa, palaa
        if next_node.is_end():
            return next_node, distance, []

        # Merkataan harmaaksi visualisoinnin vuoksi
        if next_node.is_empty():
            next_node.make_jump()

        # Pakotettujen naaprien tarkastus
        if has_forced_neighbor(next_node, drow, dcol, grid):
            # Pakotettuja naapureita löytynyt. Lasketaan niiden pakottamat suunnat.
            forced_dirs = []
            r, c = next_node.row, next_node.col

            # Viisto
            if (not is_walkable(grid, r - drow, c)
                and is_walkable(grid, r - drow, c + dcol)
                and is_walkable(grid, r, c + dcol)):
                forced_dirs.append((-drow, dcol))

            if (not is_walkable(grid, r, c - dcol)
                and is_walkable(grid, r + drow, c - dcol)
                and is_walkable(grid, r + drow, c)):
                forced_dirs.append((drow, -dcol))

            # Horisontaali liike
            elif drow == 0 and dcol != 0:
                if (not is_walkable(grid, r - 1, c)
                    and is_walkable(grid, r - 1, c + dcol)
                    and is_walkable(grid, r, c + dcol)):
                    forced_dirs.append((-1, dcol))
                
                if (not is_walkable(grid, r + 1, c)
                    and is_walkable(grid, r + 1, c + dcol)
                    and is_walkable(grid, r, c + dcol)):
                    forced_dirs.append((1, dcol))

            # Vertikaali liike
            elif drow != 0 and dcol == 0:
                if (not is_walkable(grid, r, c - 1)
                    and is_walkable(grid, r + drow, c - 1)
                    and is_walkable(grid, r + drow, c)):
                    forced_dirs.append((drow, -1))
                
                if (not is_walkable(grid, r, c + 1)
                    and is_walkable(grid, r + drow, c + 1)
                    and is_walkable(grid, r + drow, c)):
                    forced_dirs.append((drow, 1))

            return next_node, distance, forced_dirs

        # Jos liike on viisto, laukaise kardinaalisuuntiin hypyt. Jos ne päättyy JP:en,
        # niin palauta tämä viisto node.
        if drow != 0 and dcol != 0:
            # Vertikaali
            jp_vert, dist_vert, forced_v = jump(next_node, (drow, 0), grid, draw)
            if jp_vert is not None:
                forced_dirs = forced_v if forced_v else []
                # Vertikaali hyppy löysi JP:n, joten palauta tämä viisto node
                return next_node, distance, forced_dirs

            # Horisontaali
            jp_horz, dist_horz, forced_h = jump(next_node, (0, dcol), grid, draw)
            if jp_horz is not None:
                forced_dirs = forced_h if forced_h else []
                # Horisontaali hyppy löysi JP:n, joten palauta tämä viisto node
                return next_node, distance, forced_dirs

        # Seuraava node suunnassa
        next_row = next_node.row + drow
        next_col = next_node.col + dcol

        # Jos olet reunan ulkopuolella niin älä edes yritä
        if not (0 <= next_row < rows and 0 <= next_col < cols):
            return None, 0, []
        # Äläkä jos olisit seinässä
        next_node = grid[next_row][next_col]
        if next_node.is_barrier():
            return None, 0, []
        # Tai jos tämä olisi laiton viisto-hyppy seinien läpi
        if drow != 0 and dcol != 0:
            neighbor1 = grid[next_row+drow][next_col]
            neighbor2 = grid[next_row][next_col + dcol]
            if neighbor1.is_barrier() and neighbor2.is_barrier():
                return None, 0, []

def algorithm(draw, grid, start, end):
    start_time = time.time()
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}

    rows = len(grid)
    # Aseta alussa kaikkien nodejen g- ja f-score loputtomaksi.
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
            end_time = time.time()
            print(f"Resolved in {end_time - start_time} seconds")
            return True

        if current in came_from:
            parent_dir = came_from[current][1]
            if parent_dir is None:
                # Jos nodella ei parentia, nin anna kaikki suunnat
                valid_directions = [(1,1), (1,-1), (1,0), (0,1), (0,-1), (-1,1), (-1,0), (-1,-1)]
            else:
                valid_directions = get_pruned_directions(parent_dir)

            # Jos löytyy forced_directions, niin lisätään ne nyt.
            parent_entry = came_from.get(current)
            if parent_entry and len(parent_entry) >= 3:
                forced_dirs = parent_entry[2] or []
                for fd in forced_dirs:
                    if fd not in valid_directions:
                        valid_directions.append(fd)
        else:
            # Kaikki suunnat, koska olet aloitusruudussa
            valid_directions = [(1,1), (1,-1), (1,0), (0,1), (0,-1), (-1,1), (-1,0), (-1,-1)]
        for direction in valid_directions:
            # Hyppy
            jump_point, jump_distance, forced_dirs = jump(current, direction, grid, draw)
            # Seuraava if-lause pysäyttää suuntien laskennan jos löysit endin
            if jump_point is not None and jump_point == end:
                # Laita sanakirjaan tieto siitä, mistä nodesta siihen päästiin, suunta, ja forced_dir
                came_from[jump_point] = (current, direction, forced_dirs)
                reconstruct_path(came_from, end, draw)
                end.make_end()
                end_time = time.time()
                print(f"Resolved in {end_time - start_time} seconds")
                return True
            # Jos JP ei ollut end
            elif jump_point is not None:
                temp_g_score = g_score[current] + jump_distance
                if temp_g_score < g_score[jump_point]:
                    # Laita sanakirjaan tieto siitä, mistä nodesta siihen päästiin, suunta, ja forced_dir
                    came_from[jump_point] = (current, direction, forced_dirs)
                    g_score[jump_point] = temp_g_score
                    f_score[jump_point] = temp_g_score + h(jump_point.get_pos(), end.get_pos())
                    if jump_point not in open_set_hash:
                        count += 1
                        open_set.put((f_score[jump_point], count, jump_point))
                        open_set_hash.add(jump_point)
                        jump_point.make_open()


            draw()
            #time.sleep(0.2)
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