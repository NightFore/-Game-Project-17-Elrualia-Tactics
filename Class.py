from Head import *

class Map:
    def __init__(self, game, parent):
        self.game, self.main = game, game.main
        self.parent = parent
        self.data = level_dict
        self.load()
        
    def load(self):
        self.tile_size = self.main.tile_size
        self.tile_grass_1 = Graphic(self.game, "tile_grass_1")
        self.tile_water_7 = Graphic(self.game, "tile_water_7")

    def init(self, level):
        self.dict = copy.deepcopy(self.data[level])
        self.init_map()
        self.init_class()

    def init_map(self):
        self.current_map = self.dict["map"]
        self.map_length = [len(self.current_map[0]), len(self.current_map)]
        offset_x = int(self.game.screen_width/2 - self.tile_size[0] * self.map_length[0]/2)
        offset_y = int(self.game.screen_height/2 - self.tile_size[1] * self.map_length[1]/2)
        self.offset = [offset_x, offset_y]

    def init_class(self):
        self.tile_grass_1.offset = self.offset
        self.tile_water_7.offset = self.offset
        self.main.class_cursor.init([0, 0], self.tile_size, self.offset, self.map_length)

    def compute_tile_pos(self, x, y):
        tile_pos_x = int(x * self.tile_size[0] + self.offset[0])
        tile_pos_y = int(y * self.tile_size[1] + self.offset[1])
        return tile_pos_x, tile_pos_y

    def compute_path(self, x, y):
        """
        Returns the first possible path to [x, y]
        """
        for new_path in self.current_map:
            if [x, y] == new_path[-1]:
                return new_path

    @staticmethod
    def compute_map_pos(map_path):
        """
        Returns all possible positions in the paths
        """
        map_pos = []
        for new_path in map_path:
            for pos in new_path:
                if pos not in map_pos:
                    map_pos.append(pos)
        return map_pos

    def compute_map_path(self, distance, pos, d_range=1):
        """
        Returns all possible paths to a given distance
        """
        path_new = []
        path_current = path_final = [pos.copy()]
        while distance > 0:
            # Iterate for each path
            for path in path_current:
                x, y = path[-1]

                # Continue the path
                for dx in range(-d_range, d_range + 1):
                    for dy in range(-d_range, d_range + 1):
                        # Check: Maximum range
                        if (dx, dy) != (0, 0) and abs(dx) + abs(dy) <= d_range:
                            pos = [pos_x, pos_y] = [x + dx, y + dy]

                            # Check: Map limit
                            if 0 <= pos_x < len(self.current_map[0]) and 0 <= pos_y < len(self.current_map):
                                new_path = path.copy()

                                # Check: Path
                                if pos not in new_path and self.current_map[pos_y][pos_x] != 1:
                                    new_path.append(pos)
                                    path_new.append(new_path)

            # Add the current path to the final path list
            for path in path_new:
                path_final.append(path)

            # Initialize next loop
            path_current = path_new
            path_new = []
            distance -= 1

        return path_final

    def update(self):
        self.tile_grass_1.update()
        self.tile_water_7.update()

    def draw(self):
        for index_y, tile_line in enumerate(self.current_map):
            for index_x, tile in enumerate(tile_line):
                if tile == 0:
                    self.tile_grass_1.compute_rect(index_x, index_y)
                    self.tile_grass_1.draw()
                if tile == 1:
                    self.tile_water_7.compute_rect(index_x, index_y)
                    self.tile_water_7.draw()


class Units:
    def __init__(self, game, parent):
        self.game, self.main = game, game.main
        self.parent = parent
        self.data = level_dict
        self.load()
        self.new()

    def load(self):
        pass

    def new(self):
        pass

    def init(self, level):
        self.init_level(level)
        self.init_unit()
        self.init_graphic()

    def init_level(self, level):
        self.dict = copy.deepcopy(self.data[level])

    def init_unit(self):
        self.units_dict = self.dict["units"]
        self.all_units = pygame.sprite.Group()
        for team in self.units_dict:
            team_units = []
            for unit in self.units_dict[team]:
                team_units.append(Unit(self.game, unit["type"], self.all_units, unit["pos"], team))
        print(self.all_units)

    def init_graphic(self):
        for unit in self.all_units:
            unit.init_graphic(self.parent.class_map.offset)

    def search_unit(self, x, y):
        """
        Return unit at tile position
        """
        for unit in self.all_units:
            if [x, y] == unit.pos:
                return unit
        print("Empty tile: %d, %d" % (x, y))
        return None

    def update(self):
        for unit in self.all_units:
            unit.update()

    def draw(self):
        for unit in self.all_units:
            unit.draw()



class Unit(pygame.sprite.Sprite):
    def __init__(self, game, key, group, pos, team):
        # Global
        data = unit_dict

        # Initialization
        self.game, self.main = game, game.main
        self.data, self.key = data, key
        self.dict = copy.deepcopy(self.data[self.key])
        pygame.sprite.Sprite.__init__(self, group)

        # Arguments
        self.pos = pos
        self.team = team

        # Class
        self.current_class = Class(self.game, self.dict["class"])

        # Graphic
        self.graphic = Graphic(self.game, self.current_class.image)

        # Stats
        self.stats = self.dict["stats"]
        self.growth = self.dict["growth"]
        for stat in self.stats:
            self.stats[stat] += self.current_class.stats[stat]
            self.growth[stat] += self.current_class.growth[stat]

        # Level
        self.level = self.dict["level"]
        self.experience = self.dict["experience"]
        self.compute_level_up()
        self.current_hp = self.stats["hp"]

        # Inventory
        self.inventory = []
        for item_name in self.dict["inventory"]:
            self.inventory.append(Item(self.game, item_name))
        self.weapon = self.inventory[0]

        # Map
        self.map_path = []
        self.map_range = []

    def init_graphic(self, offset):
        self.graphic.compute_rect(self.pos[0], self.pos[1], offset)

    def compute_attack_repeat(self, target):
        """
        Input:
            target -> Unit
        Output:
            attack_repeat -> int (bool)
        Variable:
            speed_penalty -> int
            attack_speed -> int
        """
        speed_penalty = min(0, self.stats["con"] - self.weapon.weight)
        attack_speed = self.stats["spd"] - speed_penalty
        attack_repeat = int(attack_speed - target.stats["spd"] >= 5)
        return attack_repeat

    def compute_weapon_advantage(self, target):
        """
        Input:
            target -> Unit
        Output:
            advantage_damage -> int
            advantage_hit -> int
        Comment:
            0: Sword / Fire
            1: Lance / Thunder
            2: Axe / Wind
            0 < 1 < 2 < 1
        """
        if self.weapon.type == target.weapon.type:
            advantage_damage = 0
            advantage_hit = 0
        elif self.weapon.type == (target.weapon.type + 1) % 3:
            advantage_damage = 2
            advantage_hit = 20
        elif self.weapon.type == (target.weapon.type + 2) % 3:
            advantage_damage = -2
            advantage_hit = -20
        else:
            advantage_damage = 0
            advantage_hit = 0
        return advantage_damage, advantage_hit

    def compute_terrain_advantage(self, target):
        """
        WIP

        Input:
            target -> Unit
        Output:
            advantage_defense -> int
            advantage_avoid -> int
        """
        terrain = "test"
        if terrain == "forest":
            advantage_defense = 0
            advantage_avoid = 10
        else:
            advantage_defense = 0
            advantage_avoid = 0
        return advantage_defense, advantage_avoid

    def compute_hit_accuracy(self, target, advantage_hit, advantage_avoid):
        """
        Input:
            target -> Unit
            advantage_hit -> int
            advantage_avoid -> int
        Output:
            hit_accuracy -> int
        """
        hit_rate = self.weapon.hit + self.stats["skl"]*2 + self.stats["lck"]/2 + advantage_hit
        hit_avoid = target.stats["skl"]*2 + target.stats["lck"]/2 + advantage_avoid
        hit_accuracy = max(0, min(100, hit_rate - hit_avoid))
        return 300

    def compute_critical_accuracy(self, target):
        """
        Input:
            target -> Unit
        Output:
            critical_accuracy -> int
        Variable:
            critical_rate -> int
            critical_avoid -> int
        """
        critical_rate = self.weapon.critical + self.stats["skl"]/2
        critical_avoid = target.stats["lck"]
        critical_accuracy = max(0, min(100, critical_rate - critical_avoid))
        return critical_accuracy

    def compute_attack(self, target):
        """
        Input:
            target -> Unit
            level_map -> list[][]
        Variable:
            damage -> int (bool)
            kill -> int (bool)
        Function:
            compute_map
            compute_damage
            compute_experience
            compute_level_up
        """
        if target.pos in self.map_range:
            damage, kill = self.compute_damage(target)
            self.compute_experience(target, damage, kill)
            self.compute_level_up()
            print(target.current_hp)
            if kill:
                print("Killed")
                target.kill()
        else:
            print("Target not in range")

    def compute_damage(self, target):
        """
        Input:
            target -> Unit
        Output:
            damage -> int (bool)
            kill -> int (bool)
        Variable:
            attack_repeat -> boolean (int)
            advantage_damage -> int
            advantage_hit -> int
            advantage_defense -> int
            advantage_avoid -> int
            hit_accuracy -> boolean (int)
            critical_accuracy -> boolean (int)
            attack_power -> int
            defense_power -> int
            base_damage -> int
            total_damage -> int
            hit -> int (bool)
            critical -> int (bool)
        Function:
            compute_attack_repeat
            compute_weapon_advantage
            compute_terrain_advantage
            compute_hit_accuracy
            compute_critical_accuracy
        Class:
            target.current_hp
        """
        attack_repeat = self.compute_attack_repeat(target)
        advantage_damage, advantage_hit = self.compute_weapon_advantage(target)
        advantage_defense, advantage_avoid = self.compute_terrain_advantage(target)
        hit_accuracy = self.compute_hit_accuracy(target, advantage_hit, advantage_avoid)
        critical_accuracy = self.compute_critical_accuracy(target)
        attack_power = self.stats["str"] + self.weapon.might + advantage_damage
        defense_power = target.stats["def"] + advantage_defense
        base_damage = max(0, attack_power - defense_power)

        total_damage = 0
        for attack in range(1 + attack_repeat):
            hit = int(hit_accuracy >= random.randint(1, 100))
            critical = int(critical_accuracy >= random.randint(1, 100))
            total_damage += base_damage * hit * (1 + 2 * critical)
        target.current_hp = max(target.current_hp - total_damage, 0)
        damage = int(target.current_hp == 0 or total_damage > 0)
        kill = int(target.current_hp == 0)

        debug = True
        if debug:
            print("attack_repeat = %d" % attack_repeat)
            print("advantage_damage = %d" % advantage_damage)
            print("advantage_hit = %d" % advantage_hit)
            print("advantage_defense = %d" % advantage_defense)
            print("advantage_avoid = %d" % advantage_avoid)
            print("hit_accuracy = %d" % hit_accuracy)
            print("critical_accuracy = %d" % critical_accuracy)
            print("attack_power = %d" % attack_power)
            print("defense_power = %d" % defense_power)
            print("total_damage = %d" % damage)
            print("current_hp = %d" % target.current_hp)
            print("damage = %d" % damage)
            print("kill = %d" % kill)
            print()
        return damage, kill

    def compute_experience(self, target, damage, kill):
        """
        Input:
            target -> Unit
            damage -> int (bool)
            kill -> int (bool)
        Output:
            self.experience: Minimum = damage_total_exp
        Variable:
            damage_base_exp
            damage_unit_exp
            damage_target_exp
            damage_total_exp: Minimum = 1
            kill_base_exp
            kill_unit_exp
            kill_target_exp
            kill_total_exp: Minimum = 0
        class:
            self.experience
        """
        damage_base_exp = 31
        damage_unit_exp = self.level + 20*self.current_class.promotion
        damage_target_exp = target.level + 20*target.current_class.promotion
        damage_total_exp = round(max(1, (damage_base_exp + damage_target_exp - damage_unit_exp) / self.current_class.power))
        kill_base_exp = 20
        kill_unit_exp = self.level * self.current_class.power + 20*self.current_class.promotion
        kill_target_exp = target.level * target.current_class.power + 20*target.current_class.promotion
        kill_total_exp = round(max(0, kill_base_exp + kill_target_exp - kill_unit_exp))
        total_exp = min(100, damage*damage_total_exp + kill*kill_total_exp)
        self.experience += total_exp

        debug = True
        if debug:
            print("damage_exp: %d*%d" % (damage, damage_total_exp))
            print("kill: %d*%d" % (kill, kill_total_exp))
            print("EXP: %d" % total_exp)

    def compute_level_up(self):
        """
        Variable:
            growth_check
            max_check
        class:
            self.level
            self.experience
            self.stats
        """
        while self.experience >= 100:
            self.level += 1
            self.experience -= 100
            for stat in self.growth:
                growth_check = self.growth[stat] >= random.randint(1, 100)
                max_check = self.stats[stat] < self.current_class.max_stats[stat]
                if growth_check and max_check:
                    self.stats[stat] += 1

    def compute_movement(self, x, y):
        # Check: Map
        if [x, y] in self.map_move:
            self.pos = [x, y]
            self.graphic.compute_rect(x, y)

    def load_map(self):
        self.map_path = self.main.class_map.compute_map_path(self.stats["mov"], [self.pos])
        self.map_move = self.main.class_map.compute_map_pos(self.map_path)
        self.map_range = self.main.class_map.compute_map_pos(self.main.class_map.compute_map_path(self.stats["mov"] + self.weapon.range, [self.pos]))

    def update(self):
        self.graphic.update()

    def draw(self):
        self.graphic.draw()


class Item:
    def __init__(self, game, key):
        # Global
        data = item_dict

        # Initialization
        self.game, self.main = game, game.main
        self.data, self.key = data, key
        self.dict = copy.deepcopy(self.data[self.key])

        # Item type
        self.name = key
        self.type = self.dict["type"]

        # N/A
        if self.type == 0:
            pass

        # Sword / Lance / Axe
        elif self.type == 1 or self.type == 2 or self.type == 3:
            self.init_weapon()

    def init_weapon(self):
        self.rank = self.dict["rank"]
        self.uses = self.dict["uses"]
        self.might = self.dict["might"]
        self.hit = self.dict["hit"]
        self.critical = self.dict["critical"]
        self.range = self.dict["range"]
        self.weight = self.dict["weight"]

    def effect_1(self):
        pass


class Terrain:
    def __int__(self, defense, avoid, move_cost):
        self.defense = defense
        self.avoid = avoid
        self.move_cost = move_cost


class Class:
    def __init__(self, game, key):
        # Global
        data = class_dict

        # Initialization
        self.game, self.main = game, game.main
        self.data, self.key = data, key
        self.dict = copy.deepcopy(self.data[self.key])

        # Graphic
        self.image = self.dict["image"]

        # Class
        self.type = self.dict["type"]
        self.power = self.dict["power"]
        self.promotion = self.dict["promotion"]

        # Stats
        self.stats = self.dict["stats"]
        self.growth = self.dict["growth"]
        self.max_stats = self.dict["max_stats"]
