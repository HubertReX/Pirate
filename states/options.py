import pygame, os
from states.state import State
from states.party import PartyMenu
from button import Button, get_font, Label
import logging

class OptionsMenu(State):
    def __init__(self, game):
        #State.__init__(self, game)
        super().__init__(game)
        # Set the menu
        self.menu_img = pygame.image.load(os.path.join(
            self.game.assets_dir, "menu", "settings_menu.png"))
        self.menu_rect = self.menu_img.get_rect()
        #self.menu_rect.center = (self.game.GAME_W*.85, self.game.GAME_H*.4)
        
        # Set the cursor and menu states
        self.menu_options = {0 : "Music", 1 : "Effects", 2 : "Full screen"}
        self.index = 0
        self.cursor_img = pygame.image.load(os.path.join(self.game.assets_dir, "coins", "gold", "0.png"))
        self.cursor_rect = self.cursor_img.get_rect()
        self.cursor_pos_x = 200
        self.cursor_pos_y = 125
        self.cursor_rect.x, self.cursor_rect.y = self.cursor_pos_x, self.cursor_pos_y

        self.labels = []
        self.labels.append(Label(game.screen, "Settings", "Black",
                                 11, False, "midtop", (305, 75)))
        self.labels.append(Label(game.screen, "Music", "Black",
                                 11, False, "topleft", (240, 140)))
        self.labels.append(Label(game.screen, "SFX", "Black",
                                 11, False, "topleft", (240, 172)))
        self.labels.append(Label(game.screen, "Full screen", "Black",
                                 11, False, "topleft", (240, 267)))

        self.buttons = []
        # pygame.image.load("graphics/touchscreen/left.png")
        self.buttons.append(Button(game.screen, image=None, pos=(335, 144), size=(32, 32),
                                   text_input="", font=get_font(1), base_color="#d7fcd4", 
                                   hovering_color="White", action=self.toggle_music, inflate=(0,0),
                                   checked_img=pygame.image.load("graphics/Small Icons/sound.png"), 
                                   unchecked_img=pygame.image.load("graphics/Small Icons/nosound.png")))
        self.buttons.append(Button(game.screen, image=None, pos=(335, 176), size=(32, 32),
                                   text_input="", font=get_font(1), base_color="#d7fcd4", 
                                   hovering_color="White", action=self.toggle_sfx, inflate=(0, 0),
                                   checked_img=pygame.image.load("graphics/Small Icons/sound.png"), 
                                   unchecked_img=pygame.image.load("graphics/Small Icons/nosound.png")))
        self.buttons.append(Button(game.screen, image=None, pos=(335, 272), size=(32, 32),
                                   text_input="", font=get_font(1), base_color="#d7fcd4",  inflate=(0, 0),
                                   hovering_color="White", action=self.toggle_full_screen,
                                   checked_img=pygame.image.load("graphics/Small Icons/checked.png"), 
                                   unchecked_img=pygame.image.load("graphics/Small Icons/unchecked.png")))
        self.index = 0

    def toggle_music(self):
        self.buttons[0].toggle_check()

    def toggle_sfx(self):
        self.buttons[1].toggle_check()

    def toggle_full_screen(self):
        self.buttons[2].toggle_check()

    def update(self, delta_time, actions):  
        self.update_cursor(actions)      
        if actions["action"]:
            btn = self.buttons[self.index]
            btn.act()
        if actions["back"]:
            self.game.reset_keys()
            self.exit_state()

        self.game.reset_keys()

    def render(self, display):
        # render the gameworld behind the menu, which is right before the pause menu on the stack
        #self.game.state_stack[-2].render(display)
        if self.prev_state:
            self.prev_state.render(display)
        #display.fill("black")
        display.blit(self.menu_img, self.menu_rect)
        display.blit(self.cursor_img, self.cursor_rect)
        for label in self.labels:
            label.render(display)
        for button in self.buttons:
            button.render(display)

    def update_cursor(self, actions):
        if actions['down']:
            # self.index = (self.index + 1) % len(self.menu_options)

            self.buttons[self.index].select(False)
            self.index = (self.index + 1) % len(self.buttons)
            self.buttons[self.index].select(True)
        elif actions['up']:
            # self.index = (self.index - 1) % len(self.menu_options)

            self.buttons[self.index].select(False)
            self.index = (self.index - 1) % len(self.buttons)
            self.buttons[self.index].select(True)
        self.cursor_rect.y = self.buttons[self.index].y_pos - 16  # self.cursor_pos_y + (self.index * 32)


    

    