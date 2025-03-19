from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.button import ButtonBehavior
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.graphics import Color, RoundedRectangle, Ellipse, StencilPush, StencilPop, StencilUse, StencilUnUse, Line
from kivymd.app import MDApp


# Lớp CircularImage để hiển thị avatar hình tròn và bắt sự kiện nhấn
class CircularImage(ButtonBehavior, Widget):
    def __init__(self, source, screen_manager, size, **kwargs):
        super().__init__(size_hint=(None, None), size=size, **kwargs)
        self.source = source
        self.screen_manager = screen_manager  # Lưu ScreenManager để điều hướng
        with self.canvas:
            StencilPush()
            self.mask = Ellipse(pos=self.pos, size=self.size)
            StencilUse()
            self.img = Image(source=self.source, pos=self.pos, size=self.size)
            StencilUnUse()
            StencilPop()
            # Viền trắng quanh avatar
            Color(1, 1, 1, 1)
            self.border = Line(ellipse=(self.x, self.y, self.width, self.height), width=2)

        self.bind(pos=self.update_graphics, size=self.update_graphics)

    def on_press(self):
        print("Avatar được nhấn, chuyển sang màn hình user")
        if self.screen_manager:
            self.screen_manager.current = 'user'

    def update_graphics(self, *args):
        self.canvas.clear()
        with self.canvas:
            StencilPush()
            self.mask = Ellipse(pos=self.pos, size=self.size)
            StencilUse()
            self.img = Image(source=self.source, pos=self.pos, size=self.size)
            StencilUnUse()
            StencilPop()
            # Viền trắng quanh avatar
            Color(1, 1, 1, 1)
            self.border = Line(ellipse=(self.x, self.y, self.width, self.height), width=2)


# Lớp Header hiển thị thanh tiêu đề
class Header(BoxLayout):
    def __init__(self, screen_manager, **kwargs):
        super().__init__(size_hint_y=None, height="80dp", padding=[10, 10], spacing=10, **kwargs)

        self.screen_manager = screen_manager  # Nhận ScreenManager để điều hướng
        
        with self.canvas.before:
            Color(0, 0.5, 1, 1)  # Màu nền xanh dương
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[10, 10, 0, 0])
        self.bind(size=self.update_rect, pos=self.update_rect)

        # Ảnh đại diện hình tròn (truyền screen_manager vào)
        self.avatar = CircularImage(source="image/uta.jpg", screen_manager=self.screen_manager, size=(60, 60))

        # Thông tin người dùng
        self.user_info = BoxLayout(orientation='vertical', size_hint=(None, None), size=("220dp", "60dp"))
        self.username_label = Label(text="Username: Lê Ngọc Anh Huy", color=(1, 1, 1, 1), font_size=18, bold=True)
        self.scan_count_label = Label(text="Số lần Scan: 10", color=(1, 1, 1, 1), font_size=16)
        self.upload_count_label = Label(text="Số lần Upload: 5", color=(1, 1, 1, 1), font_size=16)
        self.user_info.add_widget(self.username_label)
        self.user_info.add_widget(self.scan_count_label)
        self.user_info.add_widget(self.upload_count_label)

        # Tiêu đề trang
        self.title_label = Label(text="Trang Chủ", bold=True, color=(1, 1, 1, 1), font_size=40)

        # Bố cục
        self.add_widget(self.avatar)
        self.add_widget(self.user_info)
        self.add_widget(Widget())  # Khoảng cách căn giữa tiêu đề
        self.add_widget(self.title_label)
        self.add_widget(Widget())  # Khoảng cách bên phải

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos


# Màn hình chính chứa Header
class MainScreen(Screen):
    def __init__(self, screen_manager, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical")

        # Thêm Header vào màn hình chính
        self.header = Header(screen_manager=screen_manager)
        layout.add_widget(self.header)

        self.add_widget(layout)


# Màn hình User khi nhấn vào Avatar
class UserScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", padding=20, spacing=15)

        title = Label(text="Màn hình User", font_size=24, color=(1, 1, 1, 1))
        layout.add_widget(title)

        # Nút quay lại
        back_button = Label(text="Quay lại", size_hint_y=None, height=50, color=(1, 0, 0, 1))
        back_button.bind(on_touch_down=self.go_back)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def go_back(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.manager.current = "main"


# Chạy ứng dụng
class MyApp(MDApp):
    def build(self):
        sm = ScreenManager()

        # Thêm màn hình chính và màn hình user vào ScreenManager
        sm.add_widget(MainScreen(sm, name='main'))  # Màn hình chính
        sm.add_widget(UserScreen(name='user'))  # Màn hình user

        return sm  # Trả về ScreenManager làm root


if __name__ == "__main__":
    MyApp().run()
