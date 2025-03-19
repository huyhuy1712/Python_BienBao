from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle, RoundedRectangle
from header import Header
from footer import Footer

class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        
        with self.canvas.before:
            Color(1, 1, 1, 1)  # Màu trắng cho Main
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[20])
        self.bind(size=self.update_rect, pos=self.update_rect)
        
        # Header (Màu xanh, bo góc)
        header = Header()
        header.padding = [10, 10]  # Tăng khoảng cách bên trong
        header.spacing = 10  # Khoảng cách giữa các phần tử
        self.add_widget(header)
        
        # Main (Có nội dung "HOME", căn giữa)
        self.main = BoxLayout(size_hint=(1, 0.8), padding=20, spacing=10)
        with self.main.canvas.before:
            Color(1, 1, 1, 1)  # Nền trắng
            self.main_rect = RoundedRectangle(size=self.main.size, pos=self.main.pos, radius=[10])
        self.main.bind(size=self.update_main_rect, pos=self.update_main_rect)
        
        home_label = Label(text="HOME", font_size=30, bold=True, color=(0, 0, 0, 1))
        self.main.add_widget(home_label)
        
        self.add_widget(self.main)
        
        # Footer (Màu xanh, bo góc)
        footer = Footer()
        footer.padding = [10, 10]
        footer.spacing = 10
        self.add_widget(footer)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def update_main_rect(self, *args):
        self.main_rect.size = self.main.size
        self.main_rect.pos = self.main.pos

class MyApp(App):
    def build(self):
        return MainScreen()

if __name__ == '__main__':
    MyApp().run()