import sys
import os

# Lấy thư mục chứa file history_crud.py (tức là model)
current_dir = os.path.abspath(os.path.dirname(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from model.db_connection import get_connection, close_connection
from mysql.connector import Error

def get_history_data():
    conn = get_connection()
    if conn is None:
        print("Không thể kết nối đến cơ sở dữ liệu.")
        return None
    cursor = None
    try:
        print("Creating cursor")
        cursor = conn.cursor()
        print("Executing query: SELECT id_user, id_sign, type, time, image, description FROM history")
        cursor.execute("SELECT id_user, id_sign, type, time, image, description FROM history")
        history_data = cursor.fetchall()
        if not history_data:
            print("Không có dữ liệu trong bảng history.")
        else:
            print(f"Fetched {len(history_data)} rows: {history_data}")
        return history_data
    except Error as e:
        print(f"Lỗi khi truy vấn dữ liệu: {e}")
        return None
    except Exception as e:
        print(f"Lỗi không xác định trong get_history_data: {str(e)}")
        import traceback
        traceback.print_exc()
        return None
    finally:
        close_connection(conn, cursor)

def add_history(id_user, type, image, description):
    conn = get_connection()
    if conn is None:
        print("Không thể kết nối đến cơ sở dữ liệu.")
        return None
    else:
        try:
            cursor = conn.cursor()
            query = "INSERT INTO history (id_user, id_sign, type, image, description) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (id_user, 1, type, image, description))
            conn.commit()
            print("Đã thêm lịch sử thành công.")
        except Exception as e:
            print(f"Lỗi khi thêm lịch sử: {e}")
        finally:
            cursor.close()
            conn.close()

    
