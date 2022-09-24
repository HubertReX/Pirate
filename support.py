from csv import reader
#from settings import TILE_SIZE
from os import walk
import pygame

def import_folder(path):
	"""reads all images files (sorted by name) from given folder and creates a colloction of pygame surfaces (eg. an animation)

	Args:
		path (str): path to folder with single image files as individual frames
	Returns:
		[pygame.Surace]: list of individual frames as surfaces
	"""		
	surface_list = []

	for _,__,image_files in walk(path):
		for image in sorted(image_files):
			full_path = path + '/' + image
			image_surf = pygame.image.load(full_path).convert_alpha()
			surface_list.append(image_surf)

	return surface_list

def import_csv_layout(path):
	terrain_map = []
	with open(path) as map:
		level = reader(map,delimiter = ',')
		for row in level:
			terrain_map.append(list(row))
		return terrain_map

def import_cut_graphics(path, tile_size):
	"""reads individual image file and divides it into colletions of tiles

	Args:
		path (str): path to image (map of n x m sprites of tile_size)
		tile_size (int): tile size
	Returns:
		[pygame.Surace]: list of individual images/sprites as surfaces (sized: tile_size x tile_size)
	"""			
	surface = pygame.image.load(path).convert_alpha()
	tile_num_x = int(surface.get_size()[0] / tile_size)
	tile_num_y = int(surface.get_size()[1] / tile_size)

	cut_tiles = []
	for row in range(tile_num_y):
		for col in range(tile_num_x):
			x = col * tile_size
			y = row * tile_size
			new_surf = pygame.Surface((tile_size, tile_size),flags = pygame.SRCALPHA)
			new_surf.blit(surface,(0,0), pygame.Rect(x, y, tile_size, tile_size))
			cut_tiles.append(new_surf)

	return cut_tiles
