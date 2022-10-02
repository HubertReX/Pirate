import pygame, os
from button import Button, get_font, Label
from states.state import State
from states.game_world import Game_World
from states.options import OptionsMenu



class Title(State):
    def __init__(self, game):
        super().__init__(game)
        # State.__init__(self, game)
        #self.game = game
        self.bg = pygame.image.load(os.path.join("graphics", "menu", "main_menu.png")).convert_alpha()
        # self.bg = pygame.transform.scale(self.bg, (game.SCREEN_WIDTH, game.SCREEN_HEIGHT))
        
        self.labels = []
        self.labels.append(Label(game.screen, "Pirate!", "#c90000",
                                 25, False, "center", (304, 48)))
        self.labels.append(Label(game.screen, "v 0.3",   "#c90000",
                                 10, False, "center", (465, 50)))

        self.labels.append(Label(game.screen, "HIGHSCORE", "#c90000",
                                 9, False, "midtop", (130, 45)))
        self.labels.append(Label(game.screen, "0032", "#ffffff",
                                 11, False, "midtop", (130, 65)))

        self.labels.append(Label(game.screen, "Made by:", "#c90000",
                                 10, False, "topleft", (470, 315)))
        self.labels.append(Label(game.screen, "Hubert,", "#c90000",
                                 10, False, "topleft", (470, 330)))
        self.labels.append(Label(game.screen, "Tymon & Mati", "#c90000",
                                 10, False, "topleft", (470, 345)))

        self.buttons = []
        self.buttons.append(Button(game.screen, image=None, pos=(305, 125), size=(600, 150),
                                text_input="PLAY", font=get_font(38), base_color="#d7fcd4", hovering_color="White", action=self.play))    
        self.buttons.append(Button(game.screen, image=None, pos=(305, 220), size=(600, 150),
                                text_input="OPTIONS", font=get_font(38), base_color="#d7fcd4", hovering_color="White", action=self.options))
        self.buttons.append(Button(game.screen, image=None, pos=(305, 320), size=(420, 150),
                                text_input="QUIT", font=get_font(38), base_color="#d7fcd4", hovering_color="White", action=self.quit))

        self.index = 0
        self.buttons[self.index].select(True)

        
    def play(self):
        new_state = Game_World(self.game)
        new_state.enter_state()

    def options(self):
        new_state = OptionsMenu(self.game)
        new_state.enter_state()

    def quit(self):
        # self.exit_state()        
        self.game.quit()

    def update_cursor(self, actions):        
        if actions['down']:
            self.buttons[self.index].select(False)
            self.index = (self.index + 1) % len(self.buttons)
            self.buttons[self.index].select(True)
        elif actions['up']:
            self.buttons[self.index].select(False)
            self.index = (self.index - 1) % len(self.buttons)
            self.buttons[self.index].select(True)

    def update(self, delta_time, actions):
        self.update_cursor(actions)

        for button in self.buttons:
            button.changeColor(self.game.mouse_pos)
            
        if actions["start"]:
            btn = self.buttons[self.index]
            btn.act()
        elif actions["mouse_button"]:
            for button in self.buttons:
                if button.checkForInput(self.game.mouse_pos):
                    button.act()
        elif actions["back"]:
            self.quit()

        self.game.reset_keys()

    def render(self, display):
        display.fill("black")
        display.blit(self.bg, (0, 0))

        #self.game.draw_text(display, "Game States Demo", (0,0,0), self.game.GAME_W/2, self.game.GAME_H/2 )
        for label in self.labels:
            label.render(display)

        for button in self.buttons:
            button.render(display)

