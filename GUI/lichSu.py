from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivymd.uix.pickers import MDDatePicker
from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton
from kivymd.uix.textfield import MDTextField
from kivy.graphics import Color, Line
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager

from footer import Footer
from header import Header

class BorderedBox(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        
        with self.canvas.before:
            Color(0.7, 0.7, 0.7, 1)
            self.line = Line(rectangle=(self.x, self.y, self.width, self.height), width=1)
        self.bind(pos=self.update_graphics, size=self.update_graphics)

    def update_graphics(self, *args):
        self.line.rectangle = (self.x, self.y, self.width, self.height)

class BorderedLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.7, 0.7, 0.7, 1)
            self.line = Line(rectangle=(self.x, self.y, self.width, self.height), width=1)
        self.bind(pos=self.update_graphics, size=self.update_graphics)

    def update_graphics(self, *args):
        self.line.rectangle = (self.x, self.y, self.width, self.height)

class HistoryScreen(BoxLayout,Screen):
    def __init__(self,screen_manager, **kwargs):
        super().__init__(orientation="vertical", spacing=10, padding=0, **kwargs)
        self.date_input = MDTextField(hint_text="dd/mm/yy", size_hint=(0.3, 1), readonly=True, mode="rectangle")
        self.md_bg_color = (1, 1, 1, 1)

        self.add_widget(Header(screen_manager,"Lịch Sử"))

        # Thanh tìm kiếm
        search_layout = BoxLayout(size_hint=(1, 0.1), spacing=5)
        self.search_input = MDTextField(hint_text="Tìm kiếm...", font_size=16, size_hint=(0.7,None), height=2, mode="rectangle")
        self.clear_button = MDIconButton(icon="close-circle", size_hint=(None, None))
        self.search_icon = MDIconButton(icon="magnify", size_hint=(None, None))
        self.refresh_icon = MDIconButton(icon="refresh", size_hint=(None, None))
        self.clear_button.bind(on_release=self.clear_search)
        
        search_layout.add_widget(self.search_input)
        search_layout.add_widget(self.clear_button)
        search_layout.add_widget(self.search_icon)
        search_layout.add_widget(self.refresh_icon)
        self.add_widget(search_layout)

        # Thanh bộ lọc
        filter_sort_layout = BoxLayout(size_hint=(1, 0.1), spacing=10)
        self.date_input = MDTextField(hint_text="dd/mm/yy", readonly=True, mode="rectangle")
        self.date_button = MDIconButton(icon="calendar", size_hint=(None, None))
        self.date_button.bind(on_release=self.show_date_picker)
        self.filter_type = Spinner(text="Hoạt động", values=["Upload", "Scan"], size_hint=(0.3, 1))
        self.sort_button = Spinner(text="Sắp xếp", values=["Mới nhất", "Cũ nhất"], size_hint=(0.3, 1))

        filter_sort_layout.add_widget(self.sort_button)
        filter_sort_layout.add_widget(self.filter_type)
        filter_sort_layout.add_widget(self.date_input)
        filter_sort_layout.add_widget(self.date_button)
        self.add_widget(filter_sort_layout)

        # Scroll View
        self.outer_scroll_view = ScrollView(size_hint=(1, 0.8), do_scroll_x=True, do_scroll_y=True)
        self.history_table = GridLayout(cols=4, size_hint_x=None, width=1500, size_hint_y=None, spacing=2, padding=[10, 10])
        self.history_table.bind(minimum_width=self.history_table.setter('width'))
        self.history_table.bind(minimum_height=self.history_table.setter('height'))
        
        self.outer_scroll_view.add_widget(self.history_table)
        self.add_widget(self.outer_scroll_view)

        # Dữ liệu mẫu
        self.sample_data = [
            ("./image/scan-solid.png", "Tải ảnh lên hệ thống", "Upload", "10:30 AM - 18/03/2025"),
            ("./image/user-solid.png", "Tra cứu thông tin người dùng", "Scan", "09:15 AM - 17/03/2025"),
            ("./image/search-solid.png", "Tải ảnh lên tài khoản cá nhân", "Upload", "10:30 AM - 18/03/2025"),
            ("./image/history-solid.png", "Tra cứu lịch sử hoạt động với thông tin chi tiết dài", "Scan", "09:15 AM - 17/03/2025"),
            ("./image/scan-solid.png", "Tải ảnh lên hệ thống", "Upload", "10:30 AM - 18/03/2025"),
        ]
        self.populate_table()

        # Nút phân trang với thiết kế đẹp hơn
        pagination_layout = BoxLayout(size_hint=(1, 0.1), spacing=10, padding=[20, 10])
        self.prev_btn = Button(
            text="Trước", font_size=20, bold=True,
            size_hint=(None, None), size=(80, 50),
            background_color=(0.2, 0.6, 1, 1),  # Màu xanh dương
            color=(1, 1, 1, 1)  # Chữ trắng
        )
        self.next_btn = Button(
            text="Sau", font_size=20, bold=True,
            size_hint=(None, None), size=(80, 50),
            background_color=(0.2, 0.6, 1, 1),
            color=(1, 1, 1, 1)
        )

        # Thêm khoảng trống để căn giữa nút
        pagination_layout.add_widget(BoxLayout(size_hint_x=0.4))  # Khoảng trống trái
        pagination_layout.add_widget(self.prev_btn)
        pagination_layout.add_widget(self.next_btn)
        pagination_layout.add_widget(BoxLayout(size_hint_x=0.4))  # Khoảng trống phải

        self.add_widget(pagination_layout)
        self.add_widget(Footer(screen_manager))



    def clear_search(self, instance):
        self.search_input.text = ""

    def show_date_picker(self, instance):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_date_selected)
        date_dialog.open()

    def on_date_selected(self, instance, value, date_range):
        self.date_input.text = value.strftime('%d/%m/%Y')

    def truncate_text(self, text, max_length=50):
        if len(text) > max_length:
            return text[:max_length-3] + "..."
        return text

    def populate_table(self):
        self.history_table.clear_widgets()
        headers = ["Ảnh", "Mô tả", "Loại hoạt động", "Thời gian"]

        # Lấy kích thước màn hình
        screen_width, screen_height = Window.size

        # Xác định tỷ lệ chiều rộng cột theo màn hình
        column_widths = [
            int(screen_width * 0.10),  # Ảnh (10% màn hình)
            int(screen_width * 0.40),  # Mô tả (40% màn hình)
            int(screen_width * 0.25),  # Loại hoạt động (25% màn hình)
            int(screen_width * 0.25),  # Thời gian (25% màn hình)
    ]

        
        # Tạo tiêu đề
        for header, width in zip(headers, column_widths):
            lbl = BorderedLabel(
                text=header, bold=True, color=(0, 0, 0, 1),
                size_hint_x=None, width=width, size_hint_y=None, height=40,  # Giảm chiều cao tiêu đề
                text_size=(width, None), halign="center", valign="middle"
            )
            lbl.texture_update()
            self.history_table.add_widget(lbl)

        # Thêm dữ liệu vào bảng
        for img_src, desc, activity, time in self.sample_data:
            img_border = BorderedBox(size_hint_x=None, width=column_widths[0], size_hint_y=None, height=60)  # Giảm chiều cao hàng
            img_layout = BoxLayout(size_hint=(1, 1), padding=2)
            img = Image(source=img_src, size_hint=(None, None), size=(40, 40))  # Giảm kích thước ảnh
            img_layout.add_widget(img)
            img_border.add_widget(img_layout)
            
            desc_label = BorderedLabel(
                text=self.truncate_text(desc, 40), color=(0, 0, 0, 1),
                size_hint_x=None, width=column_widths[1], size_hint_y=None, height=60,  # Giảm chiều cao
                text_size=(column_widths[1], 60), halign="left", valign="middle"
            )
            activity_label = BorderedLabel(
                text=activity, color=(0, 0, 0, 1),
                size_hint_x=None, width=column_widths[2], size_hint_y=None, height=60,
                halign="center", valign="middle"
            )
            time_label = BorderedLabel(
                text=time, color=(0, 0, 0, 1),
                size_hint_x=None, width=column_widths[3], size_hint_y=None, height=60,
                halign="center", valign="middle"
            )
            
            self.history_table.add_widget(img_border)
            self.history_table.add_widget(desc_label)
            self.history_table.add_widget(activity_label)
            self.history_table.add_widget(time_label)


class HistoryApp(MDApp):
    def build(self):
        sm = ScreenManager()
        return HistoryScreen(sm)

if __name__ == "__main__":
    HistoryApp().run()