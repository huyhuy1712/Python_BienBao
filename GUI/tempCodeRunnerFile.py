        # Thanh tìm kiếm ở trên cùng với bo tròn
        search_layout = BoxLayout(size_hint=(1, None), height=50, padding=[10, 0])
        self.search_bar = RoundedTextInput(hint_text="Tìm kiếm...")
        search_layout.add_widget(self.search_bar)
        main_layout.add_widget(search_layout)