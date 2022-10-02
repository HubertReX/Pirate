import pygame, sys
from button import Button, get_font

 
class Label():
    def __init__(self, screen: pygame.surface, text: str, color: str, font_size: int, antialias: bool, allign: str, postion: tuple[int, int]) -> None:
        self.screen = screen
        self.text = get_font(font_size).render(text, antialias, color)
        aligned_rect = {allign: postion}
        self.rect = self.text.get_rect(**aligned_rect)

    def render(self) -> None:
        self.screen.blit(self.text, self.rect)
        #elf.screen.blit(VER_TEXT, VER_RECT)

class Game():
    def __init__(self):
        pygame.init()

        self.SCREEN = pygame.display.set_mode((1280, 800)) # WXGA 40 x 25  (1,6 16:10)  
        pygame.display.set_caption("Menu")

        self.BG = pygame.image.load("graphics/menu/main_menu.png")
        self.BG = pygame.transform.scale(self.BG, (1280, 800))


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
            PLAY_BACK.render()

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
            OPTIONS_BACK.render()

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

    labels = []
    labels.append(Label(game.SCREEN, "Pirate!", "#c90000",
                  50, True, "center", (640, 100)))
    labels.append(Label(game.SCREEN, "v 0.3",   "#c90000",
                  20, True, "center", (975, 100)))

    labels.append(Label(game.SCREEN, "HIGHSCORE", "#c90000",
                  17, True, "midtop", (270, 100)))
    labels.append(Label(game.SCREEN, "0032", "#ffffff",
                  20, True, "midtop", (270, 140)))

    labels.append(Label(game.SCREEN, "Made by:", "#c90000",
                  20, True, "topleft", (1000, 660)))
    labels.append(Label(game.SCREEN, "Hubert,", "#c90000",
                  20, True, "topleft", (1000, 685)))
    labels.append(Label(game.SCREEN, "Tymon & Mati", "#c90000",
                  20, True, "topleft", (1000, 710)))

    buttons = []

    PLAY_BUTTON = Button(game.SCREEN, image=None, pos=(640, 265), size=(600, 150),
                         text_input="PLAY", font=get_font(50), base_color="#d7fcd4", hovering_color="White", action=game.play)
    buttons.append(PLAY_BUTTON)
    OPTIONS_BUTTON = Button(game.SCREEN, image=None, pos=(640, 400), size=(600, 150),
                            text_input="OPTIONS", font=get_font(50), base_color="#d7fcd4", hovering_color="White", action=game.options)
    buttons.append(OPTIONS_BUTTON)
    QUIT_BUTTON = Button(game.SCREEN, image=None, pos=(640, 665), size=(420, 150),
                         text_input="QUIT", font=get_font(50), base_color="#d7fcd4", hovering_color="White", action=game.quit)
    buttons.append(QUIT_BUTTON)

    while True:
        game.SCREEN.blit(game.BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        for label in labels:
            label.render()

        for button in buttons:
            button.changeColor(MENU_MOUSE_POS)
            button.render()
        
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_q] or keys[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.checkForInput(MENU_MOUSE_POS):
                        button.act()


        pygame.display.update()

if __name__ == '__main__':
    main_menu()