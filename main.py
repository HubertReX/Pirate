import asyncio
from configuration import configuration
import pygame
import sys
import time
from settings import DEBUG_LEVEL
from level import Level
from overworld import Overworld
from ui import UI
import logging

debug_fmt = '[%(levelname)7s] %(asctime)s: %(message)s'
logging.basicConfig(level=DEBUG_LEVEL, format=debug_fmt)


class Game:
    def __init__(self):
        self.process_env()
        self.cfg = configuration(self.is_mobile, self.is_web)
        self.screen = self.cfg.screen

        # game attributes
        self.max_level = self.cfg.start_max_level
        self.max_health = self.cfg.start_max_health
        self.cur_health = self.max_health
        self.coins = 0
        self.prev_time = time.perf_counter()
        self.dt = time.perf_counter() - self.prev_time

        # current fps
        self.fps = 0
        self.cfg.frame_no = 0

        # audio
        self.level_bg_music = pygame.mixer.Sound('audio/level_music.ogg')
        self.overworld_bg_music = pygame.mixer.Sound(
            'audio/overworld_music.ogg')

        # overworld creation
        self.overworld = Overworld(
            0, self.max_level, self.cfg, self.create_level)
        self.status = 'overworld'
        if self.cfg.enable_sound_on_start:
            self.overworld_bg_music.play(loops=-1)

        # user interface
        self.ui = UI(self.cfg)
        if self.cfg.god_mode:
            self.ui.button_debug.enable()
        else:
            self.ui.button_debug.disable()

    def process_env(self):
        if (sys.platform == "emscripten"):
            self.is_web = True
            logging.info("Running inside Web")
        else:
            self.is_web = False

        
        self.is_mobile = False
        n = len(sys.argv)
        if n > 1:
            logging.debug("__________ ARGV ___________")
            for i in range(1, n):
                logging.debug(sys.argv[i])
                if "mobile=" in sys.argv[i]:
                    mobile = sys.argv[i].split("=")[1]
                    if mobile.upper() != "FALSE":
                        self.is_mobile = mobile
                        logging.info("Running on mobile phone")

    def tick(self):
        self.dt = time.perf_counter() - self.prev_time
        self.prev_time = time.perf_counter()
        self.cfg.frame_no += 1

    def create_level(self, current_level):
        self.level = Level(current_level, self.cfg, self.create_overworld,
                           self.change_coins, self.change_health)
        self.status = 'level'
        self.overworld_bg_music.stop()
        if self.cfg.enable_sound_on_start:
            self.level_bg_music.play(loops=-1)

    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(
            current_level, self.max_level, self.cfg, self.create_level)
        self.status = 'overworld'
        self.level_bg_music.stop()
        if self.cfg.enable_sound_on_start:
            self.overworld_bg_music.play(loops=-1)

    def change_coins(self, amount):
        self.coins += amount

    def change_health(self, amount):
        self.cur_health += amount
        if self.cur_health > self.max_health:
            self.cur_health = self.max_health

    def show_overworld(self):
        self.cur_health = 100
        self.coins = 0
        #self.max_level = 0
        self.overworld = Overworld(
            0, self.max_level, self.cfg, self.create_level)
        self.status = 'overworld'
        self.level_bg_music.stop()
        if self.cfg.enable_sound_on_start:
            self.overworld_bg_music.play(loops=-1)

    def check_game_over(self):
        if self.cur_health <= 0:
            self.show_overworld()

    def run(self):
        self.screen.fill('grey')
        if self.status == 'overworld':
            self.overworld.run(self.ui.debug_panel.selected_line_up,
                               self.ui.debug_panel.selected_line_down, self.ui.get_touchscreen_panel, self.ui.debug_log)
            self.ui.show_titles("Pirate! Arrr...")
            self.ui.reset()
            self.ui.show_fps(self.fps)
            self.ui.debug_panel.print("Delta time: {:<4.3f}".format(self.dt))
            #self.ui.debug_panel.print("Is mobile: {}".format(self.cfg.is_mobile))
            #self.ui.debug_panel.print("In web: {}".format(__EMSCRIPTEN__))
            #self.ui.debug_panel.print("Resolution: {}x{}".format(self.cfg.screen_width, self.cfg.screen_height))
            self.ui.button_select.set_text("Select")
    


            if self.cfg.show_debug_info and self.cfg.god_mode:
                self.ui.button_up.enable()
                self.ui.button_down.enable()               
                self.ui.show_debug_info()
            else:
               self.ui.button_up.disable()
               self.ui.button_down.disable()

            if self.cfg.is_mobile or self.cfg.show_touchscreen:
                self.ui.show_touchscreen_info()
        else:
            self.ui.reset()
            self.level.run(
                self.dt, self.ui.get_touchscreen_panel, self.ui.debug_log)
            self.ui.show_fps(self.fps)
            self.ui.debug_panel.print("Delta time: {:<4.3f}".format(self.dt))
            self.ui.button_select.set_text("Jump")

            self.ui.show_health(self.cur_health, self.max_health)
            self.ui.show_coins(self.coins)
            if self.cfg.show_debug_info and self.cfg.god_mode:
                self.ui.button_up.enable()
                self.ui.button_down.enable()        
                self.ui.show_debug_info()
            else:
               self.ui.button_up.disable()
               self.ui.button_down.disable()
     
            if self.cfg.is_mobile or self.cfg.show_touchscreen:
                self.ui.show_touchscreen_info()
            self.check_game_over()


async def main():

    # Pygame setup
    pygame.init()
    # Initialize gamepad
    pygame.joystick.init()

    clock = pygame.time.Clock()
    game = Game()

    while game.cfg.is_running:
        game.tick()
        # for event in pygame.event.get():
        # 	if event.type == pygame.QUIT:
        # 		pygame.quit()
        # 		sys.exit()

        game.run()

        pygame.display.update()
        await asyncio.sleep(0)  # very important, and keep it 0
        clock.tick(game.cfg.max_fps)
        # clock.tick()
        game.fps = clock.get_fps() 
    #logging.debug("stop bg music before clean exit")
    game.overworld_bg_music.stop()
    game.overworld.game_over(game.ui.show_game_over)
    pygame.display.update()

if __name__ == '__main__':
    asyncio.run(main())

# do not add anything from here
# asyncio.run is non block on pygame-wasm
