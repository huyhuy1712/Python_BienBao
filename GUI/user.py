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


class EditProfileScreen(BoxLayout):
    def __init__(self,screen_manager, **kwargs):
        super().__init__(orientation='vertical', spacing=10, padding=0, size_hint=(1, 1), **kwargs)
        

        
        with self.canvas.before:
            Color(0.95, 0.95, 0.95, 1)  # Nền sáng hơn
            self.rect = RoundedRectangle(radius=[10])
        self.bind(size=self._update_rect, pos=self._update_rect)
        
        self.add_widget(Label(text="Chỉnh sửa hồ sơ", font_size=28, bold=True, color=(0, 0, 0, 1), size_hint=(1, 0.1)))
        
        self.current_username = "JohnDoe"
        self.current_password = "password123"
        self.current_avatar = "image/uta.jpg"
        
        avatar_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.6), spacing=10)
        self.avatar = Image(source=self.current_avatar, size_hint=(1, 1))
        avatar_layout.add_widget(self.avatar)
        
        self.change_avatar_btn = Button(text="Change Picture", size_hint=(1, 0.15), background_color=(0.3, 0.3, 0.3, 1))
        self.change_avatar_btn.bind(on_press=self.open_file_chooser)
        avatar_layout.add_widget(self.change_avatar_btn)
        
        self.add_widget(avatar_layout)
        
        form_layout = BoxLayout(orientation='vertical', spacing=10, size_hint=(1, 0.3))
        
        username_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50)
        username_layout.add_widget(Label(text="Username:", font_size=18, color=(0, 0, 0, 1), size_hint=(0.3, 1)))
        self.username_input = TextInput(text=self.current_username, multiline=False, size_hint=(0.7, 1))
        username_layout.add_widget(self.username_input)
        form_layout.add_widget(username_layout)
        
        password_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50)
        password_layout.add_widget(Label(text="Password:", font_size=18, color=(0, 0, 0, 1), size_hint=(0.3, 1)))
        self.password_input = TextInput(text=self.current_password, multiline=False, password=True, size_hint=(0.7, 1))
        password_layout.add_widget(self.password_input)
        form_layout.add_widget(password_layout)
        
        self.add_widget(form_layout)
        
        self.save_btn = Button(text="Lưu thay đổi", size_hint=(1, 0.1), background_color=(0.1, 0.6, 0.1, 1))
        self.save_btn.bind(on_press=self.save_changes)
        self.add_widget(self.save_btn)
                        # Thêm footer từ file footer.py
        self.add_widget(Footer(screen_manager))
    
    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
    
    def open_file_chooser(self, instance):
        filechooser = FileChooserIconView()
        popup = Popup(title="Chọn ảnh", content=filechooser, size_hint=(0.9, 0.9))
        
        def select_file(instance):
            if filechooser.selection:
                self.current_avatar = filechooser.selection[0]
                self.avatar.source = self.current_avatar
                popup.dismiss()
        
        select_btn = Button(text="Select", size_hint=(1, 0.2))
        select_btn.bind(on_press=select_file)
        
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(filechooser)
        layout.add_widget(select_btn)
        


        
        popup.content = layout
        popup.open()
    
    def save_changes(self, instance):
        new_username = self.username_input.text
        new_password = self.password_input.text
        print(f"Updated info: Username={new_username}, Password={new_password}, Avatar={self.current_avatar}")

class EditProfileApp(App):
    def build(self):
        sm = ScreenManager()
        return EditProfileScreen(sm)

if __name__ == "__main__":
    EditProfileApp().run()
