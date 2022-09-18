import asyncio
from configuration import configuration
import pygame, sys
#from settings import * 
from level import Level
from overworld import Overworld
from ui import UI

if (sys.platform == "emscripten"):
	__EMSCRIPTEN__ = True
else:
	__EMSCRIPTEN__ = False

print("__________ ARGV ___________")
__MOBILE__ = False
n = len(sys.argv)
for i in range(0, n):
	print(sys.argv[i])
	if "mobile=" in sys.argv[i]:
		mobile = sys.argv[i].split("=")[1]
		if mobile.upper() != "FALSE":
			__MOBILE__ = mobile

class Game:
	def __init__(self):
		self.cfg = configuration(__MOBILE__, __EMSCRIPTEN__)
		self.screen = self.cfg.screen
		# game attributes
		self.max_level = self.cfg.start_max_level
		self.max_health = self.cfg.start_max_health
		self.cur_health = self.max_health 
		self.coins = 0

		# current fps
		self.fps = 0
		
		# audio 
		self.level_bg_music = pygame.mixer.Sound('audio/level_music.wav')
		self.overworld_bg_music = pygame.mixer.Sound('audio/overworld_music.wav')

		# overworld creation
		self.overworld = Overworld(0, self.max_level, self.cfg, self.create_level)
		self.status = 'overworld'
		if self.cfg.enable_sound_on_start:
			self.overworld_bg_music.play(loops = -1)

		# user interface 
		self.ui = UI(self.cfg)


	def create_level(self,current_level):
		self.level = Level(current_level, self.cfg, self.create_overworld, self.change_coins, self.change_health)
		self.status = 'level'
		self.overworld_bg_music.stop()
		if self.cfg.enable_sound_on_start:
			self.level_bg_music.play(loops = -1)

	def create_overworld(self,current_level,new_max_level):
		if new_max_level > self.max_level:
			self.max_level = new_max_level
		self.overworld = Overworld(current_level, self.max_level, self.cfg, self.create_level)
		self.status = 'overworld'
		if self.cfg.enable_sound_on_start:
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
		self.overworld = Overworld(0, self.max_level, self.cfg, self.create_level)
		self.status = 'overworld'
		self.level_bg_music.stop()
		if self.cfg.enable_sound_on_start:
			self.overworld_bg_music.play(loops = -1)

	def check_game_over(self):
		if self.cur_health <= 0:
			self.show_overworld()

	def run(self):
		self.screen.fill('grey')
		if self.status == 'overworld':
			self.overworld.run(self.ui.debug_panel.selected_line_up, self.ui.debug_panel.selected_line_down, self.ui.get_touchscreen_panel, self.ui.debug_log)
			self.ui.show_titles("Pirat! Arrr...")
			self.ui.reset()
			self.ui.show_fps(self.fps)
			#self.ui.debug_panel.print("Is mobile: {}".format(self.cfg.is_mobile))
			#self.ui.debug_panel.print("In web: {}".format(__EMSCRIPTEN__))
			#self.ui.debug_panel.print("Resolution: {}x{}".format(self.cfg.screen_width, self.cfg.screen_height))
			
			if self.cfg.show_debug_info and self.cfg.god_mode:
				self.ui.show_debug_info()
			if self.cfg.is_mobile:
				self.ui.show_touchscreen_info()
		else:
			self.level.run(self.ui.get_touchscreen_panel, self.ui.debug_log)
			self.ui.reset()
			self.ui.show_fps(self.fps)
			self.ui.show_health(self.cur_health, self.max_health)
			self.ui.show_coins(self.coins)
			if self.cfg.show_debug_info and self.cfg.god_mode:
				self.ui.show_debug_info()
			if self.cfg.is_mobile:
				self.ui.show_touchscreen_info()
			self.check_game_over()


async def main():
	
	# Pygame setup
	pygame.init()
	# Initialize the joysticks
	pygame.joystick.init()
	
	clock = pygame.time.Clock()
	game = Game()

	while True:
		# for event in pygame.event.get():
		# 	if event.type == pygame.QUIT:
		# 		pygame.quit()
		# 		sys.exit()
				
		game.run()

		pygame.display.update()
		await asyncio.sleep(0)  # very important, and keep it 0
		clock.tick(60)
		#clock.tick()
		game.fps = clock.get_fps()

asyncio.run( main() )

# do not add anything from here
# asyncio.run is non block on pygame-wasm		