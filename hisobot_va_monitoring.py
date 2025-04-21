import pyodbc

def connect_db():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=WIN-5FOA4A1T5E2\SQLEXPRESS;"
        "DATABASE=TZ_BANK;"
        "Trusted_Connection=yes;"
    )

def total_user_balance(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(total_balance) FROM users")
    total = cursor.fetchone()[0]
    print(f"💰 Umumiy balans (bank aylanmasi): {total:,} so'm")
    cursor.close()

def top_transaction_user_by_period(conn, period='daily'):
    cursor = conn.cursor()
    if period == 'daily':
        interval = 'DAY'
    elif period == 'weekly':
        interval = 'WEEK'
    elif period == 'monthly':
        interval = 'MONTH'
    else:
        print("❌ Noto'g'ri period!")
        return
    cursor.execute(f'''
        SELECT TOP 1 u.id, u.name, COUNT(t.id) as tranz_count
        FROM users u
        JOIN cards c ON u.id = c.user_id
        JOIN transactions t ON c.id = t.from_card_id
        WHERE t.created_at >= DATEADD({interval}, -1, GETDATE())
        GROUP BY u.id, u.name
        ORDER BY tranz_count DESC
    ''')
    row = cursor.fetchone()
    print(f"👑 {period.title()} eng faol foydalanuvchi: ID {row[0]}, {row[1]}, tranzaksiya: {row[2]}")
    cursor.close()

def top_spending_targets(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT to_card_id, SUM(amount) as total_sent
        FROM transactions
        WHERE status = 'success'
        GROUP BY to_card_id
        ORDER BY total_sent DESC
    """)
    rows = cursor.fetchall()
    print("🏦 Eng ko‘p pul yuborilgan kartalar:")
    for row in rows[:10]:
        print(f"Card ID: {row[0]}, Jami: {row[1]:,} so'm")
    cursor.close()

def cash_flow_statistics(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE transaction_type = 'deposit'")
    deposit = cursor.fetchone()[0] or 0
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE transaction_type = 'withdrawal'")
    withdrawal = cursor.fetchone()[0] or 0
    print(f"📥 Depozit: {deposit:,} so'm")
    print(f"📤 Pul yechish: {withdrawal:,} so'm")
    cursor.close()

def average_card_usage_duration(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT AVG(DATEDIFF(DAY, u.created_at, c.created_at)) FROM cards c JOIN users u ON u.id = c.user_id")
    avg_days = cursor.fetchone()[0]
    print(f"📆 Kartalarning o'rtacha foydalanish boshlanish vaqti: {avg_days:.2f} kun")
    cursor.close()

if __name__ == "__main__":
    conn = connect_db()
    total_user_balance(conn)
    top_transaction_user_by_period(conn, 'daily')
    top_spending_targets(conn)
    cash_flow_statistics(conn)
    average_card_usage_duration(conn)
    conn.close()
