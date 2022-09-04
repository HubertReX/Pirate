import asyncio
import pygame, sys
from settings import * 
from level import Level
from overworld import Overworld
from ui import UI

class Game:
	def __init__(self):

		self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
		# game attributes
		self.max_level = START_MAX_LEVEL
		self.max_health = START_MAX_HEALTH
		self.cur_health = self.max_health 
		self.coins = 0
		
		# audio 
		self.level_bg_music = pygame.mixer.Sound('audio/level_music.wav')
		self.overworld_bg_music = pygame.mixer.Sound('audio/overworld_music.wav')

		# overworld creation
		self.overworld = Overworld(0, self.max_level, self.screen, self.create_level)
		self.status = 'overworld'
		if ENABLE_SOUND_ON_START:
			self.overworld_bg_music.play(loops = -1)

		# user interface 
		self.ui = UI(self.screen)


	def create_level(self,current_level):
		self.level = Level(current_level, self.screen, self.create_overworld, self.change_coins, self.change_health)
		self.status = 'level'
		self.overworld_bg_music.stop()
		if ENABLE_SOUND_ON_START:
			self.level_bg_music.play(loops = -1)

	def create_overworld(self,current_level,new_max_level):
		if new_max_level > self.max_level:
			self.max_level = new_max_level
		self.overworld = Overworld(current_level, self.max_level, self.screen, self.create_level)
		self.status = 'overworld'
		if ENABLE_SOUND_ON_START:
			self.overworld_bg_music.play(loops = -1)
		self.level_bg_music.stop()

	def change_coins(self,amount):
		self.coins += amount

	def change_health(self,amount):
		self.cur_health += amount
		if self.cur_health > self.max_health:
			self.cur_health = self.max_health

	def show_overworld(self):
		self.cur_health = 100
		self.coins = 0
		#self.max_level = 0
		self.overworld = Overworld(0, self.max_level, self.screen, self.create_level)
		self.status = 'overworld'
		self.level_bg_music.stop()
		if ENABLE_SOUND_ON_START:
			self.overworld_bg_music.play(loops = -1)

	def check_game_over(self):
		if self.cur_health <= 0:
			self.show_overworld()

	def run(self):
		self.screen.fill('grey')
		if self.status == 'overworld':
			self.overworld.run(self.ui.text.selected_line_up, self.ui.text.selected_line_down)
			self.ui.reset()
			self.ui.show_titles("Pirat! Arrr...")
			if self.overworld.show_debug_info and GOD_MODE:
				self.ui.show_debug_info()
			#self.ui.show_coins(self.coins)
		else:
			self.level.run()
			self.ui.reset()
			self.ui.show_health(self.cur_health, self.max_health)
			self.ui.show_coins(self.coins)
			self.check_game_over()

async def main():
	# Pygame setup
	pygame.init()
	# Initialize the joysticks
	pygame.joystick.init()
	
	clock = pygame.time.Clock()
	game = Game()

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
				
		game.run()

		pygame.display.update()
		await asyncio.sleep(0)  # very important, and keep it 0
		clock.tick(60)

asyncio.run( main() )

# do not add anything from here
# asyncio.run is non block on pygame-wasm		