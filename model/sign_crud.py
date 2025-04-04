# Phải import cái này máy t(nam) chạy mới được
# Dòng này thêm thư mục cha (Python_BienBao) vào sys.path, giúp Python nhận diện package model khi chạy file .py trực tiếp.
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model.db_connection import get_connection, close_connection
from model.sign import Sign

# CREATE - Thêm biển báo mới
def create_sign(sign: Sign):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        sql = "INSERT INTO sign (id_sign, name, image, type, description) VALUES (%s, %s, %s, %s, %s)"
        values = (sign.get_id_sign(), sign.get_name(), sign.get_image(), sign.get_type_sign(), sign.get_description())
        cursor.execute(sql, values)
        conn.commit()
        close_connection(conn, cursor)
        print("✅ Sign created successfully!")

# READ - Lấy danh sách tất cả biển báo
def get_all_signs():
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id_sign, name, image, type, description FROM sign")
        signs_data = cursor.fetchall()
        close_connection(conn, cursor)

        # Chuyển dữ liệu thành danh sách đối tượng Sign
        return [Sign(*data) for data in signs_data]
    return []

# READ - Lấy biển báo theo ID
def get_sign_by_id(id_sign: int):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id_sign, name, image, type, description FROM sign WHERE id_sign = %s", (id_sign,))
        data = cursor.fetchone()
        close_connection(conn, cursor)

        if data:
            return Sign(*data)
        return None

# UPDATE - Cập nhật thông tin biển báo
def update_sign(sign: Sign):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        sql = "UPDATE sign SET name = %s, image = %s, type = %s, description = %s WHERE id_sign = %s"
        values = (sign.get_name(), sign.get_image(), sign.get_type_sign(), sign.get_description(), sign.get_id_sign())
        cursor.execute(sql, values)
        conn.commit()
        close_connection(conn, cursor)
        print("✅ Sign updated successfully!")

# DELETE - Xóa biển báo theo ID
def delete_sign(id_sign: int):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        sql = "DELETE FROM sign WHERE id_sign = %s"
        cursor.execute(sql, (id_sign,))
        conn.commit()
        close_connection(conn, cursor)
        print("✅ Sign deleted successfully!")

def get_all_signs_by_type(type_sign):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id_sign, name, image, type, description FROM sign WHERE type = %s", (type_sign,))
        signs_data = cursor.fetchall()
        close_connection(conn, cursor)

        # Chuyển dữ liệu thành danh sách đối tượng Sign
        return [Sign(*data) for data in signs_data]
    return []

def get_all_signs_by_keyword(keyword,signs):
    arr_sign=[]
    for sign in signs:
        if keyword in sign.name:
            arr_sign.append(sign)
    return arr_sign
