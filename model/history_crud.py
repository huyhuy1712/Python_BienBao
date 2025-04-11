import sys
import os
from datetime import datetime

# Lấy thư mục chứa file history_crud.py (tức là model)
current_dir = os.path.abspath(os.path.dirname(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from model.db_connection import get_connection, close_connection
from mysql.connector import Error

def get_history_data(user_id):
    conn = get_connection()
    if conn is None:
        print("Không thể kết nối đến cơ sở dữ liệu.")
        return None
    cursor = None
    try:
        print("Creating cursor")
        cursor = conn.cursor()
        print(f"Executing query for user_id: {user_id}")
        query = """
            SELECT id_user, id_sign, type, time, image, description
            FROM history
            WHERE id_user = %s
        """
        cursor.execute(query, (user_id,))
        history_data = cursor.fetchall()
        if not history_data:
            print(f"Không có dữ liệu trong bảng history cho user_id = {user_id}.")
        else:
            print(f"Fetched {len(history_data)} rows for user_id {user_id}: {history_data}")
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
            query = "INSERT INTO history (id_user, id_sign, type, time, image, description) VALUES (%s, %s, %s, %s, %s, %s)"
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Ghép đường dẫn đầy đủ cho image
            full_image_path = f"image\img_scan_upload\{image}"
            cursor.execute(query, (id_user, 1, type, timestamp, full_image_path, description))
            conn.commit()
            print("Đã thêm lịch sử thành công.")
        except Exception as e:
            print(f"Lỗi khi thêm lịch sử: {e}")
        finally:
            cursor.close()
            conn.close()

def count_activity_by_type(user_id):
    conn = get_connection()
    if conn is None:
        print("Không thể kết nối đến cơ sở dữ liệu.")
        return None
    cursor = None
    try:
        cursor = conn.cursor()
        query = """
            SELECT type, COUNT(*) 
            FROM history 
            WHERE id_user = %s 
            GROUP BY type
        """
        cursor.execute(query, (user_id,))
        results = cursor.fetchall()

        counts = {1: 0, 2: 0}  # 1 = Upload, 2 = Scan
        for activity_type, count in results:
            counts[activity_type] = count

        return counts
    except Error as e:
        print(f"Lỗi truy vấn: {e}")
        return None
    finally:
        close_connection(conn, cursor)

