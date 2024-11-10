import os, sys, time, pygame
# Load our scenes
from states.title import Title
from button import Button, get_font

import asyncio
from configuration import configuration
from settings import DEBUG_LEVEL
from level import Level
from overworld import Overworld
from ui import UI
import logging

debug_fmt = '[%(levelname)7s] %(asctime)s: %(message)s'
logging.basicConfig(level=DEBUG_LEVEL, format=debug_fmt)
class Game():
        def __init__(self):
            # pygame engin initialization
            pygame.init()
            # gamepad initialize (buggy, sometimes works only after 5-10 s.)
            pygame.joystick.init()
            # process command line parameters and environment
            self.process_env()
            # load and set up configuration (incl. resolution)
            self.cfg = configuration(self.is_mobile, self.is_web)   

            self.tile_size = 32
            self.GAME_W = 19 * self.tile_size
            self.GAME_H = 12 * self.tile_size  #  608, 384 # 480, 270
            self.SCREEN_WIDTH = 1280
            self.SCREEN_HEIGHT = 800  # WXGA
            self.x_ration = self.SCREEN_WIDTH  / self.GAME_W
            self.y_ration = self.SCREEN_HEIGHT / self.GAME_H

            self.canvas = pygame.Surface((self.GAME_W, self.GAME_H)) 
            self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
            pygame.display.set_caption("Pirate!")
            
            self.running = True
            self.playing = True
            self.actions = {"left": False, "right": False, "up" : False, "down" : False, "action" : False, "back" : False, "start" : False, "debug" : False, "mouse_button" : False}
            self.dt = 0
            self.prev_time = 0
            self.mouse_pos = (0,0)
            self.state_stack = []
            self.load_assets()
            self.load_states()

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

        def game_loop(self):
            while self.playing:
                self.get_dt()
                self.get_events()
                self.update()
                self.render()

        def quit(self):
            self.playing = False
            self.running = False

        def get_events(self):
            x,y = pygame.mouse.get_pos()
            self.mouse_pos = ( int(x / self.x_ration), int(y / self.y_ration))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.actions['back'] = True
                
                if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        self.actions['back'] = event.type == pygame.KEYDOWN
                    if event.key == pygame.K_a:
                        self.actions['left'] = event.type == pygame.KEYDOWN
                    if event.key == pygame.K_d:
                        self.actions['right'] = event.type == pygame.KEYDOWN
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        self.actions['up'] = event.type == pygame.KEYDOWN
                    if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        self.actions['down'] = event.type == pygame.KEYDOWN
                    if event.key == pygame.K_SPACE:
                        self.actions['action'] = event.type == pygame.KEYDOWN
                    if event.key == pygame.K_o:
                        self.actions['debug'] = event.type == pygame.KEYDOWN
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        self.actions['start'] = event.type == pygame.KEYDOWN
                # if event.type == pygame.KEYDOWN:
                #     if event.key == pygame.K_ESCAPE:
                #        self.actions['back'] = True
                #     if event.key == pygame.K_a:
                #         self.actions['left'] = True
                #     if event.key == pygame.K_d:
                #         self.actions['right'] = True
                #     if event.key == pygame.K_w or event.key == pygame.K_UP:
                #         self.actions['up'] = True
                #     if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                #         self.actions['down'] = True
                #     if event.key == pygame.K_SPACE:
                #         self.actions['action'] = True
                #     if event.key == pygame.K_o:
                #         self.actions['debug'] = True    
                #     if event.key == pygame.K_RETURN:
                #         self.actions['start'] = True  

                # if event.type == pygame.KEYUP:
                #     if event.key == pygame.K_a:
                #         self.actions['left'] = False
                #     if event.key == pygame.K_d:
                #         self.actions['right'] = False
                #     if event.key == pygame.K_w or event.key == pygame.K_UP:
                #         self.actions['up'] = False
                #     if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                #         self.actions['down'] = False
                #     if event.key == pygame.K_SPACE:
                #         self.actions['action'] = False
                #     if event.key == pygame.K_o:
                #         self.actions['debug'] = False
                #     if event.key == pygame.K_RETURN:
                #         self.actions['start'] = False  

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.actions['mouse_button'] = True

                # if self.actions['back']:
                #      self.quit()

        def update(self):
            if len(self.state_stack) > 0:
                self.state_stack[-1].update(self.dt, self.actions)

        def render(self):
            if len(self.state_stack) > 0:
                self.state_stack[-1].render(self.canvas)

            # Render current state to the screen (resize canvas to screen size)
            self.screen.blit(pygame.transform.scale(self.canvas, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)), (0,0))
            pygame.display.flip()

        def get_dt(self):
            self.dt = time.perf_counter() - self.prev_time
            self.prev_time = time.perf_counter()
            self.cfg.frame_no += 1

        def draw_text(self, surface, text, color, x, y):
            text_surface = get_font(20, False).render(
                text, True, color)  # self.font.render(text, True, color)
            #text_surface.set_colorkey((0,0,0))
            text_rect = text_surface.get_rect()
            text_rect.center = (x, y)
            surface.blit(text_surface, text_rect)

        def load_assets(self):
            # Create pointers to directories 
            self.assets_dir = os.path.join("graphics")
            self.sprite_dir = os.path.join(self.assets_dir, "sprites")
            #self.font_dir = os.path.join(self.assets_dir, "font")
            # self.font = pygame.font.Font(os.path.join(self.font_dir, "PressStart2P-vaV7.ttf"), 20)
            #self.get_font = get_font

        def load_states(self):
            self.title_screen = Title(self)
            self.title_screen.enter_state()
            #self.state_stack.append(self.title_screen)

        def reset_keys(self):
            for action in self.actions:
                self.actions[action] = False


if __name__ == "__main__":
    g = Game()
    while g.running:
        g.game_loop()