import pyodbc

def connect_db():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=WIN-5FOA4A1T5E2\\SQLEXPRESS;"
        "DATABASE=TZ_BANK;"
        "Trusted_Connection=yes;"
    )


# VIP foydalanuvchilarni aniqlash
def detect_vip_users(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.id, u.name, SUM(t.amount) AS total_spent
        FROM users u
        JOIN cards c ON u.id = c.user_id
        JOIN transactions t ON c.id = t.from_card_id
        WHERE t.status = 'success'
        GROUP BY u.id, u.name
        HAVING SUM(t.amount) > 10000000
    """)
    for row in cursor.fetchall():
        print(f"ID: {row[0]}, Name: {row[1]}, Total: {row[2]:,} so'm")
    cursor.close()


#Yangi foydalanuvchiga Welcome bonus
def give_welcome_bonus(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, created_at 
        FROM users 
        WHERE DATEDIFF(DAY, created_at, GETDATE()) <= 1
    """)
    for row in cursor.fetchall():
        print(f"ID: {row[0]}, Name: {row[1]}, Created: {row[2]}")
    cursor.close()


#Bloklangan foydalanuvchilarni ko‘rish
def list_blocked_users(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, blocked_at, reason FROM blocked_users ORDER BY blocked_at DESC")
    for row in cursor.fetchall():
        print(row)
    cursor.close()


#Foydalanuvchining barcha kartalari
def show_user_cards(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT id, card_number, balance, is_blocked FROM cards WHERE user_id = ?", user_id)
    for row in cursor.fetchall():
        print(row)
    cursor.close()


#Cashback hisoblash (5%)
def calculate_cashback(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.id, u.name, SUM(t.amount) AS total_spent
        FROM users u
        JOIN cards c ON u.id = c.user_id
        JOIN transactions t ON c.id = t.from_card_id
        WHERE t.status = 'success'
        GROUP BY u.id, u.name
    """)
    for row in cursor.fetchall():
        cashback = int(row[2] * 0.05)
        print(f"ID: {row[0]}, Name: {row[1]}, Cashback: {cashback:,} so'm")
    cursor.close()


conn = connect_db()
detect_vip_users(conn)
give_welcome_bonus(conn)
list_blocked_users(conn)
show_user_cards(conn, user_id=5)
calculate_cashback(conn)
conn.close()


