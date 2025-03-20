import mysql.connector

# Hàm mở kết nối
def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bienbao"
        )
        return conn
    except mysql.connector.Error as e:
        print("Lỗi kết nối MySQL:", e)
        return None

# Hàm đóng kết nối
def close_connection(conn, cursor=None):
    if cursor:
        cursor.close()
    if conn:
        conn.close()
