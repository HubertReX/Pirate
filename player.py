#from cgi import print_arguments
import sys
import pygame
# from settings import * 
from support import import_folder
from math import sin

class Player(pygame.sprite.Sprite):
	def __init__(self, pos, cfg, create_jump_particles, change_health):
		super().__init__()
		self.cfg = cfg
		self.import_character_assets()
		self.frame_index = 0
		self.animation_speed = 0.15 * 60
		self.image = self.animations['idle'][self.frame_index]
		self.rect = self.image.get_rect(topleft = pos)
		self.pos = pygame.math.Vector2(self.rect.topleft)

		self.debug_log = lambda text: print(text)

		#self.show_debug_info = SHOW_DEBUG_INFO
		
		# dust particles 
		self.import_dust_run_particles()
		self.dust_frame_index = 0
		self.dust_animation_speed = 0.15
		self.display_surface = cfg.screen
		self.create_jump_particles = create_jump_particles

		# player movement
		self.direction = pygame.math.Vector2(0,0)
		self.MAX_SPEED = 8 * 60
		self.speed = self.MAX_SPEED
		self.gravity = 0.8 * 60
		self.jump_speed = -16 * 60
		self.collision_rect = pygame.Rect(self.rect.topleft,(50,self.rect.height))

		# player status
		self.status = 'idle'
		self.facing_right = True
		self.on_ground = False
		self.on_ceiling = False
		self.on_left = False
		self.on_right = False

		# health management
		self.change_health = change_health
		self.invincible = False
		self.invincibility_duration = 500
		self.hurt_time = 0

		# audio 
		self.jump_sound = pygame.mixer.Sound('audio/effects/jump.ogg')
		self.jump_sound.set_volume(0.5)
		self.hit_sound = pygame.mixer.Sound('audio/effects/hit.ogg')
		
		# touchscreen setup
		self.fingers = {}

		# gamepad setup
		self.joysticks = pygame.joystick.get_count()
		if self.joysticks > 0:
			self.joystick = pygame.joystick.Joystick(0)
			self.joystick.init()




	def import_character_assets(self):
		character_path = 'graphics/character/'
		self.animations = {'idle':[],'run':[],'jump':[],'fall':[]}

		for animation in self.animations.keys():
			full_path = character_path + animation
			self.animations[animation] = import_folder(full_path)

	def import_dust_run_particles(self):
		self.dust_run_particles = import_folder('graphics/character/dust_particles/run')

	def animate(self, dt):
		animation = self.animations[self.status]

		# loop over frame index 
		self.frame_index += self.animation_speed * dt
		if self.frame_index >= len(animation):
			self.frame_index = 0

		image = animation[int(self.frame_index)]
		if self.facing_right:
			self.image = image
			self.rect.bottomleft = self.collision_rect.bottomleft
		else:
			flipped_image = pygame.transform.flip(image,True,False)
			self.image = flipped_image
			self.rect.bottomright = self.collision_rect.bottomright

		if self.invincible:
			alpha = self.wave_value()
			self.image.set_alpha(alpha)
		else:
			self.image.set_alpha(255)

		self.rect = self.image.get_rect(midbottom = self.rect.midbottom)		

	def run_dust_animation(self, dt):
		if self.status == 'run' and self.on_ground:
			self.dust_frame_index += self.dust_animation_speed
			if self.dust_frame_index >= len(self.dust_run_particles):
				self.dust_frame_index = 0

			dust_particle = self.dust_run_particles[int(self.dust_frame_index)]

			if self.facing_right:
				pos = self.rect.bottomleft - pygame.math.Vector2(6,10)
				self.display_surface.blit(dust_particle,pos)
			else:
				pos = self.rect.bottomright - pygame.math.Vector2(6,10)
				flipped_dust_particle = pygame.transform.flip(dust_particle,True,False)
				self.display_surface.blit(flipped_dust_particle,pos)

	def get_input(self, get_touchscreen_panel, dt):
		keys = pygame.key.get_pressed()
		
		# touchscreen support
		pygame.event.pump()
		
		panel_name = ""
		# self.fingers = {}
		for event in pygame.event.get(pygame.FINGERDOWN, pump=False):
			# x = 0.18 m_x = 212
			# y = 0.88 mx_ = 449
			# w * 0.18 = 212
			self.fingers[event.finger_id] = (event.x * self.cfg.screen_width, event.y * self.cfg.screen_height)
			#self.debug_log("FINGER_DOWN {} x: {:>4.2f}, y: {:>4.2f}".format(event.finger_id,event.x, event.y) + get_touchscreen_panel(event.x * self.cfg.screen_width, event.y * self.cfg.screen_height))

		for event in pygame.event.get(pygame.FINGERMOTION, pump=False):
			self.fingers[event.finger_id] = (event.x * self.cfg.screen_width, event.y * self.cfg.screen_height)
			#self.debug_log("FINGER_MOTION {} x: {:>4.2f}, y: {:>4.2f}".format(event.finger_id,event.x, event.y) + get_touchscreen_panel(event.x * self.cfg.screen_width, event.y * self.cfg.screen_height))

		for event in pygame.event.get(pygame.FINGERUP, pump=False):
			if event.finger_id in self.fingers:
				del self.fingers[event.finger_id]
			#self.debug_log("FINGER_UP {} x: {:>4.2f}, y: {:>4.2f}".format(event.finger_id,event.x, event.y) + get_touchscreen_panel(event.x * self.cfg.screen_width, event.y * self.cfg.screen_height))

		#MESSAGE_LOG = "FINGERS: {}".format(len(self.fingers))

		for finger_id in self.fingers:
			x, y = self.fingers[finger_id]
			panel_name = get_touchscreen_panel(x,y)

			print(x, y)
			print(panel_name)

			#self.debug_log("x: {:>4.2f}, y: {:>4.2f}".format(x, y))
			#self.debug_log(panel_name)
				
		# mouse support
		# MOUSEBUTTONUP is also triggered after FINGERUP !!!
		# skip it if touchscreen has already detected event
		if panel_name == "" or len(self.fingers) == 0:
			for event in pygame.event.get(pygame.MOUSEBUTTONUP, pump=False):
				x, y = pygame.mouse.get_pos()
				panel_name = get_touchscreen_panel(x,y)

				print(x, y)
				print(panel_name)

				#self.debug_log("mouse x: {:>4.2f}, y: {:>4.2f}".format(x, y))
				self.debug_log("mouse {}".format(panel_name))

		# gamepad support
		axis_0   = 0.0
		button_0 = 0.0
		button_1 = 0.0
		button_2 = 0.0
		# print("Gamepads count: {}".format(joysticks))
		gamepad_move = False
		if self.joysticks  > 0:
			#print(joystick.get_name, joystick.get_id, joystick.get_instance_id, joystick.get_guid, joystick.get_power_level)
			
			#axes = self.joystick.get_numaxes()
			#if axes > 0:
			#	axis_0 = joystick.get_axis(0)
			axis_0 = self.joystick.get_axis(0)
			
			#buttons = self.joystick.get_numbuttons()
			#if buttons > 0:
			#	button_0 = joystick.get_button(0) 
			button_0 = self.joystick.get_button(0) 
			button_1 = self.joystick.get_button(1) 
			button_2 = self.joystick.get_button(2) 
			if button_1 > 0:
				self.status = 'quit'
			#print("axes: {} buttons: {}".format(axes, buttons))
			#print("axis_0: {} button_0: {}".format(axis_0, joystick.get_button(0) ))

			if axis_0 > 0.1:
				self.direction.x = 1
				self.speed = self.MAX_SPEED * axis_0 * dt
				self.facing_right = True
				gamepad_move = True
			elif axis_0 < -0.1:
				self.direction.x = -1
				self.speed = self.MAX_SPEED * axis_0 * dt
				self.facing_right = False
				gamepad_move = True
			else:
				self.direction.x = 0				
			#print("speed:{}".format(self.speed))

			if button_0 == 1 and self.on_ground:
				self.jump(dt)
				self.create_jump_particles(self.rect.midbottom)
		
		# keyboard support
		if (keys[pygame.K_RIGHT] or panel_name == "RIGHT") and not gamepad_move:
			self.direction.x = 1
			self.speed = self.MAX_SPEED * dt
			self.facing_right = True
		elif (keys[pygame.K_LEFT] or panel_name == "LEFT") and not gamepad_move:
			self.direction.x = -1
			self.speed = self.MAX_SPEED * dt
			self.facing_right = False
		elif not gamepad_move:
			self.direction.x = 0

		if (keys[pygame.K_SPACE] or panel_name == "SELECT") and self.on_ground:
			self.jump(dt)
			self.create_jump_particles(self.rect.midbottom)

		if keys[pygame.K_q] or keys[pygame.K_ESCAPE] or panel_name == "BACK":
				#pygame.quit()
				#sys.exit()
				self.status = 'quit'

		if keys[pygame.K_BACKQUOTE] or button_2:
			self.cfg.show_debug_info = not self.cfg.show_debug_info

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				#pygame.quit()
				#sys.exit()	
				self.status = 'quit'		

			
	def get_status(self):
		if self.direction.y < 0:
			self.status = 'jump'
		elif self.direction.y > 1:
			self.status = 'fall'
		else:
			if self.direction.x != 0:
				self.status = 'run'
			else:
				self.status = 'idle'

	def apply_gravity(self, dt):
		self.direction.y += self.gravity * dt
		self.collision_rect.y += self.direction.y

	def jump(self, dt):
		self.direction.y = self.jump_speed * dt
		if self.cfg.enable_sound_effects:
			self.jump_sound.play()

	def safe(self, dt):
		self.direction.y = 2 * self.jump_speed * dt
		if self.cfg.enable_sound_effects:
			self.jump_sound.play()


	def get_damage(self):
		if not self.invincible:
			if self.cfg.enable_sound_effects:
				self.hit_sound.play()
			self.change_health(-10)
			self.invincible = True
			self.hurt_time = pygame.time.get_ticks()

	def invincibility_timer(self):
		if self.invincible:
			current_time = pygame.time.get_ticks()
			if current_time - self.hurt_time >= self.invincibility_duration:
				self.invincible = False

	def wave_value(self):
		value = sin(pygame.time.get_ticks())
		if value >= 0: return 255
		else: return 0

	def update(self, dt, get_touchscreen_panel, debug_log):
		self.debug_log = debug_log
		self.get_input(get_touchscreen_panel, dt)
		if self.status != 'quit':
			self.get_status()
			self.animate(dt)
			self.run_dust_animation(dt)
		self.invincibility_timer()
		self.wave_value()


		