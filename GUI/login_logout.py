from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
import mysql.connector
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from model.user_crud import *
from mysql.connector import Error
from scan import ScanScreen
from uploadAnh import UploadScreen
from user import EditProfileScreen
from inf_signs import PageScreen
from lichSu import HistoryScreen
from trangchu import MainScreen


class RoundedButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)  # Ẩn nền mặc định
        self.border_radius = [20]  # Bo góc tròn hơn

        with self.canvas.before:
            self.color_bg = Color(*self.background_normal_color())  # Màu nền
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=self.border_radius)

        self.bind(pos=self.update_rect, size=self.update_rect)

    def background_normal_color(self):
        return (0.2, 0.6, 1, 1)  # Mặc định màu xanh dương

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def background_normal_color(self):
        """Định nghĩa màu nền của nút"""
        if 'background_color' in self.__dict__:
            return self.background_color
        return (0.2, 0.6, 1, 1)  # Mặc định màu xanh dương


    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class Main(Screen):
    def __init__(self,screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = screen_manager
        #layout = BoxLayout(orientation= 'vertical')
        #Thêm hình nền (background)
        self.bg = Image(
            source="image/bg.jpg",  # Đổi thành đường dẫn ảnh của bạn
            size_hint=(1, 1),  # Ảnh sẽ lấp đầy màn hình
            allow_stretch=True,  # Cho phép kéo giãn ảnh để vừa với màn hình
            keep_ratio=False,  # Không giữ tỷ lệ gốc
        )
        self.add_widget(self.bg)
        # Header (Thanh tiêu đề)
        self.header = Label(
            text="Ứng dụng nhận biết biển báo",
            font_size=30,
            bold=True,
            size_hint=(1, None),
            height=50,
            pos_hint={"top": 1},
            color=(0,0 , 0, 1),
            #background_color=(0, 0.75, 1, 1)
        )
        self.add_widget(self.header)
        # Hình ảnh đặt ở vị trí cụ thể
        self.img = Image(
            source="image\logo.png",
            size_hint=(None, None),
            size=(250, 250),  # Kích thước ảnh
            pos_hint={"center_x": 0.5, "y": 0.6},  # Đặt tọa độ
        )
        self.add_widget(self.img)
                # Nút Đăng nhập
        self.login_btn = Button(
            text="Đăng nhập",
            size_hint=(None, None),  # Kích thước cố định
            size=(300, 80),  # Rộng 200px, cao 50px
            background_color=(0, 0.5, 1, 1),  # Màu xanh dương
            color=(1, 1, 1, 1),  # Màu chữ trắng
            pos_hint={'center_x':0.5 , 'y':0.3 },
        )
        self.add_widget(self.login_btn)
        self.login_btn.bind(on_press=self.go_to_login)

        # Nút Đăng ký
        self.register_btn = Button(
            text="Đăng ký",
            size_hint=(None, None),
            size=(300, 80),
            background_color=(1, 0.3, 0.3, 1),  # Màu đỏ
            color=(1, 1, 1, 1),
            pos_hint={'center_x':0.5 , 'y':0.15 }
        )
        self.add_widget(self.register_btn)
        self.register_btn.bind(on_press=self.go_to_register)
        
    def go_to_login(self, instance):
        self.manager.transition = SlideTransition(direction="left")  # Hiệu ứng trượt sang trái
        self.manager.current = "login"  # Chuyển sang màn hình đăng nhập
    def go_to_register(self, instance):
        self.manager.transition = SlideTransition(direction="left")  # Hiệu ứng trượt sang trái
        self.manager.current = "register"  # Chuyển sang màn hình đăng ky            


class Login(Screen):
    def __init__(self,screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = screen_manager
        # Thêm hình nền (background)
        self.bg = Image(
            source="image/bg.jpg",  # Đổi thành đường dẫn ảnh của bạn
            size_hint=(1, 1),  # Ảnh sẽ lấp đầy màn hình
            allow_stretch=True,  # Cho phép kéo giãn ảnh để vừa với màn hình
            keep_ratio=False,  # Không giữ tỷ lệ gốc
        )
        self.add_widget(self.bg)
        # Hình ảnh đặt ở vị trí cụ thể
        self.img = Image(
            source="image\logo.png",
            size_hint=(None, None),
            size=(250, 250),  # Kích thước ảnh
            pos_hint={"center_x": 0.5, "y": 0.65},  # Đặt tọa độ
        )
        self.add_widget(self.img)
        
        self.username_input = TextInput(
            hint_text="Tên đăng nhập",
            size_hint=(None, None),
            size=(400, 50),
            pos_hint={"center_x": 0.5, "center_y": 0.55},
            font_size=20,
            multiline=False,
            padding=[10, 10],
        )
        self.add_widget(self.username_input)
        
        self.password_input = TextInput(
            hint_text="Mật khẩu",
            password=True,
            size_hint=(None, None),
            size=(400, 50),
            pos_hint={"center_x": 0.5, "center_y": 0.45},
            font_size=20,
            multiline=False,
            padding=[10, 10],
        )
        self.add_widget(self.password_input)
        
        # Nút Đăng nhập
        self.login_btn = Button(
            text="Đăng nhập",
            size_hint=(None, None),  # Kích thước cố định
            size=(300, 80),  # Rộng 200px, cao 50px
            background_color=(0, 0.5, 1, 1),  # Màu xanh dương
            color=(1, 1, 1, 1),  # Màu chữ trắng
            pos_hint={'center_x':0.5 , 'y':0.28 },
        )
        self.add_widget(self.login_btn)
        self.login_btn.bind(on_press=self.login_user)
        
        self.label = Label(
            text="Nếu bạn chưa có tài khoản bấm đăng ký!", 
            font_size=20,
            color=(0, 0, 0, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.25},
            bold = [True]
            )
        self.add_widget(self.label)
        
                # Nút Đăng ký
        self.register_btn = Button(
            text="Đăng ký",
            size_hint=(None, None),
            size=(300, 80),
            background_color=(1, 0.3, 0.3, 1),  # Màu đỏ
            color=(1, 1, 1, 1),
            pos_hint={'center_x':0.5 , 'y':0.12 }
        )
        self.add_widget(self.register_btn)
        self.register_btn.bind(on_press=self.go_to_register)
        
        self.back_main = RoundedButton(
            text="X",
            bold = [True],
            size_hint=(None, None),
            size=(50, 50),
            background_color=(1, 1, 0, 1),  
            color=(0, 0, 0, 1),
            pos_hint={'center_x':0.07 , 'y':0.9 }
        )
        self.add_widget(self.back_main)
        self.back_main.bind(on_press=self.back_to_main)
        
    def back_to_main(self, instance):
        self.manager.transition = SlideTransition(direction="right")  # Hiệu ứng trượt sang trái
        self.manager.current = "modau"  # Chuyển sang màn hình chính
    def go_to_register(self, instance):
        self.manager.transition = SlideTransition(direction="left")  # Hiệu ứng trượt sang trái
        self.manager.current = "register"  # Chuyển sang màn hình đăng ky 
     
    def login_user(self, instance):
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()

        if not username or not password:
            self.show_popup("Lỗi", "Vui lòng nhập tài khoản và mật khẩu!")
            return

        #hashed_password = hashlib.sha256(password.encode()).hexdigest()  # Mã hóa mật khẩu

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="bienbao"
            )
            cursor = conn.cursor()
            query = "SELECT * FROM user WHERE username = %s AND password = %s"
            cursor.execute(query, (username,password))
            user = cursor.fetchone()

            cursor.close()
            conn.close()

            if user:
                self.show_popup("Thành công", "Đăng nhập thành công!")
                user_id = user[0]
                save_user_id(str(user_id)) #lưu user id vừa mới đọc
                
                #tao moi screen manager
                # Tạo MainScreen và truyền screen_manager
                main_screen = MainScreen(self.screen_manager, name='main')
                # Tạo ScanScreen và truyền Header
                scan_screen = ScanScreen(self.screen_manager, name='scan')
                # Tạo UploadScreen truyền vào ScreenManager
                upload_screen = UploadScreen(self.screen_manager,name='upload')
                # Tạo UploadScreen truyền vào ScreenManager
                history_screen = HistoryScreen(self.screen_manager,name='history')
                sign_screen = PageScreen(self.screen_manager,name='info')
                        # Tạo màn hình User
                user_screen = Screen(name='user')
                user_screen.add_widget(EditProfileScreen(self.screen_manager))
                
                self.screen_manager.add_widget(main_screen)  # Thêm màn hình chính
                self.screen_manager.add_widget(scan_screen)  # Thêm màn hình Scan
                self.screen_manager.add_widget(user_screen) # Thêm màn hình user
                self.screen_manager.add_widget(sign_screen) # Thêm màn hình sign
                self.screen_manager.add_widget(upload_screen) # Thêm màn hình upload    
                self.screen_manager.add_widget(history_screen) # Thêm màn hình lịch sử 
                
                if self.manager:  # Kiem tra neu co ScreenManager
                    self.manager.current = "main"
                else:
                    print("Loi: Khong tim thay ScreenManager!") 
            else:
                self.show_popup("Loi", "Tai khoan hoac mat khau khong đung!")

        except Error as e:
            self.show_popup("Loi", f"Loi ket noi CSDL: {e}")

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.6, 0.4))
        popup.open()      
        
        
class Register(Screen):
    def __init__(self,screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = screen_manager

        # Thêm hình nền (background)
        self.bg = Image(
            source="image/bg.jpg",  # Đổi thành đường dẫn ảnh của bạn
            size_hint=(1, 1),  # Ảnh sẽ lấp đầy màn hình
            allow_stretch=True,  # Cho phép kéo giãn ảnh để vừa với màn hình
            keep_ratio=False,  # Không giữ tỷ lệ gốc
        )
        self.add_widget(self.bg)
        # Hình ảnh đặt ở vị trí cụ thể
        self.img = Image(
            source="image\logo.png",
            size_hint=(None, None),
            size=(250, 250),  # Kích thước ảnh
            pos_hint={"center_x": 0.5, "y": 0.65},  # Đặt tọa độ
        )
        self.add_widget(self.img)
        
        self.avatar = Image(
            size_hint=(None,None),
            size=(100,100),
            pos_hint={'center_x':0.26 , 'center_y':0.58 },
            allow_stretch=True
        )
        self.add_widget(self.avatar)
        
        upload_button = Button(
            text="Chọn ảnh", 
            size_hint=(None, None), 
            size=(200, 50),
            pos_hint={'center_x': 0.55, 'center_y':0.58 }
            )
        upload_button.bind(on_press=self.open_file_chooser)
        self.add_widget(upload_button)
        
        self.username_input = TextInput(
            hint_text="Tên đăng nhập",
            size_hint=(None, None),
            size=(400, 50),
            pos_hint={"center_x": 0.5, "center_y": 0.47},
            font_size=20,
            multiline=False,
            padding=[10, 10],
        )
        self.add_widget(self.username_input)
        
        self.password_input = TextInput(
            hint_text="Mật khẩu",
            password=True,
            size_hint=(None, None),
            size=(400, 50),
            pos_hint={"center_x": 0.5, "center_y": 0.40},
            font_size=20,
            multiline=False,
            padding=[10, 10],
        )
        self.add_widget(self.password_input)
        
        self.confirm_password = TextInput(
            hint_text="Xác nhận Mật khẩu",
            password=True,
            size_hint=(None, None),
            size=(400, 50),
            pos_hint={"center_x": 0.5, "center_y": 0.33},
            font_size=20,
            multiline=False,
            padding=[10, 10],
        )
        self.add_widget(self.confirm_password)
        
         # Nút Đăng ký
        self.register_btn = Button(
            text="Đăng ký",
            size_hint=(None, None),
            size=(300, 80),
            background_color=(1, 0.3, 0.3, 1),  # Màu đỏ
            color=(1, 1, 1, 1),
            pos_hint={'center_x':0.5 , 'y':0.18 }
        )
        self.add_widget(self.register_btn)
        self.register_btn.bind(on_press=self.register_user)
        
                # Nút Đăng nhập
        self.login_btn = Button(
            text="Đăng nhập",
            size_hint=(None, None),  # Kích thước cố định
            size=(300, 80),  # Rộng 200px, cao 50px
            background_color=(0, 0.5, 1, 1),  # Màu xanh dương
            color=(1, 1, 1, 1),  # Màu chữ trắng
            pos_hint={'center_x':0.5 , 'y':0.01 },
        )
        self.add_widget(self.login_btn)
        
        self.label = Label(
            text="Nếu bạn đã có tài khoản bấm đăng nhập!", 
            font_size=20,
            color=(0, 0, 0, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.15},
            bold = [True]
            )
        self.add_widget(self.label)
        self.login_btn.bind(on_press=self.go_to_login)
        
        self.back_main = RoundedButton(
            text="X",
            font_size=20,
            size_hint=(None, None),
            size=(50, 50),
            color=(0, 0, 0, 1),
            pos_hint={'center_x': 0.07, 'y': 0.9},
        )
        self.add_widget(self.back_main)
        self.back_main.bind(on_press=self.back_to_main)
        
    def back_to_main(self, instance):
        self.manager.transition = SlideTransition(direction="right")  # Hiệu ứng trượt sang trái
        self.manager.current = "modau"  # Chuyển sang màn hình chính
    def go_to_login(self, instance):
        self.manager.transition = SlideTransition(direction="left")  # Hiệu ứng trượt sang trái
        self.manager.current = "login"  # Chuyển sang màn hình đăng nhập
    #tải ảnh lên
    def open_file_chooser(self, instance):
        content = FileChooserListView()
        popup = Popup(title="Chọn ảnh", content=content, size_hint=(0.9, 0.9))

        def select_file(instance, selection, *args):
            if selection:
                self.avatar.source = selection[0]  # Hiển thị ảnh đã chọn
                popup.dismiss()
        content.bind(on_submit=select_file)
        popup.open()
        
    def register_user(self, instance):
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()
        confirm_password = self.confirm_password.text.strip()
        avatar_path = self.avatar.source if self.avatar.source else ""

        if not username or not password or not confirm_password:
            self.show_popup("Lỗi", "Vui lòng điền đầy đủ thông tin!")
            return

        if password != confirm_password:
            self.show_popup("Lỗi", "Mật khẩu xác nhận không khớp!")
            return

        #hashed_password = hashlib.sha256(password.encode()).hexdigest()  # Mã hóa mật khẩu

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="bienbao"
            )
            cursor = conn.cursor()
            query = "INSERT INTO user (username, password, avatar) VALUES (%s, %s, %s)"
            cursor.execute(query, (username, password, avatar_path))
            conn.commit()
            cursor.close()
            conn.close()

            self.show_popup("Thành công", "Đăng ký thành công!")
            self.manager.current = "login"  # Chuyển sang màn hình đăng nhập

        except Error as e:
            self.show_popup("Lỗi", f"Lỗi kết nối CSDL: {e}")

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.6, 0.4))
        popup.open()
    

