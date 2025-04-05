from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.button import ButtonBehavior
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.graphics import Color, RoundedRectangle, Ellipse, StencilPush, StencilPop, StencilUse, StencilUnUse, Line
from kivymd.app import MDApp
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model.user_crud import *




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
        # print("Avatar được nhấn, chuyển sang màn hình user")
        if self.screen_manager:
            self.screen_manager.current = 'user'

    def update_graphics(self, *args):
        self.mask.pos = self.pos
        self.mask.size = self.size
        self.img.pos = self.pos
        self.img.size = self.size
        self.border.ellipse = (self.x, self.y, self.width, self.height)


# Lớp Header hiển thị thanh tiêu đề
class Header(BoxLayout):
    def __init__(self, screen_manager,user_id, title, **kwargs):
        super().__init__(size_hint_y=None, height="80dp", padding=[10, 10], spacing=10, **kwargs)

        self.screen_manager = screen_manager  # Nhận ScreenManager để điều hướng
        self.curr_user = get_user_by_id(str(user_id))
        with self.canvas.before:
            Color(0, 0.5, 1, 1)  # Màu nền xanh dương
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[10, 10, 0, 0])
        self.bind(size=self.update_rect, pos=self.update_rect)

        # Ảnh đại diện hình tròn
        if is_avatar_exist(str(self.curr_user["avatar"])):
            avatar_user = "image/" + str(self.curr_user["avatar"])
        else:
            avatar_user = "image/default.jpg"

        self.avatar = CircularImage(source=avatar_user, screen_manager=self.screen_manager, size=(60, 60))

        # Thông tin người dùng
        username = "Username: " + str(self.curr_user["username"])
        self.user_info = BoxLayout(orientation='vertical', size_hint=(None, None), size=("220dp", "60dp"))
        self.username_label = Label(text=username, color=(1, 1, 1, 1), font_size=18, bold=True)
        self.scan_count_label = Label(text="Số lần Scan: 10", color=(1, 1, 1, 1), font_size=16)
        self.upload_count_label = Label(text="Số lần Upload: 5", color=(1, 1, 1, 1), font_size=16)
        self.user_info.add_widget(self.username_label)
        self.user_info.add_widget(self.scan_count_label)
        self.user_info.add_widget(self.upload_count_label)

        # Tiêu đề trang
        self.title_label = Label(text=title, bold=True, color=(1, 1, 1, 1), font_size=40)

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
        self.header = Header(screen_manager=screen_manager, title="Trang Chủ")
        layout.add_widget(self.header)

        self.add_widget(layout)

    def go_back(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.screen_manager.current = "main"




