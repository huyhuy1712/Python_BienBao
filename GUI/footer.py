from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle

class Footer(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(size_hint=(1, 0.1), padding=[10, 10], **kwargs)
        with self.canvas.before:
            Color(0, 0.5, 1, 1)  # Màu xanh dương
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[0, 0, 10, 10])
        self.bind(size=self.update_rect, pos=self.update_rect)

        self.add_widget(Label(text="FOOTER", bold=True, color=(1, 1, 1, 1), font_size=20))

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos
