import sqlite3


def insert_user(tg_id, username, name, surname, phone_number):
    with sqlite3.connect('user_info.db') as conn:
        cur = conn.cursor()

        cur.execute("INSERT INTO users (tg_id, username, name, surname, phone_number) \
                    VALUES('%s', '%s', '%s', '%s', '%s')" % (tg_id, username, name, surname, phone_number))

        conn.commit()


def check_user_exsists(tg_id, username, name, surname, phone_number):
    with sqlite3.connect('user_info.db') as conn:
        cur = conn.cursor()

        cur.execute("SELECT * FROM users \
                    WHERE tg_id='%s'\
                    AND username='%s'\
                    AND name='%s'\
                    AND surname='%s'\
                    AND phone_number='%s'" % (tg_id, username, name, surname, phone_number))

        return cur.fetchall()


def select_all():
    with sqlite3.connect('user_info.db') as conn:
        cur = conn.cursor()

        cur.execute("SELECT * FROM users")

        print(cur.fetchall())
