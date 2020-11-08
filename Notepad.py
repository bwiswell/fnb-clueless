from pynput import mouse, keyboard

import pygame

import GUIConstants

# Class to implement a notepad area with key/mouse detection in a separate thread
class Notepad(pygame.Surface):
    def __init__(self, size, position, screen, font):
        pygame.Surface.__init__(self, size)
        self.fill(GUIConstants.WHITE)
        self.position = position
        self.screen = screen
        self.rect = pygame.Rect(self.position, size)
        self.font = font

        # Label above notepad that says "Notepad"
        label = self.font.render("Notepad", True, GUIConstants.BLACK)
        label_box = pygame.Rect(0, 0, size[0], label.get_height() + GUIConstants.BORDER_RADIUS * 2)
        label_pos = (label_box.centerx - label.get_width() // 2, label_box.centery - label.get_height() // 2)
        pygame.draw.rect(self, GUIConstants.BLACK, label_box, GUIConstants.BORDER_RADIUS)
        self.blit(label, label_pos)

        # Editable area positions and sizes, as well as the current scroll position
        self.text = ""
        self.text_surface_size = (size[0] - GUIConstants.BORDER_RADIUS * 2, size[1] * 10)
        self.text_border = pygame.Rect(0, label_box.height, size[0], size[1] - label_box.height)
        self.text_box = pygame.Rect(GUIConstants.BORDER_RADIUS, label_box.height + GUIConstants.BORDER_RADIUS, self.text_surface_size[0], self.text_border.height - GUIConstants.BORDER_RADIUS * 2)
        self.text_y = 0
        self.text_max_y = 0
        self.text_absolute_max_y = self.text_surface_size[1] - self.text_box.height

        # Flags to check if the notepad should continue to update itself
        self.active = False
        self.blocked = False

        self.draw()

        # Initialize key and mouse listeners
        self.mouse_listener = mouse.Listener(on_move=self.on_move, on_click=self.on_click, on_scroll=self.on_scroll)
        self.mouse_listener.start()
        self.key_listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.key_listener.start()

    # Mouse listener methods
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
            self.draw(False)

    # Key listener methods
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

    # Methods to lock the notepad while dialogues are displayed
    def block(self):
        self.blocked = True

    def unblock(self):
        self.blocked = False

    # Method to safely end key/mouse listener threads
    def quit(self):
        self.mouse_listener.stop()
        self.key_listener.stop()

    # Method to render the stored text, bumping words to the next line when
    # they run off the side of the screen. Also draws a cursor at the end
    # of the text when the notepad is active and determines the maximum
    # (and possibly current if a character was added or removed) scroll
    # position.
    def renderText(self, jump_to_end):
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
                if x + word_object.get_width() > self.text_surface_size[0]:
                    x = 0
                    y += line_size
                text_surface.blit(word_object, (x, y))
                x += word_object.get_width()
        if self.active:
            cursor = self.font.render("|", True, GUIConstants.RED)
            text_surface.blit(cursor, (x - cursor.get_width(), y))
        self.text_max_y = min(max(0, y + line_size - self.text_box.height), self.text_absolute_max_y)
        if jump_to_end:
            self.text_y = self.text_max_y
        return text_surface

    # Renders the current text and a colored border to visually indicate if
    # the notepad is active
    def draw(self, jump_to_end=True):
        self.fill(GUIConstants.WHITE, self.text_border)
        text_object = self.renderText(jump_to_end)
        text_rect = pygame.Rect((0, self.text_y), self.text_box.size)
        self.blit(text_object, self.text_box.topleft, text_rect)
        if self.active:
            pygame.draw.rect(self, GUIConstants.BLUE, self.text_border, GUIConstants.BORDER_RADIUS)
        self.screen.draw(self)