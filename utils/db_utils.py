import sqlite3
from pprint import pprint

def insert_user(tg_id, username, name, surname, phone_number):
    with sqlite3.connect('user_info.db') as conn:
        cur = conn.cursor()

        cur.execute("INSERT INTO users (tg_id, username, name, surname, phone_number) \
                    VALUES('%s', '%s', '%s', '%s', '%s')" % (tg_id, username, name, surname, phone_number))

        conn.commit()


async def insert_state(username, state):
    with sqlite3.connect('user_info.db') as conn:
        cur = conn.cursor()

        cur.execute("INSERT INTO states (user_id, state) \
                    VALUES((SELECT id FROM users WHERE username='%s'), '%s')" % (username, state))

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

# with sqlite3.connect('user_info.db') as conn:
#         cur = conn.cursor()

#         cur.execute("INSERT INTO states(user_id, state) VALUES(1, 'HUI3')")

#         k = cur.fetchall()
#         print(k)


async def last_user_state(username):
    """
    Returns last user state
    """
    with sqlite3.connect('user_info.db') as conn:
        cur = conn.cursor()

        cur.execute("SELECT * FROM states \
                    WHERE user_id=(SELECT id FROM users WHERE username='%s') ORDER BY datetime(date_time) DESC LIMIT 1" % (username))

        result = cur.fetchall()
        return result[0][2]


def select_all():
    with sqlite3.connect('user_info.db') as conn:
        cur = conn.cursor()

        cur.execute("SELECT * FROM users")

        pprint(cur.fetchall())

        cur.execute("select * from states")
        pprint(cur.fetchall())
