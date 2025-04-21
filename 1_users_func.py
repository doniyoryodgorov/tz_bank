import pyodbc

def connect_db():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=WIN-5FOA4A1T5E2\\SQLEXPRESS;"
        "DATABASE=TZ_BANK;"
        "Trusted_Connection=yes;"
    )


#1. Barcha foydalanuvchilarni ko‘rish

def show_all_users(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, phone_number, email, status, is_vip, total_balance FROM users")
    rows = cursor.fetchall()
    print("📋 Barcha foydalanuvchilar:")
    for row in rows:
        print(row)
    cursor.close()


#2. So‘nggi 1 oy ichida faol bo‘lgan foydalanuvchilarni ko‘rish


def show_recent_users(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, last_active_at 
        FROM users 
        WHERE last_active_at >= DATEADD(MONTH, -1, GETDATE())
    """)
    rows = cursor.fetchall()
    print("🕒 Oxirgi 1 oyda faol foydalanuvchilar:")
    for row in rows:
        print(row)
    cursor.close()


#3. Har bir foydalanuvchining hisob holatini tekshirish (balans)
def check_user_balances(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, total_balance 
        FROM users
    """)
    rows = cursor.fetchall()
    print("💰 Foydalanuvchilarning hisob holati:")
    for row in rows:
        print(f"ID: {row[0]}, Name: {row[1]}, Balance: {row[2]:,} so'm")
    cursor.close()


#4. Foydalanuvchi kartalarining limitini nazorat qilish
def check_card_limits(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.id, u.name, c.card_number, c.limit_amount, c.balance
        FROM cards c
        JOIN users u ON u.id = c.user_id
        WHERE c.balance > c.limit_amount
    """)
    rows = cursor.fetchall()
    print("🚨 Limitdan oshgan kartalar:")
    for row in rows:
        print(f"Card ID: {row[0]}, User: {row[1]}, Card: {row[2]}, Limit: {row[3]:,}, Balance: {row[4]:,}")
    cursor.close()


#main
def main():
    import pyodbc
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=WIN-5FOA4A1T5E2\\SQLEXPRESS;"
        "DATABASE=TZ_BANK;"
        "Trusted_Connection=yes;"
    )

    while True:
        print("\n=== Foydalanuvchilarni boshqarish ===")
        print("1. Barcha foydalanuvchilar")
        print("2. So‘nggi 1 oyda faol foydalanuvchilar")
        print("3. Foydalanuvchi balanslari")
        print("4. Limitdan oshgan kartalar")
        print("5. Chiqish")

        tanlov = input("Tanlang: ")
        if tanlov == '1':
            show_all_users(conn)
        elif tanlov == '2':
            show_recent_users(conn)
        elif tanlov == '3':
            check_user_balances(conn)
        elif tanlov == '4':
            check_card_limits(conn)
        elif tanlov == '5':
            break
        else:
            print("❌ Noto‘g‘ri tanlov!")

    conn.close()

if __name__ == "__main__":
    main()




