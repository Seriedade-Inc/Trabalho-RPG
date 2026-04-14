class Grid:
    def __init__(self, width, height, tile_size=32):
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.tiles = [[None for _ in range(width)] for _ in range(height)]

    def in_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def is_walkable(self, x, y):
        return self.in_bounds(x, y) and self.tiles[y][x] is None

    def place_actor(self, actor):
        if self.is_walkable(actor.x, actor.y):
            self.tiles[actor.y][actor.x] = actor
            return True
        return False

    def move_actor(self, actor, new_x, new_y):
        if self.is_walkable(new_x, new_y):
            self.tiles[actor.y][actor.x] = None
            actor.x = new_x
            actor.y = new_y
            self.tiles[new_y][new_x] = actor
            return True
        return False
