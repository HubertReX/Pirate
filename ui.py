#from wsgiref.util import setup_testing_defaults
import logging
#from operator import truediv
#from re import T
#from unittest import case
import pygame
from button import Button, get_font
#from settings import *

# This is a simple class that will help us print to the screen


class TextPrint:
    def __init__(self, surface, start_x, start_y, width, line_height = 15, highlight_color=(255, 0, 0), fill_color=(200, 200, 200), highlight_border=2):
        self.display_surface = surface         
        self.start_x = start_x
        self.start_y = start_y
        self.width = width
        self.line_height = line_height
        self.highlight_color = highlight_color
        self.highlight_border = highlight_border
        self.fill_color = fill_color
        self.reset()
        self.font = pygame.font.Font(None, 20)
        self.highlighted_line = 0
        self.lines_count = 0
        self.log = []

    def selected_line_up(self):
        self.highlighted_line -= 1
        if self.highlighted_line < 0:
            self.highlighted_line = self.lines_count - 1

    def selected_line_down(self):
        self.highlighted_line += 1
        if self.highlighted_line > self.lines_count - 1:
            self.highlighted_line = 0

    def highligt_line(self):
        pygame.draw.rect(self.display_surface, 
                        self.highlight_color, 
                        pygame.Rect(self.start_x - self.highlight_border, 
                                    self.start_y - self.highlight_border + (self.highlighted_line * self.line_height), 
                                    self.width + self.highlight_border * 2, 
                                    self.line_height + self.highlight_border * 2),  
                        self.highlight_border)

    def background_line(self):
        pygame.draw.rect(self.display_surface, 
            self.fill_color, 
            pygame.Rect(self.x,
                    self.y, 
                    self.width, 
                    self.line_height), 
            0)

    def is_point_inside_panel(self, x, y):
        if (x > self.start_x and x < self.start_x + self.width) and (y > self.start_y and y < self.start_y + self.line_height):
            return True

    def add_log(self, message):
        self.log.append(message)

    def print_logs(self):
        for m in self.log:         
            self.print(m)

    def print(self, textString):
        self.background_line()
        textBitmap = self.font.render(textString, True, (50, 50, 50))
        self.display_surface.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height
        self.lines_count += 1
        
    def reset(self):
        self.x = self.start_x 
        self.y = self.start_y
        self.lines_count = 0
        self.log = []
        #self.line_height = self.line_height 
        
        
    def indent(self):
        self.x += 10
        
    def unindent(self):
        self.x -= 10

class UI:
    def __init__(self, cfg):

        # setup 
        self.cfg = cfg
        self.display_surface = self.cfg.screen 

        # health 
        self.health_bar = pygame.image.load('graphics/ui/health_bar.png').convert_alpha()
        self.health_bar_topleft = (54, 39)
        self.bar_max_width = 152
        self.bar_height = 4

        # coins 
        self.coin = pygame.image.load('graphics/ui/coin.png').convert_alpha()
        self.coin_rect = self.coin.get_rect(topleft = (50, 61))
        # wired hack to make it work on web (pygbag for using pygame in WebAssembly aka wasm)
        #self.font = pygame.font.Font('graphics/ui/ARCADEPI.ttf',30)
        self.font = pygame.font.Font(None, 30)

        # Debug info panel
        self.debug_panel = TextPrint(self.display_surface, 10, 10, 200)

        # FPS panel
        self.fps_panel   = TextPrint(self.display_surface, self.cfg.screen_width - 110, 10, 80, 15)

        # touchscreen controlls panel
        button_color = (170, 200, 170)
        #border_color = (255,   0,   0)
        #border_width = 3
        self.buttons = []
        button_size = (64,64)
        self.button_left = Button(self.display_surface, image=pygame.image.load("graphics/touchscreen/left.png"), pos=(50, self.cfg.screen_height - 50), size=button_size,
                                  text_input="←", font=get_font(1, self.cfg.is_web), base_color=button_color, hovering_color="White", action=self.on_press_left)
        self.button_right = Button(self.display_surface, image=pygame.image.load("graphics/touchscreen/right.png"), pos=(250, self.cfg.screen_height - 50), size=button_size,
                                   text_input="→", font=get_font(1, self.cfg.is_web), base_color="#d7fcd4", hovering_color="White", action=self.on_press_right)
        self.button_up    = Button(self.display_surface, image=pygame.image.load("graphics/touchscreen/up.png"), pos=(150, self.cfg.screen_height - 150), size=button_size,
                                   text_input="↑", font=get_font(1, self.cfg.is_web), base_color="#d7fcd4", hovering_color="White", action=self.on_press_up)
        self.button_down  = Button(self.display_surface, image=pygame.image.load("graphics/touchscreen/down.png"), pos=(150, self.cfg.screen_height - 50), size=button_size,
                                   text_input="↓", font=get_font(1, self.cfg.is_web), base_color="#d7fcd4", hovering_color="White", action=self.on_press_down)

        self.button_select = Button(self.display_surface, image=pygame.image.load("graphics/touchscreen/A.png"), pos=(self.cfg.screen_width - 110, self.cfg.screen_height - 50), size=button_size,
                                    text_input="Select", font=get_font(15, self.cfg.is_web), base_color="#d7fcd4", hovering_color="White", action=self.on_press_select)
        self.button_back = Button(self.display_surface, image=pygame.image.load("graphics/touchscreen/B.png"), pos=(self.cfg.screen_width -  60, self.cfg.screen_height - 150), size=button_size,
                                  text_input="Back", font=get_font(15, self.cfg.is_web), base_color="#d7fcd4", hovering_color="White", action=self.on_press_back)
        self.button_debug = Button(self.display_surface, image=pygame.image.load("graphics/touchscreen/X.png"), pos=(self.cfg.screen_width - 160, self.cfg.screen_height - 150), size=button_size,
                                   text_input="Debug", font=get_font(15, self.cfg.is_web), base_color="#d7fcd4", hovering_color="White", action=self.on_press_debug)
        
        self.buttons = [self.button_left, self.button_right, 
                        self.button_up, self.button_down,
                        self.button_select, self.button_back,
                        self.button_debug]
        #self.buttons.append(self.button_left)
        # self.touchscreen_left_panel   = TextPrint(self.display_surface,                           10, self.cfg.screen_height - 100, 100, 90, highlight_color=border_color, fill_color=button_color, highlight_border=border_width)
        # self.touchscreen_right_panel  = TextPrint(self.display_surface,                          150, self.cfg.screen_height - 100, 100, 90, highlight_color=border_color, fill_color=button_color, highlight_border=border_width)
        # self.touchscreen_select_panel = TextPrint(self.display_surface,  self.cfg.screen_width - 110, self.cfg.screen_height - 100, 100, 90, highlight_color=border_color, fill_color=button_color, highlight_border=border_width)
        # self.touchscreen_back_panel   = TextPrint(self.display_surface,  self.cfg.screen_width - 250, self.cfg.screen_height - 100, 100, 90, highlight_color=border_color, fill_color=button_color, highlight_border=border_width)

    def reset(self):
        self.debug_panel.reset()
        self.fps_panel.reset()
        # self.touchscreen_left_panel.reset()
        # self.touchscreen_right_panel.reset()
        # self.touchscreen_select_panel.reset()
        # self.touchscreen_back_panel.reset()

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
        label_surf = get_font(40, self.cfg.is_web).render(
            str(text_label), True, '#9c0000')
        label_rect = label_surf.get_rect(center=(self.cfg.screen_width/2, 100)) 
        self.display_surface.blit(label_surf, label_rect)

    def show_game_over(self):
        label_surf = get_font(60, self.cfg.is_web).render(
            "Game Over", True, '#9c0000')
        label_rect = label_surf.get_rect(center=(self.cfg.screen_width/2, self.cfg.screen_height/2))
        self.display_surface.blit(label_surf, label_rect)        
    
    def show_debug_info(self):
        self.debug_panel.print("Enable sound on start: {}".format(self.cfg.enable_sound_on_start))
        self.debug_panel.print("Moving clouds: {}".format(self.cfg.moving_clouds))
        self.debug_panel.print("God mode: {}".format(self.cfg.god_mode))
        self.debug_panel.print("Start max level: {}".format(self.cfg.start_max_level))
        self.debug_panel.print("Start max health: {}".format(self.cfg.start_max_health))
        self.debug_panel.print("Highlight line: {}".format(self.debug_panel.highlighted_line))
        self.debug_panel.print("Lines count: {}".format(self.debug_panel.lines_count))
        self.debug_panel.highligt_line()
        #self.debug_panel.print("LOG: {}".format(self.cfg.message_log))
        self.debug_panel.print("##### LOGS #####")
        self.debug_panel.print_logs()
    
    def debug_log(self, message):
        self.debug_panel.add_log(message)

    def show_fps(self, fps):
        self.fps_panel.print(f"FPS: {fps:<6.2f}")

    def on_press_left(self):
        return "LEFT"

    def on_press_right(self):
        return "RIGHT"

    def on_press_up(self):
        return "UP"

    def on_press_down(self):
        return "DOWN"

    def on_press_select(self):
        return "SELECT"
        
    def on_press_back(self):
        return "BACK"
        
    def on_press_debug(self):
        return "DEBUG"

    def set_button_text(self, button, text):
        if button == "LEFT":
            self.button_left.set_text(text)
        elif button == "RIGHT":
            self.button_right.set_text(text)
        elif button == "UP":
            self.button_up.set_text(text)
        elif button == "DOWN":
            self.button_down.set_text(text)
        elif button == "A":
            self.button_select.set_text(text)
        elif button == "B":
            self.button_back.set_text(text)
        elif button == "X":
            self.button_debug.set_text(text)

    def show_touchscreen_info(self):
        for button in self.buttons:
            button.changeColor(pygame.mouse.get_pos())
            button.update()
        # self.touchscreen_left_panel.highligt_line()
        # self.touchscreen_left_panel.background_line()
        # self.touchscreen_left_panel.print("LEFT")

        # self.touchscreen_right_panel.highligt_line()
        # self.touchscreen_right_panel.background_line()
        # self.touchscreen_right_panel.print("RIGHT")

        # self.touchscreen_select_panel.highligt_line()
        # self.touchscreen_select_panel.background_line()
        # self.touchscreen_select_panel.print("SELECT")

        # self.touchscreen_back_panel.highligt_line()
        # self.touchscreen_back_panel.background_line()
        # self.touchscreen_back_panel.print("BACK")
        

    def get_touchscreen_panel(self, x, y):
        result = None
        for button in self.buttons:
            if button.checkForInput(pygame.mouse.get_pos()):
                logging.debug(f'got button {button.text_input}')
                result = button.act()        
        
        if result:
            return result

        # if self.touchscreen_left_panel.is_point_inside_panel(x,y):
        #     return "LEFT"

        # if self.touchscreen_right_panel.is_point_inside_panel(x,y):
        #     return "RIGHT"

        # if self.touchscreen_select_panel.is_point_inside_panel(x,y):
        #     return "SELECT"

        # if self.touchscreen_back_panel.is_point_inside_panel(x,y):
        #     return "BACK"

        return "NONE"        