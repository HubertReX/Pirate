import pygame 
from support import import_folder

class Tile(pygame.sprite.Sprite):
	def __init__(self, size, x, y):
		"""contructor for Tile/sprite general class

		Args:
			size (int): tile size
			x (int): x tile postion in world coordinates
			y (int): y tile postion in world coordinates
		"""				
		super().__init__()
		self.image = pygame.Surface((size,size))
		self.rect = self.image.get_rect(topleft = (x, y))

	def update(self,shift):
		self.rect.x += shift

class StaticTile(Tile):
	def __init__(self, size, x, y, surface):
		"""contructor for Static tile/sprite general class

		Args:
			size (int): tile size
			x (int): x tile postion in world coordinates
			y (int): y tile postion in world coordinates
			surface (pygame.Surface): surface object with tile drawn on it
		"""					
		super().__init__(size, x, y)
		self.image = surface 

class Crate(StaticTile):
	def __init__(self, size, x, y):
		"""contructor for Crate static tile/sprite

		Args:
			size (int): tile size
			x (int): x tile postion in world coordinates
			y (int): y tile postion in world coordinates
		"""					
		super().__init__(size, x, y, pygame.image.load('graphics/terrain/crate.png').convert_alpha())
		offset_y = y + size
		self.rect = self.image.get_rect(bottomleft = (x, offset_y))

class AnimatedTile(Tile):
	def __init__(self, size, x, y, path):
		"""contructor for Animated tile/sprite general class

		Args:
			size (int): tile size
			x (int): x tile postion in world coordinates
			y (int): y tile postion in world coordinates
			path (str): path to folder with images of animation 
		"""				
		super().__init__(size, x, y)
		self.frames = import_folder(path)
		self.frame_index = 0
		self.image = self.frames[self.frame_index]

	def animate(self):
		self.frame_index += 0.2
		if self.frame_index >= len(self.frames):
			self.frame_index = 0
		self.image = self.frames[int(self.frame_index)]

	def update(self,shift):
		self.animate()
		self.rect.x += shift

class Coin(AnimatedTile):
	def __init__(self, size, x, y, path, value):
		"""contructor for Coin animated tile/sprite

		Args:
			size (int): tile size
			x (int): x tile postion in world coordinates
			y (int): y tile postion in world coordinates
			path (str): path to folder with images of animation 
			value (int): how mutch is given type of coins worth (there are golden and silver coins)
		"""			
		super().__init__(size, x, y, path)
		center_x = x + int(size / 2)
		center_y = y + int(size / 2)
		self.rect = self.image.get_rect(center = (center_x, center_y))
		self.value = value

class Heart(AnimatedTile):
	def __init__(self, size, x, y, path):
		"""contructor for Heart animated tile/sprite

		Args:
			size (int): tile size
			x (int): x tile postion in world coordinates
			y (int): y tile postion in world coordinates
			path (str): path to folder with images of animation 
		"""		
		factor = 2
		super().__init__(size / factor, x, y, path)
		center_x = x + int(size / factor) 
		center_y = y + int(size / factor)
		self.rect = self.image.get_rect(center = (center_x, center_y))
		#self.value = value

class Palm(AnimatedTile):
	def __init__(self, size, x, y, path, offset):
		"""contructor for Palm animated tile/sprite

		Args:
			size (int): tile size
			x (int): x tile postion in world coordinates
			y (int): y tile postion in world coordinates
			path (str): path to folder with images of animation 
			offset (int): offset on y axle to match palm top border
		"""
		super().__init__(size, x, y, path)
		offset_y = y - offset
		self.rect.topleft = (x, offset_y)