import pygame, sys, math
import settings

class configuration:
    def __init__(self, is_mobile, is_web):

        self.is_mobile = is_mobile
        self.is_web = is_web

        self.full_screen = settings.FULL_SCREEN

        # toggle wether screen resolution should be scaled in full screen mode
        self.scaled = settings.SCALED

        # playback backgroud music flag
        self.enable_sound_on_start = settings.ENABLE_SOUND_ON_START

        # playback sound effects music flag
        self.enable_sound_effects = settings.ENABLE_SOUND_EFFECTS

        # clouds on the sky moiving along with player
        self.moving_clouds = settings.MOVING_CLOUDS

        # horizon level as % of screen height
        self.horizon_level = settings.HORIZON_LEVEL

        # immortal mode for debug
        self.god_mode = settings.GOD_MODE

        # how many levels are available on start
        self.start_max_level = settings.START_MAX_LEVEL

        # maximum amount of health on start
        self.start_max_health = settings.START_MAX_HEALTH

        # show debug info on start (press '~' or 'x' on gamepad to toggle)
        self.show_debug_info = settings.SHOW_DEBUG_INFO

        # amount of health recovered by a heart
        self.heart_recovery = settings.HEART_RECOVERY

        self.message_log = settings.MESSAGE_LOG

        infoObject = pygame.display.Info()
        self.max_screen_width = infoObject.current_w
        self.max_screen_height = infoObject.current_h
        print("Native resolution {}x{}".format(infoObject.current_w, infoObject.current_h))
        #pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        # self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        self.flags = 0 

        self.tile_size = settings.TILE_SIZE

        if self.scaled:
            self.flags |= pygame.SCALED 
            
        if self.full_screen or self.is_mobile:
            self.flags |= pygame.FULLSCREEN

            self.vertical_tile_number = math.floor(self.max_screen_height / self.tile_size) 

            self.screen_width  = self.max_screen_width 
            self.screen_height = self.vertical_tile_number * self.tile_size

        else:
            self.vertical_tile_number = settings.VERTICAL_TILE_NUMBER

            self.screen_width  = settings.SCREEN_WIDTH   
            self.screen_height = self.vertical_tile_number * self.tile_size
          

        self.vertical_offset = -(self.tile_size * (17 - self.vertical_tile_number))

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height),  self.flags)
        #infoObject = pygame.display.Info()
        curr_screen_width, curr_screen_height = self.screen.get_size()
        self.screen_width = curr_screen_width 
        self.screen_height = curr_screen_height 	 		
        print("Actual resolution {}x{}".format(self.screen_width, self.screen_height))
