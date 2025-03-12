from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle

class Header(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(size_hint=(1, 0.1), padding=[10, 10], **kwargs)
        with self.canvas.before:
            Color(1, 0.8, 0, 1)  # Màu vàng
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[10, 10, 0, 0])
        self.bind(size=self.update_rect, pos=self.update_rect)

        self.add_widget(Label(text="HEADER", bold=True, color=(0, 0, 0, 1), font_size=20))

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos
