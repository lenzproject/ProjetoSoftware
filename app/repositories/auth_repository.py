from ..database import get_connection

def find_active_user(login):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute("SELECT * FROM `user` WHERE email=%s AND active=1 LIMIT 1", (login,))
        return cur.fetchone()
    finally:
        cur.close(); conn.close()

def update_password(user_id, password_hash):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE `user` SET password=%s WHERE id=%s", (password_hash, user_id))
        conn.commit()
    except Exception:
        conn.rollback(); raise
    finally:
        cur.close(); conn.close()
