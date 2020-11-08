from pynput import mouse, keyboard

import pygame

import GUIConstants

class Notepad(pygame.Surface):
    def __init__(self, size, position, screen, font):
        pygame.Surface.__init__(self, size)
        self.size = size
        self.position = position
        self.screen = screen
        self.rect = pygame.Rect(self.position, self.size)
        self.font = font
        self.text = ""
        self.text_surface_size = (self.size[0] - GUIConstants.BORDER_RADIUS * 2, self.size[1] * 10)
        self.text_size = (self.text_surface_size[0], self.size[1] - GUIConstants.BORDER_RADIUS * 2)
        self.text_y = 0
        self.text_max_y = 0
        self.text_absolute_max_y = self.text_surface_size[1] - self.text_size[1]
        self.cursor_pos = 0
        self.active = False
        self.active_rect = pygame.Rect((0, 0), self.size)
        self.blocked = False
        self.draw()
        self.mouse_listener = mouse.Listener(on_move=self.on_move, on_click=self.on_click, on_scroll=self.on_scroll)
        self.mouse_listener.start()
        self.key_listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.key_listener.start()

    def on_move(self, x, y):
        pass

    def on_click(self, x, y, button, pressed):
        if not self.blocked and pressed and button == mouse.Button.left and self.rect.collidepoint((x, y)):
            self.active = not self.active
            self.draw()

    def on_scroll(self, x, y, dx, dy):
        if not self.blocked and self.active and self.rect.collidepoint((x, y)):
            self.text_y -= dy * 10
            self.text_y = min(max(self.text_y, 0), self.text_max_y)
            self.draw()

    def on_press(self, key):
        if not self.blocked and self.active:
            try:
                self.text += key.char
            except:
                if key == keyboard.Key.space:
                    self.text += " "
                elif key == keyboard.Key.backspace:
                    self.text = self.text[:-1]
                elif key == keyboard.Key.enter:
                    self.text += "\n"
        self.draw()

    def on_release(self, key):
        pass

    def block(self):
        self.blocked = True

    def unblock(self):
        self.blocked = False

    def renderText(self):
        text_surface = pygame.Surface(self.text_surface_size)
        text_surface.fill(GUIConstants.WHITE)
        x = 0
        y = 0
        line_size = self.font.get_height()
        lines = self.text.split("\n")
        for i in range(len(lines)):
            if i != 0:
                x = 0
                y += line_size
            words = lines[i].split(" ")
            for word in words:
                word += " "
                word_object = self.font.render(word, True, GUIConstants.BLACK)
                if x + word_object.get_size()[0] > self.text_surface_size[0]:
                    x = 0
                    y += line_size
                text_surface.blit(word_object, (x, y))
                x += word_object.get_size()[0]
        self.text_max_y = min(max(0, y + line_size - self.text_size[1]), self.text_absolute_max_y)
        self.text_y = min(self.text_y, self.text_max_y)
        return text_surface

    def draw(self):
        self.fill(GUIConstants.WHITE)
        text_object = self.renderText()
        text_rect = pygame.Rect((0, self.text_y), self.text_size)
        self.blit(text_object, (GUIConstants.BORDER_RADIUS, GUIConstants.BORDER_RADIUS), text_rect)
        if self.active:
            pygame.draw.rect(self, GUIConstants.BLUE, self.active_rect, GUIConstants.BORDER_RADIUS)
        self.screen.draw(self)