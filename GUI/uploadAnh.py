from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.core.window import Window

class UploadScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=10, padding=[10, 50, 10, 10], **kwargs)  # Thêm padding trên cùng

        # **KHU VỰC HÌNH ẢNH - ĐẨY LÊN CAO**
        self.image_container = BoxLayout(size_hint=(0.8, 0.5), pos_hint={'center_x': 0.5, 'top': 0.9})
        with self.image_container.canvas.before:
            Color(1, 0.6, 0, 1)  # Màu cam
            self.outer_border = Line(rectangle=(self.image_container.x, self.image_container.y, 
                                        self.image_container.width, self.image_container.height), 
                                    width=2, dash_length=10, dash_offset=5)

            # Viền trong
            Color(0.9, 0.9, 0.9, 1)
            self.rect_img = RoundedRectangle(size=self.image_container.size, pos=self.image_container.pos, radius=[20])
        self.image_container.bind(size=self.update_rect, pos=self.update_rect)

        self.image_display = Image(source="./image/images-solid.png", size_hint=(0.6, 1))
        self.image_container.add_widget(self.image_display)
        self.add_widget(self.image_container)

        # **KHU VỰC NÚT - THÊM KHOẢNG CÁCH**
        button_container = BoxLayout(orientation='vertical', size_hint=(0.5, 0.3), spacing=15, padding=[0, 20, 0, 20], pos_hint={'center_x': 0.5})
        self.upload_btn = Button(text="Tải ảnh lên", font_size=24, bold=True,
                                 size_hint=(1, 0.3), background_color=(1, 0, 0, 1))
        self.search_btn = Button(text="Tra cứu", font_size=24, bold=True,
                                 size_hint=(1, 0.3), background_color=(1, 0.8, 0, 1))
        self.history_btn = Button(text="Lịch sử", font_size=24, bold=True,
                                 size_hint=(1, 0.3), background_color=(0, 0.78, 0, 1))

        button_container.add_widget(self.upload_btn)
        button_container.add_widget(self.search_btn)
        button_container.add_widget(self.history_btn)
        self.add_widget(button_container)

    def update_rect(self, *args):
        self.outer_border.rounded_rectangle = (self.image_container.x - 10, self.image_container.y - 10, 
                                               self.image_container.width + 20, self.image_container.height + 20, 25)
        self.rect_img.pos = self.image_container.pos
        self.rect_img.size = self.image_container.size

class UploadApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)  # Nền trắng toàn màn hình
        return UploadScreen()

if __name__ == "__main__":
    UploadApp().run()
