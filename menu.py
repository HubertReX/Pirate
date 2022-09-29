import pygame, sys
from button import Button, get_font

 

class Game():
    def __init__(self):
        pygame.init()

        self.SCREEN = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Menu")

        self.BG = pygame.image.load("graphics/ui/menu_bg.png")
        self.BG = pygame.transform.scale(self.BG, (1280, 720))


    def play(self):
        while True:
            PLAY_MOUSE_POS = pygame.mouse.get_pos()

            self.SCREEN.fill("black")

            PLAY_TEXT = get_font(45).render("This is the PLAY screen.", True, "White")
            PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
            self.SCREEN.blit(PLAY_TEXT, PLAY_RECT)

            PLAY_BACK = Button(self.SCREEN, image=None, pos=(640, 460), 
                                text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

            PLAY_BACK.changeColor(PLAY_MOUSE_POS)
            PLAY_BACK.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                        main_menu()

            pygame.display.update()

    def quit(self):
        pygame.quit()
        sys.exit()

    def options(self):
        while True:
            OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

            self.SCREEN.fill("white")

            OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
            OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
            self.SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

            OPTIONS_BACK = Button(self.SCREEN, image=None, pos=(640, 460), 
                                text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

            OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
            OPTIONS_BACK.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                        main_menu()

            pygame.display.update()

def main_menu():
    game = Game()

    while True:
        game.SCREEN.blit(game.BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
        
        buttons = []
        LEFT_BUTTON = Button(game.SCREEN, image=pygame.image.load("graphics/touchscreen/left.png"), pos=(50, 210), size=(64,64),
                            text_input="", font=get_font(70), base_color="#d7fcd4", hovering_color="White", action=game.play)
        buttons.append(LEFT_BUTTON)    
        PLAY_BUTTON = Button(game.SCREEN, image=pygame.image.load("graphics/ui/menu_button.png"), pos=(640, 210), size=(500,150),
                            text_input=" PLAY", font=get_font(70), base_color="#d7fcd4", hovering_color="White", action=game.play)
        buttons.append(PLAY_BUTTON)     
        OPTIONS_BUTTON = Button(game.SCREEN, image=pygame.image.load("graphics/ui/menu_button.png"), pos=(640, 380), size=(600,150),
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White", action=game.options)
        buttons.append(OPTIONS_BUTTON)                                 
        QUIT_BUTTON = Button(game.SCREEN, image=pygame.image.load("graphics/ui/menu_button.png"), pos=(640, 550), size=(420,150),
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White", action=game.quit)
        buttons.append(QUIT_BUTTON)     

        game.SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in buttons:
            button.changeColor(MENU_MOUSE_POS)
            button.update()
        
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_q] or keys[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.checkForInput(MENU_MOUSE_POS):
                        button.act()
                # if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                #     game.play()
                # if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                #     game.options()
                # if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):


        pygame.display.update()

if __name__ == '__main__':
    main_menu()