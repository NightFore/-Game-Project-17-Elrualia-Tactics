import pygame
import copy
from Dict import *


class Graphics:
    def __init__(self, game):
        self.game = game
        self.main = game.main
        self.data = graphic_dict
        self.dict = copy.deepcopy(self.data)

    def load(self):
        pass

    def new(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass


class Graphic:
    def __init__(self, game, key):
        # Global
        data = graphic_dict

        # Initialization
        self.game, self.main = game, game.main
        self.data, self.key = data, key
        self.dict = copy.deepcopy(self.data[self.key])

        # Image
        self.path = self.dict["path"]
        self.size_scaled = self.dict["size_scaled"]
        self.color_key = self.dict["color_key"]
        self.init_image()

        # Images
        self.images = self.dict["images"]
        if self.images:
            self.images_size = self.dict["images_size"]
            self.images_offset = self.dict["images_offset"]
            self.length = self.dict["length"]
            self.index_vh = self.dict["index_vh"]
            self.index_image = self.dict["index_image"]
            self.index_images = self.dict["index_images"]
            self.init_images()

            # Animation
            self.animation = self.dict["animation"]
            if self.animation:
                self.loop = self.dict["loop"]
                self.loop_reverse = self.dict["loop_reverse"]
                self.loop_delay = self.dict["loop_delay"]
                self.frame_speed = self.dict["frame_speed"]
                self.init_animation()

    def init_image(self):
        # Load / Convert / Scale / Color key / Rect
        self.image = pygame.image.load(self.path)
        self.image = pygame.Surface.convert_alpha(self.image)
        self.current_image = pygame.transform.scale(self.image, self.size_scaled)
        self.current_image.set_colorkey(self.color_key)
        self.pos = [0, 0]
        self.offset = [0, 0]
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size_scaled[0], self.size_scaled[1])
        self.compute_rect(self.pos[0], self.pos[1])

    def init_images(self):
        # Load Tile table
        self.images = []
        for index_images in range(self.length[2]):
            line_offset_x = index_images * self.images_size[0] * self.index_vh
            line_offset_y = index_images * self.images_size[1] * (1 - self.index_vh)
            for index_y in range(self.length[1]):
                line = []
                for index_x in range(self.length[0]):
                    # Subsurface image
                    pos_sub_x = index_x * self.images_size[0] + self.images_offset[0] + line_offset_x
                    pos_sub_y = index_y * self.images_size[1] + self.images_offset[1] + line_offset_y
                    rect_sub = (pos_sub_x, pos_sub_y, self.images_size[0], self.images_size[1])
                    image_sub = self.image.subsurface(rect_sub)

                    # Scaled & color key
                    image_scaled = pygame.transform.scale(image_sub, self.size_scaled)
                    image_scaled.set_colorkey(self.color_key)

                    line.append(image_scaled)
                self.images.append(line)

        # Index (Images: Current image)
        self.index = [0, 0]
        self.current_image = self.images[self.index[1]][self.index[0]]

    def init_animation(self):
        # Time
        self.current_time = 0
        self.delay_time = 0

        # Animation
        self.animation_time = self.frame_speed / self.game.FPS
        self.loop_delay_time = self.loop_delay / self.game.FPS

        # Index (Next frame)
        self.index_next = 1

    def compute_rect(self, x=None, y=None, offset=None):
        if x is not None:
            self.pos[0] = x
        if y is not None:
            self.pos[1] = y
        if offset is not None:
            self.offset = offset
        self.rect.x = self.pos[0] * self.size_scaled[0] + self.offset[0]
        self.rect.y = self.pos[1] * self.size_scaled[1] + self.offset[1]

    def update_animation(self):
        # Loop delay
        if self.delay_time >= 0:
            self.delay_time -= self.dt

        # Frame animation
        else:
            self.current_time += self.dt
            if self.current_time >= self.animation_time:
                self.current_time -= self.animation_time
                self.compute_index_image()

    def compute_index_image(self):
        # Index: Vertical / Horizontal
        self.index_image[self.index_vh] += self.index_next

        # Index: Loop
        if not self.loop_reverse:
            self.index_image[self.index_vh] = self.index_image[self.index_vh] % self.length[self.index_vh]
            self.delay_time = self.loop_delay_time

        # Index: Reverse loop
        elif self.index_image[self.index_vh] == 0 or self.index_image[self.index_vh] == self.length[self.index_vh] - 1:
            self.index_next = -self.index_next
            self.delay_time = self.loop_delay_time

        # Image: Next
        self.current_image = self.images[self.index_image[1]][self.index_image[0]]

    def compute_index_images(self, index_images=None):
        # Loop index images
        if index_images is None:
            if self.index_vh == 0:
                self.index_image[1] = (self.index_image[1] + 1) % len(self.images)
            elif self.index_vh == 1:
                self.index_image[0] = (self.index_image[0] + 1) % len(self.images[0])

        # Set index images
        else:
            self.index_image[1 - self.index_vh] = index_images

        # Next image
        self.current_image = self.images[self.index_image[1]][self.index_image[0]]

    def update(self):
        self.dt = self.game.dt
        self.compute_rect()

        if self.animation:
            self.update_animation()

    def draw(self):
        self.game.gameDisplay.blit(self.current_image, self.rect)
