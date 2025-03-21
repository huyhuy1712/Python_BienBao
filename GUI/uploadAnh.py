from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics import Color, RoundedRectangle
from kivy.core.window import Window

class UploadScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=15, padding=[20, 50, 20, 20], **kwargs)

        # **KHU VỰC HÌNH ẢNH**
        self.image_container = BoxLayout(size_hint=(0.85, 0.5), pos_hint={'center_x': 0.5})
        with self.image_container.canvas.before:
            # Viền cam
            Color(1, 0.6, 0, 1)
            self.outer_border = RoundedRectangle(size=self.image_container.size, pos=self.image_container.pos, radius=[20])

            # Nền xám nhạt
            Color(0.9, 0.9, 0.9, 1)
            self.rect_img = RoundedRectangle(size=self.image_container.size, pos=self.image_container.pos, radius=[20])
        
        self.image_container.bind(size=self.update_rect, pos=self.update_rect)

        # Ảnh mặc định
        self.image_display = Image(source="./image/images-solid.png", size_hint=(0.7, 1))
        self.image_container.add_widget(self.image_display)
        self.add_widget(self.image_container)

        # **KHU VỰC NÚT**
        button_container = BoxLayout(orientation='vertical', size_hint=(0.6, 0.3), spacing=10, pos_hint={'center_x': 0.5})

        self.upload_btn = self.create_rounded_button("Tải ảnh lên", (0.5, 0, 0, 1))
        self.search_btn = self.create_rounded_button("Tra cứu", (0.4, 0.3, 0, 1))
        self.history_btn = self.create_rounded_button("Lịch sử", (0, 0.5, 0, 1))

        button_container.add_widget(self.upload_btn)
        button_container.add_widget(self.search_btn)
        button_container.add_widget(self.history_btn)
        self.add_widget(button_container)

    def create_rounded_button(self, text, color):
        """Tạo nút bo tròn hoàn toàn"""
        btn = Button(text=text, font_size=22, bold=True, size_hint=(1, 0.3), background_color=(0, 0, 0, 0), background_normal="")
        with btn.canvas.before:
            Color(*color)
            btn.rect = RoundedRectangle(size=btn.size, pos=btn.pos, radius=[20])  # Bo tròn hoàn toàn
        btn.bind(size=self.update_btn_rect, pos=self.update_btn_rect)
        return btn

    def update_btn_rect(self, instance, *args):
        """Cập nhật hình chữ nhật bo góc khi thay đổi kích thước nút"""
        instance.rect.size = instance.size
        instance.rect.pos = instance.pos

    def update_rect(self, *args):
        """Cập nhật vị trí và kích thước của viền & nền"""
        self.outer_border.pos = (self.image_container.x - 5, self.image_container.y - 5)
        self.outer_border.size = (self.image_container.width + 10, self.image_container.height + 10)

        self.rect_img.pos = self.image_container.pos
        self.rect_img.size = self.image_container.size

class UploadApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)  # Nền trắng
        return UploadScreen()

if __name__ == "__main__":
    UploadApp().run()
