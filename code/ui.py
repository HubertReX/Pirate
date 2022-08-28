from wsgiref.util import setup_testing_defaults
import pygame
from settings import *

# This is a simple class that will help us print to the screen
# It has nothing to do with the joysticks, just outputting the
# information.

class TextPrint:
    def __init__(self, surface):
        self.display_surface = surface 		
        self.reset()
        self.font = pygame.font.Font(None, 20)
        self.highlighted_line = 0
        self.lines_count = 0
        
    def selected_line_up(self):
        if self.highlighted_line < self.lines_count:
            self.highlighted_line += 1
        else:
            self.highlighted_line = 0

    def selected_line_down(self):
        if self.highlighted_line > 0:
            self.highlighted_line -= 1
        else:
            self.highlighted_line = self.lines_count

    def highligt_line(self):
        pygame.draw.rect(self.display_surface, (255,0,0), pygame.Rect(7, 10+(self.highlighted_line * 15), 200, 15),  2)

    def print(self, textString):
        textBitmap = self.font.render(textString, True, (150, 150, 150))
        self.display_surface.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height
        self.lines_count += 1
        
    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15
		
        
    def indent(self):
        self.x += 10
        
    def unindent(self):
        self.x -= 10

class UI:
	def __init__(self,surface):

		# setup 
		self.display_surface = surface 

		# health 
		self.health_bar = pygame.image.load('../graphics/ui/health_bar.png').convert_alpha()
		self.health_bar_topleft = (54,39)
		self.bar_max_width = 152
		self.bar_height = 4

		# coins 
		self.coin = pygame.image.load('../graphics/ui/coin.png').convert_alpha()
		self.coin_rect = self.coin.get_rect(topleft = (50,61))
		self.font = pygame.font.Font('../graphics/ui/ARCADEPI.ttf',30)

		# label
		self.text = TextPrint(surface)

	def reset(self):
		self.text.reset()

	def show_health(self,current,full):
		self.display_surface.blit(self.health_bar,(20,10))
		current_health_ratio = current / full
		current_bar_width = self.bar_max_width * current_health_ratio
		health_bar_rect = pygame.Rect(self.health_bar_topleft,(current_bar_width,self.bar_height))
		pygame.draw.rect(self.display_surface,'#dc4949',health_bar_rect)

	def show_coins(self,amount):
		self.display_surface.blit(self.coin,self.coin_rect)
		coin_amount_surf = self.font.render(str(amount),False,'#33323d')
		coin_amount_rect = coin_amount_surf.get_rect(midleft = (self.coin_rect.right + 4,self.coin_rect.centery))
		self.display_surface.blit(coin_amount_surf,coin_amount_rect)

	def show_titles(self,text_label):
		coin_label_surf = self.font.render(str(text_label),False,'#9c0000')
		coin_label_rect = pygame.Rect((200,20),(300,50))
		self.display_surface.blit(coin_label_surf,coin_label_rect)		
	
	def show_debug_info(self):
		self.text.highligt_line()
		self.text.print("Enable sound on start: {}".format(ENABLE_SOUND_ON_START))
		self.text.print("Moving clouds: {}".format(MOVING_CLOUDS))
		self.text.print("God mode: {}".format(GOD_MODE))
		self.text.print("Start max level: {}".format(START_MAX_LEVEL))
		self.text.print("Start max health: {}".format(START_MAX_HEALTH))