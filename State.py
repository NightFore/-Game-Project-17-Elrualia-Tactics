from Head import *

class s0_title:
    def __init__(self, game):
        self.game, self.main = game, game.main
        self.buttons = Buttons(self.game, self.game.button_dict, "title", self)

    def new_game(self):
        self.main.init_level("chapter_prologue")
        self.main.class_state = self.main.s1_select

    def get_keys(self):
        for event in self.game.event:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_z:
                    self.buttons.compute_button_index(-1)
                if event.key == pygame.K_s:
                    self.buttons.compute_button_index(1)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    if self.buttons.current_button is not None:
                        self.buttons.current_button.compute_action()

    def update(self):
        self.get_keys()
        self.buttons.update()

    def draw(self):
        self.buttons.draw()

class s1_select:
    def __init__(self, game):
        self.game, self.main = game, game.main
        self.class_cursor = self.main.class_cursor

        # Variable
        # self.all_units = self.main.class_units.all_units
        self.current_unit = None
        self.selected_enemies = []
        self.map_danger = None

    def select_target(self, x, y):
        # Target = Unit on a specific position
        target = self.main.class_units.search_unit(x, y)
        if self.current_unit is None:
            # Unit
            if target is not None and target.team == "player":
                self.current_unit = target
                self.current_unit.load_map()
                self.class_cursor.init_path(self.current_unit)
            # Enemy
            elif target is not None and target.team == "enemy":
                self.select_enemy(target)

            # Terrain
            else:
                pass
        else:
            # Self
            if target is self.current_unit:
                self.main.class_state = self.main.s2_menu_unit
                self.main.class_state.current_unit = self.current_unit

            # Terrain
            elif target is None:
                self.current_unit.compute_movement(x, y)

            # Enemy
            elif target is not None and True:
                # Move
                offset = int([x, y] == self.class_cursor.path[-1])
                pos = self.class_cursor.path[-1 - offset]
                self.current_unit.compute_movement(pos[0], pos[1])

                # Attack
                self.current_unit.compute_attack(target)

            # Ally
            elif target is not None and False:
                pass

            self.current_unit = None
            self.class_cursor.init_path()

    def get_keys(self):
        for event in self.game.event:
            # Move
            if event.type == pygame.KEYDOWN:
                index_images, dx, dy = 0, 0, 0
                if event.key == pygame.K_s:
                    index_images, dy = 0, 1
                if event.key == pygame.K_a or event.key == pygame.K_q:
                    index_images, dx = 1, -1
                if event.key == pygame.K_d:
                    index_images, dx = 2, 1
                if event.key == pygame.K_w or event.key == pygame.K_z:
                    index_images, dy = 3, -1

                # Cursor
                self.class_cursor.compute_pos(dx, dy)

                # Unit
                if self.current_unit is not None:
                    # self.current_unit.graphic.compute_index_images(index_images)
                    pass

            # Confirm
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.select_target(self.class_cursor.pos[0], self.class_cursor.pos[1])

    def update(self):
        self.class_cursor.update()
        self.get_keys()

    def select_enemy(self, target):
        if target not in self.selected_enemies:
            self.selected_enemies.append(target)
            target.load_map()
        else:
            self.selected_enemies.remove(target)
        self.compute_map_danger()

    def compute_map_danger(self):
        map_danger = []
        for enemy in self.selected_enemies:
            for pos in enemy.map_range:
                if pos not in map_danger:
                    map_danger.append(pos)
        if map_danger:
            self.map_danger = map_danger
        else:
            self.map_danger = None

    def draw_tiles(self, surface, unit_map):
        for tile_pos in unit_map:
            pos = self.main.class_map.compute_tile_pos(tile_pos[0], tile_pos[1])
            self.game.gameDisplay.blit(surface, pos)

    def draw(self):
        if self.current_unit is not None:
            self.draw_tiles(self.main.tile_range_surface, self.current_unit.map_range)
            self.draw_tiles(self.main.tile_move_surface, self.current_unit.map_move)
        if self.map_danger is not None:
            self.draw_tiles(self.main.tile_danger_surface, self.map_danger)

        for enemy in self.selected_enemies:
            pos = self.main.class_map.compute_tile_pos(enemy.pos[0], enemy.pos[1])
            self.game.gameDisplay.blit(self.main.tile_enemy_surface, pos)
        self.class_cursor.draw()


class s2_menu_unit:
    def __init__(self, game):
        self.game = game
        self.main = game.main

        self.buttons = Buttons(self.game, self.game.button_dict, "unit_menu", self)
        self.current_button = self.buttons.compute_button_index(0)

        # Variable
        # self.all_units = self.parent.all_units

    def select_target(self, target_type=None):
        self.main.class_state = s3_target(self.game)

    def get_keys(self):
        for event in self.game.event:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_z:
                    self.current_button = self.buttons.compute_button_index(-1)
                if event.key == pygame.K_s:
                    self.current_button = self.buttons.compute_button_index(1)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    if self.current_button is not None:
                        self.current_button.compute_action()

    def update(self):
        self.get_keys()
        self.buttons.update()
        if self.buttons.current_button is not None:
            self.buttons.current_button.compute_active(True)

    def draw(self):
        self.buttons.draw()


class s3_target:
    def __init__(self, game):
        self.game, self.main = game, game.main

        self.all_targets = []
        for unit in self.main.class_units.all_units:
            self.all_targets.append(unit)

        self.current_index = 0
        self.current_target = self.all_targets[self.current_index]

    def select_target(self, d_index):
        self.current_index = (self.current_index + d_index) % len(self.all_targets)
        self.current_target = self.all_targets[self.current_index]

    def get_keys(self):
        for event in self.game.event:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_z:
                    self.select_target(-1)
                if event.key == pygame.K_s:
                    self.select_target(1)

    def update(self):
        self.get_keys()

    def draw(self):
        pos = self.main.class_map.compute_tile_pos(self.current_target.pos[0], self.current_target.pos[1])
        self.game.gameDisplay.blit(self.main.tile_enemy_surface, pos)

class s4_inventory:
    def __init__(self, game):
        self.game = game
        self.main = game.main

    def get_keys(self):
        for event in self.event:
            if event.type == pygame.KEYDOWN:
                pass

    def update(self):
        self.get_keys()

    def draw(self):
        pass

class s1_menu_map:
    def __init__(self, game):
        self.game = game
        self.main = game.main
        self.event = self.game.event

    def get_keys(self):
        for event in self.event:
            if event.type == pygame.KEYDOWN:
                pass

    def update(self):
        self.get_keys()

    def draw(self):
        pass