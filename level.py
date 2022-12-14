from re import S
import pygame
from support import import_csv_layout, import_cut_graphics
#from settings import * #tile_size, SCREEN_HEIGHT, SCREEN_WIDTH
from tiles import Tile, StaticTile, Crate, Coin, Palm, Heart
from enemy import Enemy
from decoration import Sky, Water, Clouds
from player import Player
from particles import ParticleEffect
from game_data import levels

class Level:
	def __init__(self, current_level, cfg, create_overworld, change_coins, change_health):
		
		# dirty hack, actuall fun passed in run, but should be passed in init
		self.get_touchscreen_panel = lambda x, y: "NONE"

		#self.show_debug_info = cfg.SHOW_DEBUG_INFO
		
		# general setup
		self.cfg = cfg
		self.display_surface = cfg.screen
		self.world_shift = 0
		self.current_x = None
		self.dt = 0.0

		# audio 
		self.coin_sound = pygame.mixer.Sound('audio/effects/coin.ogg')
		self.stomp_sound = pygame.mixer.Sound('audio/effects/stomp.ogg')
		self.heart_sound = pygame.mixer.Sound('audio/effects/heart.ogg')

		# overworld connection 
		self.create_overworld = create_overworld
		self.current_level = current_level
		level_data = levels[self.current_level]
		self.new_max_level = level_data['unlock']

		# player 
		player_layout = import_csv_layout(level_data['player'])
		self.player = pygame.sprite.GroupSingle()
		self.goal = pygame.sprite.GroupSingle()

		# user interface 
		self.change_coins = change_coins
		self.change_health = change_health

		# dust 
		self.dust_sprite = pygame.sprite.GroupSingle()
		self.player_on_ground = False

		# explosion particles 
		self.explosion_sprites = pygame.sprite.Group()

		# terrain setup
		terrain_layout = import_csv_layout(level_data['terrain'])
		self.level_width  = len(terrain_layout[0]) * self.cfg.tile_size
		self.level_height = len(terrain_layout) * self.cfg.tile_size
		#print(f"screen width: {self.cfg.screen_width / self.cfg.tile_size} height: {self.cfg.screen_height / self.cfg.tile_size}")
		#print(f"level  width: {len(terrain_layout[0])} height: {len(terrain_layout)}")
		
		self.cfg.vertical_offset = ( self.cfg.vertical_tile_number - len(terrain_layout) ) * self.cfg.tile_size
		#print(f"vertical tile number: {self.cfg.vertical_tile_number} offset: {self.cfg.vertical_offset}")

		self.player_setup(player_layout, change_health)

		self.terrain_sprites = self.create_tile_group(terrain_layout,'terrain')

		# grass setup 
		grass_layout = import_csv_layout(level_data['grass'])
		self.grass_sprites = self.create_tile_group(grass_layout, 'grass')

		# crates 
		crate_layout = import_csv_layout(level_data['crates'])
		self.crate_sprites = self.create_tile_group(crate_layout, 'crates')

		# coins 
		coin_layout = import_csv_layout(level_data['coins'])
		self.coin_sprites = self.create_tile_group(coin_layout, 'coins')

		# hearts
		heart_layout = import_csv_layout(level_data['coins'])
		self.heart_sprites = self.create_tile_group(heart_layout, 'hearts')

		# foreground palms 
		fg_palm_layout = import_csv_layout(level_data['fg palms'])
		self.fg_palm_sprites = self.create_tile_group(fg_palm_layout, 'fg palms')

		# background palms 
		bg_palm_layout = import_csv_layout(level_data['bg palms'])
		self.bg_palm_sprites = self.create_tile_group(bg_palm_layout, 'bg palms')

		# enemy 
		enemy_layout = import_csv_layout(level_data['enemies'])
		self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemies')

		# constraint 
		constraint_layout = import_csv_layout(level_data['constraints'])
		self.constraint_sprites = self.create_tile_group(constraint_layout, 'constraint')

		# decoration 
		self.sky = Sky(self.cfg)
		self.water = Water(self.cfg, self.level_width)
		self.clouds = Clouds(self.cfg, self.level_width, 30)

	def create_tile_group(self, layout, type):
		sprite_group = pygame.sprite.Group()
		#print(f"vertical tile number: {self.cfg.vertical_tile_number} offset: {self.cfg.vertical_offset}")

		for row_index, row in enumerate(layout):
			for col_index,val in enumerate(row):
				if val != '-1':
					x = col_index * self.cfg.tile_size
					y = self.cfg.vertical_offset + (row_index * self.cfg.tile_size)
					sprite = None

					if type == 'terrain':
						terrain_tile_list = import_cut_graphics('graphics/terrain/terrain_tiles.png', self.cfg.tile_size)
						tile_surface = terrain_tile_list[int(val)]
						sprite = StaticTile(self.cfg.tile_size, x, y, tile_surface)
						
					if type == 'grass':
						grass_tile_list = import_cut_graphics('graphics/decoration/grass/grass.png', self.cfg.tile_size)
						tile_surface = grass_tile_list[int(val)]
						sprite = StaticTile(self.cfg.tile_size, x, y, tile_surface)
					
					if type == 'crates':
						sprite = Crate(self.cfg.tile_size,x,y)

					if type == 'coins':
						if val == '0': sprite = Coin(self.cfg.tile_size, x, y,'graphics/coins/gold', 5)
						if val == '1': sprite = Coin(self.cfg.tile_size, x, y,'graphics/coins/silver', 1)

					if type == 'hearts':
						if val == '2': sprite = Heart(self.cfg.tile_size,x,y,'graphics/coins/potion')

					if type == 'fg palms':
						if val == '0': sprite = Palm(self.cfg.tile_size,x,y,'graphics/terrain/palm_small',38)
						if val == '1': sprite = Palm(self.cfg.tile_size,x,y,'graphics/terrain/palm_large',64)
						if val == '7': sprite = Palm(self.cfg.tile_size,x,y,'graphics/terrain/palm_small_short',-10)

					if type == 'bg palms':
						sprite = Palm(self.cfg.tile_size,x,y,'graphics/terrain/palm_bg', 64)

					if type == 'enemies':
						sprite = Enemy(self.cfg.tile_size,x,y)

					if type == 'constraint':
						sprite = Tile(self.cfg.tile_size,x,y)
					
					if sprite:
						sprite_group.add(sprite)
		
		return sprite_group

	def player_setup(self,layout,change_health):
		for row_index, row in enumerate(layout):
			for col_index,val in enumerate(row):
				x = col_index * self.cfg.tile_size
				y =  + self.cfg.vertical_offset + (row_index * self.cfg.tile_size)
				if val == '0':
					sprite = Player((x ,y), self.cfg, self.create_jump_particles, change_health)
					self.player.add(sprite)
				if val == '1':
					hat_surface = pygame.image.load('graphics/character/hat.png').convert_alpha()
					sprite = StaticTile(self.cfg.tile_size, x, y, hat_surface)
					self.goal.add(sprite)

	def enemy_collision_reverse(self):
		for enemy in self.enemy_sprites.sprites():
			if pygame.sprite.spritecollide(enemy,self.constraint_sprites,False):
				enemy.reverse()

	def create_jump_particles(self,pos):
		if self.player.sprite.facing_right:
			pos -= pygame.math.Vector2(10,5)
		else:
			pos += pygame.math.Vector2(10,-5)
		jump_particle_sprite = ParticleEffect(pos,'jump')
		self.dust_sprite.add(jump_particle_sprite)

	def horizontal_movement_collision(self):
		player = self.player.sprite
		#player.collision_rect.x += player.direction.x * player.speed
		player.collision_rect.x += player.direction.x * player.speed
		collidable_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites() + self.fg_palm_sprites.sprites()
		for sprite in collidable_sprites:
			if sprite.rect.colliderect(player.collision_rect):
				if player.direction.x < 0: 
					player.collision_rect.left = sprite.rect.right
					player.on_left = True
					self.current_x = player.rect.left
				elif player.direction.x > 0:
					player.collision_rect.right = sprite.rect.left
					player.on_right = True
					self.current_x = player.rect.right

	def vertical_movement_collision(self, dt):
		player = self.player.sprite
		player.apply_gravity(dt)
		collidable_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites() + self.fg_palm_sprites.sprites()

		for sprite in collidable_sprites:
			if sprite.rect.colliderect(player.collision_rect):
				if player.direction.y > 0: 
					player.collision_rect.bottom = sprite.rect.top
					player.direction.y = 0
					player.on_ground = True
				elif player.direction.y < 0:
					player.collision_rect.top = sprite.rect.bottom
					player.direction.y = 0
					player.on_ceiling = True

		if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
			player.on_ground = False

	def scroll_x(self, dt):
		player = self.player.sprite
		player_x = player.rect.centerx
		direction_x = player.direction.x

		if player_x < self.cfg.screen_width / 4 and direction_x < 0:
			self.world_shift = player.MAX_SPEED * dt
			player.speed = 0
		elif player_x > self.cfg.screen_width - (self.cfg.screen_width / 4) and direction_x > 0:
			self.world_shift = -player.MAX_SPEED * dt
			player.speed = 0
		else:
			self.world_shift = 0
			player.speed = player.MAX_SPEED * dt

	def get_player_on_ground(self):
		if self.player.sprite.on_ground:
			self.player_on_ground = True
		else:
			self.player_on_ground = False

	def create_landing_dust(self):
		if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
			if self.player.sprite.facing_right:
				offset = pygame.math.Vector2(10,15)
			else:
				offset = pygame.math.Vector2(-10,15)
			fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset, 'land')
			self.dust_sprite.add(fall_dust_particle)

	def check_death(self, dt):			
		if self.player.sprite.rect.top > self.cfg.screen_height:
			if not self.cfg.god_mode:
				self.create_overworld(self.current_level, 0)
			else:
				self.player.sprite.safe(dt)

			
	def check_win(self):
		if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
			self.create_overworld(self.current_level, self.new_max_level)
			
	def check_coin_collisions(self):
		collided_coins = pygame.sprite.spritecollide(self.player.sprite, self.coin_sprites, True)
		if collided_coins:
			if self.cfg.enable_sound_effects:
				self.coin_sound.play()
			for coin in collided_coins:
				self.change_coins(coin.value)

	def check_heart_collisions(self):
		collided_hearts = pygame.sprite.spritecollide(self.player.sprite, self.heart_sprites, True)
		if collided_hearts:
			if self.cfg.enable_sound_effects:
				self.heart_sound.play()
			for coin in collided_hearts:
				self.change_health(self.cfg.heart_recovery)

	def check_enemy_collisions(self):
		enemy_collisions = pygame.sprite.spritecollide(self.player.sprite, self.enemy_sprites, False)

		if enemy_collisions:
			for enemy in enemy_collisions:
				enemy_center = enemy.rect.centery
				enemy_top = enemy.rect.top
				player_bottom = self.player.sprite.rect.bottom
				if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y >= 0:
					if self.cfg.enable_sound_effects:
						self.stomp_sound.play()
					self.player.sprite.direction.y = -15
					explosion_sprite = ParticleEffect(enemy.rect.center,'explosion')
					self.explosion_sprites.add(explosion_sprite)
					enemy.kill()
				else:
					if not self.cfg.god_mode:
						self.player.sprite.get_damage()

	def run(self, dt, get_touchscreen_panel, debug_log):
		# run the entire game / level 
		
		self.dt = dt
		# touchscreen handle
		self.get_touchscreen_panel = get_touchscreen_panel
		self.debug_log = debug_log

		# sky 
		self.sky.draw(self.display_surface)
		if self.cfg.moving_clouds:
			self.clouds.draw(self.display_surface,self.world_shift)
		else:
			self.clouds.draw(self.display_surface,0)
		
		# background palms
		self.bg_palm_sprites.update(self.world_shift)
		self.bg_palm_sprites.draw(self.display_surface) 

		# dust particles 
		self.dust_sprite.update(self.world_shift)
		self.dust_sprite.draw(self.display_surface)
		
		# terrain 
		self.terrain_sprites.update(self.world_shift)
		self.terrain_sprites.draw(self.display_surface)
		
		# enemy 
		self.enemy_sprites.update(self.world_shift, dt)
		self.constraint_sprites.update(self.world_shift)
		self.enemy_collision_reverse()
		self.enemy_sprites.draw(self.display_surface)
		self.explosion_sprites.update(self.world_shift)
		self.explosion_sprites.draw(self.display_surface)

		# crate 
		self.crate_sprites.update(self.world_shift)
		self.crate_sprites.draw(self.display_surface)

		# grass
		self.grass_sprites.update(self.world_shift)
		self.grass_sprites.draw(self.display_surface)

		# coins 
		self.coin_sprites.update(self.world_shift)
		self.coin_sprites.draw(self.display_surface)

		# hearts
		self.heart_sprites.update(self.world_shift)
		self.heart_sprites.draw(self.display_surface)
		for heart in self.heart_sprites.sprites():
			self.debug_log("curr frames : {:4} heart curr frame: {:4.2f} curr frame int {:2}".format(self.cfg.frame_no, heart.frame_index, int(heart.frame_index)))
			#self.debug_log("Heart curr frame: {:4.2f}".format(heart.frame_index))
			break

		# foreground palms
		self.fg_palm_sprites.update(self.world_shift)
		self.fg_palm_sprites.draw(self.display_surface)

		# player sprites		 
		self.player.update(self.dt, self.get_touchscreen_panel, debug_log)
		#self.cfg.show_debug_info = self.player.sprite.show_debug_info
		#print(self.player.sprite.status)
		if self.player.sprite.status == 'quit':
			self.create_overworld(self.current_level, 0)
		self.horizontal_movement_collision()
		
		self.get_player_on_ground()
		self.vertical_movement_collision(dt)
		self.create_landing_dust()
		
		self.scroll_x(dt)
		self.player.draw(self.display_surface)
		self.goal.update(self.world_shift)
		self.goal.draw(self.display_surface)

		self.check_death(dt)
		self.check_win()

		self.check_coin_collisions()
		self.check_heart_collisions()
		self.check_enemy_collisions()

		# water 
		self.water.draw(self.display_surface,self.world_shift)

		# try:
		# 	pass
		# except Exception as e:
		# 	print("EXCEPTION: {}".format(e))
		# 	self.debug_log("EXCEPTION: {}".format(e))