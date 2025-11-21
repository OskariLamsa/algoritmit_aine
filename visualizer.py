import pygame
import time

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
        self.x = row * width
        self.y = col * width
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

    def make_path(self):
        self.color = PURPLE
        self._mark_dirty()

    def draw(self, surface):
        surface.fill(self.color, self.get_rect())

    def update_neighbors(self, grid):
        self.neighbors = []
        # Alas
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])
        # Ylös
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])
        # Oikea
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])
        # Vasen
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False


class Visualizer:
    def __init__(self, width=800, rows=50, caption="No name given."):
        pygame.init()
        self.width = width
        self.rows = rows
        self.win = pygame.display.set_mode((width, width))
        pygame.display.set_caption(caption)

        self.grid = self.make_grid(rows, width)
        self.start = None
        self.end = None

        self.background = pygame.Surface((width, width)).convert()
        self._render_background()
        self._dirty_rects = set()
        self._initial_drawn = False

    def _render_background(self):
        self.background.fill(WHITE)
        gap = self.width // self.rows
        for i in range(self.rows):
            pygame.draw.line(self.background, GREY, (0, i * gap), (self.width, i * gap))
            for j in range(self.rows):
                pygame.draw.line(self.background, GREY, (j * gap, 0), (j * gap, self.width))

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
            row = x // (self.width // self.rows)
            col = y // (self.width // self.rows)
            gap = self.width // self.rows
            r = x // gap
            c = y // gap
            if 0 <= r < self.rows and 0 <= c < self.rows:
                self.grid[r][c].draw(self.win)

        self._dirty_rects.clear()

        pygame.display.update(rects_to_update)

    def get_clicked_pos(self, pos):
        gap = self.width // self.rows
        y, x = pos
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

    v = Visualizer(width=800, rows=50, caption="Incremental Visualizer Demo")
    v.run(algorithm)
