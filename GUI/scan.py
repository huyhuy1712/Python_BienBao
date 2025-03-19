from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDRaisedButton
from kivy.uix.camera import Camera
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle, RoundedRectangle

# Import từ các file header.py và footer.py
from footer import Footer
from header import Header

class ScanScreen(Screen):
    def __init__(self, screen_manager, **kwargs):
        super().__init__(**kwargs)
        
        # Layout chính (dọc)
        self.main_layout = BoxLayout(orientation='vertical')
        
        # Thêm header từ file header.py
        self.main_layout.add_widget(Header(screen_manager))

        
        # Layout chính của nội dung giữa
        self.content_layout = BoxLayout(orientation='vertical', padding=[20, 20], spacing=20)
        
        # Nền xám nhạt
        with self.content_layout.canvas.before:
            Color(0.94, 0.94, 0.94, 1)
            self.bg_rect = Rectangle(size=self.content_layout.size, pos=self.content_layout.pos)
        self.content_layout.bind(size=self.update_bg, pos=self.update_bg)
        
        # Vùng hiển thị camera
        self.camera_area = AnchorLayout(size_hint=(1, 0.8))
        with self.camera_area.canvas.before:
            Color(1, 1, 1, 1)
            self.camera_bg = RoundedRectangle(size=self.camera_area.size, pos=self.camera_area.pos, radius=[20])
        self.camera_area.bind(size=self.update_camera_bg, pos=self.update_camera_bg)
        
        # Khởi tạo camera ngay từ đầu
        self.camera = Camera(play=True, resolution=(800, 600))
        self.camera_area.add_widget(self.camera)
        self.content_layout.add_widget(self.camera_area)
        
        # Layout chứa 3 nút với căn chỉnh đều
        button_layout = GridLayout(cols=3, spacing=20, size_hint_y=None, height=60, padding=[20, 0], size_hint_x=1)
        
        # Nút Scan
        self.scan_button = MDRaisedButton(
            text="Scan",
            md_bg_color=(0.13, 0.59, 0.95, 1),
            text_color=(1, 1, 1, 1),
            size_hint=(1, None),
            height=50,
        )
        self.scan_button.bind(on_press=self.restart_camera)
        
        # Nút Lịch Sử
        self.history_button = MDRaisedButton(
            text="Lịch Sử",
            md_bg_color=(0.46, 0.46, 0.46, 1),
            text_color=(1, 1, 1, 1),
            size_hint=(1, None),
            height=50,
        )
        self.history_button.bind(on_press=self.go_to_history)
        
        # Nút Xóa
        self.delete_button = MDRaisedButton(
            text="Xóa",
            md_bg_color=(0.96, 0.26, 0.21, 1),
            text_color=(1, 1, 1, 1),
            size_hint=(1, None),
            height=50,
        )
        self.delete_button.bind(on_press=self.clear_camera)
        
        button_layout.add_widget(self.scan_button)
        button_layout.add_widget(self.history_button)
        button_layout.add_widget(self.delete_button)
        
        # Thêm layout chứa nút vào content_layout
        self.content_layout.add_widget(button_layout)
        self.main_layout.add_widget(self.content_layout)
        
        # Thêm footer từ file footer.py
        self.main_layout.add_widget(Footer(screen_manager))
        self.add_widget(self.main_layout)

    def update_bg(self, *args):
        self.bg_rect.size = self.content_layout.size
        self.bg_rect.pos = self.content_layout.pos

    def update_camera_bg(self, *args):
        self.camera_bg.size = self.camera_area.size
        self.camera_bg.pos = self.camera_area.pos

    def restart_camera(self, instance=None):
        self.clear_camera()
        self.camera = Camera(play=True, resolution=(800, 600))
        self.camera_area.add_widget(self.camera)

    def clear_camera(self, instance=None):
        if self.camera:
            self.camera.play = False
            self.camera_area.remove_widget(self.camera)
            self.camera = None

    def go_to_history(self, instance):
        print("Chuyển đến màn hình lịch sử")
        
