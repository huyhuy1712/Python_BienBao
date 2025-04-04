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
from kivy.uix.popup import Popup
from kivy.uix.label import Label

from model.sign_crud import *
from model.sign import *

class ImageButton(RelativeLayout):
    def __init__(self, id_sign, image_source, **kwargs):
        super().__init__(**kwargs)
        self.id_sign = id_sign
        self.image_source = image_source
        img = Image(
            source=image_source,
            size_hint=(1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        
        btn = Button(
            text="",
            background_normal='',
            background_color=(0, 0, 0, 0.1),
            size_hint=(1, 1)
        )
        btn.bind(on_press=self.on_button_click)
        self.add_widget(img)
        self.add_widget(btn)

    def on_button_click(self, instance):
        self.show_popup()

    def show_popup(self):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)

        img = Image(source=self.image_source, size_hint=(1, 1))
        sign = get_sign_by_id(self.id_sign)
        label = Label(
            text=sign.description,
            size_hint_y=None,
            text_size=(400, None),  
            valign="top",
            halign="left"
        )

        close_btn = Button(text="X", size_hint=(None, None), size=(50, 50))
        
        # Tạo popup và bind nút X để đóng nó
        popup = Popup(
            title="Thông Tin Biển Báo",
            content=content,
            size_hint=(0.7, 0.7),
            auto_dismiss=False  # Không tự đóng khi nhấn bên ngoài
        )
        close_btn.bind(on_press=popup.dismiss)

        # Thêm vào layout
        header_layout = BoxLayout(size_hint_y=None, height=50, padding=[5, 5], spacing=5)
        header_layout.add_widget(Label(text=sign.name))
        header_layout.add_widget(close_btn)

        content.add_widget(header_layout)
        content.add_widget(img)
        content.add_widget(label)

        popup.open()


class PageScreen(Screen):
    def __init__(self, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.selected_category = "Tất cả"
        self.checkType = False
        self.Type = ""

        main_layout = BoxLayout(orientation="vertical", spacing=10, padding=[20, 20, 20, 20])

        # Header
        main_layout.add_widget(Header(screen_manager, "Biển Báo"))

        # Thanh tìm kiếm
        self.search_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=50, spacing=10) 
        

        self.category_spinner = Spinner(
            text="Chọn phân loại",
            values=["Tất cả", "Cấm", "Nguy hiểm", "Chỉ dẫn", "Hiệu lệnh", "Biển phụ"],
            size_hint=(0.3, None),
            height=40
        )
        self.category_spinner.bind(text=self.on_category_selected)

        self.search_bar = TextInput(
            hint_text="Tìm kiếm biển báo...",
            size_hint=(1, None),
            height=40
        )
        self.search_bar.bind(text=self.on_search_text)
        
        self.search_layout.add_widget(self.category_spinner)
        self.search_layout.add_widget(self.search_bar)
        main_layout.add_widget(self.search_layout)

        # **ScrollView để chứa GridLayout**
        self.scroll_view = ScrollView(size_hint=(1, 1), bar_width=10, scroll_wheel_distance=50)

        # Grid chứa các ảnh
        self.button_grid = GridLayout(
            cols=2,
            spacing=20,
            padding=[0, 20, 0, 20],
            size_hint_y=None  # Quan trọng để ScrollView hoạt động
        )

    
        signs_start = get_all_signs()
        self.load_signs(signs_start)
        
        # Thêm ScrollView vào Main Layout
        main_layout.add_widget(self.scroll_view)

        # Footer
        main_layout.add_widget(Footer(screen_manager))

        self.add_widget(main_layout)
    
    
    def load_signs(self, signs):
        self.button_grid.clear_widgets()  # Xóa danh sách cũ
        self.row_count = (len(signs) + 1) // 2  # Chia 2 cột
        self.button_grid.height = self.row_count * 150  # 150 là chiều cao mỗi hàng (có thể chỉnh)
        
        for sign in signs:
            image_path = f"image/bienbaocam/{sign.image}"
            # Kiểm tra xem file có tồn tại không
            if not os.path.exists(image_path):
                print(sign.id_sign)
            img_button = ImageButton(id_sign=sign.id_sign, image_source=image_path)
            self.button_grid.add_widget(img_button)

        # **Tính chiều cao động dựa trên số ảnh**
        self.row_count = (len(signs) + 1) // 2  # Chia 2 cột
        self.button_grid.height = self.row_count * 150  # 150 là chiều cao mỗi hàng (có thể chỉnh)
         # **Thêm Grid vào ScrollView**
        self.scroll_view.add_widget(self.button_grid)
        
    

    def on_search_text(self, instance, value):
        if self.checkType == False:
            signs = get_all_signs()
            signs_search = get_all_signs_by_keyword(value,signs)
            self.scroll_view.remove_widget(self.button_grid)  # Xóa Grid cũ trước khi thêm lại
            self.load_signs(signs_search)
        
        if self.checkType == True:
            if self.Type =="Cấm":
                signs = get_all_signs_by_type(1)
                signs_search = get_all_signs_by_keyword(value,signs)
                self.scroll_view.remove_widget(self.button_grid)  # Xóa Grid cũ trước khi thêm lại
                self.load_signs(signs_search)
            
            if self.Type == "Nguy hiểm":
                signs = get_all_signs_by_type(2)
                signs_search = get_all_signs_by_keyword(value,signs)
                self.scroll_view.remove_widget(self.button_grid)  # Xóa Grid cũ trước khi thêm lại
                self.load_signs(signs_search)

            if self.Type == "Chỉ dẫn":
                signs = get_all_signs_by_type(3)
                signs_search = get_all_signs_by_keyword(value,signs)
                self.scroll_view.remove_widget(self.button_grid)  # Xóa Grid cũ trước khi thêm lại
                self.load_signs(signs_search)

            if self.Type == "Hiệu lệnh":
                signs = get_all_signs_by_type(4)
                signs_search = get_all_signs_by_keyword(value,signs)
                self.scroll_view.remove_widget(self.button_grid)  # Xóa Grid cũ trước khi thêm lại
                self.load_signs(signs_search)

            if self.Type == "Biển phụ":
                signs = get_all_signs_by_type(5)
                signs_search = get_all_signs_by_keyword(value,signs)
                self.scroll_view.remove_widget(self.button_grid)  # Xóa Grid cũ trước khi thêm lại
                self.load_signs(signs_search)

    def on_category_selected(self, spinner, text):
        if text=="Cấm":
            signs = get_all_signs_by_type(1)
            self.scroll_view.remove_widget(self.button_grid)  # Xóa Grid cũ trước khi thêm lại
            self.load_signs(signs)
            self.Type = text
            self.checkType = True

        if text=="Nguy hiểm":
            signs = get_all_signs_by_type(2)
            self.scroll_view.remove_widget(self.button_grid)  # Xóa Grid cũ trước khi thêm lại
            self.load_signs(signs)
            self.Type = text
            self.checkType = True

        if text=="Chỉ dẫn":
            signs = get_all_signs_by_type(3)
            self.scroll_view.remove_widget(self.button_grid)  # Xóa Grid cũ trước khi thêm lại
            self.load_signs(signs)
            self.Type = text
            self.checkType = True

        if text=="Hiệu lệnh":
            signs = get_all_signs_by_type(4)
            self.scroll_view.remove_widget(self.button_grid)  # Xóa Grid cũ trước khi thêm lại
            self.load_signs(signs)

        if text=="Biển phụ":
            signs = get_all_signs_by_type(5)
            self.scroll_view.remove_widget(self.button_grid)  # Xóa Grid cũ trước khi thêm lại
            self.load_signs(signs)
            self.Type = text
            self.checkType = True

        if text=="Tất cả":
            signs = get_all_signs()
            self.scroll_view.remove_widget(self.button_grid)  # Xóa Grid cũ trước khi thêm lại
            self.load_signs(signs)
            self.checkType = False


class MyApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        sm = ScreenManager()
        sm.add_widget(PageScreen(1, sm))
        return sm


if __name__ == "__main__":
    MyApp().run()
