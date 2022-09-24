import pygame 
from tiles import AnimatedTile
from random import randint

class Enemy(AnimatedTile):
	def __init__(self, size, x, y):
		super().__init__(size, x, y, 'graphics/enemy/run')
		self.rect.y += size - self.image.get_size()[1]
		self.pos = pygame.math.Vector2(self.rect.topleft)
		self.speed = randint(200, 260)

	def move(self, dt):		
		self.pos.x += self.speed  * dt
		self.rect.x = round(self.pos.x)

	def reverse_image(self):
		if self.speed > 0:
			self.image = pygame.transform.flip(self.image, True, False)

	def reverse(self):
		self.speed *= -1

	def update(self, shift, dt):
		self.pos.x += shift
		self.rect.x += shift
		self.animate()
		self.move(dt)
		self.reverse_image()