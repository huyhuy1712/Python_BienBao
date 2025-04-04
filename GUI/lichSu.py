import sys
import os
from datetime import datetime

# Lấy thư mục chứa file lichSu.py (tức là GUI)
current_dir = os.path.abspath(os.path.dirname(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.graphics import Color, Line
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.button import MDIconButton
from kivymd.uix.textfield import MDTextField

from model.history_crud import get_history_data

try:
    from footer import Footer
    from header import Header
except ImportError:
    print("Không tìm thấy module footer hoặc header. Sử dụng giả lập.")
    class Header(BoxLayout):
        def __init__(self, screen_manager, title, **kwargs):
            super().__init__(size_hint=(1, 0.1), **kwargs)
            self.add_widget(Label(text=title, font_size=20, bold=True))

    class Footer(BoxLayout):
        def __init__(self, screen_manager, **kwargs):
            super().__init__(size_hint=(1, 0.1), **kwargs)
            self.add_widget(Label(text="Footer", font_size=16))

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

class HistoryScreen(BoxLayout, Screen):
    def __init__(self, screen_manager, **kwargs):
        super().__init__(orientation="vertical", spacing=10, padding=0, **kwargs)
        self.screen_manager = screen_manager
        self.md_bg_color = (1, 1, 1, 1)

        self.add_widget(Header(screen_manager, "Lịch Sử"))

        # Thanh tìm kiếm
        search_layout = BoxLayout(size_hint=(1, 0.16), spacing=5,padding=10)
        self.search_input = MDTextField(
            hint_text="Tìm kiếm...",
            font_size=18,
            size_hint=(0.7, None),
            height=40,
            line_color_normal=[0.7, 0.7, 0.7, 1],
            line_color_focus=[0.2, 0.6, 1, 1]
        )
        self.clear_button = MDIconButton(icon="close-circle", icon_size=30)
        self.search_icon = MDIconButton(icon="magnify", icon_size=30)
        self.refresh_icon = MDIconButton(icon="refresh", icon_size=30)
        self.clear_button.bind(on_release=self.clear_search)
        self.search_icon.bind(on_release=self.search_data)  # Gắn sự kiện tìm kiếm
        self.refresh_icon.bind(on_release=self.refresh_table)

        search_layout.add_widget(self.search_input)
        search_layout.add_widget(self.clear_button)
        search_layout.add_widget(self.search_icon)
        search_layout.add_widget(self.refresh_icon)
        self.add_widget(search_layout)

        # Bộ lọc và sắp xếp
        filter_sort_layout = BoxLayout(size_hint=(1, 0.13), spacing=5, padding=5)
        self.date_input = MDTextField(
            hint_text="dd/mm/yy",
            readonly=True,
            size_hint=(0.25, None),
            height=40,
            font_size=18,
            line_color_normal=[0.7, 0.7, 0.7, 1],
            line_color_focus=[0.2, 0.6, 1, 1]
        )
        self.date_button = MDIconButton(icon="calendar", icon_size=30, pos_hint={'center_y': 0.5})
        self.date_button.bind(on_release=self.show_date_picker)
        self.filter_type = Spinner(
            text="Hoạt động",
            values=["Tất cả", "Upload", "Scan"],
            size_hint=(0.25, None),
            height=50,
            font_size=16
        )
        self.sort_button = Spinner(
            text="Sắp xếp",
            values=["Mới nhất", "Cũ nhất"],
            size_hint=(0.25, None),
            height=50,
            font_size=16
        )
        filter_sort_layout.add_widget(self.sort_button)
        filter_sort_layout.add_widget(self.filter_type)
        filter_sort_layout.add_widget(self.date_input)
        filter_sort_layout.add_widget(self.date_button)
        self.add_widget(filter_sort_layout)

        # Bảng dữ liệu
        self.outer_scroll_view = ScrollView(size_hint=(1, 0.8), do_scroll_x=True, do_scroll_y=True)
        self.history_table = GridLayout(cols=4, size_hint_x=None, size_hint_y=None, spacing=2, padding=[10, 10])
        self.history_table.bind(minimum_width=self.history_table.setter('width'))
        self.history_table.bind(minimum_height=self.history_table.setter('height'))

        self.outer_scroll_view.add_widget(self.history_table)
        self.add_widget(self.outer_scroll_view)

        # Phân trang
        pagination_layout = BoxLayout(size_hint=(1, 0.1), spacing=10, padding=[20, 10])
        self.prev_btn = Button(
            text="Trước", font_size=20, bold=True,
            size_hint=(None, None), size=(80, 50),
            background_color=(0.2, 0.6, 1, 1),
            color=(1, 1, 1, 1)
        )
        self.next_btn = Button(
            text="Sau", font_size=20, bold=True,
            size_hint=(None, None), size=(80, 50),
            background_color=(0.2, 0.6, 1, 1),
            color=(1, 1, 1, 1)
        )
        pagination_layout.add_widget(BoxLayout(size_hint_x=0.4))
        pagination_layout.add_widget(self.prev_btn)
        pagination_layout.add_widget(self.next_btn)
        pagination_layout.add_widget(BoxLayout(size_hint_x=0.4))
        self.add_widget(pagination_layout)

        self.add_widget(Footer(screen_manager))

        # Khởi tạo bảng
        self.current_page = 1
        self.items_per_page = 10
        self.populate_table_from_db()

    def clear_search(self, instance):
        self.search_input.text = ""
        self.populate_table_from_db()

    def show_date_picker(self, instance):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_date_selected)
        date_dialog.open()

    def on_date_selected(self, instance, value, date_range):
        self.date_input.text = value.strftime('%d/%m/%Y')
        self.populate_table_from_db()

    def truncate_text(self, text, max_length=40):
        if text and len(text) > max_length:
            return text[:max_length-3] + "..."
        return text or "Không có mô tả"

    def refresh_table(self, instance):
        self.current_page = 1
        self.search_input.text = ""
        self.date_input.text = ""
        self.filter_type.text = "Tất cả"
        self.sort_button.text = "Mới nhất"
        self.populate_table_from_db()

    def search_data(self, instance):
        self.current_page = 1
        self.populate_table_from_db()

    def populate_table_from_db(self):
        try:
            self.history_table.clear_widgets()
            headers = ["Ảnh", "Mô tả", "Loại hoạt động", "Thời gian"]

            # Tính toán chiều rộng cột dựa trên kích thước màn hình
            screen_width, screen_height = Window.size
            column_widths = [
                int(screen_width * 0.15),  # Ảnh
                int(screen_width * 0.35),  # Mô tả
                int(screen_width * 0.20),  # Loại hoạt động
                int(screen_width * 0.25),  # Thời gian
            ]
            self.history_table.width = sum(column_widths)

            # Thêm tiêu đề
            for header, width in zip(headers, column_widths):
                lbl = BorderedLabel(
                    text=header, bold=True, color=(0, 0, 0, 1),
                    size_hint_x=None, width=width, size_hint_y=None, height=40,
                    text_size=(width-10, None), halign="center", valign="middle"
                )
                lbl.texture_update()
                self.history_table.add_widget(lbl)

            # Lấy dữ liệu
            history_data = get_history_data()
            if history_data is None:
                print("Không có dữ liệu từ database, có thể do lỗi kết nối.")
                no_data_label = BorderedLabel(
                    text="Không thể kết nối đến cơ sở dữ liệu", color=(0, 0, 0, 1),
                    size_hint_x=None, width=sum(column_widths), size_hint_y=None, height=60,
                    halign="center", valign="middle"
                )
                self.history_table.add_widget(no_data_label)
                return
            elif not history_data:
                print("Không có dữ liệu lịch sử trong database.")
                no_data_label = BorderedLabel(
                    text="Không có dữ liệu lịch sử", color=(0, 0, 0, 1),
                    size_hint_x=None, width=sum(column_widths), size_hint_y=None, height=60,
                    halign="center", valign="middle"
                )
                self.history_table.add_widget(no_data_label)
                return

            # Lọc và sắp xếp dữ liệu
            filtered_data = history_data

            # Lọc theo từ khóa tìm kiếm
            search_text = self.search_input.text.strip().lower()
            if search_text:
                filtered_data = [
                    row for row in filtered_data
                    if (row[5] and search_text in row[5].lower()) or  # Mô tả
                       (row[4] and search_text in row[4].lower())     # Tên file ảnh
                ]

            # Lọc theo loại hoạt động
            if self.filter_type.text in ["Upload", "Scan"]:
                activity_filter = 1 if self.filter_type.text == "Upload" else 2
                filtered_data = [row for row in filtered_data if row[2] == activity_filter]

            # Lọc theo ngày
            if self.date_input.text:
                try:
                    filter_date = datetime.strptime(self.date_input.text, '%d/%m/%Y').date()
                    filtered_data = [row for row in filtered_data if row[3].date() == filter_date]
                except ValueError as e:
                    print(f"Lỗi định dạng ngày: {e}")
                    return

            # Sắp xếp dữ liệu
            if self.sort_button.text == "Cũ nhất":
                filtered_data.sort(key=lambda x: x[3])
            else:  # Mới nhất
                filtered_data.sort(key=lambda x: x[3], reverse=True)

            # Phân trang
            total_items = len(filtered_data)
            total_pages = (total_items + self.items_per_page - 1) // self.items_per_page
            start_idx = (self.current_page - 1) * self.items_per_page
            end_idx = min(start_idx + self.items_per_page, total_items)
            paginated_data = filtered_data[start_idx:end_idx]

            # Cập nhật trạng thái nút phân trang
            self.prev_btn.disabled = self.current_page == 1
            self.next_btn.disabled = self.current_page >= total_pages
            self.prev_btn.bind(on_release=self.prev_page)
            self.next_btn.bind(on_release=self.next_page)

            # Thêm dữ liệu vào bảng
            for row in paginated_data:
                id_user, id_sign, activity_type, time, img_src, desc = row
                activity = "Upload" if activity_type == 1 else "Scan"
                time_str = time.strftime("%I:%M %p - %d/%m/%Y")

                # Cột Ảnh
                img_border = BorderedBox(size_hint_x=None, width=column_widths[0], size_hint_y=None, height=60)
                img_layout = BoxLayout(size_hint=(1, 1), padding=2)
                full_img_path = os.path.join(parent_dir, img_src) if img_src else None
                if full_img_path and os.path.exists(full_img_path):
                    img = Image(source=full_img_path, size_hint=(None, None), size=(55, 55), allow_stretch=True, keep_ratio=True)
                else:
                    print(f"File hình ảnh không tồn tại: {full_img_path}")
                    img = Label(text="No Image", size_hint=(None, None), size=(55, 55), color=(0, 0, 0, 1))
                img_layout.add_widget(img)
                img_border.add_widget(img_layout)

                # Cột Mô tả
                desc_label = BorderedLabel(
                    text=self.truncate_text(desc, 40), color=(0, 0, 0, 1),
                    size_hint_x=None, width=column_widths[1], size_hint_y=None, height=60,
                    text_size=(column_widths[1]-10, 60), halign="left", valign="middle"
                )
                # Cột Loại hoạt động
                activity_label = BorderedLabel(
                    text=activity, color=(0, 0, 0, 1),
                    size_hint_x=None, width=column_widths[2], size_hint_y=None, height=60,
                    text_size=(column_widths[2]-10, None), halign="center", valign="middle"
                )
                # Cột Thời gian
                time_label = BorderedLabel(
                    text=time_str, color=(0, 0, 0, 1),
                    size_hint_x=None, width=column_widths[3], size_hint_y=None, height=60,
                    text_size=(column_widths[3]-10, None), halign="center", valign="middle"
                )

                self.history_table.add_widget(img_border)
                self.history_table.add_widget(desc_label)
                self.history_table.add_widget(activity_label)
                self.history_table.add_widget(time_label)

            # Cập nhật chiều cao của bảng
            self.history_table.height = (len(paginated_data) + 1) * 60  # +1 cho tiêu đề

        except Exception as e:
            print(f"Lỗi trong populate_table_from_db: {str(e)}")
            import traceback
            traceback.print_exc()

    def prev_page(self, instance):
        if self.current_page > 1:
            self.current_page -= 1
            self.populate_table_from_db()

    def next_page(self, instance):
        self.current_page += 1
        self.populate_table_from_db()

class HistoryApp(MDApp):
    def build(self):
        try:
            sm = ScreenManager()
            screen = HistoryScreen(sm)
            print("HistoryScreen khởi tạo thành công")
            sm.add_widget(screen)
            return sm
        except Exception as e:
            print(f"Lỗi khi khởi tạo HistoryScreen: {str(e)}")
            import traceback
            traceback.print_exc()
            raise

if __name__ == "__main__":
    try:
        print("Bắt đầu chạy ứng dụng")
        HistoryApp().run()
    except Exception as e:
        print(f"Lỗi khi chạy ứng dụng: {str(e)}")
        import traceback
        traceback.print_exc()