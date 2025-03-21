from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.core.window import Window

class RoundedTextInput(TextInput):
    """Tùy chỉnh TextInput để bo góc & đổi màu nền thành xám."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_active = ''
        self.background_color = (0.9, 0.9, 0.9, 1)  # Màu xám nhạt
        self.foreground_color = (0, 0, 0, 1)  # Màu chữ đen
        self.padding = [10, 10]
        self.size_hint = (0.8, None)  # Giảm kích thước chiều ngang
        self.height = 40  # Giảm chiều cao
        self.radius = [20, 20, 20, 20]  # Bo tròn góc 20px

class PageScreen(Screen):
    def __init__(self, page_number, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.name = f"page{page_number}"
        self.page_number = page_number
        self.screen_manager = screen_manager

        # Layout chính theo chiều dọc
        main_layout = BoxLayout(orientation="vertical", spacing=10, padding=10)

        # Thanh tìm kiếm ở trên cùng với bo tròn
        search_layout = BoxLayout(size_hint=(1, None), height=50, padding=[10, 0])
        self.search_bar = RoundedTextInput(hint_text="Tìm kiếm...")
        search_layout.add_widget(self.search_bar)
        main_layout.add_widget(search_layout)

        # Layout chứa 5 nút chính (dùng hình ảnh bên trái)
        button_layout = GridLayout(cols=1, spacing=10, size_hint=(None, None), size=(500, 600))
        button_layout.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        # Danh sách hình ảnh (thay bằng đường dẫn hình của bạn)
        image_paths = ["image\logo.png", "image\logo.png", "image\logo.png", "image\logo.png", "image\logo.png"]

        for i in range(5):
            # Layout ngang chứa ảnh + nút
            btn_layout = BoxLayout(orientation="horizontal", size_hint=(None, None), size=(500, 100))

            # Hình ảnh nhỏ
            img = Image(source=image_paths[i], size_hint=(None, None), size=(100, 100))

            # Nút (chỉ để hiển thị ảnh và text nếu cần)
            btn = Button(text=f"Nút {i+1}", size_hint=(None, None), size=(400, 100))
            btn.bind(on_press=lambda instance, num=i+1: self.open_text_page(num))

            btn_layout.add_widget(img)  # Ảnh bên trái
            btn_layout.add_widget(btn)  # Nút bên phải

            button_layout.add_widget(btn_layout)

        # Layout chứa nút chuyển trang
        nav_layout = BoxLayout(size_hint=(1, None), height=50, spacing=10)

        prev_btn = Button(text="Trang Trước", size_hint=(0.5, 1))
        prev_btn.bind(on_press=self.prev_page)

        next_btn = Button(text="Trang Sau", size_hint=(0.5, 1))
        next_btn.bind(on_press=self.next_page)

        nav_layout.add_widget(prev_btn)
        nav_layout.add_widget(next_btn)

        main_layout.add_widget(button_layout)
        main_layout.add_widget(nav_layout)

        self.add_widget(main_layout)

    def prev_page(self, instance):
        if self.page_number > 1:
            self.screen_manager.transition = SlideTransition(direction="right")
            self.screen_manager.current = f"page{self.page_number - 1}"

    def next_page(self, instance):
        if self.page_number < 5:
            self.screen_manager.transition = SlideTransition(direction="left")
            self.screen_manager.current = f"page{self.page_number + 1}"

    def open_text_page(self, button_number):
        """Chuyển sang trang hiển thị văn bản."""
        text_page = self.screen_manager.get_screen("text_screen")
        text_page.update_text(f"Nội dung của nút {button_number}")
        self.screen_manager.transition = SlideTransition(direction="left")
        self.screen_manager.current = "text_screen"

class TextScreen(Screen):
    """Màn hình hiển thị nội dung khi bấm vào nút."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "text_screen"

        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        # Nhãn hiển thị nội dung
        self.label = Label(text="Nội dung sẽ hiển thị ở đây", font_size=24, halign="center", valign="middle", color=(0,0,0,1))
        layout.add_widget(self.label)

        # Nút quay lại
        back_button = Button(text="⬅ Quay lại", size_hint=(None, None), size=(200, 50))
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def update_text(self, new_text):
        """Cập nhật nội dung văn bản."""
        self.label.text = new_text

    def go_back(self, instance):
        """Quay lại trang trước."""
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "page1"  # Quay lại trang 1 (hoặc có thể nhớ trang trước đó)

class MyApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)  # Đặt nền trắng
        
        sm = ScreenManager()

        # Tạo 5 trang và thêm vào ScreenManager
        for i in range(1, 6):
            sm.add_widget(PageScreen(i, sm))

        # Thêm trang hiển thị văn bản
        sm.add_widget(TextScreen())

        return sm

if __name__ == "__main__":
    MyApp().run()
