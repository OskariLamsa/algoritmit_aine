import pygame
from time import sleep

# Colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Spot:

    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = col * width
        self.y = row * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        self._mark_dirty_cb = None

    def set_mark_dirty(self, cb):
        self._mark_dirty_cb = cb

    def _mark_dirty(self):
        if self._mark_dirty_cb:
            self._mark_dirty_cb(self)

    def get_pos(self):
        return self.row, self.col

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.width)
    def is_empty(self):
        return self.color == WHITE

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE
        self._mark_dirty()

    def make_start(self):
        self.color = ORANGE
        self._mark_dirty()

    def make_closed(self):
        self.color = RED
        self._mark_dirty()

    def make_open(self):
        self.color = GREEN
        self._mark_dirty()

    def make_barrier(self):
        self.color = BLACK
        self._mark_dirty()

    def make_end(self):
        self.color = TURQUOISE
        self._mark_dirty()
        
    def make_jump(self):
        self.color = GREY
        self._mark_dirty()

    def make_path(self):
        self.color = PURPLE
        self._mark_dirty()

    def draw(self, surface):
        surface.fill(self.color, self.get_rect())

    def check_barrier(self, grid, direction):
        match direction:
            case "right":
                if self.col < self.total_rows - 1 and grid[self.row][self.col + 1].is_barrier():
                    return True
            case _:
                return False
    def is_valid_and_walkable(self, grid, drow, dcol):
        # Tarkista, onko haluttu paikka ruudukon sisällä, ja onko se valkoinen, tai maali
        new_row = self.row + drow
        new_col = self.col + dcol
        
        if 0 <= new_row < self.total_rows and 0 <= new_col < self.total_rows:
            return not grid[new_row][new_col].is_barrier() and not grid[new_row][new_col].is_closed()
        return False

    def get_neighbor(self, grid, drow, dcol):
        # Palauta naapuri-spot jos on
        new_row = self.row + drow
        new_col = self.col + dcol
        
        if 0 <= new_row < self.total_rows and 0 <= new_col < self.total_rows:
            return grid[new_row][new_col]
        return None

    def update_neighbors(self, grid):
        self.neighbors = []
        directions = [
            (1, 0),   # Alas
            (-1, 0),  # Ylös
            (0, 1),   # Oikea
            (0, -1),  # Vasen
            (1, 1),   # Alas-oikea
            (1, -1),  # Alas-vasen
            (-1, 1),  # Ylös-oikea
            (-1, -1)  # Ylös-vasen
        ]
        
        for drow, dcol in directions:
            if self.is_valid_and_walkable(grid, drow, dcol):
                self.neighbors.append(self.get_neighbor(grid, drow, dcol))
    def get_forced_neighbor_directions(self, grid, drow, dcol):
        """Returns list of forced neighbor directions"""
        forced = []
        
        # Horizontal movement
        if drow == 0 and dcol != 0:
            if (not self.is_valid_and_walkable(grid, -1, 0) and 
                self.is_valid_and_walkable(grid, -1, dcol)):
                forced.append((-1, dcol))
            if (not self.is_valid_and_walkable(grid, 1, 0) and 
                self.is_valid_and_walkable(grid, 1, dcol)):
                forced.append((1, dcol))
        
        # Vertical movement
        elif dcol == 0 and drow != 0:
            if (not self.is_valid_and_walkable(grid, 0, -1) and 
                self.is_valid_and_walkable(grid, drow, -1)):
                forced.append((drow, -1))
            if (not self.is_valid_and_walkable(grid, 0, 1) and 
                self.is_valid_and_walkable(grid, drow, 1)):
                forced.append((drow, 1))
        
        # Diagonal up-right
        elif drow == -1 and dcol == 1:
            if (not self.is_valid_and_walkable(grid, 0, -1) and 
                self.is_valid_and_walkable(grid, -1, -1)):
                forced.append((-1, -1))
            if (not self.is_valid_and_walkable(grid, 1, 0) and 
                self.is_valid_and_walkable(grid, 1, 1)):
                forced.append((1, 1))
        
        # Diagonal up-left
        elif drow == -1 and dcol == -1:
            if (not self.is_valid_and_walkable(grid, 0, 1) and 
                self.is_valid_and_walkable(grid, -1, 1)):
                forced.append((-1, 1))
            if (not self.is_valid_and_walkable(grid, 1, 0) and 
                self.is_valid_and_walkable(grid, 1, -1)):
                forced.append((1, -1))
        
        # Diagonal down-right
        elif drow == 1 and dcol == 1:
            if (not self.is_valid_and_walkable(grid, 0, -1) and 
                self.is_valid_and_walkable(grid, 1, -1)):
                forced.append((1, -1))
            if (not self.is_valid_and_walkable(grid, -1, 0) and 
                self.is_valid_and_walkable(grid, -1, 1)):
                forced.append((-1, 1))
        
        # Diagonal down-left
        elif drow == 1 and dcol == -1:
            if (not self.is_valid_and_walkable(grid, 0, 1) and 
                self.is_valid_and_walkable(grid, 1, 1)):
                forced.append((1, 1))
            if (not self.is_valid_and_walkable(grid, -1, 0) and 
                self.is_valid_and_walkable(grid, -1, -1)):
                forced.append((-1, -1))
        
        return forced
    """
    def detect_forced_neighbors(self, grid, drow, dcol):
        # Tarkistaa pakotetut naapurit, ottaen huomioon liikkumissuunnan
        # Horisontaali liike
        if drow == 0 and dcol != 0:
            if (not self.is_valid_and_walkable(grid, -1, 0) and 
                self.is_valid_and_walkable(grid, -1, dcol)):
                return True
            if (not self.is_valid_and_walkable(grid, 1, 0) and 
                self.is_valid_and_walkable(grid, 1, dcol)):
                return True
        # Vertikaali liike
        elif dcol == 0 and drow != 0:
            if (not self.is_valid_and_walkable(grid, 0, -1) and 
                self.is_valid_and_walkable(grid, drow, -1)):
                return True
            if (not self.is_valid_and_walkable(grid, 0, 1) and 
                self.is_valid_and_walkable(grid, drow, 1)):
                return True
        # Diagonaal ylös-oikealle
        elif drow == -1 and dcol == 1:
            if (not self.is_valid_and_walkable(grid, 0, -1) and 
                self.is_valid_and_walkable(grid, -1, -1)):
                return True
            if (not self.is_valid_and_walkable(grid, 1, 0) and 
                self.is_valid_and_walkable(grid, 1, 1)):
                return True
        # Diagonaali ylös-vasemmalle
        elif drow == -1 and dcol == -1:
            if (not self.is_valid_and_walkable(grid, 0, 1) and 
                self.is_valid_and_walkable(grid, -1, 1)):
                return True
            if (not self.is_valid_and_walkable(grid, 1, 0) and 
                self.is_valid_and_walkable(grid, 1, -1)):
                return True
        # Diagonaali alas-oikealle
        elif drow == 1 and dcol == 1:
            if (not self.is_valid_and_walkable(grid, 0, -1) and 
                self.is_valid_and_walkable(grid, 1, -1)):
                return True
            if (not self.is_valid_and_walkable(grid, -1, 0) and 
                self.is_valid_and_walkable(grid, -1, 1)):
                return True
        # Diagonaali alas-vasemalle
        elif drow == 1 and dcol == -1:
            if (not self.is_valid_and_walkable(grid, 0, 1) and 
                self.is_valid_and_walkable(grid, 1, 1)):
                return True
            if (not self.is_valid_and_walkable(grid, -1, 0) and 
                self.is_valid_and_walkable(grid, -1, -1)):
                return True
        return False
    """            
    def __lt__(self, other):
        return False


class Visualizer:
    def __init__(self, width=800, rows=50, caption="No name given.", map_data=None):
        if map_data == None:
            print("debug: I am visualizer, and I did not get map_data.")
            self.rows = rows
        else:
            print("debug: I am visualizer, and I received map_data.")
            self.rows = int(map_data[0][0])
        pygame.init()
        self.width = width
        self.win = pygame.display.set_mode((width, width))
        pygame.display.set_caption(caption)

        self.grid = self.make_grid(self.rows, width)
        self.start = None
        self.end = None

        self.background = pygame.Surface((width, width)).convert()
        self._render_background()
        self._dirty_rects = set()
        self._initial_drawn = False
        self._draw_map_barriers(map_data)

    def _draw_map_barriers(self, map_data):
        for i in map_data[1:]:
            spot = self.grid[i[0]][i[1]]
            spot.make_barrier()

    def _render_background(self):
        self.background.fill(WHITE)

    def make_grid(self, rows, width):
        grid = []
        gap = width // rows
        for i in range(rows):
            grid.append([])
            for j in range(rows):
                spot = Spot(i, j, gap, rows)
                spot.set_mark_dirty(lambda s=spot: self.mark_dirty(s))
                grid[i].append(spot)
        return grid

    def mark_dirty(self, spot):
        rect = spot.get_rect()
        self._dirty_rects.add((rect.x, rect.y, rect.w, rect.h))

    def draw(self):
        if not self._initial_drawn:
            self.win.blit(self.background, (0, 0))
            for row in self.grid:
                for spot in row:
                    spot.draw(self.win)
            pygame.display.flip()
            self._initial_drawn = True
            self._dirty_rects.clear()
            return

        if not self._dirty_rects:
            return

        rects_to_update = []
        for x, y, w, h in list(self._dirty_rects):
            src_rect = pygame.Rect(x, y, w, h)
            self.win.blit(self.background, (x, y), src_rect)
            rects_to_update.append(src_rect)
            
            gap = self.width // self.rows
            r = min(y // gap, self.rows - 1)
            c = min(x // gap, self.rows - 1)
            
            if 0 <= r < self.rows and 0 <= c < self.rows:
                self.grid[r][c].draw(self.win)

        self._dirty_rects.clear()

        pygame.display.update(rects_to_update)

    def get_clicked_pos(self, pos):
        gap = self.width // self.rows
        x, y = pos
        row = y // gap
        col = x // gap
        return row, col

    def reset_grid(self):
        self.start = None
        self.end = None
        self.grid = self.make_grid(self.rows, self.width)
        self._initial_drawn = False

    def _update_all_neighbors(self):
        for row in self.grid:
            for spot in row:
                spot.update_neighbors(self.grid)

    def run(self, algorithm_callable):
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(120)
            self.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if pygame.mouse.get_pressed()[0]: #Vasen hiirinäppäin
                    pos = pygame.mouse.get_pos()
                    row, col = self.get_clicked_pos(pos)
                    if 0 <= row < self.rows and 0 <= col < self.rows:
                        spot = self.grid[row][col]
                        if not self.start and spot != self.end:
                            self.start = spot
                            self.start.make_start()
                        elif not self.end and spot != self.start:
                            self.end = spot
                            self.end.make_end()
                        elif spot != self.end and spot != self.start:
                            spot.make_barrier()
                    else:
                        print(f"OUT OF BOUNDS! row={row}, col={col}, self.rows={self.rows}")

                elif pygame.mouse.get_pressed()[2]:  # Oikea hiirinäppäin
                    pos = pygame.mouse.get_pos()
                    row, col = self.get_clicked_pos(pos)
                    if 0 <= row < self.rows and 0 <= col < self.rows:
                        spot = self.grid[row][col]
                        spot.reset()
                        if spot == self.start:
                            self.start = None
                        elif spot == self.end:
                            self.end = None

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.start and self.end:
                        self._update_all_neighbors()
                        algorithm_callable(lambda: self.draw(), self.grid, self.start, self.end)
                    if event.key == pygame.K_c:
                        self.reset_grid()

        pygame.quit()


if __name__ == "__main__":
    try:
        from astar import algorithm
    except Exception:
        algorithm = lambda draw, grid, start, end: None

    v = Visualizer(width=800, rows=250, caption="Incremental Visualizer Demo")
    v.run(algorithm)
