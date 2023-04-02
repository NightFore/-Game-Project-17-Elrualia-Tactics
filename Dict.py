import pygame
from Function import *
from Settings import *

main_dict = {
    "tile_size": (32, 32),
    "color_move": BLUE, "transparency_move": 220,
    "color_range": RED, "transparency_range": 220,
    "color_danger": PINK, "transparency_danger": 125,
    "color_enemy": PINK, "transparency_enemy": 0, "border_enemy": 1
}

game_dict = {
    "project_title": "Elrualia Tactics", "screen_size": (1280, 720), "FPS": 60,
    "default_music_volume": 5, "default_sound_volume": 75,
    "key_repeat": (100, 30),
}

menu_dict = {
    "title": {
        "background": "default",
        "music": "default"
    }
}

background_dict = {
    "default": {
        "color": DARK_SKY_BLUE,
        "image": None,
    },
}

font_dict = {
    "default": {"ttf": None, "size": 100},
    "LiberationSerif": {"ttf": "LiberationSerif-Regular.ttf", "size": 40},
    "LiberationSerif_30": {"ttf": "LiberationSerif-Regular.ttf", "size": 30}
}

graphic_dict = {
    "placeholder": {
        "path": "sprite_lord.png", "size_scaled": [32, 32], "color_key": (128, 160, 128),
        "images": True, "images_size": [16, 16], "images_offset": [0, 0], "reverse": 1, "length": [1, 3],
        "animation": True, "loop": True, "loop_reverse": True, "loop_delay": 36, "frame_speed": 12,
    },
    "tile_grass_1": {
        "path": "grass.png", "size_scaled": [32, 32], "color_key": None,
        "images": True, "images_size": [32, 32], "images_offset": [0, 128],
        "length": [1, 1, 1], "index_vh": 1, "index_image": [0, 0], "index_images": 0,
        "animation": False
    },
    "tile_water_7": {
        "path": "water_7.png", "size_scaled": [32, 32], "color_key": None,
        "images": True, "images_size": [32, 32], "images_offset": [0, 128],
        "length": [8, 1, 1], "index_vh": 0, "index_image": [0, 0], "index_images": 0,
        "animation": True, "loop": True, "loop_reverse": False, "loop_delay": 0, "frame_speed": 16,
    },
    "sprite_lord_map": {
        "path": "Male 01-2.png", "size_scaled": [32, 32], "color_key": (128, 160, 128),
        "images": True, "images_size": [32, 32], "images_offset": [0, 0],
        "length": [3, 1, 4], "index_vh": 0, "index_image": [0, 0], "index_images": 0,
        "animation": True, "loop": True, "loop_reverse": True, "loop_delay": 30, "frame_speed": 8,
    },
    "sprite_soldier_sword": {
        "path": "Soldier 02-1.png", "size_scaled": [32, 32], "color_key": (128, 160, 128),
        "images": True, "images_size": [32, 32], "images_offset": [0, 0],
        "length": [3, 1, 4], "index_vh": 0, "index_image": [0, 0], "index_images": 0,
        "animation": True, "loop": True, "loop_reverse": True, "loop_delay": 30, "frame_speed": 8,
    }
}

music_dict = {
    "default": None,
    "battle": "MaouDamashii_Piano13_Beat_of_the_Darkness_Moon_Piano.mp3"
}

sound_dict = {
}

button_dict = {
    "settings": {
        "init_functions": {load_button, load_text, load_sound, load_action},
        "default": {
            "size": [280, 50], "color": [DARK_SKY_BLUE, LIGHT_SKY_BLUE], "align": "nw",
            "border_size": [5, 5], "border_color": BLACK,
            "text_font": "LiberationSerif", "text_color": WHITE, "text_align": "center",
            "sound_action": None, "sound_active": None, "sound_inactive": None},
        "image": {
            "align": "center",
            "text_font": "LiberationSerif", "text_color": WHITE, "text_align": "center",
            "sound_action": None, "sound_active": None, "sound_inactive": None}
    },
    "title": {
        "new_game": {"settings": "default", "position": [10, 50], "text": "New Game", "action": "self.parent.new_game"},
        "pause": {"settings": "default", "position": [10, 120], "text": "Pause", "action": "self.game.pause_game"},
        "volume_up": {"settings": "default", "position": [10, 190], "text": "Volume +", "argument": +5, "action": "self.game.setting_volume_music"},
        "volume_down": {"settings": "default", "position": [10, 260], "text": "Volume -", "argument": -5, "action": "self.game.setting_volume_music"},
        "fullscreen": {"settings": "default", "position": [10, 330], "text": "Fullscreen", "action": "self.game.gameDisplay.fullscreen"},
        "quit_game": {"settings": "default", "position": [10, 400], "text": "Quit Game", "action": "self.game.quit_game"},
    },
    "unit_menu": {
        "attack": {"settings": "default", "position": [1000, 50], "text": "Attack", "action": "self.parent.select_target"},
        "heal": {"settings": "default", "position": [1000, 120], "text": "Heal", "action": None},
        "inventory": {"settings": "default", "position": [1000, 190], "text": "Inventory", "action": None},
        "trade": {"settings": "default", "position": [1000, 260], "text": "Trade", "action": None},
        "wait": {"settings": "default", "position": [1000, 330], "text": "Wait", "action": None},
    },
    "main": {
    },
}

interface_dict = {
    "settings": {
        "init_functions": {load_interface, load_text},
        "default": {
            "size": [180, 50], "color": DARKGREY, "align": "center",
            "border_size": [6, 6], "border_color": LIGHTSKYGREY,
            "text_font": "LiberationSerif_30", "text_color": WHITE, "text_align": "center"},
        "main": {
            "size": [180, 50], "color": DARKGREY, "align": "nw",
            "border_size": [6, 6], "border_color": LIGHTSKYGREY,
            "text_font": "LiberationSerif_30", "text_color": WHITE, "text_align": "center"},
        "big_test": {
            "size": [590, 80], "color": DARKGREY, "align": "center",
            "border_size": [6, 6], "border_color": LIGHTSKYGREY,
            "text_font": "LiberationSerif_30", "text_color": WHITE, "text_align": "center"},
    },

    "title": {
    },
    "main": {
    }
}

cursor_dict = {
    "default": {
        "cursor_size": (32, 32), "cursor_size_border": [5, 5], "cursor_align": "nw",
        "cursor_color": RED, "cursor_color_border": LIGHTBLUE,
    }
}

item_dict = {
    "Iron Sword": {
        "type": 1, "rank": "E", "uses": 46,
        "might": 5, "hit": 90, "critical": 0,
        "range": 1, "weight": 5},
    "Iron Axe": {
        "type": 3, "rank": "E", "uses": 45,
        "might": 8, "hit": 75, "critical": 0,
        "range": 1, "weight": 10},
    "Rapier": {
        "type": 1, "rank": "prf", "uses": 40,
        "might": 7, "hit": 95, "critical": 10,
        "range": 3, "weight": 5},
    "Vulnerary": {
        "type": 0},
}

terrain_dict = {
    None: {
        "defense": 0, "avoid": 0, "move_cost": None},
    "default": {
        "defense": 0, "avoid": 0, "move_cost": 1},
    "Forest": {
        "defense": 1, "avoid": 20, "move_cost": 2},
    "Wall": {
        "defense": 0, "avoid": 0, "move_cost": None},
}

class_dict = {
    "Lord": {
        "image": "sprite_lord_map",
        "type": "ground", "promotion": 0, "power": 3,
        "stats": {
            "hp": 16, "str": 4, "mag": 0, "skl": 8,
            "spd": 9, "lck": 5, "def": 3, "res": 1,
            "mov": 5, "con": 8},
        "max_stats": {
            "hp": 60, "str": 20, "mag": 0, "skl": 20,
            "spd": 20, "lck": 30, "def": 20, "res": 20,
            "mov": 15, "con": 20},
        "growth": {
            "hp": 0, "str": 0, "mag": 0, "skl": 0,
            "spd": 0, "lck": 0, "def": 0, "res": 0,
            "mov": 0, "con": 0}},
    "Fighter": {
        "image": "sprite_soldier_sword",
        "type": "ground", "promotion": 0, "power": 3,
        "stats": {
            "hp": 20, "str": 5, "mag": 0, "skl": 2,
            "spd": 4, "lck": 0, "def": 2, "res": 0,
            "mov": 5, "con": 11},
        "growth": {
            "hp": 85, "str": 55, "mag": 0, "skl": 35,
            "spd": 30, "lck": 15, "def": 15, "res": 15,
            "mov": 0, "con": 0},
        "max_stats": {
            "hp": 60, "str": 20, "mag": 0, "skl": 20,
            "spd": 20, "lck": 30, "def": 20, "res": 20,
            "mov": 15, "con": 20}},
    "Brigand": {
        "image": "sprite_soldier_sword",
        "type": "ground", "promotion": 0, "power": 3,
        "stats": {
            "hp": 20, "str": 5, "mag": 0, "skl": 1,
            "spd": 5, "lck": 0, "def": 3, "res": 0,
            "mov": 5, "con": 12},
        "growth": {
            "hp": 80, "str": 50, "mag": 0, "skl": 30,
            "spd": 20, "lck": 15, "def": 10, "res": 13,
            "mov": 0, "con": 0},
        "max_stats": {
            "hp": 60, "str": 20, "mag": 0, "skl": 20,
            "spd": 20, "lck": 30, "def": 20, "res": 20,
            "mov": 15, "con": 20}}
}

unit_dict = {
    "player": {
        "name": "N/A", "class": "Lord",
        "level": 1, "experience": 1000,
        "stats": {
            "hp": 0, "str": 0, "mag": 0, "skl": 0,
            "spd": 0, "lck": 0, "def": 0, "res": 0,
            "mov": 0, "con": 0},
        "growth": {
            "hp": 70, "str": 40, "mag": 0, "skl": 60,
            "spd": 60, "lck": 60, "def": 30, "res": 30,
            "mov": 0, "con": 0},
        "inventory": ["Rapier", "Vulnerary"]},
    "test": {
        "name": "", "class": "Brigand",
        "level": 1, "experience": 450,
        "stats": {
            "hp": 0, "str": 0, "mag": 0, "skl": 0,
            "spd": 0, "lck": 0, "def": 0, "res": 0,
            "mov": 0, "con": 0},
        "growth": {
            "hp": 0, "str": 0, "mag": 0, "skl": 0,
            "spd": 0, "lck": 0, "def": 0, "res": 0,
            "mov": 0, "con": 0},
        "inventory": ["Iron Axe"]},
    "prologue_boss": {
        "name": "Reil", "class": "Brigand",
        "level": 1, "experience": 300,
        "stats": {
            "hp": 0, "str": 0, "mag": 0, "skl": 0,
            "spd": 0, "lck": 0, "def": 0, "res": 0,
            "mov": 0, "con": 0},
        "growth": {
            "hp": 0, "str": 0, "mag": 0, "skl": 0,
            "spd": 0, "lck": 0, "def": 0, "res": 0,
            "mov": 0, "con": 0},
        "inventory": ["Iron Axe"]},
    "prologue_1": {
        "name": None, "class": "Brigand",
        "level": 1, "experience": 0,
        "stats": {
            "hp": 0, "str": 0, "mag": 0, "skl": 0,
            "spd": 0, "lck": 0, "def": 0, "res": 0,
            "mov": 0, "con": 0},
        "growth": {
            "hp": 0, "str": 0, "mag": 0, "skl": 0,
            "spd": 0, "lck": 0, "def": 0, "res": 0,
            "mov": 0, "con": 0},
        "inventory": ["Iron Axe"]},
    "prologue_2": {
        "name": None, "class": "Brigand",
        "level": 1, "experience": 100,
        "stats": {
            "hp": 0, "str": 0, "mag": 0, "skl": 0,
            "spd": 0, "lck": 0, "def": 0, "res": 0,
            "mov": 0, "con": 0},
        "growth": {
            "hp": 0, "str": 0, "mag": 0, "skl": 0,
            "spd": 0, "lck": 0, "def": 0, "res": 0,
            "mov": 0, "con": 0},
        "inventory": ["Iron Axe"]},
}

level_dict = {
    "title_screen": {
        "map": [[]],
        "music": {
            "preparation": None,
            "map": None,
            "battle": "battle",
        },
        "units": {
        },
        "win": None
    },
    "chapter_prologue": {
        "map": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]],
        "music": {
            "preparation": None,
            "map": None,
            "battle": "battle",
        },
        "units": {
            "player": [
                {"type": "player", "pos": [4, 5]}],
            "enemy": [
                {"type": "prologue_1", "pos": [8, 6]},
                {"type": "prologue_2", "pos": [9, 6]},
                {"type": "prologue_2", "pos": [9, 7]},
                {"type": "prologue_boss", "pos": [10, 8]}]
        },
        "win": "Rout"
    },
    "chapter_1": {
        "map": [[0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0]],
        "music": {
            "preparation": None,
            "map": None,
            "battle": "battle",
        },
        "units": {
            "player": [
                {"type": "player", "pos": [4, 5]}],
            "enemy": [
                {"type": "prologue_1", "pos": [8, 6]},
                {"type": "prologue_2", "pos": [9, 6]},
                {"type": "prologue_2", "pos": [9, 7]},
                {"type": "prologue_boss", "pos": [10, 8]}]
        },
        "win": "Rout"
    },
}
