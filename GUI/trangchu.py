from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.label import Label
from kivy.uix.image import Image
from footer import Footer
from header import Header
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from model.user_crud import *


class MainScreen(Screen):
    def __init__(self, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = screen_manager  # Lưu ScreenManager để truyền vào Footer

        layout = BoxLayout(orientation='vertical')

        # Tạo Header có screen_manager để điều hướng
        self.user_id = load_user_id()
        self.header = Header(screen_manager=self.screen_manager,user_id=self.user_id,title="Trang chủ")
        layout.add_widget(self.header)
  
        
        # Layout chính (dạng lưới 2x2)
        self.main_layout = GridLayout(cols=2, rows=2, spacing=15, padding=[20, 15], size_hint=(1, 1))

        # Thêm các khu vực trong lưới
        self.add_section("Upload Hình Ảnh", "image/upload_icon.png", (1, 0.5, 0.5, 1), 'upload')
        self.add_section("Xem Thông Tin Biển Báo", "image/sign_icon.png", (0.5, 0.7, 1, 1), 'info')
        self.add_section("Xem Lịch Sử", "image/history_icon.png", (0.5, 1, 0.5, 1), 'history')
        self.add_section("Scan Ảnh", "image/scan_icon.png", (0.9, 0.9, 0.4, 1), 'scan')
     
        
        layout.add_widget(self.main_layout)

        # Footer: Truyền screen_manager vào Footer
        footer = Footer(screen_manager)
        layout.add_widget(footer)

        self.add_widget(layout)

    def add_section(self, text, image_path, bg_color, screen_name):
        section = AnchorLayout(size_hint=(1, 1))
        with section.canvas.before:
            Color(*bg_color)
            section.rect = RoundedRectangle(size=section.size, pos=section.pos, radius=[20])
        section.bind(size=self.update_rect_section, pos=self.update_rect_section)

        box = BoxLayout(orientation='vertical', padding=15, spacing=15)
        img = Image(source=image_path, size_hint=(1, 0.6))
        label = Label(text=text, font_size=40, bold=True, color=(1, 1, 1, 1), size_hint=(1, 0.4))
        box.add_widget(img)
        box.add_widget(label)

        section.add_widget(box)

        # Gán sự kiện khi nhấn vào section  
        section.bind(on_touch_down=lambda instance, touch: self.on_section_touch(instance, touch, screen_name))

        self.main_layout.add_widget(section)

    def on_section_touch(self, instance, touch, screen_name):
        if instance.collide_point(*touch.pos):
            if self.manager:

                print(f"Chuyen sang man hinh: {screen_name}")  
                self.manager.current = screen_name
            else:
                print("ScreenManager chưa được gán vào MainScreen!")

    def update_rect_section(self, instance, *args):
        instance.rect.size = instance.size
        instance.rect.pos = instance.pos

    