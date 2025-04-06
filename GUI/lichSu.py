import sys
import os
from datetime import datetime
import pytz  # Thêm module pytz để xử lý múi giờ

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
from kivy.uix.anchorlayout import AnchorLayout
from kivy.graphics import Color, Line
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.button import MDIconButton, MDFlatButton
from kivymd.uix.textfield import MDTextField

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from model.user_crud import *

from model.history_crud import get_history_data
from model.user_crud import *
try:
    from footer import Footer
    from header import Header
except ImportError:
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

        screen_width, screen_height = Window.size
        self.column_widths = [
            int(screen_width * 0.25),
            int(screen_width * 0.35),
            int(screen_width * 0.40),
             int(screen_width * 0.60),
        ]
        self.table_width = sum(self.column_widths)

        user_id = str(load_user_id())
        self.add_widget(Header(screen_manager,user_id, "Lịch Sử"))

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
        self.refresh_icon = MDIconButton(icon="refresh", icon_size=30, pos_hint={'center_y': 0.5})
        self.refresh_icon.bind(on_release=self.refresh_table)

        self.filter_type.bind(text=self.on_filter_change)
        self.sort_button.bind(text=self.on_filter_change)

        filter_sort_layout.add_widget(self.sort_button)
        filter_sort_layout.add_widget(self.filter_type)
        filter_sort_layout.add_widget(self.date_input)
        filter_sort_layout.add_widget(self.date_button)
        filter_sort_layout.add_widget(self.refresh_icon)
        self.add_widget(filter_sort_layout)

        # Bảng dữ liệu (chỉ 4 cột)
        self.outer_scroll_view = ScrollView(size_hint=(1, 0.8), do_scroll_x=True, do_scroll_y=True)
        self.history_table = GridLayout(cols=4, size_hint_x=None, size_hint_y=None, spacing=2, padding=[10, 10])
        self.history_table.bind(minimum_width=self.history_table.setter('width'))
        self.history_table.bind(minimum_height=self.history_table.setter('height'))

        self.outer_scroll_view.add_widget(self.history_table)
        self.add_widget(self.outer_scroll_view)

        # Phân trang
        self.pagination_layout = BoxLayout(size_hint=(1, 0.1), spacing=5, padding=[10, 5])
        self.add_widget(self.pagination_layout)

        self.add_widget(Footer(screen_manager))

        self.current_page = 1
        self.items_per_page = 8
        self.max_page_buttons = 5
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
        self.date_input.text = ""
        self.filter_type.text = "Tất cả"
        self.sort_button.text = "Mới nhất"
        self.populate_table_from_db()

    # Hàm được gọi khi giá trị của bộ lọc thay đổi
    def on_filter_change(self, instance, value):
        self.current_page = 1
        self.populate_table_from_db()

    # Cập nhật các nút phân trang
    def update_pagination(self, total_pages):
        self.pagination_layout.clear_widgets()

        pagination_inner_layout = BoxLayout(
            size_hint=(None, 1),
            spacing=5,
            padding=[5, 0]
        )

        prev_btn = MDFlatButton(
            text="Trước", font_size=16,
            size_hint=(None, None), size=(60, 40),
            md_bg_color=(0.1, 0.5, 0.9, 1),
            md_bg_color_disabled=(0.1, 0.5, 0.9, 1),
            text_color=(1, 1, 1, 1),
            disabled_color=(0.7, 0.7, 0.7, 1),
            disabled=self.current_page == 1
        )
        prev_btn.bind(on_release=self.prev_page)
        pagination_inner_layout.add_widget(prev_btn)

        if total_pages <= self.max_page_buttons:
            page_range = range(1, total_pages + 1)
        else:
            half_range = self.max_page_buttons // 2
            start_page = max(2, self.current_page - half_range)
            end_page = min(total_pages - 1, self.current_page + half_range)

            if self.current_page <= half_range + 1:
                end_page = self.max_page_buttons - 1
            elif self.current_page >= total_pages - half_range:
                start_page = total_pages - self.max_page_buttons + 2

            page_range = [1]
            if start_page > 2:
                page_range.append("...")
            page_range.extend(range(start_page, end_page + 1))
            if end_page < total_pages - 1:
                page_range.append("...")
            page_range.append(total_pages)

        for page in page_range:
            if page == "...":
                page_label = Label(
                    text="...", font_size=16, color=(0, 0, 0, 1),
                    size_hint=(None, None), size=(30, 40)
                )
                pagination_inner_layout.add_widget(page_label)
            else:
                page_btn = MDFlatButton(
                    text=str(page), font_size=16,
                    size_hint=(None, None), size=(30, 40),
                    md_bg_color=(0.2, 0.6, 1, 1) if page != self.current_page else (0.4, 0.8, 1, 1),
                    text_color=(0, 0, 0, 1)
                )
                page_btn.bind(on_release=lambda btn, p=page: self.go_to_page(p))
                pagination_inner_layout.add_widget(page_btn)

        next_btn = MDFlatButton(
            text="Sau", font_size=16,
            size_hint=(None, None), size=(60, 40),
            md_bg_color=(0.1, 0.5, 0.9, 1),
            md_bg_color_disabled=(0.1, 0.5, 0.9, 1),
            text_color=(1, 1, 1, 1),
            disabled_color=(0.7, 0.7, 0.7, 1),
            disabled=self.current_page == total_pages
        )
        next_btn.bind(on_release=self.next_page)
        pagination_inner_layout.add_widget(next_btn)

        total_width = (len(page_range) * 30) + (2 * 60) + (len(page_range) * 5)
        pagination_inner_layout.width = total_width

        self.pagination_layout.add_widget(BoxLayout(size_hint_x=0.5))
        self.pagination_layout.add_widget(pagination_inner_layout)
        self.pagination_layout.add_widget(BoxLayout(size_hint_x=0.5))

    def populate_table_from_db(self):
        try:
            self.history_table.clear_widgets()
            headers = ["Ảnh", "Loại hoạt động", "Thời gian", "Kết quả"]

            column_widths = self.column_widths
            self.history_table.width = self.table_width

            for header, width in zip(headers, column_widths):
                lbl = BorderedLabel(
                    text=header, bold=True, color=(0, 0, 0, 1),
                    size_hint_x=None, width=width, size_hint_y=None, height=40,
                    text_size=(width-10, None), halign="center", valign="middle"
                )
                lbl.texture_update()
                self.history_table.add_widget(lbl)

            user_id = str(load_user_id())
            history_data = get_history_data(user_id)
            
            if history_data is None:
                no_data_label = BorderedLabel(
                    text="Không thể kết nối đến cơ sở dữ liệu", color=(0, 0, 0, 1),
                    size_hint_x=None, width=sum(column_widths), size_hint_y=None, height=60,
                    halign="center", valign="middle"
                )
                self.history_table.add_widget(no_data_label)
                return
            elif not history_data:
                no_data_label = BorderedLabel(
                    text="Không có dữ liệu lịch sử", color=(0, 0, 0, 1),
                    size_hint_x=None, width=sum(column_widths), size_hint_y=None, height=60,
                    halign="center", valign="middle"
                )
                self.history_table.add_widget(no_data_label)
                return

            filtered_data = history_data

            if self.filter_type.text in ["Upload", "Scan"]:
                activity_filter = 1 if self.filter_type.text == "Upload" else 2
                filtered_data = [row for row in filtered_data if row[2] == activity_filter]

            if self.date_input.text:
                try:
                    filter_date = datetime.strptime(self.date_input.text, '%d/%m/%Y').date()
                    filtered_data = [row for row in filtered_data if row[3].date() == filter_date]
                except ValueError:
                    return

            if self.sort_button.text == "Cũ nhất":
                filtered_data.sort(key=lambda x: x[3])
            else:
                filtered_data.sort(key=lambda x: x[3], reverse=True)

            total_items = len(filtered_data)
            total_pages = (total_items + self.items_per_page - 1) // self.items_per_page
            start_idx = (self.current_page - 1) * self.items_per_page
            end_idx = min(start_idx + self.items_per_page, total_items)
            paginated_data = filtered_data[start_idx:end_idx]

            self.update_pagination(total_pages if total_pages > 0 else 1)

            # Định nghĩa múi giờ Việt Nam (UTC+7)
            vn_timezone = pytz.timezone('Asia/Ho_Chi_Minh')

            for row in paginated_data:
                activity_type, time, img_src, desc = row
                activity = "Upload" if activity_type == 1 else "Scan"

                # Chuyển đổi thời gian sang múi giờ Việt Nam
                if time.tzinfo is None:
                    # Nếu thời gian không có múi giờ, giả định nó là UTC
                    time = pytz.utc.localize(time)
                time_vn = time.astimezone(vn_timezone)
                # Định dạng thời gian theo giờ Việt Nam (24h)
                time_str = time_vn.strftime("%H:%M - %d/%m/%Y")

                img_border = BorderedBox(
                    size_hint_x=None, 
                    width=column_widths[0], 
                    size_hint_y=None, 
                    height=60
                )
                img_layout = AnchorLayout(
                    anchor_x='center',
                    anchor_y='center',
                    size_hint=(1, 1)
                )
                if img_src:
                    img_filename = img_src.split("image/")[-1] if "image/" in img_src else img_src
                    full_img_path = os.path.join(parent_dir, "image", img_filename)
                    if os.path.exists(full_img_path):
                        img_size = min(column_widths[0] - 10, 55)
                        img = Image(
                            source=full_img_path,
                            size_hint=(None, None),
                            size=(img_size, img_size),
                            allow_stretch=True,
                            keep_ratio=True
                        )
                    else:
                        img = Label(
                            text="No Image",
                            size_hint=(None, None),
                            size=(55, 55),
                            color=(0, 0, 0, 1)
                        )
                else:
                    img = Label(
                        text="No Image",
                        size_hint=(None, None),
                        size=(55, 55),
                        color=(0, 0, 0, 1)
                    )
                img_layout.add_widget(img)
                img_border.add_widget(img_layout)

                activity_label = BorderedLabel(
                    text=activity, color=(0, 0, 0, 1),
                    size_hint_x=None, width=column_widths[1], size_hint_y=None, height=60,
                    text_size=(column_widths[1]-10, None), halign="center", valign="middle"
                )
                time_label = BorderedLabel(
                    text=time_str, color=(0, 0, 0, 1),
                    size_hint_x=None, width=column_widths[2], size_hint_y=None, height=60,
                    text_size=(column_widths[2]-10, None), halign="center", valign="middle"
                )
                
                            # Cột kết quả (description)
                description_label = BorderedLabel(
                    text=desc if desc else "Không có",
                    color=(0, 0, 0, 1),
                    size_hint_x=None, width=column_widths[3],
                    size_hint_y=None, height=60,
                    text_size=(column_widths[3]-10, None), halign="center", valign="middle"
    )

                self.history_table.add_widget(img_border)
                self.history_table.add_widget(activity_label)
                self.history_table.add_widget(time_label)
                self.history_table.add_widget(description_label)

            self.history_table.height = (len(paginated_data) + 1) * 60

        except Exception:
            pass

    def prev_page(self, instance):
        if self.current_page > 1:
            self.current_page -= 1
            self.populate_table_from_db()

    def next_page(self, instance):
        self.current_page += 1
        self.populate_table_from_db()

    def go_to_page(self, page):
        self.current_page = page
        self.populate_table_from_db()

class HistoryApp(MDApp):
    def build(self):
        try:
            sm = ScreenManager()
            screen = HistoryScreen(sm)
            sm.add_widget(screen)
            return sm
        except Exception:
            raise

if __name__ == "__main__":
    try:
        HistoryApp().run()
    except Exception:
        pass