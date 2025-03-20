from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.button import Button

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
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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
            source="image/—Pngtree—various road traffic signs_8255888.png",
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
        self.manager.translate = SlideTransition(direction="left")  # Hiệu ứng trượt sang trái
        self.manager.current = "login"  # Chuyển sang màn hình đăng nhập
    def go_to_register(self, instance):
        self.manager.translate = SlideTransition(direction="left")  # Hiệu ứng trượt sang trái
        self.manager.current = "register"  # Chuyển sang màn hình đăng ky            



class Login(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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
            source="image/—Pngtree—various road traffic signs_8255888.png",
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
        self.manager.translate = SlideTransition(direction="left")  # Hiệu ứng trượt sang trái
        self.manager.current = "main"  # Chuyển sang màn hình chính
    def go_to_register(self, instance):
        self.manager.translate = SlideTransition(direction="left")  # Hiệu ứng trượt sang trái
        self.manager.current = "register"  # Chuyển sang màn hình đăng ky 
        
class Register(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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
            source="image/—Pngtree—various road traffic signs_8255888.png",
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
        
        self.numberphone_input = TextInput(
            hint_text="Mật khẩu",
            size_hint=(None, None),
            size=(400, 50),
            pos_hint={"center_x": 0.5, "center_y": 0.45},
            font_size=20,
            multiline=False,
            padding=[10, 10],
        )
        self.add_widget(self.numberphone_input)
        
        self.password_input = TextInput(
            hint_text="Xác nhận Mật khẩu",
            size_hint=(None, None),
            size=(400, 50),
            pos_hint={"center_x": 0.5, "center_y": 0.35},
            font_size=20,
            multiline=False,
            padding=[10, 10],
        )
        self.add_widget(self.password_input)
        
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
        self.manager.translate = SlideTransition(direction="left")  # Hiệu ứng trượt sang trái
        self.manager.current = "main"  # Chuyển sang màn hình chính
    def go_to_login(self, instance):
        self.manager.translate = SlideTransition(direction="left")  # Hiệu ứng trượt sang trái
        self.manager.current = "login"  # Chuyển sang màn hình đăng nhập

class MyApp(App):
    def build(self):
        Window.size=(500,700)
        sm = ScreenManager()
        sm.add_widget(Main(name="main"))
        sm.add_widget(Login(name="login"))
        sm.add_widget(Register(name="register"))
        return sm


if __name__ == "__main__":
    MyApp().run()
