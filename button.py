import pygame

def get_font(size, is_web=False): # Returns Press-Start-2P in the desired size
    if not is_web:
        f = pygame.font.Font("graphics/ui/ARCADEPI.ttf", size)
    else:
        f = pygame.font.Font(None, int(size*1.5))
    return f

class Button():
    def __init__(self, screen, image, pos, text_input, font, base_color, hovering_color, size=(0,0), action=None):
        self.screen = screen
        self.enabled = True
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        else:
            if size != (0,0):
                self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.action = action

    def act(self):
        if self.enabled:
            if self.action:
                return self.action()
        return None
    
    def toggle(self):
        self.enabled = 1 - self.enabled

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def set_text(self, text):
        self.text_input = text
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
            self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        if self.enabled:
            if self.image is not None:
                self.screen.blit(self.image, self.rect)
            self.screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if self.enabled:
            if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
                return True
        return False

    def changeColor(self, position):
        if self.enabled:
            if self.checkForInput(position):
                self.text = self.font.render(self.text_input, True, self.hovering_color)
            else:
                self.text = self.font.render(self.text_input, True, self.base_color)