import pygame

# Värit
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Pixel:
    # Luokka ruuduille, jotka pygame sitten piirtää
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

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

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        # Alempana
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])
        # Ylempänä
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])
        # Oikealla
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])
        # Vasemmalla
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False


class Visualizer:
    # pygame luokka, joka visuaalisesti näyttää algoritmin edistymisen.
    def __init__(self, width=800, rows=50, caption="No_name_given"):
        pygame.init()
        self.width = width
        self.rows = rows
        self.win = pygame.display.set_mode((width, width))
        pygame.display.set_caption(caption)
        self.grid = self.make_grid(rows, width)
        self.start = None
        self.end = None

    def make_grid(self, rows, width):
        grid = []
        gap = width // rows
        for i in range(rows):
            grid.append([])
            for j in range(rows):
                spot = Pixel(i, j, gap, rows)
                grid[i].append(spot)
        return grid

    def draw_grid_lines(self):
        gap = self.width // self.rows
        for i in range(self.rows):
            pygame.draw.line(self.win, GREY, (0, i * gap), (self.width, i * gap))
            for j in range(self.rows):
                pygame.draw.line(self.win, GREY, (j * gap, 0), (j * gap, self.width))

    def draw(self):
        self.win.fill(WHITE)
        for row in self.grid:
            for spot in row:
                spot.draw(self.win)
        self.draw_grid_lines()
        pygame.display.update()

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

    def _update_all_neighbors(self):
        for row in self.grid:
            for spot in row:
                spot.update_neighbors(self.grid)

    def run(self, algorithm_callable):
        run = True
        while run:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if pygame.mouse.get_pressed()[0]:  # Vasen hiirinäppäin
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
    v = Visualizer()
    v.run(lambda draw, grid, start, end: None)