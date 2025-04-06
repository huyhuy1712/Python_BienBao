from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDRaisedButton
from kivy.uix.camera import Camera
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle, RoundedRectangle
from tensorflow.keras.models import load_model
from datetime import datetime
import numpy as np
import cv2
from kivy.uix.label import Label
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from model.user_crud import *
from model.history_crud import *

model = load_model("models_train/my_model4.keras")  

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


class ScanScreen(Screen):
    def __init__(self, screen_manager, **kwargs):
        super().__init__(**kwargs)
        
        # Layout chính (dọc)
        self.main_layout = BoxLayout(orientation='vertical')
        self.screen_manager = screen_manager
        # Thêm header
        user_id = load_user_id()
        self.main_layout.add_widget(Header(screen_manager,user_id, "Scan Ảnh"))

        # Layout nội dung giữa
        self.content_layout = BoxLayout(orientation='vertical', padding=[20, 20], spacing=20)
        
        # Thêm nền
        with self.content_layout.canvas.before:
            Color(0.94, 0.94, 0.94, 1)
            self.bg_rect = Rectangle(size=self.content_layout.size, pos=self.content_layout.pos)
        self.content_layout.bind(size=self.update_bg, pos=self.update_bg)

        # Camera
        self.camera_area = AnchorLayout(size_hint=(1, 0.8))
        with self.camera_area.canvas.before:
            Color(1, 1, 1, 1)
            self.camera_bg = RoundedRectangle(size=self.camera_area.size, pos=self.camera_area.pos, radius=[20])
        self.camera_area.bind(size=self.update_camera_bg, pos=self.update_camera_bg)
        
        self.camera = Camera(play=True, resolution=(800, 600))
        self.camera_area.add_widget(self.camera)
        self.content_layout.add_widget(self.camera_area)

        # 🟢 **Thêm Label để hiển thị kết quả**
        self.result_label = Label(
            text="Kết quả sẽ hiển thị ở đây",
            size_hint=(1, None),
            height=50,
            color=(0, 0, 0, 1),  # Màu chữ đen
        )
        self.content_layout.add_widget(self.result_label)

        # Layout chứa 3 nút
        button_layout = GridLayout(cols=3, spacing=20, size_hint_y=None, height=60, padding=[20, 0], size_hint_x=1)

        # Nút Scan
        self.scan_button = MDRaisedButton(
            text="Scan",
            md_bg_color=(0.13, 0.59, 0.95, 1),
            text_color=(1, 1, 1, 1),
            size_hint=(1, None),
            height=50,
        )
        self.scan_button.bind(on_press=self.capture_image)

        # Nút Lịch Sử
        self.history_button = MDRaisedButton(
            text="Lịch Sử",
            md_bg_color=(0.46, 0.46, 0.46, 1),
            text_color=(1, 1, 1, 1),
            size_hint=(1, None),
            height=50,
        )
        self.history_button.bind(on_press=self.go_to_history)

        # Nút Xóa
        self.delete_button = MDRaisedButton(
            text="Xóa",
            md_bg_color=(0.96, 0.26, 0.21, 1),
            text_color=(1, 1, 1, 1),
            size_hint=(1, None),
            height=50,
        )
        self.delete_button.bind(on_press=self.restart_camera)

        button_layout.add_widget(self.scan_button)
        button_layout.add_widget(self.history_button)
        button_layout.add_widget(self.delete_button)

        self.content_layout.add_widget(button_layout)
        self.main_layout.add_widget(self.content_layout)

        # Thêm footer
        self.main_layout.add_widget(Footer(screen_manager))
        self.add_widget(self.main_layout)

    def update_bg(self, *args):
        self.bg_rect.size = self.content_layout.size
        self.bg_rect.pos = self.content_layout.pos

    def update_camera_bg(self, *args):
        self.camera_bg.size = self.camera_area.size
        self.camera_bg.pos = self.camera_area.pos

    def restart_camera(self, instance=None):
        self.clear_camera()
        self.camera = Camera(play=True, resolution=(800, 600))
        self.camera_area.add_widget(self.camera)

    def clear_camera(self, instance=None):
        if self.camera:
            self.camera.play = False
            self.camera_area.remove_widget(self.camera)
            self.camera = None
    
    # Xóa kết quả hiển thị
        self.result_label.text = "Kết quả sẽ hiển thị ở đây"



    def go_to_history(self, instance):
        print("Chuyển đến màn hình lịch sử")
        self.screen_manager.current = 'history'
    
    def capture_image(self, instance):
        if self.camera:
            texture = self.camera.texture
            size = texture.size
            pixels = texture.pixels
            
            # Chuyển đổi ảnh từ texture của Kivy sang OpenCV
            img = np.frombuffer(pixels, dtype=np.uint8).reshape(size[1], size[0], 4)
            img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)

            # Resize ảnh theo kích thước của model (100x100)
            img_resized = cv2.resize(img, (100, 100)) / 255.0
            img_resized = np.expand_dims(img_resized, axis=0).astype(np.float32)  # Thêm batch dimension và chuyển kiểu

            print("Shape of img_resized:", img_resized.shape)  # Debug

            # Dự đoán biển báo
            prediction = model.predict(img_resized)  # TensorFlow/Keras
            predicted_class = np.argmax(prediction)

            # Lấy tên biển báo từ classes
            result_text = f"Biển báo nhận diện: {classes.get(predicted_class, 'Không xác định')}"
            self.result_label.text = result_text  # Hiển thị trên giao diện
            
            # Lưu ảnh đã scan vào folder
            img_path = str(self.save_image(img,"image/img_scan_upload"))
            user_id = str(load_user_id())
            description = "Kết quả: " + str(result_text)
            add_history(user_id,2,img_path,description) #thêm vào lịch sử
            

    def save_image(self,image, folder_path, filename_prefix="capture"):
        # Tạo folder nếu chưa tồn tại
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Tạo tên file theo thời gian
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{filename_prefix}_{timestamp}.png"
        file_path = os.path.join(folder_path, filename)

        # Lưu ảnh bằng OpenCV
        success = cv2.imwrite(file_path, image)
        
        if success:
            print(f"Ảnh đã được lưu tại: {file_path}")
            return filename
        else:
            print("Lỗi khi lưu ảnh.")
            return None
            

