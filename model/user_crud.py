#Phải import cái này máy t(nam) chạy mới được
#Dòng này thêm thư mục cha (Python_BienBao) vào sys.path, giúp Python nhận diện package model khi chạy file .py trực tiếp.
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model.db_connection import get_connection, close_connection

# CREATE - Thêm user mới
def create_user(username, password, avatar):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        sql = "INSERT INTO user (username, password, avatar) VALUES (%s, %s, %s)"
        values = (username, password, avatar)
        cursor.execute(sql, values)
        conn.commit()
        close_connection(conn, cursor)
        print("✅ User created successfully!")

# READ - Lấy danh sách user
def read_users():
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user")
        users = cursor.fetchall()
        close_connection(conn, cursor)
        return users

# UPDATE - Cập nhật thông tin user
def update_user(user_id, new_username, new_avatar):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        sql = "UPDATE user SET username = %s, avatar = %s WHERE id_user = %s"
        values = (new_username, new_avatar, user_id)
        cursor.execute(sql, values)
        conn.commit()
        close_connection(conn, cursor)
        print("✅ User updated successfully!")

# DELETE - Xóa user
def delete_user(user_id):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        sql = "DELETE FROM user WHERE id_user = %s"
        cursor.execute(sql, (user_id,))
        conn.commit()
        close_connection(conn, cursor)
        print("✅ User deleted successfully!")

def update_pass_avatar(user_id, current_pass, newpass, new_avatar):
    conn = get_connection()  # Lấy kết nối đến CSDL
    if conn:
        try:
            cursor = conn.cursor()
            sql = "UPDATE user SET password = %s, avatar = %s WHERE id_user = %s and password = %s"
            values = (newpass, new_avatar, user_id, current_pass)
            cursor.execute(sql, values)
            
            # Kiểm tra nếu có dòng nào bị ảnh hưởng
            if cursor.rowcount > 0:
                conn.commit()  # Chỉ commit khi có dòng bị thay đổi
                return True
            else:
                return False  # Nếu không có dòng nào bị thay đổi
        except Exception as e:
            print(f"Error: {e}")
            return False  # Nếu có lỗi xảy ra
        finally:
            # Đảm bảo đóng kết nối và con trỏ
            close_connection(conn, cursor)
    else:
        return False  # Nếu không kết nối được đến CSDL

def check_Password(user_id, password):
    conn = get_connection()  # Lấy kết nối đến CSDL
    if conn:
        try:
            cursor = conn.cursor()
            # Truy vấn để kiểm tra mật khẩu
            sql = "SELECT password FROM user WHERE id_user = %s"
            cursor.execute(sql, (user_id,))
            
            result = cursor.fetchone()  # Lấy một kết quả (dòng) từ truy vấn
            if result:
                # Kiểm tra mật khẩu
                stored_password = result[0]
                if stored_password == password:
                    return True  # Mật khẩu đúng
                else:
                    return False  # Mật khẩu sai
            else:
                return False  # Không tìm thấy người dùng với id_user
        except Exception as e:
            print(f"Error: {e}")
            return False  # Nếu có lỗi xảy ra
        finally:
            # Đảm bảo đóng kết nối và con trỏ
            close_connection(conn, cursor)
    else:
        return False  # Nếu không kết nối được đến CSDL


def get_user_id_from_username(username):
    conn = get_connection()  # Kết nối đến cơ sở dữ liệu
    if conn:
        try:
            cursor = conn.cursor()
            # Truy vấn lấy id_user từ username
            sql = "SELECT id_user FROM user WHERE username = %s"
            cursor.execute(sql, (username,))
            
            result = cursor.fetchone()  # Lấy một dòng kết quả
            if result:
                # Trả về id_user nếu tìm thấy
                return result[0]
            else:
                # Trả về None nếu không tìm thấy username
                return None
        except Exception as e:
            print(f"Error: {e}")
            return None  # Nếu có lỗi xảy ra
        finally:
            close_connection(conn, cursor)  # Đảm bảo đóng kết nối và con trỏ
    else:
        return None  # Nếu không kết nối được đến CSDL

def get_avatar_by_id(user_id):
    """ Lấy avatar của người dùng từ cơ sở dữ liệu dựa trên id_user """
    conn = get_connection()  # Lấy kết nối đến cơ sở dữ liệu
    if conn:
        try:
            cursor = conn.cursor()
            # Truy vấn để lấy avatar của người dùng theo id_user
            sql = "SELECT avatar FROM user WHERE id_user = %s"
            cursor.execute(sql, (user_id,))
            
            result = cursor.fetchone()  # Lấy một kết quả (dòng) từ truy vấn
            if result:
                # Trả về đường dẫn của avatar
                return result[0]  # result[0] chứa đường dẫn avatar
            else:
                return None  # Nếu không tìm thấy người dùng với id_user
        except Exception as e:
            print(f"Error: {e}")
            return None  # Nếu có lỗi xảy ra
        finally:
            # Đảm bảo đóng kết nối và con trỏ
            close_connection(conn, cursor)
    else:
        return None  # Nếu không kết nối được đến cơ sở dữ liệu   


