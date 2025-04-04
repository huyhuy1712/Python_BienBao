from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.graphics import Color, RoundedRectangle
from footer import Footer
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.modalview import ModalView
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import shutil
from model.user_crud import *
class EditProfileScreen(BoxLayout):
    def __init__(self,screen_manager, **kwargs):
        super().__init__(orientation='vertical', spacing=10, padding=0, size_hint=(1, 1), **kwargs)
        
        with self.canvas.before:
            Color(0.95, 0.95, 0.95, 1)  # Nền sáng hơn
            self.rect = RoundedRectangle(radius=[10])
        self.bind(size=self._update_rect, pos=self._update_rect)
        
        self.add_widget(Label(text="Chỉnh sửa hồ sơ", font_size=28, bold=True, color=(0, 0, 0, 1), size_hint=(1, 0.1)))
        
        self.current_username = "hoainam"
        self.current_password = ""
        self.current_avatar = "image/"+get_avatar_by_id(get_user_id_from_username(self.current_username))
        
        avatar_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.4), spacing=10)
        self.avatar = Image(source=self.current_avatar, size_hint=(1, 0.8))
        avatar_layout.add_widget(self.avatar)
        
        self.change_avatar_btn = Button(text="Thay đổi ảnh", size_hint=(1, 0.2), background_color=(0.3, 0.3, 0.3, 1))
        self.change_avatar_btn.bind(on_press=self.open_file_chooser)
        avatar_layout.add_widget(self.change_avatar_btn)
        
        self.add_widget(avatar_layout)
        
        form_layout = BoxLayout(orientation='vertical', spacing=10, size_hint=(1, 0.5))
        
        username_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50)
        username_layout.add_widget(Label(text="Tên tài khoản:", font_size=18, color=(0, 0, 0, 1), size_hint=(0.3, 1)))
        self.username_input = TextInput(text=self.current_username, multiline=False, size_hint=(0.7, 1),readonly=True)
        username_layout.add_widget(self.username_input)
        form_layout.add_widget(username_layout)
        
        password_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50)
        password_layout.add_widget(Label(text="Mật khẩu:", font_size=18, color=(0, 0, 0, 1), size_hint=(0.3, 1)))
        self.password_input = TextInput(text=self.current_password, multiline=False, password=True, size_hint=(0.7, 1))
        password_layout.add_widget(self.password_input)
        form_layout.add_widget(password_layout)
        
        new_password_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50)
        new_password_layout.add_widget(Label(text="Mật khẩu mới:", font_size=18, color=(0, 0, 0, 1), size_hint=(0.3, 1)))
        self.new_password_input = TextInput(multiline=False, password=True, size_hint=(0.7, 1))
        new_password_layout.add_widget(self.new_password_input)
        form_layout.add_widget(new_password_layout)
        
        confirm_password_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50)
        confirm_password_layout.add_widget(Label(text="Nhập lại mật khẩu mới:", font_size=18, color=(0, 0, 0, 1), size_hint=(0.3, 1)))
        self.confirm_password_input = TextInput(multiline=False, password=True, size_hint=(0.7, 1))
        confirm_password_layout.add_widget(self.confirm_password_input)
        form_layout.add_widget(confirm_password_layout)
        
        self.add_widget(form_layout)
        
        self.save_btn = Button(text="Lưu thay đổi", size_hint=(1, 0.1), background_color=(0.1, 0.6, 0.1, 1))
        self.save_btn.bind(on_press=self.on_save_button_click)
        self.add_widget(self.save_btn)
                        # Thêm footer từ file footer.py
        self.add_widget(Footer(screen_manager))
    
    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
    
    def open_file_chooser(self, instance):
        """ Mở hộp thoại chọn ảnh từ bất kỳ đâu trên máy tính """
        self.file_chooser = ModalView(size_hint=(0.8, 0.8))
        layout = BoxLayout(orientation='vertical')

        # Đặt root_path về thư mục gốc của hệ thống
        system_root = "C:/" if os.name == "nt" else "/"  # Windows thì "C:/", Linux/macOS thì "/"
        self.file_view = FileChooserListView(rootpath=system_root, filters=['*.png', '*.jpg', '*.jpeg'])
        layout.add_widget(self.file_view)

        select_button = Button(text="Chọn ảnh", size_hint=(1, 0.1))
        select_button.bind(on_press=self.on_file_selected)
        layout.add_widget(select_button)

        self.file_chooser.add_widget(layout)
        self.file_chooser.open()

    
    def on_file_selected(self, instance):
        """ Cập nhật avatar khi chọn ảnh """
        selected_file = self.file_view.selection and self.file_view.selection[0]
        if selected_file:
            # Lấy tên tệp ảnh
            filename = os.path.basename(selected_file)
            
            # Đảm bảo thư mục image/avatar tồn tại
            save_path = os.path.join('image', filename)
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            # Sao chép ảnh vào thư mục image/avatar
            shutil.copy(selected_file, save_path)
            
            # Cập nhật avatar với đường dẫn mới
            self.avatar.source = save_path  # In ra đường dẫn của ảnh
            print(os.path.basename(self.avatar.source))
        self.file_chooser.dismiss()


    def show_popup(self, title, message):
        """ Hiển thị một popup với thông báo """
        popup = Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()

    def on_save_button_click(self, instance):
        iduser = get_user_id_from_username(self.current_username)
        
        if check_Password(iduser, self.password_input.text) == True:
            if self.new_password_input.text == self.confirm_password_input.text:
                # Cập nhật mật khẩu và avatar
                check_change = update_pass_avatar(iduser, self.password_input.text, self.new_password_input.text, os.path.basename(self.avatar.source))
                if check_change == True:
                    # Nếu thay đổi thành công, thông báo thành công
                    self.show_popup("Thành công", "Lưu thay đổi thành công!")
                else:
                    # Nếu không thay đổi thành công, thông báo lỗi
                    self.show_popup("Lỗi", "Không thể lưu thay đổi!")
            else:
                # Nếu mật khẩu mới và xác nhận mật khẩu không khớp
                self.show_popup("Lỗi", "Mật khẩu mới và xác nhận mật khẩu không khớp!")
        else:
            # Nếu mật khẩu cũ không chính xác
            self.show_popup("Lỗi", "Mật khẩu cũ không đúng!")

class EditProfileApp(App):
    def build(self):
        sm = ScreenManager()
        return EditProfileScreen(sm)

if __name__ == "__main__":
    EditProfileApp().run()