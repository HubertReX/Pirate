import sys
import pygame 
from game_data import levels
from support import import_folder
from decoration import Sky
#from settings import *

class Node(pygame.sprite.Sprite):
	def __init__(self, pos, status, icon_speed, path):
		super().__init__()
		self.frames = import_folder(path)
		self.frame_index = 0
		self.image = self.frames[self.frame_index]
		if status == 'available':
			self.status = 'available'
		else:
			self.status = 'locked'
		self.rect = self.image.get_rect(center = pos)

		self.detection_zone = pygame.Rect(self.rect.centerx-(icon_speed/2),self.rect.centery-(icon_speed/2),icon_speed,icon_speed)

	def animate(self):
		self.frame_index += 0.15
		if self.frame_index >= len(self.frames):
			self.frame_index = 0
		self.image = self.frames[int(self.frame_index)]

	def update(self):
		if self.status == 'available':
			self.animate()
		else:
			tint_surf = self.image.copy()
			tint_surf.fill('black',None,pygame.BLEND_RGBA_MULT)
			self.image.blit(tint_surf,(0,0))

class Icon(pygame.sprite.Sprite):
	def __init__(self,pos):
		super().__init__()
		self.pos = pos
		self.image = pygame.image.load('graphics/overworld/hat.png').convert_alpha()
		self.rect = self.image.get_rect(center = pos)

	def update(self):
		self.rect.center = self.pos

class Overworld:
	def __init__(self, start_level, max_level, cfg, create_level):

		# setup 
		self.cfg = cfg
		self.display_surface = cfg.screen 
		self.max_level = max_level
		self.current_level = start_level
		self.create_level = create_level
		self.debug_log = print

		# movement logic
		self.moving = False
		self.move_direction = pygame.math.Vector2(0,0)
		self.speed = 8

		# sprites 
		self.setup_nodes()
		self.setup_icon()
		self.sky = Sky(self.cfg, 'overworld')

		# time 
		self.start_time = pygame.time.get_ticks()
		self.allow_input = False
		self.timer_length = 300

		# touchscreen fingers pressed dictionary
		self.fingers = {}

		# gamepade
		self.joysticks = pygame.joystick.get_count()
		if self.joysticks > 0:
			self.joystick = pygame.joystick.Joystick(0)
			self.joystick.init()		

		#self.show_debug_info = SHOW_DEBUG_INFO


	def setup_nodes(self):
		self.nodes = pygame.sprite.Group()

		for index, node_data in enumerate(levels.values()):
			if index <= self.max_level:
				node_sprite = Node(node_data['node_pos'],'available',self.speed,node_data['node_graphics'])
			else:
				node_sprite = Node(node_data['node_pos'],'locked',self.speed,node_data['node_graphics'])
			self.nodes.add(node_sprite)

	def draw_paths(self):
		if self.max_level > 0:
			points = [node['node_pos'] for index,node in enumerate(levels.values()) if index <= self.max_level]
			pygame.draw.lines(self.display_surface,'#a04f45',False,points,6)

	def setup_icon(self):
		self.icon = pygame.sprite.GroupSingle()
		icon_sprite = Icon(self.nodes.sprites()[self.current_level].rect.center)
		self.icon.add(icon_sprite)

	def input(self, selected_line_up, selected_line_down, get_touchscreen_panel):
		# touchscreen support
		pygame.event.pump()
		
		panel_name = ""
		self.fingers = {}
		for event in pygame.event.get(pygame.FINGERDOWN, pump=False):
			self.fingers[event.finger_id] = (event.x, event.y)

		for event in pygame.event.get(pygame.FINGERMOTION, pump=False):
			self.fingers[event.finger_id] = (event.x, event.y)

		# for event in pygame.event.get(pygame.FINGERUP, pump=False):
		# 	try:
		# 		del self.fingers[event.finger_id]
		# 	except:
		# 		pass

		for finger_id in self.fingers:
			x, y = self.fingers[finger_id]
			panel_name = get_touchscreen_panel(x,y)

			print(x,y)
			print(panel_name)

			#self.debug_log("x: {:>4.2f}, y: {:>4.2f}".format(x,y))
			#self.debug_log(panel_name)
				
		# mouse support
		# MOUSEBUTTONUP is also triggered after FINGERUP !!!
		# skip it if touchscreen has already detected event
		if panel_name == "" or len(self.fingers) == 0:
			for event in pygame.event.get(pygame.MOUSEBUTTONUP, pump=False):
				x,y = pygame.mouse.get_pos()
				panel_name = get_touchscreen_panel(x,y)

				print(x,y)
				print(panel_name)

				#self.debug_log("x: {:>4.2f}, y: {:>4.2f}".format(x,y))
				self.debug_log("mouse {}".format(panel_name))
				
		# gamepad support
		keys = pygame.key.get_pressed()

		axis_0   = 0.0
		button_0 = 0.0
		button_1 = 0.0				
		button_2 = 0.0				
		if self.joysticks  > 0:
			axis_0 = self.joystick.get_axis(0)
			button_0 = self.joystick.get_button(0) 
			button_1 = self.joystick.get_button(1) 
			button_2 = self.joystick.get_button(2) 
		
		# keyboard support
		if not self.moving and self.allow_input:
			if keys[pygame.K_q] or keys[pygame.K_ESCAPE] or button_1 or panel_name == "BACK":
					pygame.quit()
					sys.exit()			
			elif (keys[pygame.K_RIGHT] or axis_0 > 0.5 or panel_name == "RIGHT") and self.current_level < self.max_level:
				self.move_direction = self.get_movement_data('next')
				self.current_level += 1
				self.moving = True
			elif (keys[pygame.K_LEFT] or axis_0 < -0.5 or panel_name == "LEFT") and self.current_level > 0:
				self.move_direction = self.get_movement_data('previous')
				self.current_level -= 1
				self.moving = True
			elif (keys[pygame.K_UP]):
				selected_line_up()
			elif (keys[pygame.K_DOWN]):
				selected_line_down()
			elif keys[pygame.K_SPACE] or button_0 or panel_name == "SELECT":
				self.create_level(self.current_level)
			elif keys[pygame.K_BACKQUOTE] or button_2:
				self.cfg.show_debug_info = not self.cfg.show_debug_info

	def get_movement_data(self,target):
		start = pygame.math.Vector2(self.nodes.sprites()[self.current_level].rect.center)
		
		if target == 'next': 
			end = pygame.math.Vector2(self.nodes.sprites()[self.current_level + 1].rect.center)
		else:
			end = pygame.math.Vector2(self.nodes.sprites()[self.current_level - 1].rect.center)

		return (end - start).normalize()

	def update_icon_pos(self):
		if self.moving and self.move_direction:
			self.icon.sprite.pos += self.move_direction * self.speed
			target_node = self.nodes.sprites()[self.current_level]
			if target_node.detection_zone.collidepoint(self.icon.sprite.pos):
				self.moving = False
				self.move_direction = pygame.math.Vector2(0,0)

	def input_timer(self):
		if not self.allow_input:
			current_time = pygame.time.get_ticks()
			if current_time - self.start_time >= self.timer_length:
				self.allow_input = True

	def run(self, selected_line_up, selected_line_down, get_touchscreen_panel, debug_log):
		self.debug_log = debug_log
		self.input_timer()
		self.input(selected_line_up, selected_line_down, get_touchscreen_panel)
		self.update_icon_pos()
		self.icon.update()
		self.nodes.update()

		self.sky.draw(self.display_surface)
		self.draw_paths()
		self.nodes.draw(self.display_surface)
		self.icon.draw(self.display_surface)