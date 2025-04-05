from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics import Color, RoundedRectangle
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
import os
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image as PILImage
from kivy.uix.label import Label



# Import từ các file header.py và footer.py
from footer import Footer
from header import Header

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from model.user_crud import *


classes = {
    0: 'Giới hạn tốc độ (20km/h)\nBáo hiệu giới hạn tốc độ tối đa cho phép là 20km/h.',
    1: 'Giới hạn tốc độ (30km/h)\nBáo hiệu giới hạn tốc độ tối đa cho phép là 30km/h.',
    2: 'Giới hạn tốc độ (50km/h)\nBáo hiệu giới hạn tốc độ tối đa cho phép là 50km/h.',
    3: 'Giới hạn tốc độ (60km/h)\nBáo hiệu giới hạn tốc độ tối đa cho phép là 60km/h.',
    4: 'Giới hạn tốc độ (70km/h)\nBáo hiệu giới hạn tốc độ tối đa cho phép là 70km/h.',
    5: 'Giới hạn tốc độ (80km/h)\nBáo hiệu giới hạn tốc độ tối đa cho phép là 80km/h.',
    6: 'Kết thúc giới hạn tốc độ (80km/h)\nBáo hiệu kết thúc khu vực giới hạn tốc độ tối đa 80km/h.',
    7: 'Giới hạn tốc độ (100km/h)\nBáo hiệu giới hạn tốc độ tối đa cho phép là 100km/h.',
    8: 'Giới hạn tốc độ (120km/h)\nBáo hiệu giới hạn tốc độ tối đa cho phép là 120km/h.',
    9: 'Cấm vượt\nBáo hiệu cấm các phương tiện vượt qua nhau.',
    10: 'Cấm vượt xe trọng tải trên 3.5 tấn\nBáo hiệu cấm các phương tiện có trọng lượng vượt quá 3.5 tấn vượt qua nhau.',
    11: 'Ưu tiên ở giao lộ\nBáo hiệu các phương tiện cần nhường đường cho các phương tiện khác ở giao lộ.',
    12: 'Đường ưu tiên\nBáo hiệu đường có ưu tiên đi trước so với các đường khác giao cắt.',
    13: 'Nhường đường\nBáo hiệu các phương tiện cần nhường đường cho các phương tiện khác.',
    14: 'Dừng lại\nBáo hiệu các phương tiện cần dừng lại tại vị trí báo hiệu.',
    15: 'Cấm xe\nBáo hiệu cấm các phương tiện đi qua đoạn đường được báo hiệu.',
    16: 'Cấm xe trọng tải trên 3.5 tấn\nBáo hiệu cấm các phương tiện có trọng lượng vượt quá 3.5 tấn đi qua đoạn đường được báo hiệu.',
    17: 'Cấm đi\nBáo hiệu cấm các phương tiện đi vào đoạn đường được báo hiệu.',
    18: 'Chú ý chung\nBáo hiệu cảnh báo về các tình huống đặc biệt hoặc lưu ý quan trọng.',
    19: 'Nguy hiểm ngoặc vòng bên trái\nBáo hiệu sắp đến đoạn đường có cua rẽ vòng bên trái.',
    20: 'Nguy hiểm ngoặc vòng bên phải\nBáo hiệu sắp đến đoạn đường có cua rẽ vòng bên phải.',
    21: 'Nguy hiểm ngoặc vòng kép\nBáo hiệu sắp đến đoạn đường có cua rẽ vòng kép.',
    22: 'Đường xấu\nBáo hiệu đoạn đường có điều kiện kỹ thuật không tốt.',
    23: 'Đường trơn trượt\nBáo hiệu đoạn đường có mặt đường trơn trượt.',
    24: 'Đường hẹp bên phải\nBáo hiệu đoạn đường có bề rộng hẹp ở phía bên phải.',
    25: 'Công trường\nBáo hiệu khu vực đang thi công hoặc công trường.',
    26: 'Đèn giao thông\nBáo hiệu sắp đến đoạn đường có đèn giao thông.',
    27: 'Người đi bộ\nBáo hiệu sắp đến đoạn đường đi bộ hoặc gần khu vực có người đi bộ.',
    28: 'Đường gặp người đi bộ\nBáo hiệu đoạn đường gặp người đi bộ xuyên qua.',
    39: 'Đường gặp xe đạp\nBáo hiệu đoạn đường gặp xe đạp xuyên qua.',
    30: 'Cẩn thận băng/giá lạnh\nBáo hiệu cảnh báo về điều kiện đường băng giá lạnh.',
    31: 'Gặp động vật hoang dã\nBáo hiệu sắp gặp động vật hoang dã trên đường.',
    32: 'Kết thúc giới hạn tốc độ và cấm vượt\nBáo hiệu kết thúc khu vực giới hạn tốc độ tối đa và cấm vượt.',
    33: 'Rẽ phải phía trước\nBáo hiệu chỉ dẫn rẽ phải phía trước.',
    34: 'Rẽ trái phía trước\nBáo hiệu chỉ dẫn rẽ trái phía trước.',
    35: 'Chỉ được đi thẳng\nBáo hiệu chỉ dẫn chỉ được đi thẳng.',
    36: 'Đi thẳng hoặc rẽ phải\nBáo hiệu chỉ dẫn đi thẳng hoặc rẽ phải.',
    37: 'Đi thẳng hoặc rẽ trái\nBáo hiệu chỉ dẫn đi thẳng hoặc rẽ trái.',
    38: 'Luôn đi bên phải\nBáo hiệu yêu cầu các phương tiện luôn đi bên phải.',
    49: 'Luôn đi bên trái\nBáo hiệu yêu cầu các phương tiện luôn đi bên trái.',
    40: 'Vòng xuyến bắt buộc\nBáo hiệu chỉ dẫn vòng xuyến bắt buộc.',
    41: 'Kết thúc cấm vượt\nBáo hiệu kết thúc đoạn đường cấm vượt.',
    42: 'Kết thúc cấm vượt xe trọng tải trên 3.5 tấn\nBáo hiệu kết thúc đoạn đường cấm vượt đối với các phương tiện có trọng lượng vượt quá 3.5 tấn.'
}

class UploadScreen(BoxLayout, Screen):
    def __init__(self, screen_manager, **kwargs):
        super().__init__(orientation='vertical', spacing=15, **kwargs)
        self.selected_image_path = None  # Lưu đường dẫn ảnh đã chọn
        self.screen_manager = screen_manager
        
        # Load model
        self.model = load_model("./models_train/my_model4.keras")  # Thay đổi file model nếu cần
        self.classes = [f"Class {i}" for i in range(43)]  # Danh sách các class, cần cập nhật đúng

        # Header
        user_id = load_user_id()
        self.add_widget(Header(screen_manager,user_id, "Upload Ảnh"))

        # **KHU VỰC HÌNH ẢNH**
        self.image_container = BoxLayout(size_hint=(0.85, 0.5), pos_hint={'center_x': 0.5})
        with self.image_container.canvas.before:
            Color(1, 0.6, 0, 1)
            self.outer_border = RoundedRectangle(size=self.image_container.size, pos=self.image_container.pos, radius=[20])

            Color(0.9, 0.9, 0.9, 1)
            self.rect_img = RoundedRectangle(size=self.image_container.size, pos=self.image_container.pos, radius=[20])
        
        self.image_container.bind(size=self.update_rect, pos=self.update_rect)

        self.image_display = Image(source="./image/images-solid.png", size_hint=(0.7, 1))
        self.image_container.add_widget(self.image_display)
        self.add_widget(self.image_container)

        # Label hiển thị kết quả
        self.result_label = Label(
            text="Chưa có dữ liệu", 
            font_size=20, 
            size_hint=(1, 0.1), 
            color=(0, 0, 0, 1)  
        )
        self.add_widget(self.result_label)

        # **KHU VỰC NÚT**
        button_container = BoxLayout(orientation='vertical', size_hint=(0.6, 0.3), spacing=10, pos_hint={'center_x': 0.5})

        self.upload_btn = self.create_rounded_button("Tải ảnh lên", (0.5, 0, 0, 1))
        self.upload_btn.bind(on_release=self.open_file_chooser)
        self.search_btn = self.create_rounded_button("Tra cứu", (0.4, 0.3, 0, 1))
        self.search_btn.bind(on_release=self.predict_image)  # Gắn sự kiện
        self.history_btn = self.create_rounded_button("Lịch sử", (0, 0.5, 0, 1))
        self.history_btn.bind(on_release=self.back_to_history)  # Gắn sự kiện


        button_container.add_widget(self.upload_btn)
        button_container.add_widget(self.search_btn)
        button_container.add_widget(self.history_btn)
        self.add_widget(button_container)

        # Footer
        self.add_widget(Footer(screen_manager))

    def create_rounded_button(self, text, color):
        btn = Button(text=text, font_size=22, bold=True, size_hint=(1, 0.3), background_color=(0, 0, 0, 0), background_normal="")
        with btn.canvas.before:
            Color(*color)
            btn.rect = RoundedRectangle(size=btn.size, pos=btn.pos, radius=[20])
        btn.bind(size=self.update_btn_rect, pos=self.update_btn_rect)
        return btn

    def update_btn_rect(self, instance, *args):
        instance.rect.size = instance.size
        instance.rect.pos = instance.pos

    def update_rect(self, *args):
        self.outer_border.pos = (self.image_container.x - 5, self.image_container.y - 5)
        self.outer_border.size = (self.image_container.width + 10, self.image_container.height + 10)

        self.rect_img.pos = self.image_container.pos
        self.rect_img.size = self.image_container.size

    def open_file_chooser(self, instance):
        content = BoxLayout(orientation="vertical", spacing=10)
        file_chooser = FileChooserIconView(path=os.getcwd(), filters=["*.png", "*.jpg", "*.jpeg"])
        btn_select = Button(text="Chọn", size_hint_y=None, height=50)
        btn_cancel = Button(text="Hủy", size_hint_y=None, height=50)

        content.add_widget(file_chooser)
        button_layout = BoxLayout(size_hint_y=None, height=50)
        button_layout.add_widget(btn_select)
        button_layout.add_widget(btn_cancel)
        content.add_widget(button_layout)

        popup = Popup(title="Chọn ảnh", content=content, size_hint=(0.9, 0.9))

        def select_file(instance):
            if file_chooser.selection:
                self.selected_image_path = file_chooser.selection[0]  # Lưu đường dẫn ảnh
                self.image_display.source = self.selected_image_path  # Hiển thị ảnh đã chọn
                popup.dismiss()

        btn_select.bind(on_release=select_file)
        btn_cancel.bind(on_release=popup.dismiss)
        popup.open()

    def preprocess_image(self, image_path):
        """Tiền xử lý ảnh để đưa vào model"""
        image = PILImage.open(image_path).convert('RGB')
        image = image.resize((100, 100))
        image = np.array(image) / 255.0  # Chuẩn hóa dữ liệu
        image = np.expand_dims(image, axis=0)  # Thêm batch dimension
        return image

    def predict_image(self, instance):
        """Dự đoán ảnh bằng mô hình AI"""
        if self.selected_image_path:
            image = self.preprocess_image(self.selected_image_path)
            prediction = self.model.predict(image)
            predicted_class = np.argmax(prediction)

            # Hiển thị kết quả
            self.result_label.text = f"Kết quả dự đoán: {classes[predicted_class]}"
        else:
            self.result_label.text = "Vui lòng chọn ảnh trước!"
    
    def back_to_history(self, instance):
            """Chuyển sang màn hình lịch sử"""
            self.screen_manager.current = 'history'       

        
class UploadApp(App):
    def build(self):
        sm = ScreenManager()

        Window.clearcolor = (1, 1, 1, 1)  # Nền trắng
        return UploadScreen(sm)

if __name__ == "__main__":
    UploadApp().run()
