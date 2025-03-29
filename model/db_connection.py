import mysql.connector


# Hàm mở kết nối
def get_connection():
    try:

        conn = mysql.connector.connect(
            host="localhost",
            port=3307,
            user="root",
            password="",
            database="databienbao"
        )
        return conn
    except mysql.connector.Error as e:
        print("Loi SQL:", e)
        return None


# Hàm đóng kết nối
def close_connection(conn, cursor=None):
    if cursor:
        cursor.close()
    if conn:
        conn.close()


con = get_connection()
if con:
    print("Ket noi thanh cong")
