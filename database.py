# database.py
import mysql.connector
from db_config import DB_CONFIG
import random
import string
from datetime import datetime


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


# -------------------------------
# USER FUNCTIONS
# -------------------------------

def create_user(name, email, password):
    conn = get_connection()
    cur = conn.cursor()
    sql = "INSERT INTO users (name, email, password) VALUES (%s,%s,%s)"
    cur.execute(sql, (name, email, password))
    conn.commit()
    cur.close()
    conn.close()


def validate_user(email, password):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user


# -------------------------------
# MEETING FUNCTIONS
# -------------------------------

def generate_meeting_code(n=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))


def create_meeting(host_id, title, date_str, time_str, duration):
    conn = get_connection()
    cur = conn.cursor()
    code = generate_meeting_code()
    sql = """
        INSERT INTO meetings (host_id, title, meeting_code, date, start_time, duration_mins)
        VALUES (%s,%s,%s,%s,%s,%s)
    """
    cur.execute(sql, (host_id, title, code, date_str, time_str, duration))
    conn.commit()
    cur.close()
    conn.close()
    return code


def get_upcoming_meetings(user_id=None):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    today = datetime.today().date()

    if user_id:
        cur.execute(
            "SELECT * FROM meetings WHERE host_id=%s AND date>=%s ORDER BY date,start_time",
            (user_id, today)
        )
    else:
        cur.execute(
            "SELECT * FROM meetings WHERE date>=%s ORDER BY date,start_time",
            (today,)
        )

    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows