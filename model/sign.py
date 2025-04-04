class Sign:
    def __init__(self, id_sign: int, name: str, image: str, type_sign: int, description: str):
        self.id_sign = int(id_sign)  # Ép kiểu int
        self.name = str(name)        # Ép kiểu str
        self.image = str(image)      # Ép kiểu str
        self.type_sign = int(type_sign)  # Ép kiểu int
        self.description = str(description)  # Ép kiểu str

    # Getter và Setter cho id_sign (int)
    def get_id_sign(self) -> int:
        return self.id_sign

    def set_id_sign(self, id_sign: int):
        self.id_sign = int(id_sign)

    # Getter và Setter cho name (str)
    def get_name(self) -> str:
        return self.name

    def set_name(self, name: str):
        self.name = str(name)

    # Getter và Setter cho image (str)
    def get_image(self) -> str:
        return self.image

    def set_image(self, image: str):
        self.image = str(image)

    # Getter và Setter cho type_sign (int)
    def get_type_sign(self) -> int:
        return self.type_sign

    def set_type_sign(self, type_sign: int):
        self.type_sign = int(type_sign)

    # Getter và Setter cho description (str)
    def get_description(self) -> str:
        return self.description

    def set_description(self, description: str):
        self.description = str(description)

    # Hàm hiển thị thông tin biển báo
    def display_info(self) -> str:
        return f"ID: {self.id_sign}, Name: {self.name}, Image: {self.image}, Type: {self.type_sign}, Description: {self.description}"
    def __str__(self):
        return f"Sign(id={self.id_sign}, name={self.name}, image={self.image}, type={self.type_sign})"