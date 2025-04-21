import pyodbc

def connect_db():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=WIN-5FOA4A1T5E2\\SQLEXPRESS;"
        "DATABASE=TZ_BANK;"
        "Trusted_Connection=yes;"
    )

#1. Hisobot generatsiyasi (kunlik, haftalik, oylik)
def generate_reports(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT report_type, created_at, total_transactions, flagged_transactions, total_amount 
        FROM reports
        ORDER BY created_at DESC
    """)
    rows = cursor.fetchall()
    print("📊 Hisobotlar ro‘yxati (kunlik/haftalik/oylik):")
    for row in rows:
        print(row)
    cursor.close()


#2. Bloklangan va tekshirilayotgan kartalarni kuzatish
def track_blocked_and_flagged_cards(conn):
    cursor = conn.cursor()
    print("\n🚫 Bloklangan kartalar:")
    cursor.execute("SELECT id, card_number, balance FROM cards WHERE is_blocked = 1")
    for row in cursor.fetchall():
        print(row)
    print("\n🚩 Shubhali (flagged) tranzaksiyalar:")
    cursor.execute("SELECT id, from_card_id, to_card_id, amount FROM transactions WHERE is_flagged = 1")
    for row in cursor.fetchall():
        print(row)
    cursor.close()


#3. Har bir foydalanuvchining tranzaksiya tarixini ko‘rish
def show_user_transaction_history(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.id, t.from_card_id, t.to_card_id, t.amount, t.status, t.created_at
        FROM transactions t
        JOIN cards c ON t.from_card_id = c.id
        WHERE c.user_id = ?
        ORDER BY t.created_at DESC
    """, user_id)
    print(f"\n🧾 Foydalanuvchi ID {user_id} tranzaksiya tarixi:")
    for row in cursor.fetchall():
        print(row)
    cursor.close()


#4. Balansni tahlil qilish (o‘rtacha balans, eng ko‘p tranzaksiya qilgan foydalanuvchi)
def analyze_balances_and_top_user(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT AVG(total_balance) FROM users")
    avg_balance = cursor.fetchone()[0]
    print(f"\n📈 O‘rtacha balans: {avg_balance:,.2f} so'm")
    cursor.execute("""
        SELECT u.id, u.name, COUNT(t.id) AS transaction_count
        FROM users u
        JOIN cards c ON u.id = c.user_id
        JOIN transactions t ON c.id = t.from_card_id
        GROUP BY u.id, u.name
        ORDER BY transaction_count DESC
    """)
    top_user = cursor.fetchone()
    print(f"👑 Eng faol foydalanuvchi: ID {top_user[0]}, Ismi: {top_user[1]}, Tranzaksiyalar soni: {top_user[2]}")
    cursor.close()



def main():
    conn = connect_db()
    while True:
        print("\n=== Qo‘shimcha funksiyalar menyusi ===")
        print("1. Hisobot generatsiyasi")
        print("2. Bloklangan va flagged kartalarni ko‘rish")
        print("3. Foydalanuvchining tranzaksiya tarixi")
        print("4. Balans tahlili va eng faol foydalanuvchi")
        print("5. Chiqish")

        tanlov = input("Tanlovni kiriting (1-5): ")

        if tanlov == '1':
            generate_reports(conn)
        elif tanlov == '2':
            track_blocked_and_flagged_cards(conn)
        elif tanlov == '3':
            user_id = int(input("Foydalanuvchi ID sini kiriting: "))
            show_user_transaction_history(conn, user_id)
        elif tanlov == '4':
            analyze_balances_and_top_user(conn)
        elif tanlov == '5':
            print("Dastur yakunlandi.")
            break
        else:
            print("❌ Noto‘g‘ri tanlov!")

    conn.close()

if __name__ == "__main__":
    main()
