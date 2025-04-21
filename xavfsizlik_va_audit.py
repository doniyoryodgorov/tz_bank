import pyodbc

def connect_db():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=WIN-5FOA4A1T5E2\SQLEXPRESS;"
        "DATABASE=TZ_BANK;"
        "Trusted_Connection=yes;"
    )

def block_card(conn, card_id):
    cursor = conn.cursor()
    cursor.execute("UPDATE cards SET is_blocked = 1 WHERE id = ?", card_id)
    conn.commit()
    print(f"🚫 Karta ID {card_id} muvaffaqiyatli bloklandi.")
    cursor.close()

def detect_anomalies(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.id, u.name, AVG(CAST(t.amount AS BIGINT)) as avg_amount
        FROM users u
        JOIN cards c ON u.id = c.user_id
        JOIN transactions t ON c.id = t.from_card_id
        WHERE t.status = 'success'
        GROUP BY u.id, u.name
    """)
    user_averages = cursor.fetchall()

    print("🚨 Noan’anaviy tranzaksiyalar:")
    for user_id, name, avg_amount in user_averages:
        cursor.execute("""
            SELECT t.id, t.amount, t.created_at
            FROM transactions t
            JOIN cards c ON t.from_card_id = c.id
            WHERE c.user_id = ? AND t.amount > CAST(? AS BIGINT) * 50 AND t.status = 'success'
        """, (user_id, avg_amount))
        anomalies = cursor.fetchall()
        for a in anomalies:
            print(f"User: {name}, Tranzaksiya ID: {a[0]}, Amount: {a[1]:,} so'm, Sana: {a[2]}")
    cursor.close()

if __name__ == "__main__":
    conn = connect_db()
    block_card(conn, card_id=10)
    detect_anomalies(conn)
    conn.close()
