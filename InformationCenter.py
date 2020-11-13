from pynput import mouse, keyboard

from MultiLineTextScrollers import MultiLineTextScroller, Notepad

class InformationCenter:
    def __init__(self, size, position, font, screen):
        half_size = (size[0], size[1] // 2)
        self.message_queue = MultiLineTextScroller(half_size, position, font, "Messages", screen)
        notepad_pos = (position[0], position[1] + half_size[1])
        self.notepad = Notepad(half_size, notepad_pos, font, screen)

        self.screen = screen

        self.mouse_listener = mouse.Listener(on_move=self.on_move, on_click=self.on_click, on_scroll=self.on_scroll)
        self.mouse_listener.start()
        self.key_listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.key_listener.start()

    def postMessage(self, text, color):
        self.message_queue.addLine(text, color)

    # Mouse listener methods
    def on_move(self, x, y):
        pass

    def on_click(self, x, y, button, pressed):
        if pressed and button == mouse.Button.left:
            if self.notepad.active and not self.notepad.rect.collidepoint((x, y)):
                self.notepad.deactivate()
            elif not self.notepad.active and self.notepad.rect.collidepoint((x, y)):
                self.notepad.activate()

    def on_scroll(self, x, y, dx, dy):
        if self.message_queue.rect.collidepoint((x, y)):
            self.message_queue.scroll(dy)
        elif self.notepad.rect.collidepoint((x, y)):
            self.notepad.scroll(dy)

    # Key listener methods
    def on_press(self, key):
        if self.notepad.active:
            try:
                self.notepad.addChar(key.char)
            except:
                if key == keyboard.Key.space:
                    self.notepad.addChar(" ")
                elif key == keyboard.Key.backspace:
                    self.notepad.deleteChar()
                elif key == keyboard.Key.enter:
                    self.notepad.addChar("\n")

    def on_release(self, key):
        pass

    # Method to safely end key/mouse listener threads
    def quit(self):
        self.mouse_listener.stop()
        self.key_listener.stop()