from Head import *

class Main:
    def __init__(self, game):
        self.game = game
        self.main = game.main = self
        self.dict = copy.deepcopy(main_dict)

    def load(self):
        self.load_dict()
        self.load_class()
        self.load_state()
        self.load_tile()

    def load_dict(self):
        self.tile_size = self.dict["tile_size"]
        self.color_move = self.dict["color_move"]
        self.color_range = self.dict["color_range"]
        self.color_danger = self.dict["color_danger"]
        self.color_enemy = self.dict["color_enemy"]
        self.transparency_move = self.dict["transparency_move"]
        self.transparency_range = self.dict["transparency_range"]
        self.transparency_danger = self.dict["transparency_danger"]
        self.transparency_enemy = self.dict["transparency_enemy"]
        self.border_enemy = self.dict["border_enemy"]

    def load_class(self):
        self.class_map = Map(self.game, self)
        self.class_units = Units(self.game, self)
        self.class_cursor = Cursor(self.game, "default")
        self.class_state = s0_title(self.game)

    def load_state(self):
        self.s1_select = s1_select(self.game)
        self.s2_menu_unit = s2_menu_unit(self.game)

    def load_tile(self):
        self.tile_move_surface = self.compute_tile_surface(self.tile_size, self.color_move, self.transparency_move)
        self.tile_range_surface = self.compute_tile_surface(self.tile_size, self.color_range, self.transparency_range)
        self.tile_danger_surface = self.compute_tile_surface(self.tile_size, self.color_danger, self.transparency_danger)
        self.tile_enemy_surface = self.compute_tile_surface(self.tile_size, self.color_enemy, self.transparency_enemy, self.border_enemy)

    def new(self):
        self.current_menu = "title"

    # -------------------- #
    @staticmethod
    def compute_tile_surface(size, color, transparency, border=0):
        rect = (0, 0, size[0], size[1])
        surface = pygame.Surface(size)
        surface.set_alpha(transparency)
        pygame.draw.rect(surface, color, rect, border)
        return surface

    # -------------------- #
    def init_title(self):
        self.current_menu = "title"
        self.class_state = s0_title(self.game)

    def init_level(self, level):
        self.current_menu = "level"
        self.class_map.init(level)
        self.class_units.init(level)

    # -------------------- #
    def update(self):
        if self.current_menu == "title":
            self.class_state.update()
        elif self.current_menu == "level":
            self.class_map.update()
            self.class_state.update()
            self.class_cursor.update()
            self.class_units.update()


    def draw(self):
        if self.current_menu == "title":
            self.class_state.draw()
        elif self.current_menu == "level":
            self.class_map.draw()
            self.class_state.draw()
            self.class_cursor.draw()
            self.class_units.draw()
