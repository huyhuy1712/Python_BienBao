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
            pos_hint={"center_x": 0.5, "center_y": 0.15},
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
            pos_hint={'center_x':0.5 , 'y':0.01 }
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
        