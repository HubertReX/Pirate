#from cgi import print_arguments
import sys
import pygame 
from support import import_folder
from math import sin

class Player(pygame.sprite.Sprite):
	def __init__(self,pos,surface,create_jump_particles,change_health):
		super().__init__()
		self.import_character_assets()
		self.frame_index = 0
		self.animation_speed = 0.15
		self.image = self.animations['idle'][self.frame_index]
		self.rect = self.image.get_rect(topleft = pos)
		
		# dust particles 
		self.import_dust_run_particles()
		self.dust_frame_index = 0
		self.dust_animation_speed = 0.15
		self.display_surface = surface
		self.create_jump_particles = create_jump_particles

		# player movement
		self.direction = pygame.math.Vector2(0,0)
		self.MAX_SPEED = 8
		self.speed = self.MAX_SPEED
		self.gravity = 0.8
		self.jump_speed = -16
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
		self.jump_sound = pygame.mixer.Sound('audio/effects/jump.wav')
		self.jump_sound.set_volume(0.5)
		self.hit_sound = pygame.mixer.Sound('audio/effects/hit.wav')
		

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

	def animate(self):
		animation = self.animations[self.status]

		# loop over frame index 
		self.frame_index += self.animation_speed
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

	def run_dust_animation(self):
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

	def get_input(self):
		keys = pygame.key.get_pressed()
		
		axis_0   = 0.0
		button_0 = 0.0
		button_1 = 0.0
		# print("Gamepads count: {}".format(joysticks))
		gamepad_move = False
		if self.joysticks  > 0:
			#print(joystick.get_name, joystick.get_id, joystick.get_instance_id, joystick.get_guid, joystick.get_power_level)
			
			axes = self.joystick.get_numaxes()
			#if axes > 0:
			#	axis_0 = joystick.get_axis(0)
			axis_0 = self.joystick.get_axis(0)
			
			buttons = self.joystick.get_numbuttons()
			#if buttons > 0:
			#	button_0 = joystick.get_button(0) 
			button_0 = self.joystick.get_button(0) 
			button_1 = self.joystick.get_button(1) 
			if button_1 > 0:
				self.status = 'quit'
			#print("axes: {} buttons: {}".format(axes, buttons))
			#print("axis_0: {} button_0: {}".format(axis_0, joystick.get_button(0) ))

			if axis_0 > 0.1:
				self.direction.x = 1
				self.speed = self.MAX_SPEED * axis_0
				self.facing_right = True
				gamepad_move = True
			elif axis_0 < -0.1:
				self.direction.x = -1
				self.speed = self.MAX_SPEED * axis_0 * -1
				self.facing_right = False
				gamepad_move = True
			else:
				self.direction.x = 0				
			#print("speed:{}".format(self.speed))

			if button_0 == 1 and self.on_ground:
				self.jump()
				self.create_jump_particles(self.rect.midbottom)

		if keys[pygame.K_RIGHT] and not gamepad_move:
			self.direction.x = 1
			self.facing_right = True
		elif keys[pygame.K_LEFT] and not gamepad_move:
			self.direction.x = -1
			self.facing_right = False
		elif not gamepad_move:
			self.direction.x = 0

		if keys[pygame.K_SPACE] and self.on_ground:
			self.jump()
			self.create_jump_particles(self.rect.midbottom)

		if keys[pygame.K_q] or keys[pygame.K_ESCAPE]:
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

	def apply_gravity(self):
		self.direction.y += self.gravity
		self.collision_rect.y += self.direction.y

	def jump(self):
		self.direction.y = self.jump_speed
		self.jump_sound.play()

	def safe(self):
		self.direction.y = 2 * self.jump_speed
		self.jump_sound.play()


	def get_damage(self):
		if not self.invincible:
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

	def update(self):
		self.get_input()
		if self.status != 'quit':
			self.get_status()
			self.animate()
			self.run_dust_animation()
		self.invincibility_timer()
		self.wave_value()

		