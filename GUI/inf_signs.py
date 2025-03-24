from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from footer import Footer
from header import Header

class ImageButton(RelativeLayout):
    def __init__(self, text, image_source, **kwargs):
        super().__init__(**kwargs)
        
        # Hình ảnh
        img = Image(
            source=image_source,
            size_hint=(1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        
        # Nút bấm
        btn = Button(
            text=text,
            background_normal='',  # Loại bỏ màu nền mặc định
            background_color=(0, 0, 0, 0.5),  # Làm trong suốt 50%
            size_hint=(1, 1)
        )

        self.add_widget(img)
        self.add_widget(btn)

class PageScreen(Screen):
    def __init__(self, page_number, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.name = f"page{page_number}"

        main_layout = BoxLayout(orientation="vertical", spacing=10, padding=[20, 20, 20, 20])

        # Header
        main_layout.add_widget(Header(screen_manager, "Biển Báo"))

        # Thanh tìm kiếm
        search_layout = BoxLayout(size_hint_y=None, height=50)  # Đặt chiều cao cố định
        search_bar = TextInput(
            hint_text="Tìm kiếm biển báo...",
            size_hint=(1, None),
            height=50
        )
        search_layout.add_widget(search_bar)
        main_layout.add_widget(search_layout)

        # Lưới chứa các nút có hình ảnh
        button_grid = GridLayout(
            cols=2,
            spacing=20,
            padding=[0, 20, 0, 20],
            size_hint_y=None,
            height=460
        )

        # Danh sách ảnh mẫu (Bạn có thể thay bằng ảnh thực tế)
        images = ["image/bg.jpg"]*9

        for i in range(1, 9):
            img_button = ImageButton(text=f"", image_source=images[i - 1])
            button_grid.add_widget(img_button)

        # Thêm lưới nút vào layout chính
        main_layout.add_widget(button_grid)

        # Footer
        main_layout.add_widget(Footer(screen_manager))

        self.add_widget(main_layout)

class MyApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        sm = ScreenManager()
        sm.add_widget(PageScreen(1, sm))
        return sm

if __name__ == "__main__":
    MyApp().run()
