import pygame
import json
import os

class Level:
    def __init__(self, map_path):
        self.map_path = map_path
        self.load_map()
        self.load_tileset()

    def load_map(self):
        with open(self.map_path, 'r') as f:
            self.map_data = json.load(f)
        self.width = self.map_data['width']
        self.height = self.map_data['height']
        self.tilewidth = self.map_data['tilewidth']
        self.tileheight = self.map_data['tileheight']
        self.layers = self.map_data['layers']

    def load_tileset(self):
        tileset = self.map_data['tilesets'][0]
        tileset_path = os.path.join(os.path.dirname(self.map_path), tileset['source'])
        with open(tileset_path, 'r') as f:
            tileset_data = f.read()
        # Parse the tsx file to get the image source
        import xml.etree.ElementTree as ET
        root = ET.fromstring(tileset_data)
        image_source = root.find('image').get('source')
        image_source = image_source.replace('Assets', 'assets').replace('Sprites', 'sprites')
        self.tileset_image = pygame.image.load(os.path.join(os.path.dirname(tileset_path), image_source)).convert_alpha()
        self.columns = int(root.get('columns'))
        self.firstgid = tileset['firstgid']

    def draw(self, surface):
        for layer in self.layers:
            if layer['type'] == 'tilelayer' and layer['visible']:
                self.draw_tile_layer(surface, layer)

    def draw_tile_layer(self, surface, layer):
        data = layer['data']
        width = layer['width']
        height = layer['height']
        for y in range(height):
            for x in range(width):
                gid = data[y * width + x]
                if gid == 0:
                    continue
                tile_index = gid - self.firstgid
                col = tile_index % self.columns
                row = tile_index // self.columns
                src_rect = pygame.Rect(col * self.tilewidth, row * self.tileheight, self.tilewidth, self.tileheight)
                dest_rect = pygame.Rect(x * self.tilewidth, y * self.tileheight, self.tilewidth, self.tileheight)
                surface.blit(self.tileset_image, dest_rect, src_rect)