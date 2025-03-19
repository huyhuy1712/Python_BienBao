from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager


class Footer(BoxLayout):
    def __init__(self, screen_manager, **kwargs):
        super().__init__(size_hint=(1, 0.12), padding=[10, 10, 10, 5], spacing=10, **kwargs)  # Tăng padding bottom
        self.screen_manager = screen_manager

        with self.canvas.before:
            Color(1, 0.8, 0, 1)  # Màu vàng
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[0, 0, 10, 10])
        self.bind(size=self.update_rect, pos=self.update_rect)

        # Layout chứa nút Home
        home_layout = BoxLayout(size_hint=(None, 0.9), width=90)
        home_button = Button(size_hint=(None, None), size=(80, 80),
                             background_normal="image/home_icon.png",
                             background_down="image/home_icon.png",
                             pos_hint={"center_x": 0.5, "y": 0})
        home_button.bind(on_release=self.go_home)
        home_layout.add_widget(home_button)

        # Câu khẩu hiệu
        slogan_label = Label(text="Không uống rượu bia khi lái xe", bold=True,
                             color=(0.2, 0.2, 0.2, 1), font_size=22, valign='center')

        # Layout chứa nút Logout
        logout_layout = BoxLayout(size_hint=(None, 0.5), width=90)
        logout_button = Button(size_hint=(None, None), size=(80, 80),
                               background_normal="image/logout_icon.png",
                               background_down="image/logout_icon.png",
                               pos_hint={"center_x": 0.5, "y": 0})
        logout_button.bind(on_release=self.logout)
        logout_layout.add_widget(logout_button)

        # Thêm vào Footer
        self.add_widget(home_layout)
        self.add_widget(slogan_label)
        self.add_widget(logout_layout)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def go_home(self, instance):
        if self.screen_manager and 'main' in self.screen_manager.screen_names:
            print("Chuyển về màn hình main")
            self.screen_manager.current = 'main'
        else:
            print(" Lỗi: Không tìm thấy màn hình 'main'")

    def logout(self, instance):
        print("Đăng xuất khỏi ứng dụng")
      

# Chạy thử Footer bằng ứng dụng KivyMD
class MyApp(MDApp):
    def build(self):
        sm = ScreenManager()
        return Footer(sm)

if __name__ == "__main__":
    MyApp().run()
