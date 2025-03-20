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
