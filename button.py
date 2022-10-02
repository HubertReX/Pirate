import pygame, os

def get_font(size, is_web=False) -> pygame.font: # Returns Press-Start-2P in the desired size
    if not is_web:
        f = pygame.font.Font(os.path.join("graphics", "ui", "ARCADEPI.ttf"), size)
    else:
        f = pygame.font.Font(None, int(size*1.5))
    return f


class Label():
    def __init__(self, screen: pygame.surface, text: str, color: str, font_size: int, antialias: bool, allign: str, postion: tuple[int, int]) -> None:
        self.screen = screen
        self.text = get_font(font_size).render(text, antialias, color)
        aligned_rect = {allign: postion}
        self.rect = self.text.get_rect(**aligned_rect)

    def render(self, display) -> None:
        display.blit(self.text, self.rect)
        #elf.screen.blit(VER_TEXT, VER_RECT)

class Button():
    def __init__(self, screen, image, pos, text_input, font, base_color, hovering_color, size=(0, 0), inflate=(10, 10), action=None, checked_img=None, unchecked_img=None):
        self.screen = screen
        self.enabled = True
        self.selected = False
        self.checked = False
        self.image = image
        self.checked_img = checked_img
        self.unchecked_img = unchecked_img
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.inflate = inflate
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        else:
            if size != (0,0):
                self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        if checked_img:
            self.checked_img_rect = self.checked_img.get_rect(
                center=(self.x_pos, self.y_pos))
        if unchecked_img:
            self.unchecked_img_rect = self.unchecked_img.get_rect(
                center=(self.x_pos, self.y_pos))
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

    def select(self, selected):
        self.selected = selected

    def check(self, chekced):
        self.checked = chekced

    def toggle_check(self):
        self.checked = not self.checked

    def set_text(self, text):
        self.text_input = text
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
            self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def render(self, display):
        if self.enabled:
            if self.image is not None:
                display.blit(self.image, self.rect)
            if self.checked:
                if self.checked_img:
                    display.blit(self.checked_img, self.checked_img_rect)
            else:
                if self.unchecked_img:
                    display.blit(self.unchecked_img, self.unchecked_img_rect)
            if self.selected:
                pygame.draw.rect(display, self.base_color,
                                 self.text_rect.inflate(self.inflate), 3)
            display.blit(self.text, self.text_rect)


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