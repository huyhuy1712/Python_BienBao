import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from footer import Footer
from header import Header

from model.sign_crud import *
from model.sign import *

class ImageButton(RelativeLayout):
    def __init__(self, text, image_source, **kwargs):
        super().__init__(**kwargs)
        
        img = Image(
            source=image_source,
            size_hint=(1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        
        btn = Button(
            text=text,
            background_normal='',
            background_color=(0, 0, 0, 0.1),
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
        search_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=50, spacing=10) 
        
        category_spinner = Spinner(
            text="Chọn phân loại",
            values=["Cấm", "Nguy hiểm", "Chỉ dẫn", "Hiệu lệnh", "Biển phụ"],
            size_hint=(0.3, None),
            height=40
        )

        search_bar = TextInput(
            hint_text="Tìm kiếm biển báo...",
            size_hint=(1, None),
            height=40
        )
        search_layout.add_widget(category_spinner)
        search_layout.add_widget(search_bar)
        main_layout.add_widget(search_layout)

        # **ScrollView để chứa GridLayout**
        scroll_view = ScrollView(size_hint=(1, 1), bar_width=10, scroll_wheel_distance=50)

        # Grid chứa các ảnh
        button_grid = GridLayout(
            cols=2,
            spacing=20,
            padding=[0, 20, 0, 20],
            size_hint_y=None  # Quan trọng để ScrollView hoạt động
        )

        signs = get_all_signs()
        # Danh sách ảnh mẫu
        #images = ["image/bienbaocam/bien-bao-cam-109-1590225560-width224height224.jpg"] * 20  # 20 ảnh để test cuộn

        # **Tính chiều cao động dựa trên số ảnh**
        row_count = (len(signs) + 1) // 2  # Chia 2 cột
        button_grid.height = row_count * 150  # 150 là chiều cao mỗi hàng (có thể chỉnh)

        #for i, img in enumerate(images):
        #    img_button = ImageButton(text=f"", image_source=img)
         #   button_grid.add_widget(img_button)
        
        for sign in signs:
            image_path = f"image/bienbaocam/{sign.image}"
            # Kiểm tra xem file có tồn tại không
            if not os.path.exists(image_path):
                print(sign.id_sign)
            img_button = ImageButton(text="", image_source=image_path)
            button_grid.add_widget(img_button)


        # **Thêm Grid vào ScrollView**
        scroll_view.add_widget(button_grid)

        # Thêm ScrollView vào Main Layout
        main_layout.add_widget(scroll_view)

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
