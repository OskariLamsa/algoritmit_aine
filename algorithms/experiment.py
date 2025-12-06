import time
from queue import PriorityQueue

# Directions (4-way)
DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # (dr, dc): down, up, right, left

def in_bounds(r, c, grid):
    return 0 <= r < len(grid) and 0 <= c < len(grid[0])

def is_walkable(r, c, grid):
    return in_bounds(r, c, grid) and not grid[r][c].is_barrier()

def get_node(grid, r, c):
    return grid[r][c]

def manhattan(a_pos, b_pos):
    (ar, ac) = a_pos
    (br, bc) = b_pos
    return abs(ar - br) + abs(ac - bc)

def reconstruct_path(came_from, current, draw):
    # re-use your existing reconstruct_path if you have one; this is placeholder
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

# -------------------------
# Jump Point Search helpers
# -------------------------

def find_neighbors_jps(node, parent, grid):
    """
    Prune neighbors based on direction of travel (parent -> node).
    If no parent (start), return all walkable neighbors.
    Works for 4-directional movement.
    """
    neighbors = []
    r, c = node.get_pos()  # assume get_pos returns (row, col)

    if parent is None:
        # at start: return all walkable direct neighbors
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if is_walkable(nr, nc, grid):
                neighbors.append(get_node(grid, nr, nc))
        return neighbors

    pr, pc = parent.get_pos()
    dr = r - pr
    dc = c - pc
    # normalize to direction (-1, 0, 1)
    dr = 0 if dr == 0 else (1 if dr > 0 else -1)
    dc = 0 if dc == 0 else (1 if dc > 0 else -1)

    # For JPS pruning in cardinal moves:
    if dr != 0:  # moving vertically (up/down)
        # try forward
        nr, nc = r + dr, c
        if is_walkable(nr, nc, grid):
            neighbors.append(get_node(grid, nr, nc))
        # forced neighbors: left or right if those cells are walkable while the cell diagonally (behind) is blocked
        # Check left
        if is_walkable(r, c - 1, grid) and not is_walkable(r - dr, c - 1, grid):
            neighbors.append(get_node(grid, r, c - 1))
        # Check right
        if is_walkable(r, c + 1, grid) and not is_walkable(r - dr, c + 1, grid):
            neighbors.append(get_node(grid, r, c + 1))
    else:  # dc != 0 : moving horizontally (left/right)
        nr, nc = r, c + dc
        if is_walkable(nr, nc, grid):
            neighbors.append(get_node(grid, nr, nc))
        # forced neighbors: up or down
        if is_walkable(r - 1, c, grid) and not is_walkable(r - 1, c - dc, grid):
            neighbors.append(get_node(grid, r - 1, c))
        if is_walkable(r + 1, c, grid) and not is_walkable(r + 1, c - dc, grid):
            neighbors.append(get_node(grid, r + 1, c))

    # Deduplicate and return only walkable nodes
    unique = []
    seen = set()
    for n in neighbors:
        pos = n.get_pos()
        if pos not in seen and not n.is_barrier():
            seen.add(pos)
            unique.append(n)
    return unique

def has_forced_neighbor(r, c, dr, dc, grid):
    """
    Simplified forced neighbor detection for 4-way JPS.
    Returns True if there is any forced neighbor at (r,c) given we moved into (r,c) with direction (dr,dc).
    The condition used is a pragmatic/standard one for 4-way JPS:
      - if moving horizontally, there is a forced neighbor if a vertical neighbor is walkable while
        the cell diagonally behind that vertical neighbor is blocked.
      - if moving vertically, symmetric logic applies.
    """
    if dr != 0:  # moving vertically
        # check left
        if is_walkable(r, c - 1, grid) and not is_walkable(r - dr, c - 1, grid):
            return True
        # check right
        if is_walkable(r, c + 1, grid) and not is_walkable(r - dr, c + 1, grid):
            return True
    else:  # moving horizontally
        if is_walkable(r - 1, c, grid) and not is_walkable(r - 1, c - dc, grid):
            return True
        if is_walkable(r + 1, c, grid) and not is_walkable(r + 1, c - dc, grid):
            return True
    return False

def jump(from_node, dr, dc, grid, end):
    """
    Jump from from_node in direction (dr, dc) until:
      - we reach the end -> return that node
      - we hit a non-walkable cell -> return None
      - we find a forced neighbor -> return the jump point node
      - otherwise continue jumping
    Returns Spot or None.
    IMPORTANT: This is a 4-directional JPS jump function (no diagonals).
    """
    r, c = from_node.get_pos()
    nr, nc = r + dr, c + dc

    # step once first
    while True:
        if not in_bounds(nr, nc, grid):
            return None
        if grid[nr][nc].is_barrier():
            return None

        node = get_node(grid, nr, nc)

        # reached goal?
        if node == end:
            return node

        # check whether this node has forced neighbors (pruning rule) -> then it's a jump point
        if has_forced_neighbor(nr, nc, dr, dc, grid):
            return node

        # continue stepping
        nr += dr
        nc += dc

# -------------------------
# JPS-aware algorithm
# -------------------------

def jps_algorithm(draw, grid, start, end):
    """
    Jump Point Search integrated with an A* open set.
    Assumptions:
      - grid is 2D list of Spot-like objects with methods: get_pos(), is_barrier(), make_open(), make_closed(), make_end(), etc.
      - movement is 4-directional (up/down/left/right).
      - Heuristic used here: Manhattan distance.
    Notes:
      - This implementation prunes neighbors using find_neighbors_jps().
      - It calls jump() for each pruned neighbor to discover jump points and only inserts the jump points into the open set.
      - The jump function is a 4-way recursive/iterative jump (no diagonal jumps included).
    """

    start_time = time.time()
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}

    # g and f as in your original A*
    g_score = {pixel: float("inf") for row in grid for pixel in row}
    g_score[start] = 0
    f_score = {pixel: float("inf") for row in grid for pixel in row}
    f_score[start] = manhattan(start.get_pos(), end.get_pos())

    open_set_hash = {start}
    parent = {}  # parent map used for neighbor pruning (parent[child] = parent_node)

    while not open_set.empty():
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            end_time = time.time()
            print(f"Resolved in {end_time - start_time} seconds")
            return True

        # Determine parent for pruning
        par = parent.get(current, None)

        # Prune neighbors according to JPS rules
        neighbors = find_neighbors_jps(current, par, grid)

        for nbr in neighbors:
            # determine direction from current to neighbor as unit vector
            cr, cc = current.get_pos()
            nr, nc = nbr.get_pos()
            dr = nr - cr
            dc = nc - cc
            dr = 0 if dr == 0 else (1 if dr > 0 else -1)
            dc = 0 if dc == 0 else (1 if dc > 0 else -1)

            # perform jump along (dr, dc)
            jump_node = jump(current, dr, dc, grid, end)
            if jump_node is None:
                continue

            # compute tentative g for jump_node as g(current) + distance(current->jump_node)
            jr, jc = jump_node.get_pos()
            dist = abs(jr - cr) + abs(jc - cc)  # since 4-way, Manhattan distance equals step count
            temp_g_score = g_score[current] + dist

            if temp_g_score < g_score[jump_node]:
                came_from[jump_node] = current
                parent[jump_node] = current  # parent used for further pruning (we jumped to jump_node from current)
                g_score[jump_node] = temp_g_score
                f_score[jump_node] = temp_g_score + manhattan(jump_node.get_pos(), end.get_pos())

                if jump_node not in open_set_hash:
                    count += 1
                    open_set.put((f_score[jump_node], count, jump_node))
                    open_set_hash.add(jump_node)
                    jump_node.make_open()

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
        v.run(jps_algorithm)
    else:
        print("Called jps with map_data" \
        "")
        map_data = sys.argv[1]
        map_data = map_loader(map_data)
        v = Visualizer(width=1100, rows=250, caption="JPS", map_data=map_data)
        v.run(jps_algorithm)